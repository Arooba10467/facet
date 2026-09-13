# Facet — Streamlit Dashboard

Real-time Focus Score dashboard implementing Proposal Sections 6-7, built for
free deployment via Streamlit Community Cloud + GitHub.

## Run locally first (recommended before deploying)

```
pip install -r requirements.txt
streamlit run app.py
```

Opens automatically at http://localhost:8501

## Deploy for free (so your supervisor just opens a link — no setup needed)

### Step 1 — Push this folder to GitHub
1. Go to https://github.com and create a new repository (e.g. `facet-fyp`)
2. Make sure `app.py` and `requirements.txt` are both in the root of the repo
   (not inside a subfolder), since Streamlit Cloud looks for `app.py` at the
   top level by default.
3. Upload the files (via GitHub's web "Add file → Upload files" button is
   the simplest way if you're not using git commands yet), then commit.

### Step 2 — Deploy on Streamlit Community Cloud
1. Go to https://share.streamlit.io
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository, branch (`main`), and main file path (`app.py`)
5. Click "Deploy"

Streamlit will install the requirements automatically and give you a public
URL like `https://your-app-name.streamlit.app` within a minute or two.

### Step 3 — Share the link
Send that URL to your supervisor. She can open it directly in any browser —
no Python, no CMD, no installation on her end at all.

## Notes

- The "Simulated live feed" mode updates every 2 seconds automatically,
  matching the proposal's sampling interval (Section 6.2).
- "Manual input" mode lets you drag sliders to test the Focus Score formula
  live — useful for a defense demo where you want to show a specific
  scenario (e.g., "what if CO2 hits 1500?") instantly.
- The Focus Score formula (weights, thresholds) is identical to the
  FastAPI version, so both implementations produce the same results from
  the same inputs.
