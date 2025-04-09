# ews_engine.py (Updated to support optional ICU-level inputs)

from mews_score import calculate_mews
from pews_score import calculate_pews
from newborn_ews import calculate_newborn_ews
from obstetric_ews import calculate_obstetric_ews

def run_ews(age: float, temp_c: float, hr: int, rr: int, sbp: int, spo2: int = None,
            avpu: str = "A", behavior: str = None, crt: float = None,
            grunting: bool = False, neuro: str = None, urine_output: float = None,
            pain_score: int = None, pregnant: bool = False, postpartum: bool = False) -> dict:
    """
    Dispatches to the correct Early Warning Score system
    based on age and obstetric status. Supports ICU extensions.
    """
    result = {
        "score": 0,
        "risk": "",
        "system": "",
        "breakdown": {}
    }

    if pregnant or postpartum:
        score, risk, breakdown = calculate_obstetric_ews(
            temp_c, hr, rr, sbp, spo2, avpu, urine_output, pain_score
        )
        result.update({"score": score, "risk": risk, "system": "OBSTETRIC EWS", "breakdown": breakdown})

    elif age < 0.1:  # Newborn (approx <28 days)
        score, risk, breakdown = calculate_newborn_ews(
            temp_c, hr, rr, spo2, neuro, grunting, pain_score
        )
        result.update({"score": score, "risk": risk, "system": "NEWBORN EWS", "breakdown": breakdown})

    elif age < 16:
        score, risk, breakdown = calculate_pews(
            temp_c, hr, rr, sbp, spo2, avpu, behavior, crt, pain_score
        )
        result.update({"score": score, "risk": risk, "system": "PEWS", "breakdown": breakdown})

    else:
        score, risk, breakdown = calculate_mews(
            hr, rr, sbp, temp_c, avpu, spo2, urine_output, pain_score
        )
        result.update({"score": score, "risk": risk, "system": "MEWS", "breakdown": breakdown})

    return result
