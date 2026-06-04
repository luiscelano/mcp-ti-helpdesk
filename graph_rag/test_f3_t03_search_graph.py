import unittest

from graph_rag.search_graph import format_graph_response, search_graph


class TestF3T03SearchGraph(unittest.TestCase):
    def test_graph_001_recovers_access_relations(self) -> None:
        result = search_graph("AccesoBloqueado")
        lines = format_graph_response(result)

        self.assertIn("AccesoBloqueado -> DesbloqueoIAM", lines)
        self.assertIn("DesbloqueoIAM -> VerificacionIdentidad", lines)
        self.assertIn("DesbloqueoIAM -> OficialCumplimiento", lines)

    def test_graph_002_recovers_print_relations(self) -> None:
        result = search_graph("IncidenteImpresion")
        lines = format_graph_response(result)

        self.assertIn("IncidenteImpresion -> ReiniciarCola", lines)
        self.assertIn("IncidenteImpresion -> ReinstalarControladores", lines)

    def test_graph_003_recovers_ssl_path(self) -> None:
        result = search_graph("SistemaPrestamos")
        lines = format_graph_response(result)

        self.assertIn("SistemaPrestamos -> ProblemaSSL", lines)
        self.assertIn("ProblemaSSL -> VerificarCertificados", lines)


if __name__ == "__main__":
    unittest.main()
