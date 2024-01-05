import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account
import io


def authenticate():
    # Replace with the path to your service account JSON file
    service_account_file = "finalyearop-cb5035f55e5d.json"

    creds = service_account.Credentials.from_service_account_file(
        service_account_file, scopes=["https://www.googleapis.com/auth/drive"]
    )
    return creds


def download_excel_file(file_id, destination_path, credentials):
    drive_service = build("drive", "v3", credentials=credentials)

    # Set the MIME type for Excel files
    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    request = drive_service.files().export_media(fileId=file_id, mimeType=mime_type)

    fh = io.FileIO(destination_path, mode="wb")
    downloader = MediaIoBaseDownload(fh, request)

    done = False
    while not done:
        status, done = downloader.next_chunk()

    print(f"Downloaded Excel file ID: {file_id} to {destination_path}")


def list_files_in_folder(folder_id, credentials):
    drive_service = build("drive", "v3", credentials=credentials)

    results = (
        drive_service.files()
        .list(q=f"'{folder_id}' in parents", fields="files(id, name)")
        .execute()
    )
    files = results.get("files", [])

    return files


if __name__ == "__main__":
    # Replace with the folder ID of the folder containing your Excel files
    folder_id_to_download = "1mNfzd72uQtNOeGGW0nvkff5dycBwHVCA"

    # Replace with the path to the folder where you want to save the downloaded Excel files
    # local_destination_folder = "path/to/local/destination/folder"
    local_destination_folder = "UploadedData"

    # Authenticate and get Google Drive service
    credentials = authenticate()

    # List Excel files in the specified folder
    excel_files_to_download = [
        file
        for file in list_files_in_folder(folder_id_to_download, credentials)
        if file["name"].endswith(".xlsx")
    ]

    # Download each Excel file in the folder
    for excel_file in excel_files_to_download:
        excel_file_id = excel_file["id"]
        excel_file_name = excel_file["name"]
        local_destination_path = os.path.join(local_destination_folder, excel_file_name)

        download_excel_file(excel_file_id, local_destination_path, credentials)


# if __name__ == "__main__":
#     # Replace with the folder ID of the folder containing your files


#     # Authenticate and get Google Drive service
#     credentials = authenticate()

#     # List files in the specified folder
#     files_to_download = list_files_in_folder(folder_id_to_download, credentials)

#     # Download each file in the folder
#     for file in files_to_download:
#         file_id = file["id"]
#         file_name = file["name"]
#         local_destination_path = os.path.join(local_destination_folder, file_name)

#         download_file(file_id, local_destination_path, credentials)


#   # Replace with the folder ID of the folder containing your files
#     folder_id_to_download = "1mNfzd72uQtNOeGGW0nvkff5dycBwHVCA"

#     # Replace with the path to the folder where you want to save the downloaded files
#     local_destination_folder = "UploadedData"
