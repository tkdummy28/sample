import json
import azure.functions as func

from pipeline.step0_upload_case import upload_case
from pipeline.step1_read_case_files import read_case
from pipeline.step2_ocr_case_docs import ocr_case_documents
from pipeline.step3_extract_entities import extract_entities
from pipeline.step4_generate_case_summary import generate_summary


def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        payload = req.get_json()
        case_id = payload["caseId"]

        # STEP 0 – Upload files
        upload_case(payload)

        # STEP 1 – Read metadata
        email_desc = payload["email"]["description"]

        # STEP 2 – OCR
        ocr_text = ocr_case_documents(case_id)

        # STEP 3 – Entities
        entities = extract_entities(email_desc, ocr_text)

        # STEP 4 – Summary
        summary = generate_summary(email_desc, ocr_text, entities)

        response = {
            "caseId": case_id,
            **entities,
            **summary
        }

        return func.HttpResponse(
            json.dumps(response, indent=2),
            status_code=200,
            mimetype="application/json"
        )

    except Exception as e:
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500
        )


