# Copilot instructions for Recruiter Assistant (WhatsApp)

Quick, actionable guide for AI coding agents working on this repo.

## Big picture
- **Purpose:** conversational recruiter assistant that runs either as a CLI (`scripts/run_cli.py`) or a Flask webhook for Twilio WhatsApp (`scripts/run_server.py` → [src/api/app.py](src/api/app.py)).
- **Core flow:** conversation state is a simple dict manipulated by `RecruiterAssistant` in [src/main.py](src/main.py). The flow phases are: meeting booking → permission → question sequence (see `questions` in [config/settings.py](config/settings.py)).
- **Routing & nodes:** routing functions live in [src/routers/flow_routers.py](src/routers/flow_routers.py) and concrete steps are implemented as node functions under [src/nodes/](src/nodes). The graph orchestration is in [src/graph/workflow.py](src/graph/workflow.py).

## Key services and singletons
- `llm_service` — [src/services/llm_service.py](src/services/llm_service.py): wraps the LLM client (DeepInfra/OpenAI compatibility). Note: `classify_yes_no` expects the model to return strict JSON that matches `YesNoIntent` in [src/models/state.py](src/models/state.py).
- `twilio_service` — [src/services/twilio_service.py](src/services/twilio_service.py): Twilio `Client` wrapper and global `twilio_service` instance used to send messages.
- `session_manager` — [src/services/session_manager.py](src/services/session_manager.py): in-memory session store (timeout based). There is also a simpler `storage/sessions.py` helper (unused by the server stack).

## Configuration & required env vars
- Main config: [config/settings.py](config/settings.py). The following env vars are required to run the server or initiate messages:
  - `DEEPINFRA_API_KEY` (LLM)
  - `TWILIO_ACCOUNT_SID`
  - `TWILIO_AUTH_TOKEN`
  - Optional: `TWILIO_WHATSAPP_NUMBER` (defaults to Twilio sandbox in settings)
- Other useful settings: `BOOKING_LINK`, `QUESTIONS`, `WELCOME_MESSAGE_TEMPLATE`, and `SESSION_TIMEOUT_MINUTES` are defined in `config/settings.py`.

## How to run / developer workflows
- CLI (local conversation):

  python scripts/run_cli.py

- Start Flask webhook server (for Twilio):

  python scripts/run_server.py

- Send a proactive welcome message (helper script):

  python scripts/initiate_conversation.py

- When testing webhooks, use `ngrok` to expose port `5000` and point Twilio to the public URL's `/webhook/whatsapp` route. Health and debug endpoints:
  - `/health` — health check ([src/api/app.py](src/api/app.py))
  - `/session/<phone_number>` — inspect per-user session
  - `/sessions` — count active sessions

## Patterns & conventions specific to this repo
- Global singletons: many services expose a module-level instance (e.g., `twilio_service`, `llm_service`, `session_manager`). Code expects these globals and imports them from their modules.
- In-memory sessions: sessions are stored in memory (not persistent) and cleaned up after `SESSION_TIMEOUT_MINUTES`. Multi-process deployment will break session affinity — use an external store before scaling.
- Message model: conversation messages are stored in `state['messages']` as dicts `{'role': 'assistant'|'user', 'content': '...'}`. The assistant returns only new assistant messages via `get_new_messages`/`get_last_message` APIs in `RecruiterAssistant`.
- LLM outputs: `llm_service.classify_yes_no` parses JSON responses and uses a confidence threshold (`CONFIDENCE_THRESHOLD`). Treat any low-confidence result as `None`/unclear.

## Integration points & third-party dependencies
- Twilio: sending messages via `twilio_service` uses the Twilio REST client (`twilio` package). Numbers must be prefixed `whatsapp:+...` — helper `validate_phone_number` in `scripts/initiate_conversation.py`.
- DeepInfra/OpenAI: LLM calls are routed through `langchain_openai.ChatOpenAI` in `llm_service`. The repo expects `res.content` to contain JSON for classification tasks.

## Where to change behavior or messages
- Edit templates and questions in [config/settings.py](config/settings.py) — `WELCOME_MESSAGE_TEMPLATE` and `QUESTIONS` drive the conversation text.
- Booking link: change `BOOKING_LINK` in settings.
- Conversation logic: modify routers in [src/routers/flow_routers.py](src/routers/flow_routers.py) or node handlers in [src/nodes/](src/nodes).

## Debugging tips
- Use the `/session/<phone_number>` endpoint to inspect a user's state while reproducing a webhook call.
- Watch stdout of `scripts/run_server.py` for printed incoming messages and errors from `webhooks.py`.
- If multiple assistant messages are returned, extra messages are sent via `twilio_service.send_message` (see logic in [src/api/webhooks.py](src/api/webhooks.py)).

## Tests & CI
- There are no formal tests in `tests/`. Before making assumptions about behavior, run `scripts/run_cli.py` locally to exercise the flow quickly.

## Small gotchas to surface to contributors
- Session persistence: in-memory sessions mean restarting the Python process clears all sessions.
- JSON parsing from the LLM is brittle — treat parsing failures as `None` and fall back to `unclear` routes.
- Multiple send behavior: webhook returns only the first message to Twilio; subsequent messages are sent with the Twilio REST API — ensure rate limits and ordering are acceptable.

If any of this is incorrect or you want me to add examples (curl/webhook payloads, common debugging commands, or CI instructions), tell me which area to expand. 
