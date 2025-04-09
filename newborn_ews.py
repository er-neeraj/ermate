# newborn_ews.py (Newborn Early Warning Score)

def calculate_newborn_ews(temp_c, hr, rr, spo2=None, neuro=None, grunting=False, pain_score=None):
    score = 0
    breakdown = {}

    # Heart Rate (bpm)
    if hr < 90:
        score += 3; breakdown['HR'] = 3
    elif 90 <= hr <= 100:
        score += 1; breakdown['HR'] = 1
    elif 101 <= hr <= 180:
        breakdown['HR'] = 0
    elif hr > 180:
        score += 2; breakdown['HR'] = 2

    # Respiratory Rate (breaths/min)
    if rr < 30:
        score += 3; breakdown['RR'] = 3
    elif 30 <= rr <= 40:
        score += 1; breakdown['RR'] = 1
    elif 41 <= rr <= 60:
        breakdown['RR'] = 0
    elif rr > 60:
        score += 2; breakdown['RR'] = 2

    # Temperature
    if temp_c < 36.0:
        score += 2; breakdown['Temp'] = 2
    elif 36.0 <= temp_c <= 37.5:
        breakdown['Temp'] = 0
    elif temp_c > 37.5:
        score += 1; breakdown['Temp'] = 1

    # SpO2
    if spo2 is not None:
        if spo2 < 85:
            score += 3; breakdown['SpO2'] = 3
        elif 85 <= spo2 <= 90:
            score += 2; breakdown['SpO2'] = 2
        elif 91 <= spo2 <= 94:
            score += 1; breakdown['SpO2'] = 1
        else:
            breakdown['SpO2'] = 0

    # Neurologic status (Normal / Irritable / Lethargic / Seizure)
    if neuro:
        neuro_scores = {
            'Normal': 0,
            'Irritable': 1,
            'Lethargic': 2,
            'Seizure': 3
        }
        ns = neuro_scores.get(neuro.capitalize(), 0)
        score += ns; breakdown['Neuro'] = ns

    # Grunting
    if grunting:
        score += 2; breakdown['Grunting'] = 2

    # Pain Score (optional)
    if pain_score is not None:
        if pain_score >= 7:
            score += 2; breakdown['Pain Score'] = 2
        elif 4 <= pain_score <= 6:
            score += 1; breakdown['Pain Score'] = 1
        else:
            breakdown['Pain Score'] = 0

    # Risk
    if score >= 7:
        risk = "CRITICAL – NICU Consult"
    elif score >= 4:
        risk = "HIGH – Close Monitoring"
    elif score >= 2:
        risk = "MODERATE – Reassess"
    else:
        risk = "LOW – Routine newborn care"

    return score, risk, breakdown
