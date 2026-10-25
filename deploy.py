"""Deploy the ADK agent to Vertex AI Agent Engine / Agent Runtime.

Usage:
  python deploy.py

This creates an Agent Engine resource; it does NOT automatically expose an A2A URL.
A2A requires a reachable authenticated adapter endpoint and a valid live agent card.
"""
import os
import vertexai
from vertexai import agent_engines
from secure_agent.agent import root_agent

def main():
    project = os.environ["GOOGLE_CLOUD_PROJECT"]
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    bucket = os.environ["STAGING_BUCKET"]
    vertexai.init(project=project, location=location, staging_bucket=bucket)
    remote = agent_engines.create(
        agent_engines.AdkApp(agent=root_agent, enable_tracing=True),
        requirements=["google-cloud-aiplatform[agent_engines,adk]>=1.120.0", "google-adk[gcp]>=2.8.0,<3"],
        extra_packages=["secure_agent"],
        display_name="adk-secure-agent-redteam",
    )
    print("Agent Runtime resource:", remote.resource_name)
    print("Tracing enabled. Configure OTEL_TO_CLOUD=true in your runtime environment if supported.")

if __name__ == "__main__":
    main()
