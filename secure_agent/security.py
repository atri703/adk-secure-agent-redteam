"""Deterministic policy independent of LLM compliance."""
import re
from .data import ROLE_LEVEL, DOC_LEVEL, DOCS
REFUSAL = "I can't provide that information or perform that action."
CANARY = "TEST_SECRET_CANARY_7XZ9"

def authorize(role: str, document_id: str) -> bool:
    item = DOCS.get(document_id)
    return bool(item) and ROLE_LEVEL.get(role, -1) >= DOC_LEVEL[item["classification"]]

def safe_document(role: str, document_id: str) -> dict:
    if not authorize(role, document_id):
        return {"status": "denied", "message": REFUSAL}
    return {"status": "ok", "id": document_id, "content": DOCS[document_id]["text"]}

def check_output(text: str, role: str) -> str:
    return REFUSAL if re.search(re.escape(CANARY), text, re.IGNORECASE) else text
