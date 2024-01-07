# pip install google-api-python-client
from googleapiclient.discovery import build
from google.oauth2 import service_account

SCOPES = ["https://www.googleapis.com/auth/drive"]
SERVICE_ACCOUNT_FILE = "finalyearop-cb5035f55e5d.json"
PARENT_FOLDER_ID = "1mNfzd72uQtNOeGGW0nvkff5dycBwHVCA"


def authenticate():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    return creds


def upload_files(file_path):
    creds = authenticate()
    service = build("drive", "v3", credentials=creds)

    file_metadata = {"name": "Demonstration", "parents": [PARENT_FOLDER_ID]}

    file = service.files().create(body=file_metadata, media_body=file_path).execute()


upload_files("finalyrdata_1.xlsx")


# https://drive.google.com/drive/folders/1mNfzd72uQtNOeGGW0nvkff5dycBwHVCA?usp=sharing
