from __future__ import annotations

import json
import re
from typing import Any

from models import ToonPayload
from services.errors import GenerationError

try:
    from groq import Groq
except ImportError:  # pragma: no cover - exercised only when optional dependency is absent
    Groq = None  # type: ignore[assignment,misc]


def _extract_json_object(raw: str) -> dict[str, Any]:
    text = raw.strip()
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.IGNORECASE | re.DOTALL).strip()
    try:
        value = json.loads(text)
    except json.JSONDecodeError:
        start, end = text.find("{"), text.rfind("}")
        if start < 0 or end <= start:
            raise GenerationError("The AI returned an unreadable response.")
        try:
            value = json.loads(text[start : end + 1])
        except json.JSONDecodeError as exc:
            raise GenerationError("The AI returned malformed JSON.", exc) from exc
    if not isinstance(value, dict):
        raise GenerationError("The AI returned an invalid response shape.")
    return value


def parse_generation_response(raw: str, topic: str, language: str, style: str) -> ToonPayload:
    data = _extract_json_object(raw)
    data.setdefault("topic", topic)
    data.setdefault("language", language)
    data.setdefault("style", style)
    try:
        return ToonPayload.model_validate(data)
    except Exception as exc:
        raise GenerationError("The AI response did not match the required lesson format.", exc) from exc


class GroqProvider:
    def __init__(self, api_key: str, model_name: str, timeout_seconds: float = 30.0, max_retries: int = 1):
        if not api_key:
            raise GenerationError("A Groq API key is not configured.")
        if Groq is None:
            raise GenerationError("The Groq package is not installed in this environment.")
        self.api_key = api_key
        self.model_name = model_name
        self.timeout_seconds = timeout_seconds
        self.max_retries = max(0, max_retries)

    def generate(self, topic: str, language: str, style: str) -> ToonPayload:
        client = Groq(api_key=self.api_key, timeout=self.timeout_seconds, max_retries=self.max_retries)
        prompt = (
            "Create a four-scene educational cartoon lesson and a three-question multiple-choice quiz. "
            f"Topic: {topic}\nLanguage: {language}\nStyle: {style}\n"
            "Return only a JSON object with keys topic, language, style, scenes, quiz. "
            "Each scene needs scene_number, title, narrative, dialogue, visual_description. "
            "Each quiz item needs question_id, question, options (exactly four), correct_answer, explanation."
        )
        try:
            response = client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You produce concise educational JSON only."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.4,
                response_format={"type": "json_object"},
            )
            raw = response.choices[0].message.content or ""
            return parse_generation_response(raw, topic, language, style)
        except GenerationError:
            raise
        except Exception as exc:
            raise GenerationError("Story generation failed. Check connectivity and try again.", exc) from exc
