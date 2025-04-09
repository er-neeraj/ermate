# ai_symptom_extractor.py

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_keywords(symptom_text: str, rules_dict: dict) -> list:
    all_keywords = []
    for level, keywords in rules_dict.items():
        all_keywords.extend(keywords)

    prompt = f"""
You're a medical assistant helping triage patients. Based on the input description, identify relevant keywords that match clinical symptoms from the known triage list.

Known Symptoms:
{all_keywords}

User says: "{symptom_text}"

Return only the most relevant symptom keywords from the list, separated by commas.
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=100
    )

    output = response.choices[0].message.content
    return [kw.strip().lower() for kw in output.split(",") if kw.strip()]
