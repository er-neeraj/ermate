# ✅ er_observation_view.py (enhanced with vitals input form)

import streamlit as st
from datetime import datetime, timezone
from vitals_checker import analyze_vitals, decide_priority_from_vitals
from ews_engine import run_ews
from vital_timestamp_checker import check_vital_freshness


def render_observation_page(enable_popups=False, allow_next_step_button=False):
    st.subheader("Patients Under ER Observation")

    patients = [p for p in st.session_state.er_patients if not p.get("shifted_to") and not p.get("discharged")]

    if not patients:
        st.info("No patients currently in ER Observation.")
        return

    for i, patient in enumerate(patients):
        st.markdown(f"### 🧍 {patient['name']} (Priority {patient['priority']})")

        if enable_popups:
            priority = patient.get("priority", "")
            if priority == "I":
                st.error("🚨 PRIORITY I patient! Monitor closely.")
            elif priority == "II":
                st.warning("⚠️ PRIORITY II: Requires monitoring.")
            elif priority == "III":
                st.info("ℹ️ PRIORITY III: Stable")

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

        with st.expander("📜 Previous Vitals Log"):
            for log in reversed(vitals.get("log", [])):
                log_time = log['timestamp']
                summary = f"🕒 {log_time} → HR: {log['HR']}, RR: {log['RR']}, SBP: {log['SBP']}, Temp: {log['Temp']}, SpO₂: {log['SpO2']}"
                st.markdown(summary)

        with st.expander("✏️ Actions"):
            cols = st.columns(3)
            if cols[0].button(f"Mark as Reviewed – {patient['name']}", key=f"review_{i}"):
                patient['reviewed'] = True
                st.success(f"✅ Reviewed at {datetime.now(timezone.utc).isoformat()}")
                st.rerun()

            with cols[1].form(f"update_vitals_form_{i}"):
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
                    st.success("Vitals updated!")
                    st.rerun()

            if cols[2].button(f"Discharge – {patient['name']}", key=f"discharge_{i}"):
                patient['discharged'] = True
                patient['discharged_at'] = datetime.now(timezone.utc).isoformat()
                st.success(f"✅ {patient['name']} discharged.")
                st.rerun()

        if allow_next_step_button:
            st.markdown("---")
            with st.expander("🏥 Shift to ICU / Ward / Room"):
                options = ["MICU", "SICU", "PICU", "Ward 1", "Ward 2", "Room 101", "Room 202"]
                selection = st.selectbox(f"Shift {patient['name']} to:", options, key=f"shift_select_{i}")
                if st.button(f"🚚 Confirm Shift to {selection}", key=f"confirm_shift_{i}"):
                    patient['shifted_to'] = selection
                    st.success(f"➡️ Patient moved to {selection}")
                    st.rerun()