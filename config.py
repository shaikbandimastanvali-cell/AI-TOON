from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class AppConfig:
    groq_api_key: str | None
    model_name: str = "llama-3.3-70b-versatile"
    timeout_seconds: float = 30.0
    max_retries: int = 1
    use_mock: bool = True
    allow_dev_key_input: bool = False


def _secret_value(name: str) -> str | None:
    try:
        import streamlit as st

        value = st.secrets.get(name)
        if value:
            return str(value)
    except Exception:
        pass
    return os.getenv(name) or None


def load_config() -> AppConfig:
    api_key = _secret_value("GROQ_API_KEY")
    use_mock = os.getenv("AI_TOON_USE_MOCK", "true").lower() in {"1", "true", "yes", "on"}
    if api_key and "AI_TOON_USE_MOCK" not in os.environ:
        use_mock = False
    return AppConfig(
        groq_api_key=api_key,
        model_name=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
        timeout_seconds=float(os.getenv("GROQ_TIMEOUT_SECONDS", "30")),
        max_retries=max(0, int(os.getenv("GROQ_MAX_RETRIES", "1"))),
        use_mock=use_mock,
        allow_dev_key_input=os.getenv("AI_TOON_ALLOW_DEV_KEY_INPUT", "false").lower() in {"1", "true", "yes", "on"},
    )
