from __future__ import annotations

from typing import ClassVar

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

SUPPORTED_LANGUAGES = ("English", "Hindi", "Telugu", "Spanish")
SUPPORTED_STYLES = ("Funny", "Adventure", "Comic")


def _clean_text(value: str) -> str:
    value = value.strip()
    if not value:
        raise ValueError("value must not be blank")
    return value


class StoryScene(BaseModel):
    model_config = ConfigDict(extra="forbid")

    scene_number: int = Field(ge=1)
    title: str = Field(min_length=1, max_length=160)
    narrative: str = Field(min_length=1, max_length=4000)
    dialogue: str = Field(min_length=1, max_length=1000)
    visual_description: str = Field(min_length=1, max_length=2000)

    _clean_fields: ClassVar[tuple[str, ...]] = ("title", "narrative", "dialogue", "visual_description")

    @field_validator(*_clean_fields)
    @classmethod
    def strip_text(cls, value: str) -> str:
        return _clean_text(value)


class QuizQuestion(BaseModel):
    model_config = ConfigDict(extra="forbid")

    question_id: int = Field(ge=1)
    question: str = Field(min_length=1, max_length=1000)
    options: list[str] = Field(min_length=4, max_length=4)
    correct_answer: str = Field(min_length=1, max_length=500)
    explanation: str = Field(min_length=1, max_length=2000)

    @field_validator("question", "correct_answer", "explanation")
    @classmethod
    def strip_text(cls, value: str) -> str:
        return _clean_text(value)

    @field_validator("options")
    @classmethod
    def validate_options(cls, value: list[str]) -> list[str]:
        cleaned = [_clean_text(option) for option in value]
        if len(set(cleaned)) != len(cleaned):
            raise ValueError("options must be unique")
        return cleaned

    @model_validator(mode="after")
    def answer_must_be_an_option(self) -> "QuizQuestion":
        if self.correct_answer not in self.options:
            raise ValueError("correct_answer must exactly match one option")
        return self


class ToonPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    topic: str = Field(min_length=1, max_length=200)
    style: str
    language: str
    scenes: list[StoryScene] = Field(min_length=4, max_length=4)
    quiz: list[QuizQuestion] = Field(min_length=3, max_length=3)

    @field_validator("topic")
    @classmethod
    def clean_topic(cls, value: str) -> str:
        return _clean_text(value)

    @field_validator("style")
    @classmethod
    def validate_style(cls, value: str) -> str:
        value = _clean_text(value)
        if value not in SUPPORTED_STYLES:
            raise ValueError(f"style must be one of {SUPPORTED_STYLES}")
        return value

    @field_validator("language")
    @classmethod
    def validate_language(cls, value: str) -> str:
        value = _clean_text(value)
        if value not in SUPPORTED_LANGUAGES:
            raise ValueError(f"language must be one of {SUPPORTED_LANGUAGES}")
        return value

    @model_validator(mode="after")
    def validate_ids(self) -> "ToonPayload":
        scene_ids = [scene.scene_number for scene in self.scenes]
        quiz_ids = [question.question_id for question in self.quiz]
        if len(set(scene_ids)) != len(scene_ids):
            raise ValueError("scene_number values must be unique")
        if len(set(quiz_ids)) != len(quiz_ids):
            raise ValueError("question_id values must be unique")
        return self
