from __future__ import annotations

from typing import Protocol

from models import ToonPayload


class GenerationProvider(Protocol):
    def generate(self, topic: str, language: str, style: str) -> ToonPayload:
        ...
