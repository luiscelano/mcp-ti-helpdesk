import re
import unicodedata
from dataclasses import dataclass


@dataclass(frozen=True)
class SecurityDecision:
    status: str
    reason: str | None


def _normalize_text(user_input: str) -> str:
    normalized = unicodedata.normalize("NFKD", user_input)
    without_accents = "".join(ch for ch in normalized if not unicodedata.combining(ch))
    return without_accents.lower().strip()


def _is_prompt_injection_attempt(text: str) -> bool:
    patterns = [
        r"\bignora\b",
        r"\bignore\b",
        r"\bdesactiva\b",
        r"\bomite\b",
        r"\brevela\b",
        r"\bbypass\b",
        r"\bpoliticas?\b",
    ]
    hits = sum(1 for pattern in patterns if re.search(pattern, text))
    return hits >= 2


def _is_unauthorized_action_request(text: str) -> bool:
    asks_unlock = bool(re.search(r"\b(desbloque|desbloquear|desbloqueo)\b", text))
    asks_without_auth = bool(re.search(r"\bsin\s+autorizaci(?:o|ó)n\b", text))
    return asks_unlock and asks_without_auth


def evaluate_security(user_input: str) -> SecurityDecision:
    normalized = _normalize_text(user_input)

    if _is_prompt_injection_attempt(normalized):
        return SecurityDecision(status="blocked", reason="prompt_injection")

    if _is_unauthorized_action_request(normalized):
        return SecurityDecision(status="blocked", reason="unauthorized_action")

    return SecurityDecision(status="allowed", reason=None)
