"""
This is the main program that transfer the data in folder into cvs output.
University Data Extractor Script

Description:
This script processes a folder of university directories, each containing text files
(e.g., 1.txt, 2.txt), and compiles their content into a structured CSV file.
The CSV rows represent universities, and each column contains content from the respective text file.
"""

import os
import csv

# Set the path to the main folder that contains university subfolders
wave3_path = "/Users/helanwang/PycharmProjects/divHelan/Wave3/2021UniversityFiles"

# Initialize an empty list to store all rows for the CSV
output_data = []

# Get all university folder names and sort them alphabetically
# Each folder represents a university (e.g., "adelphi", "albany")
folder_names = sorted([f for f in os.listdir(wave3_path) if os.path.isdir(os.path.join(wave3_path, f))])

# Iterate through each university folder
for folder_name in folder_names:
    folder_path = os.path.join(wave3_path, folder_name)

    # Get all .txt files inside the folder and sort them by filename
    # Files are expected to be named like 1.txt, 2.txt, etc.
    txt_files = sorted([f for f in os.listdir(folder_path) if f.endswith(".txt")])  # Also sort files

    # Create a dictionary for the current university row
    # "W4.Num" is a sequential number; "Code" is the folder name
    row = {"W4.Num": len(output_data) + 1, "Code": folder_name}

    # Read each .txt file and store its content under a key like "UniversityLink1", "UniversityLink2", etc.
    for i, txt_file in enumerate(txt_files, start=1):
        file_path = os.path.join(folder_path, txt_file)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()  # Remove leading/trailing whitespace
                row[f"UniversityLink{i}"] = content  # Store the content in the row
        except Exception as e:
            # If the file can't be read (e.g., encoding issue), print the error and insert a placeholder
            print(f"Error reading {file_path}: {e}")
            row[f"UniversityLink{i}"] = "ERROR_READING_FILE"

    # Add the current university's data row to the full dataset
    output_data.append(row)

# Set the path for the output CSV file
output_csv_path = "/Users/helanwang/PycharmProjects/divHelan/outputCvs/output_wave3_content_ordered.csv"

# Define the CSV column headers: W4.Num, Code, and up to 6 UniversityLink columns
fieldnames = ["W4.Num", "Code"] + [f"UniversityLink{i}" for i in range(1, 7)]  # Adjust columns as needed

# Open the output file and write the data using csv.DictWriter
with open(output_csv_path, mode="w", newline="", encoding="utf-8") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()           # Write the column headers
    writer.writerows(output_data) # Write each university row

# Notify the user that the file was created successfully
print(f"CSV file saved to: {output_csv_path}")

# Count and print the total number of unique university codes processed
unique_codes = set(row['Code'] for row in output_data)
university_count = len(unique_codes)
print(f"Total number of universities (unique codes): {university_count}")