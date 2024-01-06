import numpy as np
import pandas as pd
import os


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


# Set random seed for reproducibility
np.random.seed(42)


# Function to organize data into folders
def organize_data_into_folders(dataset):
    base_folder = "VibrationData"
    for material in dataset["Material"].unique():
        material_folder = os.path.join(base_folder, material)
        os.makedirs(material_folder, exist_ok=True)

        for classification in dataset["Classification"].unique():
            classification_folder = os.path.join(material_folder, classification)
            os.makedirs(classification_folder, exist_ok=True)

            file_name = f"{classification}.csv"
            file_path = os.path.join(classification_folder, file_name)

            filtered_data = dataset[
                (dataset["Material"] == material)
                & (dataset["Classification"] == classification)
            ]
            filtered_data.to_csv(file_path, index=False)


# Generate 'Good' and 'Bad' industrial vibration datasets
good_data = pd.concat(
    [
        generate_vibration_data(num_samples=1000, material="A", classification="Good"),
        generate_vibration_data(num_samples=1000, material="B", classification="Good"),
        generate_vibration_data(num_samples=1000, material="C", classification="Good"),
    ],
    ignore_index=True,
)

bad_data = pd.concat(
    [
        generate_vibration_data(num_samples=200, material="A", classification="Bad"),
        generate_vibration_data(num_samples=200, material="B", classification="Bad"),
        generate_vibration_data(num_samples=200, material="C", classification="Bad"),
    ],
    ignore_index=True,
)

full_dataset = pd.concat([good_data, bad_data], ignore_index=True)

# Shuffle the dataset
full_dataset = full_dataset.sample(frac=1).reset_index(drop=True)

# Save the dataset to a CSV file
full_dataset.to_csv("industrial_vibration_dataset.csv", index=False)

# Organize data into folders
organize_data_into_folders(full_dataset)
