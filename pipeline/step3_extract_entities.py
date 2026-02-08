import json
from openai import AzureOpenAI
# from step2_ocr_case_docs import ocr_case_documents
import os , sys
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(PROJECT_ROOT)

# 🔒 FORCE SAME VALUES AS WORKING CODE

FOUNDRY_DEPLOYMENT_NAME = "gpt-4o"
API_VERSION = "2024-12-01-preview"

from config import (
    FOUNDRY_API_KEY,
    FOUNDRY_ENDPOINT,
)

llm_client = AzureOpenAI(
    azure_endpoint=FOUNDRY_ENDPOINT,
    api_key=FOUNDRY_API_KEY,
    api_version=API_VERSION
)


def extract_entities(email_description: str, ocr_text: str) -> dict:
    prompt = f"""
Extract ONLY the following entities.
Return STRICT JSON.

Applicant Name
Customer ID
Branch Code
Requested Amount
Sanctioned Amount

EMAIL:
{email_description}

DOCUMENT TEXT:
{ocr_text}
"""

    response = llm_client.chat.completions.create(
        model=FOUNDRY_DEPLOYMENT_NAME,
        messages=[
            {"role": "system", "content": "You extract structured fraud investigation entities."},
            {"role": "user", "content": prompt}
        ],
        temperature=0,
        max_tokens=400
    )

    raw_output = response.choices[0].message.content

    print("\n🧠 RAW MODEL OUTPUT:\n")
    print(raw_output)

    cleaned = raw_output.strip()

    if cleaned.startswith("```"):
        cleaned = cleaned.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"LLM did not return valid JSON.\n\nRAW OUTPUT:\n{raw_output}"
        ) from e





if __name__ == "__main__":
    CASE_ID = "D365-FRAUD-AMT-1049"

    email_description = (
        "System controls detected that the loan amount credited exceeds "
        "the sanctioned amount. Possible amount manipulation during disbursement."
    )

    # ocr_text = ocr_case_documents(CASE_ID)
    # entities = extract_entities(email_description, ocr_text)
    with open("output/ocr_text.txt", "r", encoding="utf-8") as f:
        ocr_text = f.read()

    entities = extract_entities(email_description, ocr_text)

    os.makedirs("output", exist_ok=True)

    with open("output/entities.json", "w", encoding="utf-8") as f:
        json.dump(entities, f, indent=2)

    print("\n💾 Entities saved to output/entities.json")


    print(json.dumps(entities, indent=2))



