from __future__ import annotations

import streamlit as st

from components.quiz_view import render_quiz_view
from components.story_view import render_story_view
from components.ui_styles import apply_custom_theme
from config import AppConfig, load_config
from models import SUPPORTED_LANGUAGES, SUPPORTED_STYLES, ToonPayload
from services.errors import GenerationError
from services.groq_service import GroqProvider
from services.mock_provider import MockProvider


def build_provider(config: AppConfig, development_key: str | None = None):
    api_key = development_key if config.allow_dev_key_input and development_key else config.groq_api_key
    if config.use_mock or not api_key:
        return MockProvider()
    return GroqProvider(api_key, config.model_name, config.timeout_seconds, config.max_retries)


def generate_payload(config: AppConfig, topic: str, language: str, style: str, development_key: str | None = None) -> ToonPayload:
    topic = topic.strip()
    if not topic:
        raise ValueError("Enter an academic topic before generating a lesson.")
    if language not in SUPPORTED_LANGUAGES or style not in SUPPORTED_STYLES:
        raise ValueError("Choose a supported language and storytelling style.")
    return build_provider(config, development_key).generate(topic, language, style)


def main() -> None:
    st.set_page_config(page_title="AI Toon", page_icon="🤖", layout="wide")
    apply_custom_theme()
    st.title("🤖 AI Toon")
    st.caption("Turn an academic topic into a playful lesson and quiz.")
    config = load_config()

    with st.sidebar:
        st.header("Create a lesson")
        topic = st.text_input("Academic topic", placeholder="e.g. Photosynthesis")
        language = st.selectbox("Language", SUPPORTED_LANGUAGES)
        style = st.selectbox("Story style", SUPPORTED_STYLES)
        development_key = None
        if config.allow_dev_key_input:
            development_key = st.text_input("Temporary development API key", type="password", help="Used only for this run and never stored by AI Toon.")
        generate = st.button("✨ Generate lesson", type="primary", use_container_width=True)
        st.caption("Mock mode is active." if config.use_mock or not config.groq_api_key else "Groq mode is active.")

    if generate:
        try:
            with st.spinner("Creating your lesson…"):
                payload = generate_payload(config, topic, language, style, development_key)
            st.session_state["ai_toon_payload"] = payload
            st.session_state["ai_toon_story_scene_index"] = 0
            st.success("Lesson ready.")
        except (ValueError, GenerationError) as exc:
            st.error(getattr(exc, "user_message", str(exc)))
        except Exception:
            st.error("Something unexpected happened while creating the lesson. Try again.")

    payload = st.session_state.get("ai_toon_payload")
    if isinstance(payload, ToonPayload):
        story_tab, quiz_tab = st.tabs(["📖 Story scenes", "📝 Quiz"])
        with story_tab:
            render_story_view(payload)
        with quiz_tab:
            render_quiz_view(payload)
    else:
        st.info("Choose a topic and generate a lesson to begin.")


if __name__ == "__main__":
    main()
