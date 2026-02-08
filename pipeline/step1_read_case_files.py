from azure.storage.blob import BlobServiceClient
import os , sys
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(PROJECT_ROOT)

from config import BLOB_CONN_STR

CONTAINER_NAME = "case-documents"

def read_case_files(case_id: str):
    blob_service = BlobServiceClient.from_connection_string(BLOB_CONN_STR)
    container = blob_service.get_container_client(CONTAINER_NAME)

    print(f"\n📂 Reading files for case: {case_id}\n")

    found = False

    for blob in container.list_blobs(name_starts_with=f"{case_id}/"):
        found = True
        print(f"📄 File: {blob.name}")
        print(f"   Size: {blob.size} bytes\n")

    if not found:
        print("❌ No files found for this case")

if __name__ == "__main__":
    read_case_files("D365-FRAUD-AMT-1049")


