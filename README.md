
# SIUE Intelligent Prompting — Weekly Modules (Dynamic)

This Streamlit app renders your full course syllabus as interactive weekly modules using `syllabus.yaml`.

## Quick Start (Streamlit Cloud)
1) Create a public GitHub repo and upload:
   - `app.py`
   - `requirements.txt`
   - `syllabus.yaml`
2) In Streamlit Cloud → New app → select repo → main file `app.py`.
3) In **Settings → Secrets**, add: `OPENAI_API_KEY = sk-...`

## Local Run
```bash
pip install -r requirements.txt
export OPENAI_API_KEY=your_key  # or set in your terminal/OS env
streamlit run app.py
```

## Notes
- Uses retry/backoff for rate limits.
- Exact module names and titles are taken from `syllabus.yaml` and shown verbatim.
- You can update weekly content by editing `syllabus.yaml` without touching code.
