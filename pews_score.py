# pews_score.py (Pediatric Early Warning Score – with extended options)

def calculate_pews(temp_c, hr, rr, sbp, spo2=None, avpu=None, behavior=None, crt=None, pain_score=None):
    score = 0
    breakdown = {}

    # HR
    if hr < 60:
        score += 3; breakdown['HR'] = 3
    elif 60 <= hr <= 100:
        breakdown['HR'] = 0
    elif 101 <= hr <= 130:
        score += 1; breakdown['HR'] = 1
    elif 131 <= hr <= 150:
        score += 2; breakdown['HR'] = 2
    else:
        score += 3; breakdown['HR'] = 3

    # RR
    if rr < 10:
        score += 3; breakdown['RR'] = 3
    elif 10 <= rr <= 20:
        breakdown['RR'] = 0
    elif 21 <= rr <= 29:
        score += 1; breakdown['RR'] = 1
    elif 30 <= rr <= 39:
        score += 2; breakdown['RR'] = 2
    else:
        score += 3; breakdown['RR'] = 3

    # SBP
    if sbp < 70:
        score += 3; breakdown['SBP'] = 3
    elif 70 <= sbp <= 90:
        score += 2; breakdown['SBP'] = 2
    elif 91 <= sbp <= 110:
        breakdown['SBP'] = 0
    else:
        score += 1; breakdown['SBP'] = 1

    # Optional SpO₂
    if spo2 is not None:
        if spo2 < 90:
            score += 3; breakdown['SpO2'] = 3
        elif 90 <= spo2 <= 93:
            score += 2; breakdown['SpO2'] = 2
        elif 94 <= spo2 <= 95:
            score += 1; breakdown['SpO2'] = 1
        else:
            breakdown['SpO2'] = 0

    # Optional AVPU
    avpu_score = {'A': 0, 'V': 1, 'P': 2, 'U': 3}
    if avpu and avpu.upper() in avpu_score:
        score += avpu_score[avpu.upper()]
        breakdown['AVPU'] = avpu_score[avpu.upper()]

    # Optional Behavior (Alert, Irritable, Lethargic, Unresponsive)
    if behavior:
        behavior_score = {
            'Alert': 0,
            'Irritable': 1,
            'Lethargic': 2,
            'Unresponsive': 3
        }
        b_score = behavior_score.get(behavior.capitalize(), 0)
        score += b_score
        breakdown['Behavior'] = b_score

    # Optional Cap Refill Time (sec)
    if crt is not None:
        if crt > 3:
            score += 2; breakdown['CRT'] = 2
        elif crt > 2:
            score += 1; breakdown['CRT'] = 1
        else:
            breakdown['CRT'] = 0

    # Optional Pain Score (0–10)
    if pain_score is not None:
        if pain_score >= 7:
            score += 2; breakdown['Pain Score'] = 2
        elif 4 <= pain_score <= 6:
            score += 1; breakdown['Pain Score'] = 1
        else:
            breakdown['Pain Score'] = 0

    # Risk Interpretation
    if score >= 7:
        risk = "CRITICAL – Pediatric Emergency Team"
    elif score >= 4:
        risk = "HIGH – Urgent review"
    elif score >= 2:
        risk = "MODERATE – Reassess"
    else:
        risk = "LOW – Routine monitoring"

    return score, risk, breakdown
