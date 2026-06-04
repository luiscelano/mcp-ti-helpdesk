import re
import unicodedata
from typing import Dict, Iterable, List


class HelpdeskEmbeddingFunction:
    _CONCEPT_ALIASES: Dict[str, List[str]] = {
        "usuario": ["usuario", "usuarios", "cuenta", "acceso"],
        "bloqueado": ["bloqueado", "bloqueada", "bloqueo"],
        "desbloqueo": ["desbloquear", "desbloqueo", "desbloquea"],
        "iam": ["iam"],
        "impresora": ["impresora", "impresion", "imprime"],
        "controladores": ["controladores", "drivers"],
        "cola": ["cola", "papel", "atascos", "red"],
        "prestamos": ["prestamos", "prestamo"],
        "sistema": ["sistema", "software", "aplicacion"],
        "ssl": ["ssl", "certificados", "certificado"],
        "carga": ["carga", "cargar", "funciona", "cargar"],
        "seguridad": ["seguridad", "sospechosa", "sospechoso"],
        "autorizacion": ["autorizacion", "cumplimiento"],
        "cache": ["cache", "navegador"],
    }

    def __call__(self, input: Iterable[str]) -> List[List[float]]:
        return [self._embed_text(text) for text in input]

    def embed_documents(self, input: Iterable[str]) -> List[List[float]]:
        return self(input)

    def embed_query(self, input):
        if isinstance(input, list):
            return [self._embed_text(text) for text in input]
        return self._embed_text(input)

    @staticmethod
    def name() -> str:
        return "helpdesk-keyword-embedding"

    @staticmethod
    def is_legacy() -> bool:
        return False

    @staticmethod
    def default_space() -> str:
        return "cosine"

    @staticmethod
    def supported_spaces() -> List[str]:
        return ["cosine", "l2", "ip"]

    @staticmethod
    def get_config() -> dict:
        return {
            "name": HelpdeskEmbeddingFunction.name(),
            "space": HelpdeskEmbeddingFunction.default_space(),
        }

    @staticmethod
    def build_from_config(config: dict) -> "HelpdeskEmbeddingFunction":
        return HelpdeskEmbeddingFunction()

    @classmethod
    def _normalize_text(cls, text: str) -> str:
        normalized = unicodedata.normalize("NFKD", text)
        without_accents = "".join(
            ch for ch in normalized if not unicodedata.combining(ch)
        )
        return without_accents.lower().strip()

    @classmethod
    def _tokenize(cls, text: str) -> List[str]:
        return re.findall(r"[a-z0-9_]+", cls._normalize_text(text))

    @classmethod
    def _embed_text(cls, text: str) -> List[float]:
        tokens = cls._tokenize(text)
        vector: List[float] = []

        for aliases in cls._CONCEPT_ALIASES.values():
            count = 0.0
            for alias in aliases:
                count += sum(1.0 for token in tokens if token == alias)
            vector.append(count)

        return vector