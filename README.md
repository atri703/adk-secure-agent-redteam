# ADK Secure Agent Red-Team Lab

Read-only synthetic enterprise knowledge assistant implemented with Google ADK, Gemini on Vertex AI, deterministic RBAC tools and optional fail-closed Model Armor plugin integration.

## Stack
Python 3.11+, google-adk[gcp]>=2.8, Gemini 2.5 Flash, Model Armor templates, pytest and GitHub Actions.

## Setup
```bash
python -m venv .venv
# activate venv
pip install -r requirements.txt
python -m pytest -q
```
Configure Vertex AI credentials and environment variables shown in .env.example. See https://adk.dev/integrations/model-armor/ .

## Run
```bash
python -m secure_agent.cli "Read document handbook" --role guest
python -m secure_agent.cli "Read document finance" --role guest
python -m secure_agent.cli "Read document policy" --role employee
```

The CLI role flag is for a trusted **local demonstration only**. Do not let a network client select their own authorization role; integrate verified OIDC identity into trusted session state before production usage. The records are entirely synthetic.

## Security behavior
- Document authorization happens inside the tool, not by trusting the LLM.
- Tool allowlisting rejects unknown tools and extra arguments.
- Retrieved documents must be treated as data, not instructions.
- Planted test canary is stopped in an output callback as defense-in-depth.
- Model Armor plugin screens input/output with prompt and response templates, with block_on_screening_failure=True.
- Set REQUIRE_MODEL_ARMOR=1 to refuse startup without templates. The plugin does not scan tool responses; secure tool access and an additional scanner are necessary for real documents.

## Evaluation and limitations
Run `python -m pytest -q` for offline deterministic tests of RBAC, tools and output checks. Live adversarial evaluation of injections, multi-turn jailbreaks, encoding, document-indirect instructions and Model Armor failure is still required. Finite tests cannot prove complete immunity. No external connections or executable tools are exposed. No real secrets should be stored in this repository.
