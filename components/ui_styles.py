from __future__ import annotations

import streamlit as st


def apply_custom_theme() -> None:
    st.markdown(
        """
        <style>
        :root { --toon-purple: #5b21b6; --toon-yellow: #fef3c7; --toon-ink: #211a2d; }
        .toon-card { background: #fff; border: 2px solid #ddd6fe; border-radius: 1rem; padding: 1.25rem; margin: .5rem 0 1rem; box-shadow: 0 8px 22px rgba(91,33,182,.10); }
        .toon-badge { display: inline-block; background: var(--toon-purple); color: white; border-radius: 999px; padding: .25rem .7rem; font-weight: 700; }
        .toon-visual { background: var(--toon-yellow); border-left: 5px solid #f59e0b; border-radius: .5rem; padding: .75rem 1rem; }
        .feedback-label { font-weight: 700; }
        button:focus, input:focus, textarea:focus { outline: 3px solid #f59e0b !important; outline-offset: 2px; }
        @media (max-width: 640px) { .toon-card { padding: 1rem; } }
        </style>
        """,
        unsafe_allow_html=True,
    )
