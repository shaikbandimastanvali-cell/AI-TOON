# AI Toon Implementation Plan

> **For agentic workers:** Execute this plan task-by-task with verification after each task. Preserve the handoff files and update them after every completed stage.

**Goal:** Build a tested Streamlit AI Toon capstone app that generates validated educational stories and quizzes through Groq or a deterministic offline provider.

**Architecture:** A typed domain layer feeds a provider interface with mock and Groq implementations. Streamlit components consume only validated payloads and keep independent session-state keys for scene navigation and quiz feedback.

**Tech Stack:** Python 3.10+, Streamlit, Pydantic, Requests, Groq SDK, JSON, pytest.

## Global Constraints

- API keys must come from environment variables or Streamlit secrets and must never be logged or persisted.
- The app must run offline in deterministic mock mode.
- Invalid provider output must fail validation before rendering.
- Streamlit reruns must preserve unrelated session state.
- Every completed stage must update `work/progress.md` and `HANDOFF.md`.

---

### Task 1: Project foundation and typed contracts

**Files:**
- Create: `app.py`
- Create: `config.py`
- Create: `models.py`
- Create: `services/__init__.py`
- Create: `components/__init__.py`
- Create: `requirements.txt`
- Create: `.env.example`
- Create: `.gitignore`
- Create: `tests/test_models.py`
- Modify: `work/task_plan.md`
- Modify: `work/progress.md`

**Interfaces:**
- `models.py` exports `StoryScene`, `QuizQuestion`, `ToonPayload`, `SUPPORTED_LANGUAGES`, and `SUPPORTED_STYLES`.
- `config.py` exports `AppConfig` and `load_config()`.
- `AppConfig` exposes `groq_api_key: str | None`, `model_name: str`, `timeout_seconds: float`, `max_retries: int`, and `use_mock: bool`.

- [ ] Write tests for valid payload creation, unsupported style/language rejection, duplicate IDs, invalid correct answers, and exact scene/quiz counts.
- [ ] Run `pytest tests/test_models.py -q` and confirm the new tests fail before implementation.
- [ ] Implement strict Pydantic models with normalized non-empty strings, bounded collections, unique IDs, and answer membership validation.
- [ ] Implement configuration precedence as Streamlit secrets, then environment variables, then safe defaults; do not print secret values.
- [ ] Add dependency pins or minimum versions for Python 3.10+, Streamlit, Pydantic, Requests, Groq, and pytest.
- [ ] Run `pytest tests/test_models.py -q` and confirm it passes.

### Task 2: Deterministic mock provider and service errors

**Files:**
- Create: `services/errors.py`
- Create: `services/provider.py`
- Create: `services/mock_provider.py`
- Create: `tests/test_mock_provider.py`
- Create: `tests/test_provider_contract.py`

**Interfaces:**
- `services/provider.py` defines `GenerationProvider.generate(topic: str, language: str, style: str) -> ToonPayload`.
- `services/errors.py` defines `GenerationError` with a safe `user_message` and optional internal cause.
- `services/mock_provider.py` exports `MockProvider` implementing `GenerationProvider`.

- [ ] Write tests asserting deterministic output, requested metadata preservation, and invalid input rejection.
- [ ] Run the focused tests and confirm failure before implementation.
- [ ] Implement a deterministic four-scene, three-question provider using the requested topic/language/style in safe content fields.
- [ ] Ensure mock data is suitable for UI demonstrations and contains four unique options per question.
- [ ] Run focused tests and confirm they pass.

### Task 3: Resilient Groq provider

**Files:**
- Create: `services/groq_service.py`
- Create: `tests/test_groq_service.py`
- Modify: `config.py`

**Interfaces:**
- `GroqProvider(api_key: str, model_name: str, timeout_seconds: float, max_retries: int)` implements `GenerationProvider`.
- `GroqProvider.generate(...) -> ToonPayload`.
- Internal parsing must expose a testable `parse_generation_response(raw: str, topic: str, language: str, style: str) -> ToonPayload`.

- [ ] Write tests for raw JSON, fenced JSON, extra surrounding text, malformed JSON, schema-invalid JSON, timeout, transport failure, and missing API key.
- [ ] Run `pytest tests/test_groq_service.py -q` and confirm failure before implementation.
- [ ] Implement a strict generation prompt, JSON-mode request, bounded timeout, limited retry behavior, and safe exception mapping.
- [ ] Parse only an object payload, validate with `ToonPayload`, and reject missing/extra-invalid fields without rendering partial data.
- [ ] Ensure exceptions and logs never include the API key or full prompt contents.
- [ ] Run focused tests and confirm they pass.

### Task 4: UI theme and pure interaction state

**Files:**
- Create: `components/ui_styles.py`
- Create: `components/story_view.py`
- Create: `components/quiz_view.py`
- Create: `tests/test_ui_state.py`

**Interfaces:**
- `components/story_view.py` exports `render_story_view(payload: ToonPayload) -> None`.
- `components/quiz_view.py` exports `render_quiz_view(payload: ToonPayload) -> None`.
- Pure helpers expose bounded scene-index transitions and quiz feedback calculations for tests.

- [ ] Write tests for previous/next bounds, payload replacement resetting only story-local state, answer correctness, and score calculation.
- [ ] Run focused tests and confirm failure before implementation.
- [ ] Implement accessible native Streamlit controls with stable namespaced session-state keys.
- [ ] Render scene title, narrative, dialogue, and visual description with clear headings and non-color feedback labels.
- [ ] Render one quiz question at a time or in a stable list, preserving submitted feedback and unrelated answers across reruns.
- [ ] Apply responsive CSS with readable contrast, visible focus states, and reduced reliance on decorative HTML.
- [ ] Run focused tests and confirm they pass.

### Task 5: Streamlit integration

**Files:**
- Modify: `app.py`
- Create: `tests/test_app_helpers.py`
- Modify: `work/progress.md`

**Interfaces:**
- `app.py` provides the runnable Streamlit entry point.
- App-level helpers validate topic input, choose mock/Groq provider, and replace `st.session_state.toon_payload` only after successful generation.

- [ ] Write tests for blank topics, invalid selections, mock-provider selection, and failure preservation of an existing payload.
- [ ] Run focused tests and confirm failure before implementation.
- [ ] Implement page configuration, sidebar inputs, generation action, loading state, success/error messages, and story/quiz tabs.
- [ ] Keep prior content visible when a new generation fails.
- [ ] Use configuration-driven mock mode and secrets/environment credentials without persisting secrets in session state.
- [ ] Run focused tests and confirm they pass.

### Task 6: Verification and handoff

**Files:**
- Create: `HANDOFF.md`
- Create: `README.md`
- Modify: `work/task_plan.md`
- Modify: `work/progress.md`

- [ ] Run the complete test suite with `pytest -q`.
- [ ] Run a compile check with `python -m compileall .`.
- [ ] Run a mock-mode Streamlit smoke check if the local environment supports it.
- [ ] Record exact pass/fail output and any environment limitations.
- [ ] Document setup, secrets configuration, mock mode, test commands, module boundaries, and the next continuation prompt.
- [ ] Review the repository for accidental secret files, generated artifacts, and stale placeholders.
- [ ] Mark only verified work complete; do not claim zero defects without evidence.
