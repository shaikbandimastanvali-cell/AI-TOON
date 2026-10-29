# AI Toon

AI Toon is a Streamlit educational storytelling capstone. It turns an academic topic into four cartoon-style learning scenes and a three-question quiz.

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```

The app runs in deterministic mock mode by default. To use Groq, set `GROQ_API_KEY` in the environment or Streamlit secrets and set `AI_TOON_USE_MOCK=false`.

## Verify

```powershell
python -m pytest tests -q
python -m compileall .
```

See `HANDOFF.md` for the module map, current status, and continuation prompt.
