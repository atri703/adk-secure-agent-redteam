from types import SimpleNamespace
from secure_agent.guardrails import before_tool_callback, after_model_callback
from google.adk.models import LlmResponse
from google.genai import types

def test_unknown_tool_fails_closed():
    assert before_tool_callback(SimpleNamespace(name="run_shell"), {}, SimpleNamespace())["status"] == "denied"

def test_invalid_tool_args_denied():
    result = before_tool_callback(SimpleNamespace(name="read_document"), {"document_id": "finance", "role": "admin"}, SimpleNamespace())
    assert result["status"] == "denied"

def test_output_canary_blocked():
    response = LlmResponse(content=types.Content(role="model", parts=[types.Part(text="TEST_SECRET_CANARY_7XZ9")]))
    replaced = after_model_callback(SimpleNamespace(state={"verified_role": "guest"}), response)
    assert "TEST_SECRET_CANARY" not in replaced.content.parts[0].text
