import unittest

from mcp_server.security_gate import handle_entry_gate


class TestF2T04EntryGate(unittest.TestCase):
    def test_blocked_requests_do_not_advance(self) -> None:
        calls = {"rag": 0, "graph": 0, "planner": 0}

        def rag_runner() -> None:
            calls["rag"] += 1

        def graph_runner() -> None:
            calls["graph"] += 1

        def planner_runner() -> None:
            calls["planner"] += 1

        response = handle_entry_gate(
            "¿Cómo desbloqueo una cuenta sin autorización?",
            rag_runner=rag_runner,
            graph_runner=graph_runner,
            planner_runner=planner_runner,
        )

        self.assertEqual(response["status"], "blocked")
        self.assertEqual(calls, {"rag": 0, "graph": 0, "planner": 0})
        self.assertEqual(response["classification"], {})
        self.assertEqual(response["rag_results"], [])
        self.assertEqual(response["graph_results"], [])
        self.assertEqual(response["resolution_plan"], [])

    def test_legitimate_requests_are_classified_and_continue(self) -> None:
        calls = {"rag": 0, "graph": 0, "planner": 0}

        def rag_runner() -> None:
            calls["rag"] += 1

        def graph_runner() -> None:
            calls["graph"] += 1

        def planner_runner() -> None:
            calls["planner"] += 1

        response = handle_entry_gate(
            "Mi usuario está bloqueado.",
            rag_runner=rag_runner,
            graph_runner=graph_runner,
            planner_runner=planner_runner,
        )

        self.assertEqual(response["status"], "allowed")
        self.assertEqual(response["classification"]["category"], "acceso")
        self.assertEqual(calls, {"rag": 1, "graph": 1, "planner": 1})


if __name__ == "__main__":
    unittest.main()
