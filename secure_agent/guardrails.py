"""ADK callback guardrails."""
from google.adk.models import LlmResponse
from google.genai import types
from .security import REFUSAL, check_output

def before_tool_callback(tool, args, tool_context):
    if tool.name != "read_document":
        return {"status": "denied", "message": REFUSAL}
    if set(args) != {"document_id"} or not isinstance(args.get("document_id"), str):
        return {"status": "denied", "message": REFUSAL}
    return None

def after_model_callback(callback_context, llm_response):
    if not llm_response.content or not llm_response.content.parts:
        return None
    text = "\n".join(part.text or "" for part in llm_response.content.parts if getattr(part, "text", None))
    if check_output(text, callback_context.state.get("verified_role", "guest")) != text:
        return LlmResponse(content=types.Content(role="model", parts=[types.Part(text=REFUSAL)]))
    return None
