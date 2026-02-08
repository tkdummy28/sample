from azure.storage.blob import BlobServiceClient
import sys, os

# -------------------------------
# Ensure parent folder is in path to import config.py
# -------------------------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(PROJECT_ROOT)

from config import BLOB_CONN_STR  # Now works even if running directly

# -------------------------------
# Resolve data directory absolute paths
# -------------------------------
DATA_DIR = os.path.join(PROJECT_ROOT, "data", "D365-FRAUD-AMT-1049")

# Map attachment filenames to their absolute paths
attachments_files = {
    "Loan_Application.pdf": os.path.join(DATA_DIR, "Loan_Application.pdf"),
    "Disbursement_Statement.pdf": os.path.join(DATA_DIR, "Disbursement_Statement.pdf"),
    "Customer_Complaint.pdf": os.path.join(DATA_DIR, "Customer_Complaint.pdf"),
    "Core_Banking_Screenshot.png": os.path.join(DATA_DIR, "Core_Banking_Screenshot.png")
}

# Check if all files exist
for name, path in attachments_files.items():
    if not os.path.exists(path):
        print(f"❌ Missing file: {path}")

# -------------------------------
# Simulated Dataverse / Power Automate payload
# -------------------------------
case_id = "D365-FRAUD-AMT-1049"

api_payload = {
    "caseId": case_id,
    "caseType": "Application Fraud",
    "fraudCategory": "Amount Fraud",
    "priority": "High",
    "email": {
        "from": "alerts@bankcore.com",
        "subject": "Excess Loan Amount Credited",
        "description": (
            "System controls detected that the loan amount credited "
            "exceeds the sanctioned amount. Preliminary review indicates "
            "possible amount manipulation during disbursement."
        ),
        "receivedOn": "2026-02-08T10:15:00Z"
    },
    "customer": {
        "name": "Anil Sharma",
        "customerId": "CUST-774512",
        "accountType": "Retail Loan"
    },
    "attachments": [
        {"fileName": fname, "localPath": path} for fname, path in attachments_files.items()
    ]
}

# -------------------------------
# Azure configuration
# -------------------------------
container_name = "case-documents"
blob_service = BlobServiceClient.from_connection_string(BLOB_CONN_STR)
container_client = blob_service.get_container_client(container_name)

# -------------------------------
# Upload attachments (FLAT, CASE-WISE)
# -------------------------------
for attachment in api_payload["attachments"]:
    file_name = attachment["fileName"]
    local_path = attachment["localPath"]

    if not os.path.exists(local_path):
        print(f"❌ Missing file: {local_path}")
        continue

    # Flat structure: only caseId/filename
    blob_path = f"{case_id}/{file_name}"

    with open(local_path, "rb") as data:
        container_client.upload_blob(
            name=blob_path,
            data=data,
            overwrite=True
        )

    print(f"✅ Uploaded: {blob_path}")

print("🚨 Amount fraud case uploaded successfully")

















# from azure.storage.blob import BlobServiceClient
# # from ..config import BLOB_CONN_STR

# import sys, os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from config import BLOB_CONN_STR

# # Get the root folder (parent of 'pipeline')
# PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# DATA_DIR = os.path.join(PROJECT_ROOT, "data", "D365-FRAUD-AMT-1049")

# loan_file = os.path.join(DATA_DIR, "Loan_Application.pdf")
# disbursement_file = os.path.join(DATA_DIR, "Disbursement_Statement.pdf")
# complaint_file = os.path.join(DATA_DIR, "Customer_Complaint.pdf")
# screenshot_file = os.path.join(DATA_DIR, "Core_Banking_Screenshot.png")

# # Example check
# for f in [loan_file, disbursement_file, complaint_file, screenshot_file]:
#     if not os.path.exists(f):
#         print(f"❌ Missing file: {f}")


# # -------------------------------
# # Simulated Dataverse / Power Automate payload
# # -------------------------------
# api_payload = {
#     "caseId": "D365-FRAUD-AMT-1049",
#     "caseType": "Application Fraud",
#     "fraudCategory": "Amount Fraud",
#     "priority": "High",

#     "email": {
#         "from": "alerts@bankcore.com",
#         "subject": "Excess Loan Amount Credited",
#         "description": (
#             "System controls detected that the loan amount credited "
#             "exceeds the sanctioned amount. Preliminary review indicates "
#             "possible amount manipulation during disbursement."
#         ),
#         "receivedOn": "2026-02-08T10:15:00Z"
#     },

#     "customer": {
#         "name": "Anil Sharma",
#         "customerId": "CUST-774512",
#         "accountType": "Retail Loan"
#     },

#     "attachments": [
#         {"fileName": "Loan_Application.pdf", "localPath": "data/D365-FRAUD-AMT-1049/Loan_Application.pdf"},
#         {"fileName": "Disbursement_Statement.pdf", "localPath": "data/D365-FRAUD-AMT-1049/Disbursement_Statement.pdf"},
#         {"fileName": "Customer_Complaint.pdf", "localPath": "data/D365-FRAUD-AMT-1049/Customer_Complaint.pdf"},
#         {"fileName": "Core_Banking_Screenshot.png", "localPath": "data/D365-FRAUD-AMT-1049/Core_Banking_Screenshot.png"}
#     ]
# }

# # -------------------------------
# # Azure configuration
# # -------------------------------
# container_name = "case-documents"
# case_id = api_payload["caseId"]

# blob_service = BlobServiceClient.from_connection_string(BLOB_CONN_STR)
# container_client = blob_service.get_container_client(container_name)

# # -------------------------------
# # Upload attachments (FLAT, CASE-WISE)
# # -------------------------------
# for attachment in api_payload["attachments"]:
#     file_name = attachment["fileName"]

#     # 🔑 Resolve absolute path safely (Windows/Linux/Azure)
#     local_path = os.path.abspath(attachment["localPath"])

#     if not os.path.exists(local_path):
#         print(f"❌ Missing file: {local_path}")
#         continue

#     # 🔑 Flat structure: only caseId/filename
#     blob_path = f"{case_id}/{file_name}"

#     with open(local_path, "rb") as data:
#         container_client.upload_blob(
#             name=blob_path,
#             data=data,
#             overwrite=True
#         )

#     print(f"✅ Uploaded: {blob_path}")

# print("🚨 Amount fraud case uploaded successfully")





