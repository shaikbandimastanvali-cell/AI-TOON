import pytest
from pydantic import ValidationError

from models import QuizQuestion, ToonPayload


def scene(number: int = 1) -> dict:
    return {
        "scene_number": number,
        "title": "A clear concept",
        "narrative": "A short educational explanation.",
        "dialogue": "Learning can be fun!",
        "visual_description": "Bright cartoon classroom with labeled objects.",
    }


def question(number: int = 1) -> dict:
    return {
        "question_id": number,
        "question": "Which answer is correct?",
        "options": ["A", "B", "C", "D"],
        "correct_answer": "A",
        "explanation": "A is correct because it matches the concept.",
    }


def payload() -> dict:
    return {
        "topic": "Photosynthesis",
        "style": "Funny",
        "language": "English",
        "scenes": [scene(i) for i in range(1, 5)],
        "quiz": [question(i) for i in range(1, 4)],
    }


def test_valid_payload_is_strictly_parsed():
    result = ToonPayload.model_validate(payload())
    assert result.scenes[0].scene_number == 1
    assert result.quiz[0].correct_answer == "A"


@pytest.mark.parametrize("field,value", [("style", "Drama"), ("language", "Klingon")])
def test_unsupported_choices_are_rejected(field, value):
    data = payload()
    data[field] = value
    with pytest.raises(ValidationError):
        ToonPayload.model_validate(data)


def test_duplicate_ids_are_rejected():
    data = payload()
    data["scenes"][1]["scene_number"] = 1
    with pytest.raises(ValidationError):
        ToonPayload.model_validate(data)


def test_correct_answer_must_match_an_option():
    data = question()
    data["correct_answer"] = "E"
    with pytest.raises(ValidationError):
        QuizQuestion.model_validate(data)


def test_exact_scene_and_quiz_counts_are_required():
    data = payload()
    data["scenes"] = data["scenes"][:3]
    with pytest.raises(ValidationError):
        ToonPayload.model_validate(data)
