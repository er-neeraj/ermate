# ✅ post_shift_monitoring.py (with vitals color-coded table)

import streamlit as st
from datetime import datetime
from ews_engine import run_ews
from vital_timestamp_checker import check_vital_freshness
import random
import pandas as pd

if 'er_patients' not in st.session_state:
    st.session_state.er_patients = []

st.title("🏥 In-Hospital Monitoring (ICU / Ward / Room)")

shifted_patients = [p for p in st.session_state.er_patients if p.get("shifted_to") and not p.get("discharged")]

if not shifted_patients:
    st.info("No patients have been shifted from ER yet.")

for i, patient in enumerate(shifted_patients):
    st.subheader(f"🧍 {patient['name']} – {patient['shifted_to']}")

    vitals = patient.get("vitals")
    freshness = check_vital_freshness(vitals)

    for vital, data in vitals.items():
        if vital != "log":
            freshness_status = freshness[vital]
            age = freshness_status.get("age_minutes", "N/A")
            stale = freshness_status.get("is_stale", True)
            msg = f"{vital}: {data['value']} (Last updated {age} mins ago)"
            st.warning(msg) if stale else st.success(msg)

    score = run_ews(
        age=patient['age'],
        temp_c=vitals['Temp']['value'],
        hr=vitals['HR']['value'],
        rr=vitals['RR']['value'],
        sbp=vitals['SBP']['value'],
        spo2=vitals['SpO2']['value'],
        avpu="A"
    )

    st.markdown(f"**🧠 {score['system']}**: {score['score']} points → {score['risk']}")

    if 'log' in vitals and vitals['log']:
        df = pd.DataFrame(vitals['log'])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True)

        def highlight(val, vital):
            if vital == 'HR':
                return 'background-color: #ff4d4f' if val < 60 or val > 100 else ''
            elif vital == 'RR':
                return 'background-color: #ff4d4f' if val < 12 or val > 20 else ''
            elif vital == 'SBP':
                return 'background-color: #ff4d4f' if val < 90 or val > 140 else ''
            elif vital == 'Temp':
                return 'background-color: #ff4d4f' if val < 36 or val > 38 else ''
            elif vital == 'SpO2':
                return 'background-color: #ff4d4f' if val < 94 else ''
            return ''

        st.markdown("### 📈 Previous Vitals")
        st.dataframe(df.style.apply(lambda col: [highlight(val, col.name) for val in col], axis=0), use_container_width=True)

    with st.expander("🔄 Update Vitals or Discharge"):
        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"Update Vitals – {patient['name']}", key=f"update_{i}_inhouse"):
                new_log = {
                    "timestamp": datetime.now().isoformat(),
                    "HR": random.randint(70, 140),
                    "RR": random.randint(16, 35),
                    "SBP": random.randint(90, 140),
                    "Temp": round(random.uniform(36, 39), 1),
                    "SpO2": random.randint(85, 99)
                }
                patient['vitals'].update({
                    "HR": {"value": new_log["HR"], "timestamp": new_log["timestamp"]},
                    "RR": {"value": new_log["RR"], "timestamp": new_log["timestamp"]},
                    "SBP": {"value": new_log["SBP"], "timestamp": new_log["timestamp"]},
                    "Temp": {"value": new_log["Temp"], "timestamp": new_log["timestamp"]},
                    "SpO2": {"value": new_log["SpO2"], "timestamp": new_log["timestamp"]}
                })
                patient['vitals']['log'].append(new_log)
                st.success("Vitals updated!")
                st.rerun()

        with col2:
            if st.button(f"Discharge – {patient['name']}", key=f"discharge_{i}"):
                patient['discharged'] = True
                patient['discharged_at'] = datetime.now().isoformat()
                st.success(f"✅ {patient['name']} discharged at {patient['discharged_at']}")
                st.rerun()

# Future Feature: Return visit detection
def check_previous_visits(name):
    visits = [p for p in st.session_state.er_patients if p['name'] == name and p.get("discharged")]
    if visits:
        st.info(f"🔁 Previous visit(s) detected for {name} – Last discharged on {visits[-1]['discharged_at']}")
