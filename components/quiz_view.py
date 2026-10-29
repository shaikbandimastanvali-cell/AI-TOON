from __future__ import annotations

import streamlit as st

from models import QuizQuestion, ToonPayload


def answer_feedback(question: QuizQuestion, answer: str | None) -> tuple[bool, str]:
    if answer is None:
        return False, "Choose an answer before submitting."
    if answer == question.correct_answer:
        return True, f"Correct. {question.explanation}"
    return False, f"Incorrect. The correct answer is {question.correct_answer}. {question.explanation}"


def render_quiz_view(payload: ToonPayload) -> None:
    st.subheader("Quiz and feedback")
    score = 0
    for question in payload.quiz:
        answer_key = f"ai_toon_answer_{question.question_id}"
        submitted_key = f"ai_toon_submitted_{question.question_id}"
        st.markdown(f"### Question {question.question_id}: {question.question}")
        answer = st.radio("Choose one answer", question.options, key=answer_key, index=None)
        if st.button("Submit answer", key=f"ai_toon_submit_{question.question_id}"):
            st.session_state[submitted_key] = True
        if st.session_state.get(submitted_key):
            correct, message = answer_feedback(question, answer)
            if correct:
                score += 1
                st.success(f"Correct — {message}")
            else:
                st.error(message)
    st.info("Your score is calculated from submitted answers shown above.")
