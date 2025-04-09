# ✅ post_shift_monitoring.py (enhanced with vitals form for manual input)

import streamlit as st
from datetime import datetime, timezone
from ews_engine import run_ews
from vital_timestamp_checker import check_vital_freshness


def render_monitoring_page(enable_popups=False, allow_discharge_button=False):
    if 'er_patients' not in st.session_state:
        st.session_state.er_patients = []

    shifted_patients = [p for p in st.session_state.er_patients if p.get("shifted_to") and not p.get("discharged")]

    if not shifted_patients:
        st.info("No patients are currently admitted to ICU / Ward / Room.")
        return

    selected_unit = st.selectbox("Filter by Location", options=sorted(set(p['shifted_to'] for p in shifted_patients)))
    st.title(f"🏥 In-Hospital Monitoring: {selected_unit}")

    for i, patient in enumerate([p for p in shifted_patients if p['shifted_to'] == selected_unit]):
        st.markdown(f"### 🧍 {patient['name']} – {selected_unit}")

        if enable_popups:
            priority = patient.get("priority", "")
            if priority == "I":
                st.error("🚨 PRIORITY I: Continuous monitoring advised!")
            elif priority == "II":
                st.warning("⚠️ PRIORITY II: Monitor every 30 minutes.")
            elif priority == "III":
                st.info("ℹ️ PRIORITY III: Stable. 1-hour monitoring.")

        vitals = patient.get("vitals")
        freshness = check_vital_freshness(vitals)
        for vital, data in vitals.items():
            if vital == "log":
                continue
            status = freshness[vital]
            age = status.get("age_minutes", "N/A")
            stale = status.get("is_stale", True)
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

        with st.expander("📜 Previous Vitals Log"):
            for log in reversed(vitals.get("log", [])):
                log_time = log['timestamp']
                summary = f"🕒 {log_time} → HR: {log['HR']}, RR: {log['RR']}, SBP: {log['SBP']}, Temp: {log['Temp']}, SpO₂: {log['SpO2']}"
                st.markdown(summary)

        with st.expander("✏️ Update Vitals or Discharge"):
            with st.form(f"update_vitals_form_{i}"):
                hr = st.number_input("Heart Rate", min_value=0, value=vitals['HR']['value'], key=f"hr_{i}")
                rr = st.number_input("Respiratory Rate", min_value=0, value=vitals['RR']['value'], key=f"rr_{i}")
                sbp = st.number_input("Systolic BP", min_value=0, value=vitals['SBP']['value'], key=f"sbp_{i}")
                temp = st.number_input("Temperature (°C)", value=vitals['Temp']['value'], key=f"temp_{i}")
                spo2 = st.number_input("SpO₂ (%)", min_value=0, max_value=100, value=vitals['SpO2']['value'], key=f"spo2_{i}")
                submitted = st.form_submit_button("Update Vitals")

                if submitted:
                    now = datetime.now(timezone.utc).isoformat()
                    new_vals = {"HR": hr, "RR": rr, "SBP": sbp, "Temp": temp, "SpO2": spo2}
                    for k, v in new_vals.items():
                        patient['vitals'][k]['value'] = v
                        patient['vitals'][k]['timestamp'] = now
                    patient['vitals']['log'].append({"timestamp": now, **new_vals})
                    st.success("Vitals updated.")
                    st.rerun()

            if allow_discharge_button and st.button(f"Discharge – {patient['name']}", key=f"discharge_monitor_{i}"):
                patient['discharged'] = True
                patient['discharged_at'] = datetime.now(timezone.utc).isoformat()
                st.success(f"✅ {patient['name']} successfully discharged.")
                st.rerun()
