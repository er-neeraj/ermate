from comorbidity_logic import apply_comorbidity_logic

def get_vital_reference(age: int):
    if age < 1:
        return {"HR": (100, 160), "RR": (30, 60), "SBP": (70, 100), "SpO2": 94}
    elif age <= 3:
        return {"HR": (90, 150), "RR": (24, 40), "SBP": (75, 105), "SpO2": 94}
    elif age <= 5:
        return {"HR": (80, 140), "RR": (22, 34), "SBP": (80, 110), "SpO2": 94}
    elif age <= 12:
        return {"HR": (70, 120), "RR": (18, 30), "SBP": (85, 115), "SpO2": 94}
    elif age <= 16:
        return {"HR": (60, 100), "RR": (12, 20), "SBP": (90, 120), "SpO2": 94}
    else:
        return {"HR": (60, 100), "RR": (12, 20), "SBP": (90, 140), "SpO2": 94}

def classify_vital(value, normal_range, name):
    if isinstance(normal_range, tuple):
        if value < normal_range[0]:
            return f"{name}: LOW (Brady{name.lower()})"
        elif value > normal_range[1]:
            return f"{name}: HIGH (Tachy{name.lower()})"
        else:
            return f"{name}: Normal"
    else:
        return f"{name}: LOW (Hypoxia)" if value < normal_range else f"{name}: Normal"

def analyze_vitals(age, hr, rr, sbp, spo2, gcs=None, avpu=None, temp_c=None):
    reference = get_vital_reference(age)
    result = {
        "Heart Rate": classify_vital(hr, reference["HR"], "Heart Rate"),
        "Respiratory Rate": classify_vital(rr, reference["RR"], "Respiratory Rate"),
        "Systolic BP": classify_vital(sbp, reference["SBP"], "Systolic BP"),
        "SpO2": classify_vital(spo2, reference["SpO2"], "SpO2")
    }

    if temp_c is not None:
        result["Temperature (°C)"] = f"{temp_c} °C"
        result["Temperature (°F)"] = f"{round((temp_c * 9/5) + 32, 1)} °F"

    if gcs is not None:
        result["GCS"] = f"GCS Score: {gcs} – {'Severe' if gcs <= 8 else 'Moderate' if gcs <= 12 else 'Mild'}"
    if avpu is not None:
        result["AVPU"] = f"AVPU Status: {avpu.upper()} – {'Unresponsive' if avpu.upper() == 'U' else 'Altered' if avpu.upper() in ['P','V'] else 'Alert'}"

    return result


def decide_priority_from_vitals(vitals_report, comorbidities=[]):
    red_flags = ["Brady", "Tachy", "Hypoxia", "Severe", "Unresponsive"]
    base_score = 0

    for value in vitals_report.values():
        for flag in red_flags:
            if flag in value:
                base_score += 2

    comorb_score = apply_comorbidity_logic(vitals_report, comorbidities)
    total_score = base_score + comorb_score

    if total_score >= 6:
        return "PRIORITY I – IMMEDIATE: Vitals + comorbidities indicate critical condition."
    elif total_score >= 3:
        return "PRIORITY II – URGENT: Patient needs close monitoring."
    elif total_score >= 1:
        return "PRIORITY III – MODERATE: Evaluate within standard time."
    else:
        return None
