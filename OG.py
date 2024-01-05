import os
import pandas as pd
from datetime import datetime
import time
import openpyxl
from google.oauth2 import service_account
from googleapiclient.discovery import build


# Function to read sensor data
def read_sensor_data():
    # Replace this with your actual sensor reading code
    # Example: sensor_data = read_actual_sensor_data()
    sensor_data = {"Temperature": 25.5, "Humidity": 60.0}
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


# Function to upload file to Google Drive
def upload_to_drive(file_path, drive_service, folder_id=None):
    file_metadata = {"name": os.path.basename(file_path)}

    # If folder_id is provided, set the parent folder
    if folder_id:
        file_metadata["parents"] = [folder_id]

    media = {
        "mimeType": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "body": open(file_path, "rb"),
    }
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


# Main loop for continuous data collection
record_count = 0
excel_file_path = None
folder_count = 0
while record_count < 200:  # Run for 2 days (2 days * 100 records/day)
    sensor_data = read_sensor_data()

    if record_count % 100 == 0:
        # Create a new Excel file after 100 records
        excel_file_path = f"finalyrdata_{record_count // 100 + 1}.xlsx"

    append_to_excel(sensor_data, excel_file_path)

    # Increment record count
    record_count += 1

    # Wait for 5 minutes (300 seconds)
    time.sleep(20)

    # Check if it's time to upload to Google Drive (daily basis)
    if record_count % 100 == 0:
        creds_path = "path/to/your/service/account/key.json"
        drive_service = get_drive_service(creds_path)

        # Create a new folder for every 2 Excel files
        if record_count % 200 == 0:
            folder_count += 1
            folder_name = f"DataFolder_{folder_count}"
            folder_id = create_drive_folder(drive_service, folder_name)
        else:
            folder_id = None

        upload_to_drive(excel_file_path, drive_service, folder_id)
