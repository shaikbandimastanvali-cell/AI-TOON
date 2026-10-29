from __future__ import annotations

import streamlit as st

from models import ToonPayload


def next_scene_index(index: int, total: int) -> int:
    return min(max(index + 1, 0), max(total - 1, 0))


def previous_scene_index(index: int, total: int) -> int:
    return max(min(index - 1, max(total - 1, 0)), 0)


def render_story_view(payload: ToonPayload) -> None:
    key = "ai_toon_story_scene_index"
    st.session_state.setdefault(key, 0)
    index = min(st.session_state[key], len(payload.scenes) - 1)
    scene = payload.scenes[index]
    st.markdown(f'<span class="toon-badge">Scene {index + 1} of {len(payload.scenes)}</span>', unsafe_allow_html=True)
    st.markdown(f"## {scene.title}")
    st.markdown(f'<div class="toon-card"><p>{scene.narrative}</p><blockquote>“{scene.dialogue}”</blockquote><div class="toon-visual"><strong>Visual description:</strong> {scene.visual_description}</div></div>', unsafe_allow_html=True)
    previous, spacer, next_button = st.columns([1, 2, 1])
    with previous:
        if st.button("← Previous", disabled=index == 0, key="ai_toon_previous"):
            st.session_state[key] = previous_scene_index(index, len(payload.scenes))
            st.rerun()
    with next_button:
        if st.button("Next →", disabled=index == len(payload.scenes) - 1, key="ai_toon_next"):
            st.session_state[key] = next_scene_index(index, len(payload.scenes))
            st.rerun()
