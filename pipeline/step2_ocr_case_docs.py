

from azure.storage.blob import BlobServiceClient
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
import os , sys
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(PROJECT_ROOT)

from config import (
    BLOB_CONN_STR,
    DOC_INTEL_ENDPOINT,
    DOC_INTEL_KEY
)

CONTAINER_NAME = "case-documents"

def ocr_case_documents(case_id: str) -> str:
    blob_service = BlobServiceClient.from_connection_string(BLOB_CONN_STR)
    container = blob_service.get_container_client(CONTAINER_NAME)

    doc_client = DocumentAnalysisClient(
        endpoint=DOC_INTEL_ENDPOINT,
        credential=AzureKeyCredential(DOC_INTEL_KEY)
    )

    print(f"\n🔍 Running OCR for case: {case_id}\n")

    all_text = []

    for blob in container.list_blobs(name_starts_with=f"{case_id}/"):
        print(f"📄 OCR processing: {blob.name}")

        blob_client = container.get_blob_client(blob.name)
        file_bytes = blob_client.download_blob().readall()

        poller = doc_client.begin_analyze_document(
            model_id="prebuilt-layout",
            document=file_bytes
        )

        result = poller.result()

        for page in result.pages:
            for line in page.lines:
                all_text.append(line.content)

    combined_text = "\n".join(all_text)

    print("\n✅ OCR completed")
    print("📌 Sample OCR output (first 500 chars):\n")
    print(combined_text[:500])

    return combined_text


# if __name__ == "__main__":
#     ocr_text = ocr_case_documents("D365-FRAUD-AMT-1049")

import os
if __name__ == "__main__":
    CASE_ID = "D365-FRAUD-AMT-1049"

    ocr_text = ocr_case_documents(CASE_ID)

    os.makedirs("output", exist_ok=True)

    with open("output/ocr_text.txt", "w", encoding="utf-8") as f:
        f.write(ocr_text)

    print("\n💾 OCR text saved to output/ocr_text.txt")


