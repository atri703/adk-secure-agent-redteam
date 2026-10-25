"""Read-only ADK document retrieval with identity derived from trusted session state."""
from google.adk.tools import ToolContext
from .security import safe_document

def read_document(document_id: str, tool_context: ToolContext) -> dict:
    """Read an authorized synthetic document.

    Args:
        document_id: One of handbook, policy, finance, injected.
    """
    role = tool_context.state.get("verified_role", "guest")
    return safe_document(role, document_id)
