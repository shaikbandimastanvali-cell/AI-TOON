from __future__ import annotations

from models import ToonPayload


class MockProvider:
    def generate(self, topic: str, language: str, style: str) -> ToonPayload:
        scenes = [
            {
                "scene_number": i,
                "title": f"{topic}: chapter {i}",
                "narrative": f"In this {style.lower()} lesson, our toon guide explains {topic} in {language}.",
                "dialogue": f"Let us explore {topic} one step at a time!",
                "visual_description": f"A bright cartoon classroom showing the idea from {topic}, scene {i}.",
            }
            for i in range(1, 5)
        ]
        quiz = [
            {
                "question_id": i,
                "question": f"What should a learner remember about {topic}, point {i}?",
                "options": [f"Key idea {i}", "A random guess", "An unrelated fact", "No idea"],
                "correct_answer": f"Key idea {i}",
                "explanation": f"Key idea {i} is the lesson's main point for {topic}.",
            }
            for i in range(1, 4)
        ]
        return ToonPayload(topic=topic, language=language, style=style, scenes=scenes, quiz=quiz)
