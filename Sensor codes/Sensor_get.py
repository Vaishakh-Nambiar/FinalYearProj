import smbus
import time
import pandas as pd
from datetime import datetime
import os
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload
import numpy as np


# I2C address of the SEN0433 sensor
SEN0433_ADDRESS = 0x68

# Register addresses for accelerometer data
ACCEL_XOUT_H = 0x3B
ACCEL_XOUT_L = 0x3C
ACCEL_YOUT_H = 0x3D
ACCEL_YOUT_L = 0x3E
ACCEL_ZOUT_H = 0x3F
ACCEL_ZOUT_L = 0x40

# Initialize the I2C bus
bus = smbus.SMBus(1)  # 1 indicates the I2C bus number


# Assuming you have the SEN0433 connected to the default I2C bus
bus = smbus.SMBus(1)

# SEN0433 sensor constants
SEN0433_ADDRESS = 0x53
ACCEL_XOUT_H = 0x32
ACCEL_YOUT_H = 0x34
ACCEL_ZOUT_H = 0x36
TEMP_OUT_H = 0x39


def read_sensor_data():
    # Read raw accelerometer data
    x_raw = bus.read_i2c_block_data(SEN0433_ADDRESS, ACCEL_XOUT_H, 2)
    y_raw = bus.read_i2c_block_data(SEN0433_ADDRESS, ACCEL_YOUT_H, 2)
    z_raw = bus.read_i2c_block_data(SEN0433_ADDRESS, ACCEL_ZOUT_H, 2)

    # Read raw temperature data
    temp_raw = bus.read_i2c_block_data(SEN0433_ADDRESS, TEMP_OUT_H, 2)

    # Convert raw data to acceleration values
    x_accel = (x_raw[0] << 8 | x_raw[1]) / 16384.0  # Sensitivity: +/- 2g
    y_accel = (y_raw[0] << 8 | y_raw[1]) / 16384.0
    z_accel = (z_raw[0] << 8 | z_raw[1]) / 16384.0

    # Convert raw temperature data to Celsius
    temp_celsius = ((temp_raw[0] << 8 | temp_raw[1]) / 340.0) + 36.53

    return {
        "x_acceleration": x_accel,
        "y_acceleration": y_accel,
        "z_acceleration": z_accel,
        "temperature": temp_celsius,
    }


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


record_count = 0
excel_file_path = None
days = 10
recordNum = 1200
# t = 1
t = 0.01

folder_count = 0
excel_files_in_folder = 0

# Replace with your actual parent folder ID
# parent_folder_id = "1mNfzd72uQtNOeGGW0nvkff5dycBwHVCA"
parent_folder_id = "1mNfzd72uQtNOeGGW0nvkff5dycBwHVCA"

# # Set the path to your service account JSON file
service_account_file = "finalyearop-cb5035f55e5d.json"

# service_account_file = "finalyearproject-410409-fc9ec0410fb0.json"


# Replace with your actual parent folder ID
# parent_folder_id = "1SqzUmCWsy_e9p6GuInBXVJJdDv7eu8Kz"

# Authenticate and get Google Drive service
drive_service = get_drive_service(service_account_file)

while record_count < (days * recordNum):  # Run for 2 days (2 days * 10 records/day)
    sensor_data = read_sensor_data()

    if record_count % recordNum == 0:
        # Create a new Excel file after recordNum records
        excel_files_in_folder += 1
        if excel_files_in_folder > 3:
            # Create a new folder every 3 Excel files
            folder_count += 1
            folder_name = f"DataFolder_{folder_count}"
            parent_folder_id = create_drive_folder(
                drive_service, folder_name, parent_folder_id=parent_folder_id
            )
            excel_files_in_folder = 1

        excel_file_path = f"finalyrdata_{record_count // recordNum + 1}.xlsx"

    append_to_excel(sensor_data, excel_file_path)

    # Increment record count
    record_count += 1

    # Wait for 5 minutes (300 seconds)
    time.sleep(t)

    # Check if it's time to upload to Google Drive (daily basis)
    if record_count % recordNum == 0:
        upload_to_drive(excel_file_path, drive_service, parent_folder_id)
# https://drive.google.com/drive/folders/1mNfzd72uQtNOeGGW0nvkff5dycBwHVCA?usp=sharing
