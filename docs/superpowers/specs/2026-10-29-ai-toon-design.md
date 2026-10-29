# AI Toon Capstone Design

## Goal

Build a production-quality Streamlit educational storytelling app that turns an academic topic into a short, structured cartoon-style lesson followed by an interactive quiz.

## Scope

The first release supports:

- Academic topic input
- English, Hindi, Telugu, and Spanish language choices
- Funny, Adventure, and Comic storytelling styles
- Four generated educational scenes with narrative, dialogue, and visual descriptions
- Three multiple-choice quiz questions with explanations and answer feedback
- Offline mock mode for development and automated tests
- Groq-backed generation when credentials are configured

Future-scope items from the supplied presentation, including voice learning, personalization, progress tracking, and additional subjects, remain explicitly out of scope for the first release.

## Architecture

The application uses focused modules with typed boundaries:

```text
validated user input
        |
        v
generation provider interface
   /                 \
mock provider       Groq provider
        \             /
         validated ToonPayload
                |
        Streamlit session state
          /                 \
     story viewer       quiz viewer
```

`app.py` orchestrates the workflow. Pydantic models own payload validation. Providers return typed payloads or typed service errors. UI components render already-validated data and manage only their own session-state keys.

## Configuration and secret handling

- Read the Groq API key from `GROQ_API_KEY` or `st.secrets["GROQ_API_KEY"]`.
- Never write the key to files, logs, session state, generated prompts, or error messages.
- Permit an explicitly labelled development-only sidebar override only when enabled by a local configuration flag.
- Default to mock mode when no key is configured so the interface remains usable offline.
- Make model name, timeout, retry count, and generation limits configurable through environment variables with safe defaults.

## Data contracts

`StoryScene` contains a positive scene number, non-empty title, narrative, dialogue, and visual description.

`QuizQuestion` contains a positive question ID, one question, exactly four unique options, a correct answer that matches one option exactly, and an explanation.

`ToonPayload` contains the requested topic, language, style, exactly four scenes, and exactly three quiz questions. It rejects unsupported styles/languages and duplicate scene or question IDs.

## Reliability

- Use bounded HTTP/API timeouts.
- Convert provider, transport, JSON, and validation failures into safe user-facing messages.
- Preserve the previous generated payload when a later generation attempt fails.
- Reject malformed model output instead of rendering partial or unsafe content.
- Keep mock data deterministic for repeatable tests and demonstrations.

## UI and accessibility

- Use a clear two-step experience: generate lesson, then explore story and quiz.
- Keep the cartoon purple/yellow visual direction from the supplied materials while maintaining readable contrast.
- Use labels, help text, and visible validation messages for every input.
- Use native Streamlit controls for interaction and avoid relying on color alone for correct/incorrect feedback.
- Keep scene navigation and quiz submission state stable across Streamlit reruns.
- Make layout usable on narrow screens by preferring responsive columns and avoiding fixed-width content.

## Testing and handoff

Tests cover model validation, provider parsing, error mapping, configuration precedence, deterministic mock output, and pure state-transition helpers. UI smoke checks run with mock mode where practical. The project includes `HANDOFF.md` with completion status, verification commands, known limitations, and a continuation prompt for another model.

## Acceptance criteria

- The app starts in mock mode without a Groq key.
- Valid topic, language, and style selections produce a fully validated payload.
- Invalid model output never reaches the renderer.
- Scene navigation survives reruns and stays within bounds.
- Quiz feedback persists after submission and does not reset other answers.
- Missing credentials and provider failures show actionable, non-sensitive messages.
- Automated tests pass for all implemented modules, and any remaining failures are documented rather than hidden.
