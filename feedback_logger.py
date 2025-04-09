# feedback_logger.py
import json
from pathlib import Path

LOG_FILE = Path("feedback_log.jsonl")

def log_feedback(data: dict):
    try:
        with LOG_FILE.open("a") as f:
            f.write(json.dumps(data) + "\n")
    except Exception as e:
        print(f"Error saving feedback: {e}")
