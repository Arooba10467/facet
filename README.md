# Facet — Streamlit Dashboard

Real-time Focus Score dashboard implementing Proposal Sections 6-7, built for
free deployment via Streamlit Community Cloud + GitHub.

## Run locally first (recommended before deploying)

```
pip install -r requirements.txt
streamlit run app.py
```

Opens automatically at http://localhost:8501

## Notes
- The "Simulated live feed" mode updates every 2 seconds automatically,
  matching the proposal's sampling interval (Section 6.2).
- "Manual input" mode lets you drag sliders to test the Focus Score formula
  live — useful for a defense demo where you want to show a specific
  scenario (e.g., "what if CO2 hits 1500?") instantly.
- The Focus Score formula (weights, thresholds) is identical to the
  FastAPI version, so both implementations produce the same results from
  the same inputs.
