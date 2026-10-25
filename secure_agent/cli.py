"""Local trusted-role demonstration: NOT a production identity provider."""
import argparse
import asyncio
import os
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from .agent import app
from .security import check_output

async def run(question: str, role: str):
    if role not in {"guest", "employee", "admin"}:
        raise ValueError("Unsupported role")
    if os.getenv("REQUIRE_MODEL_ARMOR", "0") == "1" and not app.plugins:
        raise RuntimeError("Model Armor is mandatory")
    service = InMemorySessionService()
    await service.create_session(app_name=app.name, user_id="demo", session_id="one", state={"verified_role": role})
    runner = Runner(app=app, session_service=service)
    async for event in runner.run_async(
        user_id="demo", session_id="one",
        new_message=types.Content(role="user", parts=[types.Part(text=question)]),
    ):
        if event.is_final_response() and event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    print(check_output(part.text, role))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("question")
    parser.add_argument("--role", choices=["guest", "employee", "admin"], default="guest")
    args = parser.parse_args()
    asyncio.run(run(args.question, args.role))
