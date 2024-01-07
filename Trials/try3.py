import pandas as pd
from datetime import datetime
import time
import random
import os
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload


# Function to read sensor data
def read_sensor_data():
    # Replace this with your actual sensor data reading logic
    # For testing, generate random values for temperature and humidity
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


# Function to create a new folder in Google Drive
def create_drive_folder(drive_service, folder_name, parent_folder_id=None):
    folder_metadata = {
        "name": folder_name,
        "mimeType": "application/vnd.google-apps.folder",
    }
    if parent_folder_id:
        folder_metadata["parents"] = [parent_folder_id]

    folder = drive_service.files().create(body=folder_metadata, fields="id").execute()
    return folder.get("id")


# Function to authenticate and get Google Drive service
def get_drive_service(creds_path):
    credentials = service_account.Credentials.from_service_account_file(
        creds_path, scopes=["https://www.googleapis.com/auth/drive"]
    )
    drive_service = build("drive", "v3", credentials=credentials)
    return drive_service


# Function to upload files to Google Drive
def upload_to_drive(file_path, drive_service, folder_id=None):
    file_metadata = {"name": os.path.basename(file_path)}

    # If folder_id is provided, set the parent folder
    if folder_id:
        file_metadata["parents"] = [folder_id]

    media_body = MediaFileUpload(
        file_path,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    drive_service.files().create(body=file_metadata, media_body=media_body).execute()
    print(f"Data uploaded to Google Drive: {file_path}")


# Function to upload data to Google Drive with additional folder structure
def upload_data_with_structure(
    drive_service, days, record_num, parent_folder_id, service_account_file
):
    record_count = 0
    folder_count = 0
    excel_files_in_folder = 0

    while record_count < (days * record_num):
        sensor_data = read_sensor_data()

        if record_count % record_num == 0:
            # Create a new Excel file after record_num records
            excel_files_in_folder += 1
            if excel_files_in_folder > 3:
                # Create a new folder every 3 Excel files
                folder_count += 1
                folder_name = f"DataFolder_{folder_count}"
                parent_folder_id = create_drive_folder(
                    drive_service, folder_name, parent_folder_id=parent_folder_id
                )
                excel_files_in_folder = 1

            excel_file_path = f"finalyrdata_{record_count // record_num + 1}.xlsx"

        append_to_excel(sensor_data, excel_file_path)

        # Increment record count
        record_count += 1

        # Wait for 5 minutes (300 seconds)
        time.sleep(2)  # Reduced wait time for testing

        # Check if it's time to upload to Google Drive (daily basis)
        if record_count % record_num == 0:
            upload_to_drive(excel_file_path, drive_service, parent_folder_id)


# Replace with your actual parent folder ID
# parent_folder_id = "1mNfzd72uQtNOeGGW0nvkff5dycBwHVCA"
parent_folder_id = "1SqzUmCWsy_e9p6GuInBXVJJdDv7eu8Kz"

# Set the path to your service account JSON file
# service_account_file = "finalyearop-cb5035f55e5d.json"
service_account_file = "finalyearproject-410409-fc9ec0410fb0.json"

# Authenticate and get Google Drive service
drive_service = get_drive_service(service_account_file)

# Upload data to Google Drive with additional folder structure
upload_data_with_structure(
    drive_service,
    days=4,
    record_num=5,
    parent_folder_id=parent_folder_id,
    service_account_file=service_account_file,
)
