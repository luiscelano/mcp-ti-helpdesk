import unittest

from classifier.incident_classifier import classify_incident_as_dict


class TestCLSRegression(unittest.TestCase):
    def test_cls_001_access(self) -> None:
        result = classify_incident_as_dict("Mi usuario está bloqueado.")
        self.assertEqual(result["category"], "acceso")

    def test_cls_002_hardware(self) -> None:
        result = classify_incident_as_dict("La impresora no genera comprobantes.")
        self.assertEqual(result["category"], "hardware")

    def test_cls_003_software(self) -> None:
        result = classify_incident_as_dict("El sistema de préstamos no carga.")
        self.assertEqual(result["category"], "software")

    def test_cls_004_security(self) -> None:
        result = classify_incident_as_dict("Detecté actividad sospechosa en mi cuenta.")
        self.assertEqual(result["category"], "seguridad")


if __name__ == "__main__":
    unittest.main()
