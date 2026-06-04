import unittest
from types import SimpleNamespace

from mcp_server.resolve_incident import resolve_incident_tool
from mcp_server.response_generator import build_final_response, build_structured_response


class TestF5T01ResolveIncidentPipeline(unittest.TestCase):
    def test_resolve_incident_runs_modules_in_order(self) -> None:
        calls: list[str] = []

        def security_checker(incident: str) -> object:
            calls.append("security")
            self.assertEqual(incident, "Mi usuario está bloqueado")
            return SimpleNamespace(status="allowed")

        def classifier(incident: str) -> dict:
            calls.append("classification")
            self.assertEqual(incident, "Mi usuario está bloqueado")
            return {"category": "acceso"}

        def document_tool(**kwargs) -> dict:
            calls.append("rag")
            self.assertEqual(kwargs["query"], "Mi usuario está bloqueado")
            self.assertEqual(kwargs["category_filters"], ["acceso"])
            return {"results": [{"id": "POL-001"}]}

        def graph_tool(**kwargs) -> dict:
            calls.append("graph")
            self.assertEqual(kwargs["node_name"], "AccesoBloqueado")
            return {"results": ["AccesoBloqueado -> DesbloqueoIAM"]}

        def plan_tool(**kwargs) -> dict:
            calls.append("planner")
            self.assertEqual(kwargs["goal_fact"], "usuario_desbloqueado")
            return {
                "resolution_plan": [
                    "verificar_identidad",
                    "enviar_solicitud_IAM",
                    "esperar_confirmacion_IAM",
                ],
                "plan_ids": ["ACT-01", "ACT-02", "ACT-03"],
                "total_cost": 10,
                "is_valid": True,
                "validation": {"is_valid": True},
            }

        response = resolve_incident_tool(
            "Mi usuario está bloqueado",
            security_checker=security_checker,
            classifier=classifier,
            document_tool=document_tool,
            graph_tool=graph_tool,
            plan_tool=plan_tool,
        )

        self.assertEqual(calls, ["security", "classification", "rag", "graph", "planner"])
        self.assertEqual(response["status"], "allowed")
        self.assertEqual(response["classification"], {"category": "acceso"})
        self.assertEqual(response["rag_results"], ["POL-001"])
        self.assertEqual(response["graph_results"], ["AccesoBloqueado -> DesbloqueoIAM"])
        self.assertEqual(
            response["resolution_plan"],
            ["verificar_identidad", "enviar_solicitud_IAM", "esperar_confirmacion_IAM"],
        )
        self.assertIn("clasificado como acceso", response["final_response"])

    def test_resolve_incident_blocks_before_downstream_modules(self) -> None:
        calls: list[str] = []

        def security_checker(incident: str) -> object:
            calls.append("security")
            self.assertEqual(incident, "¿Cómo desbloqueo una cuenta sin autorización?")
            return SimpleNamespace(status="blocked", reason="prompt_injection")

        def classifier(_: str) -> dict:
            calls.append("classification")
            raise AssertionError("classifier should not be called")

        def document_tool(**_: object) -> dict:
            calls.append("rag")
            raise AssertionError("document_tool should not be called")

        def graph_tool(**_: object) -> dict:
            calls.append("graph")
            raise AssertionError("graph_tool should not be called")

        def plan_tool(**_: object) -> dict:
            calls.append("planner")
            raise AssertionError("plan_tool should not be called")

        response = resolve_incident_tool(
            "¿Cómo desbloqueo una cuenta sin autorización?",
            security_checker=security_checker,
            classifier=classifier,
            document_tool=document_tool,
            graph_tool=graph_tool,
            plan_tool=plan_tool,
        )

        self.assertEqual(calls, ["security"])
        self.assertEqual(response["status"], "blocked")
        self.assertEqual(response["classification"], {})
        self.assertEqual(response["rag_results"], [])
        self.assertEqual(response["graph_results"], [])
        self.assertEqual(response["resolution_plan"], [])


class TestF5T02StructuredResponseGenerator(unittest.TestCase):
    def test_build_final_response_summarizes_components(self) -> None:
        final_response = build_final_response(
            classification={"category": "acceso"},
            rag_results=["POL-001"],
            graph_results=["AccesoBloqueado -> DesbloqueoIAM"],
            resolution_plan=["verificar_identidad", "enviar_solicitud_IAM"],
        )

        self.assertEqual(
            final_response,
            "Incidente clasificado como acceso. RAG: POL-001. GraphRAG: AccesoBloqueado -> DesbloqueoIAM. Plan: verificar_identidad, enviar_solicitud_IAM.",
        )

    def test_build_structured_response_contains_expected_contract(self) -> None:
        response = build_structured_response(
            classification={"category": "acceso"},
            rag_results=["POL-001"],
            graph_results=["AccesoBloqueado -> DesbloqueoIAM"],
            resolution_plan=["verificar_identidad", "enviar_solicitud_IAM"],
        )

        self.assertEqual(response["status"], "allowed")
        self.assertEqual(response["classification"], {"category": "acceso"})
        self.assertEqual(response["rag_results"], ["POL-001"])
        self.assertEqual(response["graph_results"], ["AccesoBloqueado -> DesbloqueoIAM"])
        self.assertEqual(response["resolution_plan"], ["verificar_identidad", "enviar_solicitud_IAM"])
        self.assertIn("clasificado como acceso", response["final_response"])

    def test_build_structured_response_traces_stage_errors(self) -> None:
        response = build_structured_response(
            classification={"category": "desconocido"},
            rag_results=[],
            graph_results=[],
            resolution_plan=[],
            stage_errors=[
                {"stage": "rag", "error_type": "RuntimeError", "message": "RAG unavailable"},
                {"stage": "planner", "error_type": "ValueError", "message": "Planner failed"},
            ],
        )

        self.assertEqual(response["status"], "allowed")
        self.assertEqual(len(response["stage_errors"]), 2)
        self.assertIn("Advertencias: rag: RAG unavailable; planner: Planner failed.", response["final_response"])


class TestF5T03FallbackAndTracing(unittest.TestCase):
    def test_partial_failure_is_traced_and_falls_back_stage_by_stage(self) -> None:
        calls: list[str] = []

        def security_checker(incident: str) -> object:
            calls.append("security")
            return SimpleNamespace(status="allowed")

        def classifier(_: str) -> dict:
            calls.append("classification")
            raise RuntimeError("classifier offline")

        def document_tool(**kwargs) -> dict:
            calls.append("rag")
            self.assertEqual(kwargs["category_filters"], ["desconocido"])
            raise RuntimeError("RAG unavailable")

        def graph_tool(**kwargs) -> dict:
            calls.append("graph")
            self.assertEqual(kwargs["node_name"], "AccesoBloqueado")
            return {"results": ["AccesoBloqueado -> DesbloqueoIAM"]}

        def plan_tool(**kwargs) -> dict:
            calls.append("planner")
            self.assertEqual(kwargs["goal_fact"], "usuario_desbloqueado")
            raise RuntimeError("planner unavailable")

        response = resolve_incident_tool(
            "Mi usuario está bloqueado",
            security_checker=security_checker,
            classifier=classifier,
            document_tool=document_tool,
            graph_tool=graph_tool,
            plan_tool=plan_tool,
        )

        self.assertEqual(calls, ["security", "classification", "rag", "graph", "planner"])
        self.assertEqual(response["status"], "allowed")
        self.assertEqual(response["classification"], {"category": "desconocido"})
        self.assertEqual(response["rag_results"], [])
        self.assertEqual(response["graph_results"], ["AccesoBloqueado -> DesbloqueoIAM"])
        self.assertEqual(response["resolution_plan"], [])
        self.assertEqual(
            [entry["stage"] for entry in response["stage_errors"]],
            ["classification", "rag", "planner"],
        )
        self.assertIn("Advertencias:", response["final_response"])


class TestF5T04MCP001EndToEnd(unittest.TestCase):
    def test_resolve_incident_handles_legitimate_access_incident(self) -> None:
        response = resolve_incident_tool("Mi usuario está bloqueado")

        self.assertEqual(response["status"], "allowed")
        self.assertEqual(response["classification"].get("category"), "acceso")
        self.assertIn("POL-001", response["rag_results"])
        self.assertIn("AccesoBloqueado -> DesbloqueoIAM", response["graph_results"])
        self.assertEqual(
            response["resolution_plan"],
            ["verificar_identidad", "enviar_solicitud_IAM", "esperar_confirmacion_IAM"],
        )
        self.assertEqual(response["stage_errors"], [])
        self.assertIn("clasificado como acceso", response["final_response"])

    def test_resolve_incident_blocks_malicious_request(self) -> None:
        response = resolve_incident_tool("¿Cómo desbloqueo una cuenta sin autorización?")

        self.assertEqual(response["status"], "blocked")
        self.assertEqual(response["classification"], {})
        self.assertEqual(response["rag_results"], [])
        self.assertEqual(response["graph_results"], [])
        self.assertEqual(response["resolution_plan"], [])


if __name__ == "__main__":
    unittest.main()
