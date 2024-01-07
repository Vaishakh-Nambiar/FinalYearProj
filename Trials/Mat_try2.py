import numpy as np
import pandas as pd
from datetime import datetime
import time
import random
import os
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload


# Function to generate random vibration data
def generate_vibration_data(num_samples):
    good_percentage = 0.7
    num_good = int(num_samples * good_percentage)
    num_bad = num_samples - num_good

    x_values_good = np.random.uniform(-25, -1, size=num_good)
    y_values_good = np.random.uniform(9, 35, size=num_good)
    z_values_good = np.random.uniform(-1016, -1011, size=num_good)

    x_values_bad = np.random.uniform(-40, -1, size=num_bad)
    y_values_bad = np.random.uniform(5, 35, size=num_bad)
    z_values_bad = np.random.uniform(-1030, -1011, size=num_bad)

    data = {
        "X": np.concatenate((x_values_good, x_values_bad)),
        "Y": np.concatenate((y_values_good, y_values_bad)),
        "Z": np.concatenate((z_values_good, z_values_bad)),
    }

    return pd.DataFrame(data)


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


# Set the path to your service account JSON file
# service_account_file = "finalyearop-cb5035f55e5d.json"
service_account_file = "finalyearproject-410409-fc9ec0410fb0.json"
    

# Replace with your actual parent folder ID
parent_folder_id = "1SqzUmCWsy_e9p6GuInBXVJJdDv7eu8Kz"

# Authenticate and get Google Drive service
drive_service = get_drive_service(service_account_file)

record_count = 0
excel_file_path = None
days = 4
recordNum = 50
t = 5

material_folders = ["Material_A", "Material_B", "Material_C"]
material_folder_ids = [
    create_drive_folder(drive_service, folder) for folder in material_folders
]

while record_count < (days * recordNum):  # Run for 4 days (4 days * 50 records/day)
    for material_folder_id in material_folder_ids:
        if record_count % recordNum == 0:
            # Create a new datasheet every day
            day_folder_name = f"Day_{record_count // (recordNum * days) + 1}"
            day_folder_id = create_drive_folder(
                drive_service, day_folder_name, parent_folder_id=material_folder_id
            )
            print(
                f"Created Day Folder: {day_folder_name} in Material Folder: {material_folder_id}"
            )

        excel_file_path = f"finalyrdata_{record_count // recordNum + 1}.xlsx"
        sensor_data = generate_vibration_data(recordNum)
        sensor_data.to_excel(excel_file_path, index=False)

        # Increment record count
        record_count += recordNum

        # Upload to Google Drive
        upload_to_drive(excel_file_path, drive_service, folder_id=day_folder_id)
        print(
            f"Data uploaded to Day Folder: {day_folder_name} in Material Folder: {material_folder_id}"
        )

        # Wait for 5 minutes (300 seconds)
        time.sleep(t)
