import os
import csv

wave3_path = "/Wave3/2021UniversityFiles"
output_data = []

# Get all folders and SORT them to maintain order
folder_names = sorted([f for f in os.listdir(wave3_path) if os.path.isdir(os.path.join(wave3_path, f))])

for folder_name in folder_names:
    folder_path = os.path.join(wave3_path, folder_name)
    txt_files = sorted([f for f in os.listdir(folder_path) if f.endswith(".txt")])  # Also sort files

    row = {"W4.Num": len(output_data) + 1, "Code": folder_name}

    # Read each text file's content (sorted)
    for i, txt_file in enumerate(txt_files, start=1):
        file_path = os.path.join(folder_path, txt_file)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                row[f"UniversityLink{i}"] = content
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            row[f"UniversityLink{i}"] = "ERROR_READING_FILE"

    output_data.append(row)

# Write to CSV
output_csv_path = "../outputCvs/output_wave3_content_ordered.csv"
fieldnames = ["W4.Num", "Code"] + [f"UniversityLink{i}" for i in range(1, 7)]  # Adjust columns as needed

with open(output_csv_path, mode="w", newline="", encoding="utf-8") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(output_data)

print(f"CSV file saved to: {output_csv_path}")

# Add this at the end of your original script
unique_codes = set(row['Code'] for row in output_data)
university_count = len(unique_codes)
print(f"Total number of universities (unique codes): {university_count}")