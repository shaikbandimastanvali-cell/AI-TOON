from models import QuizQuestion
from components.quiz_view import answer_feedback
from components.story_view import next_scene_index, previous_scene_index


def test_scene_indices_stay_in_bounds():
    assert previous_scene_index(0, 4) == 0
    assert next_scene_index(3, 4) == 3
    assert next_scene_index(1, 4) == 2


def test_quiz_feedback_is_explicit():
    question = QuizQuestion(question_id=1, question="Q", options=["A", "B", "C", "D"], correct_answer="A", explanation="Because A.")
    assert answer_feedback(question, "A")[0] is True
    assert answer_feedback(question, "B")[0] is False
    assert answer_feedback(question, None)[1].startswith("Choose")
