from vitals_checker import analyze_vitals, decide_priority_from_vitals
from triage_engine import find_priority_ai

print("\n---- ER Triage ----\n")

age = int(input("Enter patient age: "))
symptom_text = input("Describe the main symptom(s): ")
hr = int(input("Heart Rate: "))
rr = int(input("Respiratory Rate: "))
sbp = int(input("Systolic BP: "))
spo2 = int(input("SpO2: "))

gcs_input = input("GCS (press Enter to skip): ")
gcs = int(gcs_input) if gcs_input else None

avpu_input = input("AVPU (press Enter to skip): ")
avpu = avpu_input if avpu_input else None

comorb_input = input("List comorbidities (comma separated, e.g. COPD, CHF): ")
comorbidities = [c.strip() for c in comorb_input.split(",") if c.strip()]

print("\n--- VITALS ANALYSIS ---")
vitals_report = analyze_vitals(age, hr, rr, sbp, spo2, gcs, avpu)
for key, val in vitals_report.items():
    print(f"{key}: {val}")

print("\n--- TRIAGE DECISION ---")
vitals_priority = decide_priority_from_vitals(vitals_report, comorbidities)

if vitals_priority:
    print(vitals_priority)
else:
    result = find_priority_ai(symptom_text, age)
    print(result)
