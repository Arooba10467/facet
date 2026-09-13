"""
Facet - Intelligent Cognitive Environment Monitor
Streamlit dashboard implementation (Proposal Section 6-7)

"""

import time
import random
import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh

# ---------------------------------------------------------------------------
# Focus Score engine - matches Proposal Section 7.1 (Parameter Normalization)
# and Section 7.2 (Composite Score). Identical logic to the FastAPI version,
# so results are consistent across both implementations.
# ---------------------------------------------------------------------------

def interp(x, pts):
    if x <= pts[0][0]:
        return pts[0][1]
    if x >= pts[-1][0]:
        return pts[-1][1]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if x0 <= x <= x1:
            t = (x - x0) / (x1 - x0)
            return y0 + t * (y1 - y0)
    return pts[-1][1]


def norm_co2(ppm):  return interp(ppm, [(400, 100), (800, 85), (1000, 60), (1400, 25), (2000, 0)])
def norm_temp(c):   return interp(c,   [(16, 40), (20, 100), (24, 100), (28, 40), (32, 10)])
def norm_hum(pct):  return interp(pct, [(20, 40), (40, 100), (60, 100), (80, 40), (95, 10)])

W_CO2, W_TEMP, W_HUM = 0.5, 0.3, 0.2  # per Proposal Section 7.2


def compute_focus(co2, temp, hum):
    c, t, h = norm_co2(co2), norm_temp(temp), norm_hum(hum)
    score = W_CO2 * c + W_TEMP * t + W_HUM * h
    return score, c, t, h


def zone_of(score):
    if score >= 80: return "Optimal", "#0F8B8D"
    if score >= 60: return "Acceptable", "#C9A63D"
    if score >= 35: return "Degraded", "#C97B3D"
    return "Poor", "#A83232"


def recommendation_for(zone, c, t, h):
    if zone == "Optimal":
        return "Conditions look great. No action needed right now."
    worst = min([("CO2", c, "Open a window or step outside for fresh air."),
                 ("temperature", t, "Improve ventilation or cooling in the room."),
                 ("humidity", h, "Use a fan or dehumidifier to bring humidity back into range.")],
                key=lambda x: x[1])
    return f"**{zone} focus zone** — {worst[0]} is the main factor. {worst[2]}"


# ---------------------------------------------------------------------------
# Page setup
# ---------------------------------------------------------------------------
st.set_page_config(page_title="Facet — Cognitive Focus Monitor", page_icon="🧭", layout="wide")

st.markdown("""
<style>
    .big-score { font-size: 64px; font-weight: 700; line-height: 1; }
    .zone-tag { font-size: 16px; font-weight: 600; }
    .rec-box { padding: 14px 18px; border-radius: 6px; border: 1px solid #D8DEE2; margin-top: 14px;
               background: #FFFFFF; color: #1B2528; }
    div[data-testid="stMetric"] {
        background: #FFFFFF;
        border: 1px solid #D8DEE2;
        border-radius: 6px;
        padding: 10px;
    }
    div[data-testid="stMetric"] label,
    div[data-testid="stMetricLabel"] {
        color: #5B6A70 !important;
    }
    div[data-testid="stMetricValue"] {
        color: #1B2528 !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("🧭 Facet — Real-Time Cognitive Focus Monitor")
st.caption("FYP-I Demonstration · SZABIST University, Larkana Campus")

# ---------------------------------------------------------------------------
# Session state - simulated device + history (stands in for the proposal's
# Sensing layer + time-series database, Section 6)
# ---------------------------------------------------------------------------
if "history" not in st.session_state:
    st.session_state.history = []
if "sim_state" not in st.session_state:
    st.session_state.sim_state = {"co2": 600.0, "temp": 23.0, "hum": 50.0, "dir": 1}

# ---------------------------------------------------------------------------
# Sidebar - mode control
# ---------------------------------------------------------------------------
st.sidebar.header("Data Source")
mode = st.sidebar.radio("Mode", ["Simulated live feed", "Manual input"], index=0)

if mode == "Simulated live feed":
    st_autorefresh(interval=2000, key="refresh")  # matches proposal's 2-second sampling interval
    s = st.session_state.sim_state
    s["co2"] += random.uniform(-4, 18) * s["dir"]
    s["temp"] += random.uniform(-0.02, 0.12) * s["dir"]
    s["hum"] += random.uniform(-0.05, 0.3) * s["dir"]
    if s["co2"] > 1900 or s["co2"] < 450:
        s["dir"] *= -1
    s["co2"] = max(420, min(1950, s["co2"]))
    s["temp"] = max(17, min(33, s["temp"]))
    s["hum"] = max(22, min(88, s["hum"]))
    co2, temp, hum = s["co2"], s["temp"], s["hum"]
    st.sidebar.success("● Live — updates every 2s")
else:
    st.sidebar.info("Drag sliders to test the model")
    co2 = st.sidebar.slider("CO2 (ppm)", 400, 2000, 600, step=10)
    temp = st.sidebar.slider("Temperature (°C)", 16.0, 34.0, 23.0, step=0.5)
    hum = st.sidebar.slider("Relative Humidity (%)", 20, 90, 50, step=1)

# ---------------------------------------------------------------------------
# Compute + record
# ---------------------------------------------------------------------------
score, c_score, t_score, h_score = compute_focus(co2, temp, hum)
zone, color = zone_of(score)
rec = recommendation_for(zone, c_score, t_score, h_score)

st.session_state.history.append({"time": len(st.session_state.history), "focus_score": score, "zone": zone})
if len(st.session_state.history) > 150:
    st.session_state.history.pop(0)

# ---------------------------------------------------------------------------
# Main layout
# ---------------------------------------------------------------------------
col1, col2 = st.columns([1, 1.3])

with col1:
    st.markdown(f'<div class="big-score" style="color:{color}">{score:.0f}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="zone-tag" style="color:{color}">{zone}</div>', unsafe_allow_html=True)

    st.markdown("###")
    m1, m2, m3 = st.columns(3)
    m1.metric("CO2", f"{co2:.0f} ppm")
    m2.metric("Temperature", f"{temp:.1f} °C")
    m3.metric("Humidity", f"{hum:.0f} %")

    st.progress(min(int(c_score), 100), text="CO2 comfort score")
    st.progress(min(int(t_score), 100), text="Temperature comfort score")
    st.progress(min(int(h_score), 100), text="Humidity comfort score")

    st.markdown(f'<div class="rec-box">{rec}</div>', unsafe_allow_html=True)

with col2:
    st.markdown("**Focus Score — session history**")
    df = pd.DataFrame(st.session_state.history)
    if len(df) > 1:
        st.line_chart(df.set_index("time")["focus_score"], height=280)

    st.markdown("**Time in each zone**")
    if len(df) > 0:
        zone_counts = df["zone"].value_counts(normalize=True) * 100
        for z in ["Optimal", "Acceptable", "Degraded", "Poor"]:
            pct = zone_counts.get(z, 0)
            st.write(f"{z}: {pct:.0f}%")

st.markdown("---")
st.caption("Focus Score = 0.5×CO2_score + 0.3×Temperature_score + 0.2×Humidity_score  "
           "(Proposal Section 7.2). Data source above is simulated ahead of ESP8266 hardware integration.")
