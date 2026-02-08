import json
from openai import AzureOpenAI
import os
import os , sys
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(PROJECT_ROOT)

import config as config
# ---- Azure OpenAI Config ----

DEPLOYMENT = "gpt-4o"
API_VERSION = "2024-12-01-preview"
from config import (
    FOUNDRY_API_KEY,
    FOUNDRY_ENDPOINT,
)

client = AzureOpenAI(
    azure_endpoint=FOUNDRY_ENDPOINT,
    api_key=FOUNDRY_API_KEY,
    api_version=API_VERSION
)

# ---- Load previous step outputs ----
with open("output/ocr_text.txt", "r", encoding="utf-8") as f:
    ocr_text = f.read()

with open("output/entities.json", "r", encoding="utf-8") as f:
    entities = json.load(f)

CASE_ID = "D365-FRAUD-AMT-1049"

# ---- Prompt ----
prompt = f"""
You are a senior bank fraud investigation officer.

Using ONLY the data below, generate a clear investigation summary.

CASE ID:
{CASE_ID}

EXTRACTED ENTITIES:
{json.dumps(entities, indent=2)}

OCR DOCUMENT TEXT:
{ocr_text}

Return STRICT JSON with:
- case_id
- summary (3–4 sentences)
- key_findings (bullet list)
- risk_level (LOW / MEDIUM / HIGH)
- recommended_action (single sentence)

No markdown. No explanations.
"""

response = client.chat.completions.create(
    model=DEPLOYMENT,
    messages=[
        {"role": "system", "content": "You produce fraud investigation summaries."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.2,
    max_tokens=500
)

raw_output = response.choices[0].message.content.strip()

print("\n🧠 RAW SUMMARY OUTPUT:\n")
print(raw_output)

# ---- JSON Guard ----
if raw_output.startswith("```"):
    raw_output = raw_output.replace("```json", "").replace("```", "").strip()

summary_json = json.loads(raw_output)

# ---- Save final report ----
with open("output/final_case_summary.json", "w", encoding="utf-8") as f:
    json.dump(summary_json, f, indent=2)

print("\n✅ STEP 4 COMPLETE — Final case summary generated")



