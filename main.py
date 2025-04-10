import os
import csv

# Define the path to the Wave 3 folder
wave3_path = "/Users/helanwang/PycharmProjects/divHelan/Wave3/2021UniversityFiles"
# Initialize the output data
output_data = []

# Iterate through each folder in Wave 3
for folder_name in os.listdir(wave3_path):
    folder_path = os.path.join(wave3_path, folder_name)

    # Check if it's a folder
    if os.path.isdir(folder_path):
        # List all text files in the folder
        links = [f for f in os.listdir(folder_path) if f.endswith(".txt")]

        # Create a row for the output data
        row = {
            "W4.Num": len(output_data) + 1,  # Assign a unique number
            "Code": folder_name,  # Folder name as the code
        }

        # Add links to the row
        for i, link in enumerate(links, start=1):
            row[f"UniversityLink{i}"] = link

        # Add the row to the output data
        output_data.append(row)

# Define the output CSV file path
output_csv_path = "output_wave3.csv"  # Replace with your desired output file path

# Write the output data to a CSV file
with open(output_csv_path, mode="w", newline="", encoding="utf-8") as csv_file:
    # Define the column headers
    fieldnames = ["W4.Num", "Code"] + [f"UniversityLink{i}" for i in
                                       range(1, 7)]  # Adjust the number of links if needed

    # Create a CSV writer
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    # Write the header row
    writer.writeheader()

    # Write the data rows
    for row in output_data:
        writer.writerow(row)

print(f"CSV file saved to: {output_csv_path}")