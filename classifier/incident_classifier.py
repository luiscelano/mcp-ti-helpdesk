import unicodedata
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class ClassificationResult:
    category: str
    confidence: float
    keywords: list[str]


_KEYWORD_RULES = {
    "acceso": ["usuario", "bloqueado", "cuenta", "acceso", "login", "iam"],
    "hardware": ["impresora", "papel", "controladores", "hardware", "comprobantes"],
    "software": ["sistema", "prestamos", "carga", "ssl", "software", "aplicacion"],
    "seguridad": ["sospechosa", "sospechoso", "seguridad", "fraude", "comprometida", "actividad"],
}


def _normalize_text(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text)
    without_accents = "".join(ch for ch in normalized if not unicodedata.combining(ch))
    return without_accents.lower().strip()


def classify_incident(user_input: str) -> ClassificationResult:
    normalized = _normalize_text(user_input)

    best_category = "acceso"
    best_keywords: list[str] = []
    best_score = -1

    for category, keywords in _KEYWORD_RULES.items():
        matches = [keyword for keyword in keywords if keyword in normalized]
        score = len(matches)
        if score > best_score:
            best_score = score
            best_category = category
            best_keywords = matches

    confidence = 1.0 if best_score > 0 else 0.25
    return ClassificationResult(
        category=best_category,
        confidence=confidence,
        keywords=best_keywords,
    )


def classify_incident_as_dict(user_input: str) -> dict:
    return asdict(classify_incident(user_input))
