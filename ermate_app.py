# ✅ ermate_app.py (with triage popup alerts, manual page transitions everywhere)

import streamlit as st
from vitals_checker import analyze_vitals, decide_priority_from_vitals
from triage_engine import find_priority_ai
from feedback_logger import log_feedback
from datetime import datetime, timezone

st.set_page_config(page_title='ErMate – Your Assistant', layout="wide")
st.sidebar.title("🧠 ErMate Navigation")

if 'er_patients' not in st.session_state:
    st.session_state.er_patients = []
if 'voice_input' not in st.session_state:
    st.session_state.voice_input = ""
if 'view' not in st.query_params:
    st.query_params['view'] = "Triage"

page = st.sidebar.radio("Go to:", ["Triage", "ER Observation Bay", "In-Hospital Monitoring"], index=["Triage", "ER Observation Bay", "In-Hospital Monitoring"].index(st.query_params.get("view", "Triage")))

if page == "Triage":
    st.title("🩺 Triage")
    if st.button("➕ Add New Patient"):
        st.query_params.update({"view": "Triage"})
        st.rerun()

    with st.form("triage_form"):
        name = st.text_input("Patient Name")
        age = st.number_input("Age", min_value=0, max_value=120)
        symptom_text = st.text_area("Describe symptoms", value=st.session_state.voice_input, height=100)
        hr = st.number_input("Heart Rate (bpm)", min_value=0)
        rr = st.number_input("Respiratory Rate (breaths/min)", min_value=0)
        sbp = st.number_input("Systolic BP (mmHg)", min_value=0)
        spo2 = st.number_input("SpO₂ (%)", min_value=0, max_value=100)
        temp_f = st.number_input("Temperature (°F)", min_value=90.0, max_value=110.0)
        gcs = st.number_input("GCS (optional)", min_value=3, max_value=15, value=15)
        avpu = st.selectbox("AVPU (optional)", options=["", "A", "V", "P", "U"])
        comorb_input = st.text_input("Comorbidities (if known)", placeholder="e.g. COPD, CHF, Elderly")
        submitted = st.form_submit_button("Run Triage")

    if submitted:
        comorbidities = [c.strip().upper() for c in comorb_input.split(",") if c.strip()]
        temp_c = round((temp_f - 32) * 5/9, 1)

        st.subheader("🔍 Vitals Analysis")
        vitals_report = analyze_vitals(age, hr, rr, sbp, spo2, gcs, avpu if avpu else None, temp_c)
        for key, val in vitals_report.items():
            st.write(f"**{key}**: {val}")

        st.subheader("📋 Triage Decision")
        priority = decide_priority_from_vitals(vitals_report, comorbidities)
        st.session_state.current_priority = priority or find_priority_ai(symptom_text, age)

        if st.session_state.current_priority.startswith("PRIORITY I"):
            st.error("🚨 PRIORITY I: Immediate attention required!")
        elif st.session_state.current_priority.startswith("PRIORITY II"):
            st.warning("⚠️ PRIORITY II: Urgent care recommended.")
        elif st.session_state.current_priority.startswith("PRIORITY III"):
            st.info("ℹ️ PRIORITY III: Moderate case, monitor appropriately.")

        st.success(st.session_state.current_priority)
        st.success("✅ Patient admitted to ER Observation.")

        timestamp = datetime.now(timezone.utc).isoformat()
        st.session_state.er_patients.append({
            "name": name or f"PT{len(st.session_state.er_patients)+1}",
            "age": age,
            "symptoms": symptom_text,
            "priority": st.session_state.current_priority.split()[1] if st.session_state.current_priority else "P3",
            "admitted_at": timestamp,
            "vitals": {
                "HR": {"value": hr, "timestamp": timestamp},
                "RR": {"value": rr, "timestamp": timestamp},
                "SBP": {"value": sbp, "timestamp": timestamp},
                "Temp": {"value": temp_c, "timestamp": timestamp},
                "SpO2": {"value": spo2, "timestamp": timestamp},
                "log": [
                    {"timestamp": timestamp, "HR": hr, "RR": rr, "SBP": sbp, "Temp": temp_c, "SpO2": spo2}
                ]
            },
            "comorbidities": comorbidities,
            "discharged": False,
            "shifted_to": None,
            "reviewed": False
        })

        st.success("🚀 Step 1 complete!")
        st.markdown("### ➡️ [Go to ER Observation](?view=ER%20Observation%20Bay)")

elif page == "ER Observation Bay":
    st.title("🧪 ER Observation")
    from er_observation_view import render_observation_page
    render_observation_page(enable_popups=True, allow_next_step_button=True)

elif page == "In-Hospital Monitoring":
    st.title("🏥 In-Hospital Monitoring")
    from post_shift_monitoring import render_monitoring_page
    render_monitoring_page(enable_popups=True, allow_discharge_button=True)
