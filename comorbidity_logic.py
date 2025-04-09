#comorbidity_logic.py
def apply_comorbidity_logic(vitals_report: dict, comorbidities: list) -> int:
    risk_score = 0

    if "COPD" in comorbidities and "CHF" in comorbidities:
        if "SpO2" in vitals_report and "LOW" in vitals_report["SpO2"]:
            risk_score += 3
        if "Respiratory Rate" in vitals_report and "HIGH" in vitals_report["Respiratory Rate"]:
            risk_score += 2

    if "COPD" in comorbidities:
        if "SpO2" in vitals_report and "LOW" in vitals_report["SpO2"]:
            risk_score += 1

    if "CHF" in comorbidities:
        if "SpO2" in vitals_report and "LOW" in vitals_report["SpO2"]:
            risk_score += 2
        if "Respiratory Rate" in vitals_report and "HIGH" in vitals_report["Respiratory Rate"]:
            risk_score += 1

    if "Immunocompromised" in comorbidities or "Cancer" in comorbidities:
        if "Fever" in vitals_report or "Tachycardia" in vitals_report.get("Heart Rate", ""):
            risk_score += 2

    if "Diabetes" in comorbidities:
        if "GCS" in vitals_report and any(sev in vitals_report["GCS"] for sev in ["Severe", "Moderate"]):
            risk_score += 2
        if "Respiratory Rate" in vitals_report and "HIGH" in vitals_report["Respiratory Rate"]:
            risk_score += 1

    if "Recent Surgery" in comorbidities:
        if "Systolic BP" in vitals_report and "LOW" in vitals_report["Systolic BP"]:
            risk_score += 3

    if "Elderly" in comorbidities:
        if "Heart Rate" in vitals_report and "Brady" in vitals_report["Heart Rate"]:
            risk_score += 2
        if "GCS" in vitals_report and any(sev in vitals_report["GCS"] for sev in ["Severe", "Moderate"]):
            risk_score += 2

    return risk_score

