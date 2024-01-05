import os
import pandas as pd
from datetime import datetime
import time
import openpyxl
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

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

    # Try to read the existing Excel file, if it exists
    try:
        existing_df = pd.read_excel(excel_path, index_col=0)
        df = pd.concat([existing_df, df])
    except FileNotFoundError:
        # If the file doesn't exist, create a new DataFrame
        pass

    # Write the combined DataFrame to the Excel file
    df.to_excel(excel_path, index=True)
    print(f"Data written to Excel file: {excel_path}")


# Function to authenticate and get Google Drive service
def get_drive_service(creds_path):
    credentials = service_account.Credentials.from_service_account_file(
        creds_path, scopes=["https://www.googleapis.com/auth/drive"]
    )
    drive_service = build("drive", "v3", credentials=credentials)
    return drive_service


# Function to create a Google Drive folder
def create_drive_folder(drive_service, folder_name):
    folder_metadata = {
        "name": folder_name,
        "mimeType": "application/vnd.google-apps.folder",
    }
    folder = drive_service.files().create(body=folder_metadata, fields="id").execute()
    return folder.get("id")


# Function to upload a file to Google Drive
def upload_to_drive(file_path, drive_service, folder_id=None):
    file_metadata = {"name": os.path.basename(file_path)}

    # If folder_id is provided, set the parent folder
    if folder_id:
        file_metadata["parents"] = [folder_id]

    media = MediaFileUpload(
        file_path,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    drive_service.files().create(body=file_metadata, media_body=media).execute()
    print(f"Data uploaded to Google Drive: {file_path}")


# Main loop for continuous data collection
record_count = 0
excel_file_path = None
days = 2
recordNum = 10
t = 5

folder_count = 0
folder_id = "1mNfzd72uQtNOeGGW0nvkff5dycBwHVCA"

while record_count < (days * recordNum):  # Run for 2 days (2 days * 100 records/day)
    sensor_data = read_sensor_data()

    if record_count % recordNum == 0:
        # Create a new Excel file after recordNum records
        excel_file_path = f"finalyrdata_{record_count // recordNum + 1}.xlsx"

    append_to_excel(sensor_data, excel_file_path)

    # Increment record count
    record_count += 1

    # Wait for 5 minutes (300 seconds)
    time.sleep(t)

    # Check if it's time to upload to Google Drive (daily basis)
    if record_count % recordNum == 0:
        creds_path = "finalyearop-cb5035f55e5d.json"
        drive_service = get_drive_service(creds_path)

        if record_count % (days * recordNum) == 0:
            folder_count += 1
            folder_name = f"DataFolder_{folder_count}"
            folder_id = create_drive_folder(drive_service, folder_name)
        else:
            folder_id = None

        upload_to_drive(excel_file_path, drive_service, folder_id)
