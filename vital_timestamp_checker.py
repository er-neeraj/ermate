# vital_timestamp_checker.py

from datetime import datetime, timedelta

FRESHNESS_THRESHOLD_MINUTES = 240  # 4 hours

def check_vital_freshness(vitals_dict: dict, current_time=None):
    """
    Checks freshness of vitals.
    Each vital should be a dict with 'value' and 'timestamp' (ISO format).
    Returns dict of {vital_name: freshness_minutes, is_stale: bool}
    """
    if current_time is None:
        current_time = datetime.utcnow()

    freshness_report = {}
    for vital_name, vital_data in vitals_dict.items():
        try:
            ts = datetime.fromisoformat(vital_data['timestamp'])
            minutes_old = (current_time - ts).total_seconds() / 60
            is_stale = minutes_old > FRESHNESS_THRESHOLD_MINUTES
            freshness_report[vital_name] = {
                "age_minutes": round(minutes_old, 1),
                "is_stale": is_stale
            }
        except Exception as e:
            freshness_report[vital_name] = {
                "error": str(e),
                "is_stale": True
            }

    return freshness_report
