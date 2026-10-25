"""Standalone A2A server for an ADK agent. Deploy separately from Agent Runtime."""
import os
import uvicorn
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from secure_agent.agent import root_agent

# The ADK A2A adapter generates the actual served agent card and task handling.
# agent_card.json is an illustrative deployment template, not a live endpoint.
app = to_a2a(root_agent, port=int(os.getenv("PORT", "8080")))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8080")))
