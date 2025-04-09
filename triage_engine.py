## triage_engine.py
from utils.loader import load_rules
from ai_symptom_extractor import extract_keywords

def find_priority(symptom: str, age: int) -> str:
    symptom = symptom.lower()
    file_path = "rules/pediatric_rules.json" if age <= 16 else "rules/adult_rules.json"
    rules = load_rules(file_path)

    for priority_level, keywords in rules.items():
        for keyword in keywords:
            if keyword in symptom:
                return f"{'PEDIATRIC' if age <= 16 else 'ADULT'}: {priority_level.upper()} – Matched keyword: '{keyword}'"
    
    return f"{'PEDIATRIC' if age <= 16 else 'ADULT'}: PRIORITY UNDETERMINED – No matching condition found."


# ✅ ADD THIS FUNCTION BELOW THE ABOVE ONE

def find_priority_ai(symptom_text: str, age: int) -> str:
    file_path = "rules/pediatric_rules.json" if age <= 16 else "rules/adult_rules.json"
    rules = load_rules(file_path)

    matched_keywords = extract_keywords(symptom_text, rules)

    for keyword in matched_keywords:
        for level, items in rules.items():
            if keyword in [k.lower() for k in items]:
                return f"{'PEDIATRIC' if age <= 16 else 'ADULT'}: {level.upper()} – Matched via AI: '{keyword}'"

    return f"{'PEDIATRIC' if age <= 16 else 'ADULT'}: PRIORITY UNDETERMINED – No AI-matched rule found."
