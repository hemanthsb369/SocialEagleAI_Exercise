# file_transfer.py

import shutil
import os

# Define source and destination paths
source_folder = "source_folder"
destination_folder = "destination_folder"
file_name = "sample.txt"

# Ensure destination folder exists
os.makedirs(destination_folder, exist_ok=True)

# Full paths
source_path = os.path.join(source_folder, file_name)
destination_path = os.path.join(destination_folder, file_name)

# Transfer the file
try:
    shutil.copy2(source_path, destination_path)
    print(f"File '{file_name}' successfully transferred to '{destination_folder}'.")
except FileNotFoundError:
    print(f"File '{file_name}' not found in '{source_folder}'.")
except Exception as e:
    print(f"Error occurred: {e}")