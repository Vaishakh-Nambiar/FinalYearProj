import os
import pandas as pd
from datetime import datetime
import time
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import openpyxl
import random


# Function to read sensor data
def read_sensor_data():
    # Generate random values for temperature and humidity
    temperature = round(random.uniform(20.0, 30.0), 2)
    humidity = round(random.uniform(40.0, 80.0), 2)

    sensor_data = {"Temperature": temperature, "Humidity": humidity}
    return sensor_data


# Function to append data to Excel sheet
def append_to_excel(data, excel_path):
    df = pd.DataFrame(data, index=[datetime.now()])

    try:
        existing_df = pd.read_excel(excel_path, index_col=0)
        df = pd.concat([existing_df, df])
    except FileNotFoundError:
        pass

    df.to_excel(excel_path, index=True)
    print(f"Data written to Excel file: {excel_path}")


# Function to authenticate and get Google Drive service
def get_drive_service(credentials_path, scopes):
    flow = InstalledAppFlow.from_client_secrets_file(credentials_path, scopes=scopes)
    credentials = flow.run_local_server(port=8080)
    drive_service = build("drive", "v3", credentials=credentials)
    return drive_service


# Function to upload file to Google Drive
def upload_to_drive(file_path, drive_service, folder_id=None):
    file_metadata = {"name": os.path.basename(file_path)}

    if folder_id:
        file_metadata["parents"] = [folder_id]

    media = MediaFileUpload(file_path)
    drive_service.files().create(body=file_metadata, media_body=media).execute()
    print(f"Data uploaded to Google Drive: {file_path}")


# Function to create a new folder in Google Drive
def create_drive_folder(drive_service, folder_name):
    folder_metadata = {
        "name": folder_name,
        "mimeType": "application/vnd.google-apps.folder",
    }
    folder = drive_service.files().create(body=folder_metadata, fields="id").execute()
    return folder.get("id")


record_count = 0
excel_file_path = None
days = 2
recordNum = 10
t = 5

folder_count = 0

# Specify the path to the credentials.json file
credentials_path = "path/to/your/credentials.json"
# Define the scopes for the Google Drive API
scopes = ["https://www.googleapis.com/auth/drive.file"]

# Set up the OAuth 2.0 flow and obtain credentials
drive_service = get_drive_service(credentials_path, scopes)

folder_id = "1mNfzd72uQtNOeGGW0nvkff5dycBwHVCA"

while record_count < (days * recordNum):
    sensor_data = read_sensor_data()

    if record_count % recordNum == 0:
        excel_file_path = f"finalyrdata_{record_count // recordNum + 1}.xlsx"

    append_to_excel(sensor_data, excel_file_path)

    record_count += 1
    time.sleep(t)

    if record_count % recordNum == 0:
        if record_count % (days * recordNum) == 0:
            folder_count += 1
            folder_name = f"DataFolder_{folder_count}"
            folder_id = create_drive_folder(drive_service, folder_name)
        else:
            folder_id = None

        upload_to_drive(excel_file_path, drive_service, folder_id)
