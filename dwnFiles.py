import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from io import FileIO


from google_auth_oauthlib.flow import InstalledAppFlow

# If modifying these SCOPES, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly"]


def get_drive_service(client_secret_file, token_file):
    flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, SCOPES)
    creds = flow.run_local_server(port=0)
    return build("drive", "v3", credentials=creds)


# Function to download file from Google Drive
def download_file(file_id, local_destination_path, credentials):
    service = build("drive", "v3", credentials=credentials)
    request = service.files().get_media(fileId=file_id)
    local_file_path = os.path.join(local_destination_path, request.execute()["name"])
    with open(local_file_path, "wb") as fh:
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print(f"Downloading {int(status.progress() * 100)}%")


# Function to list files in a folder
def list_files_in_folder(folder_id, credentials):
    service = build("drive", "v3", credentials=credentials)
    results = (
        service.files()
        .list(q=f"'{folder_id}' in parents", fields="files(id, name)")
        .execute()
    )
    files = results.get("files", [])
    return files


# Function to download contents of a folder
def download_folder_contents(folder_id, local_destination_path, credentials):
    files = list_files_in_folder(folder_id, credentials)
    for file in files:
        file_id = file["id"]
        download_file(file_id, local_destination_path, credentials)


def main():
    # Replace with your actual folder ID and service account JSON file path
    folder_id = "1mNfzd72uQtNOeGGW0nvkff5dycBwHVCA"
    creds_path = "finalyearop-cb5035f55e5d.json"
    # service_account_file = "finalyearop-cb5035f55e5d.json"
    local_destination_folder = "UploadedData"

    # Authenticate and get Google Drive service
    drive_service = get_drive_service(creds_path)

    # Download contents of the folder
    download_folder_contents(folder_id, local_destination_folder, drive_service)


if __name__ == "__main__":
    main()
