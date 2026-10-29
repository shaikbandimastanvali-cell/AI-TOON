import json

import pytest

from services.errors import GenerationError
from services.groq_service import parse_generation_response


def valid_data() -> dict:
    return {
        "scenes": [
            {"scene_number": i, "title": f"S{i}", "narrative": "N", "dialogue": "D", "visual_description": "V"}
            for i in range(1, 5)
        ],
        "quiz": [
            {"question_id": i, "question": "Q", "options": ["A", "B", "C", "D"], "correct_answer": "A", "explanation": "E"}
            for i in range(1, 4)
        ],
    }


def test_parser_accepts_json_and_fenced_json():
    raw = json.dumps(valid_data())
    assert parse_generation_response(raw, "Gravity", "English", "Funny").topic == "Gravity"
    assert parse_generation_response(f"```json\n{raw}\n```", "Gravity", "English", "Funny").style == "Funny"


def test_parser_rejects_malformed_json():
    with pytest.raises(GenerationError):
        parse_generation_response("not json", "Gravity", "English", "Funny")


def test_parser_rejects_invalid_schema():
    data = valid_data()
    data["quiz"] = []
    with pytest.raises(GenerationError):
        parse_generation_response(json.dumps(data), "Gravity", "English", "Funny")
