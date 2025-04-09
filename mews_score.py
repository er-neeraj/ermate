# mews_score.py (Extended with SpO₂, Urine Output, Pain Score)

def calculate_mews(hr, rr, sbp, temp_c, avpu, spo2=None, urine_output=None, pain_score=None):
    score = 0
    details = {}

    # Respiratory Rate
    if rr <= 8:
        score += 3; details['RR'] = 3
    elif 9 <= rr <= 14:
        details['RR'] = 0
    elif 15 <= rr <= 20:
        score += 1; details['RR'] = 1
    elif 21 <= rr <= 29:
        score += 2; details['RR'] = 2
    elif rr >= 30:
        score += 3; details['RR'] = 3

    # Heart Rate
    if hr < 40:
        score += 3; details['HR'] = 3
    elif 40 <= hr <= 50:
        score += 1; details['HR'] = 1
    elif 51 <= hr <= 100:
        details['HR'] = 0
    elif 101 <= hr <= 110:
        score += 1; details['HR'] = 1
    elif 111 <= hr <= 129:
        score += 2; details['HR'] = 2
    elif hr >= 130:
        score += 3; details['HR'] = 3

    # Systolic BP
    if sbp < 70:
        score += 3; details['SBP'] = 3
    elif 70 <= sbp <= 80:
        score += 2; details['SBP'] = 2
    elif 81 <= sbp <= 100:
        score += 1; details['SBP'] = 1
    elif 101 <= sbp <= 199:
        details['SBP'] = 0
    elif sbp >= 200:
        score += 2; details['SBP'] = 2

    # Temperature (°C)
    if temp_c < 35:
        score += 2; details['Temp'] = 2
    elif 35 <= temp_c <= 38.4:
        details['Temp'] = 0
    elif 38.5 <= temp_c <= 39.9:
        score += 1; details['Temp'] = 1
    elif temp_c >= 40:
        score += 2; details['Temp'] = 2

    # AVPU (A/V/P/U)
    avpu_score = {'A': 0, 'V': 1, 'P': 2, 'U': 3}
    if avpu.upper() in avpu_score:
        score += avpu_score[avpu.upper()]
        details['AVPU'] = avpu_score[avpu.upper()]
    else:
        details['AVPU'] = 0

    # Optional: SpO2
    if spo2 is not None:
        if spo2 < 90:
            score += 3; details['SpO2'] = 3
        elif 90 <= spo2 <= 93:
            score += 2; details['SpO2'] = 2
        elif 94 <= spo2 <= 95:
            score += 1; details['SpO2'] = 1
        else:
            details['SpO2'] = 0

    # Optional: Urine Output (mL/hr)
    if urine_output is not None:
        if urine_output < 30:
            score += 2; details['Urine Output'] = 2
        else:
            details['Urine Output'] = 0

    # Optional: Pain Score (0–10)
    if pain_score is not None:
        if pain_score >= 7:
            score += 2; details['Pain Score'] = 2
        elif 4 <= pain_score <= 6:
            score += 1; details['Pain Score'] = 1
        else:
            details['Pain Score'] = 0

    # Risk Interpretation
    if score >= 7:
        risk = "EMERGENCY – Call MET/RRT"
    elif score >= 5:
        risk = "HIGH RISK – Urgent review"
    elif score >= 3:
        risk = "MODERATE – Increase monitoring"
    else:
        risk = "LOW – Routine care"

    return score, risk, details
