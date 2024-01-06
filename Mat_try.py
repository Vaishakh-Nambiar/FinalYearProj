import pandas as pd
from datetime import datetime
import time
import random
import os
import numpy as np
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload


# Function to generate random vibration data
def generate_vibration_data(num_samples, material, classification):
    x_values = (
        np.random.uniform(-40, -1)
        if classification == "Bad"
        else np.random.uniform(-25, -1)
    )
    y_values = (
        np.random.uniform(5, 35)
        if classification == "Bad"
        else np.random.uniform(9, 35)
    )
    z_values = (
        np.random.uniform(-1030, -1011)
        if classification == "Bad"
        else np.random.uniform(-1016, -1011)
    )

    data = {
        "X": np.random.uniform(x_values, size=num_samples),
        "Y": np.random.uniform(y_values, size=num_samples),
        "Z": np.random.uniform(z_values, size=num_samples),
        "Material": material,
        "Classification": classification,
    }

    return pd.DataFrame(data)


# Function to read sensor data (using the provided vibration data generation code)
def read_sensor_data():
    # Generate random vibration data for the example
    good_data = generate_vibration_data(
        num_samples=1200, material="A", classification="Good"
    )
    bad_data = generate_vibration_data(
        num_samples=1200, material="A", classification="Bad"
    )

    # Combine the dataframes and shuffle the data
    full_data = (
        pd.concat([good_data, bad_data], ignore_index=True)
        .sample(frac=1)
        .reset_index(drop=True)
    )

    return full_data


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
def upload_to_drive(
    file_path, drive_service, folder_id=None, material=None, classification=None
):
    file_metadata = {"name": os.path.basename(file_path)}

    # If folder_id is provided, set the parent folder
    if folder_id:
        file_metadata["parents"] = [folder_id]

    media_body = MediaFileUpload(
        file_path,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    drive_service.files().create(body=file_metadata, media_body=media_body).execute()

    # Log which material folder and classification file the data is being uploaded to
    # print(
    #     f"Data uploaded to Material Folder: {material}, Classification: {classification}"
    # )
    print(f"Data uploaded to Google Drive: {file_path}")


# Set the path to your service account JSON file
service_account_file = "finalyearop-cb5035f55e5d.json"

# Replace with your actual parent folder ID
# parent_folder_id = "1mNfzd72uQtNOeGGW0nvkff5dycBwHVCA"
parent_folder_id = "1HydWnhc03M59UdBc88fNNnP-KGH4oqGo"

# Authenticate and get Google Drive service
drive_service = get_drive_service(service_account_file)

record_count = 0
excel_file_path = None
days = 4
recordNum = 20
t = 2

material_folder_count = 0
day_folder_count = 0
excel_files_in_folder = 0

max_files = 4

material_folder_id = None
day_folder_id = None

while record_count < (days * recordNum):  # Run for 4 days (4 days * 50 records/day)
    sensor_data = read_sensor_data()

    if excel_files_in_folder > max_files:
        # Create a new material folder every 4 Excel files
        material_folder_count += 1
        material_folder_name = f"MaterialFolder_{material_folder_count}"
        material_folder_id = create_drive_folder(
            drive_service, material_folder_name, parent_folder_id=parent_folder_id
        )

        # Reset the day_folder_count
        day_folder_count = 0

    # Create a new day folder every recordNum records
    if record_count % recordNum == 0:
        day_folder_count += 1
        day_folder_name = f"DayFolder_{day_folder_count}"

        # Create a new day folder
        day_folder_id = create_drive_folder(
            drive_service, day_folder_name, parent_folder_id=material_folder_id
        )

        # Reset the excel_files_in_folder count
        excel_files_in_folder = 1

    excel_file_path = f"finalyrdata_{record_count // recordNum + 1}.xlsx"
    sensor_data.to_excel(excel_file_path, index=False)  # Save sensor data to Excel file
    upload_to_drive(excel_file_path, drive_service, day_folder_id)

    # Increment record count
    record_count += 1

    # Wait for 5 minutes (300 seconds)
    time.sleep(t)
