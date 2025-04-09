# obstetric_ews.py (Obstetric Early Warning Score – OEWS)

def calculate_obstetric_ews(temp_c, hr, rr, sbp, spo2, avpu, urine_output=None, pain_score=None):
    score = 0
    breakdown = {}

    # Heart Rate
    if hr < 50:
        score += 3; breakdown['HR'] = 3
    elif 50 <= hr <= 100:
        breakdown['HR'] = 0
    elif 101 <= hr <= 119:
        score += 1; breakdown['HR'] = 1
    elif 120 <= hr <= 139:
        score += 2; breakdown['HR'] = 2
    else:
        score += 3; breakdown['HR'] = 3

    # Respiratory Rate
    if rr < 10:
        score += 3; breakdown['RR'] = 3
    elif 10 <= rr <= 20:
        breakdown['RR'] = 0
    elif 21 <= rr <= 24:
        score += 1; breakdown['RR'] = 1
    elif 25 <= rr <= 29:
        score += 2; breakdown['RR'] = 2
    else:
        score += 3; breakdown['RR'] = 3

    # Systolic BP
    if sbp < 90:
        score += 3; breakdown['SBP'] = 3
    elif 90 <= sbp <= 100:
        score += 1; breakdown['SBP'] = 1
    elif 101 <= sbp <= 149:
        breakdown['SBP'] = 0
    elif 150 <= sbp <= 159:
        score += 1; breakdown['SBP'] = 1
    else:
        score += 2; breakdown['SBP'] = 2

    # Temperature
    if temp_c < 35:
        score += 2; breakdown['Temp'] = 2
    elif 35 <= temp_c <= 38:
        breakdown['Temp'] = 0
    elif temp_c > 38:
        score += 1; breakdown['Temp'] = 1

    # SpO2
    if spo2 < 90:
        score += 3; breakdown['SpO2'] = 3
    elif 90 <= spo2 <= 94:
        score += 1; breakdown['SpO2'] = 1
    else:
        breakdown['SpO2'] = 0

    # AVPU
    avpu_score = {'A': 0, 'V': 1, 'P': 2, 'U': 3}
    score += avpu_score.get(avpu.upper(), 0)
    breakdown['AVPU'] = avpu_score.get(avpu.upper(), 0)

    # Urine Output (mL/hr)
    if urine_output is not None:
        if urine_output < 20:
            score += 3; breakdown['Urine Output'] = 3
        elif 20 <= urine_output < 30:
            score += 1; breakdown['Urine Output'] = 1
        else:
            breakdown['Urine Output'] = 0

    # Pain Score (0–10)
    if pain_score is not None:
        if pain_score >= 7:
            score += 2; breakdown['Pain Score'] = 2
        elif 4 <= pain_score <= 6:
            score += 1; breakdown['Pain Score'] = 1
        else:
            breakdown['Pain Score'] = 0

    # Risk Stratification
    if score >= 8:
        risk = "CRITICAL – Immediate OB team review"
    elif score >= 5:
        risk = "HIGH – Close monitoring and OB referral"
    elif score >= 3:
        risk = "MODERATE – Reassess frequently"
    else:
        risk = "LOW – Routine care"

    return score, risk, breakdown
