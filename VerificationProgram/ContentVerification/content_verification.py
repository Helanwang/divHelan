"""Find any mismatched txt file with university codes."""

import os
import csv
from datetime import datetime

# ===== Configuration =====
wave3_path = "/Users/helanwang/PycharmProjects/divHelan/Wave3/2021UniversityFiles"  # Path to university folders
output_csv_name = "university_links.csv"  # Name of output CSV file
strict_validation = True  # Enable strict content verification
overwrite_existing = True  # Allow overwriting existing CSV file if it exists

# ===== Initialize =====
output_data = []     # Will hold each university's data row
mismatches = []      # Will collect read errors or verification mismatches

# Validate that the input directory exists
if not os.path.exists(wave3_path):
    raise FileNotFoundError(f"Directory not found: {wave3_path}")

# Check if output file exists and prevent overwrite if not allowed
if os.path.exists(output_csv_name) and not overwrite_existing:
    raise FileExistsError(
        f"Output file {output_csv_name} already exists. "
        "Set overwrite_existing=True to overwrite or change output_csv_name."
    )

# ===== Process Folders =====
# Get a sorted list of all university folders
folder_names = sorted([f for f in os.listdir(wave3_path) if os.path.isdir(os.path.join(wave3_path, f))])

# Find the max number of .txt files any folder contains (used for dynamic column generation)
max_links = max(
    len([f for f in os.listdir(os.path.join(wave3_path, folder))
         if f.endswith('.txt') and os.path.isfile(os.path.join(wave3_path, folder, f))])
    for folder in folder_names
)

# Loop through each folder and read the text files
for idx, folder_name in enumerate(folder_names, 1):
    folder_path = os.path.join(wave3_path, folder_name)

    # Get sorted list of all .txt files in this university folder
    txt_files = sorted(
        [f for f in os.listdir(folder_path) if f.endswith(".txt") and os.path.isfile(os.path.join(folder_path, f))]
    )

    # Warn if the folder has no .txt files
    if not txt_files:
        print(f"⚠️ No text files in {folder_name}")
        continue

    # Initialize row data with ID number and folder name
    row = {"W4.Num": idx, "Code": folder_name}

    # Read content of each .txt file and store in row
    for i, txt_file in enumerate(txt_files, 1):
        file_path = os.path.join(folder_path, txt_file)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()  # Read file and strip whitespace
                row[f"UniversityLink{i}"] = content  # Add to CSV row
        except Exception as e:
            # If reading fails, record the error and insert placeholder
            error_msg = f"Error reading {file_path}: {str(e)}"
            print(error_msg)
            row[f"UniversityLink{i}"] = "ERROR_READING_FILE"
            mismatches.append({
                "Folder": folder_name,
                "File": txt_file,
                "Error": error_msg,
                "Type": "Read Error"
            })

    output_data.append(row)  # Save completed row

# ===== Write Main CSV =====
# Generate column headers: W4.Num, Code, UniversityLink1 ~ UniversityLinkN
fieldnames = ["W4.Num", "Code"] + [f"UniversityLink{i}" for i in range(1, max_links + 1)]

# Write the full CSV file
with open(output_csv_name, mode="w", newline="", encoding="utf-8") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()           # Write header row
    writer.writerows(output_data)  # Write all university rows

# Confirm success
print(f"\n✅ Data saved to: {output_csv_name}")
print(f"Total universities processed: {len(output_data)}")

# ===== Strict Verification Phase =====
print("\n🔍 Starting STRICT verification...")

# Go back and verify if CSV content matches original .txt file content
for row in output_data:
    folder_name = row["Code"]
    folder_path = os.path.join(wave3_path, folder_name)

    # Get list of .txt files for this university
    txt_files = sorted(
        [f for f in os.listdir(folder_path) if f.endswith(".txt") and os.path.isfile(os.path.join(folder_path, f))]
    )

    for i, txt_file in enumerate(txt_files, 1):
        file_path = os.path.join(folder_path, txt_file)
        csv_value = row.get(f"UniversityLink{i}", "")  # Get value from CSV

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                file_content = f.read().strip()  # Read actual file content again

                # Compare CSV value with file content
                if strict_validation and (csv_value != file_content):
                    mismatches.append({
                        "Folder": folder_name,
                        "File": txt_file,
                        "CSV Value": csv_value,
                        "File Content": file_content,
                        "Error": "EXACT CONTENT MISMATCH",
                        "Type": "Content Mismatch"
                    })
        except Exception as e:
            # If verification fails, log the issue
            error_msg = f"Verification failed for {file_path}: {str(e)}"
            print(error_msg)
            mismatches.append({
                "Folder": folder_name,
                "File": txt_file,
                "Error": error_msg,
                "Type": "Verification Error"
            })

# ===== Results Summary =====
if not mismatches:
    print("✅ Perfect match! All CSV entries EXACTLY match source files.")
else:
    print(f"\n❌ Found {len(mismatches)} issues:")

    # Print the first 5 issues
    for issue in mismatches[:5]:
        print(f"\n→ Folder: {issue['Folder']}/{issue['File']}")
        print(f"   Error Type: {issue['Type']}")
        if 'CSV Value' in issue:
            print(f"   CSV Value: {issue['CSV Value']}")
            print(f"   File Content: {issue['File Content']}")
        print(f"   Error: {issue['Error']}")

    # Save mismatch details to a timestamped CSV
    mismatch_log_path = f"mismatches_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with open(mismatch_log_path, mode='w', newline='', encoding='utf-8') as log_file:
        writer = csv.DictWriter(log_file, fieldnames=["Folder", "File", "CSV Value", "File Content", "Error", "Type"])
        writer.writeheader()
        writer.writerows(mismatches)
    print(f"\n📝 Mismatch details saved to: {mismatch_log_path}")

# ===== Final Stats =====
# Count universities that passed without any issues
success_count = len(output_data) - len([m for m in mismatches if m["Type"] != "Read Error"])

# Print final report
print(f"\n📊 Final stats:")
print(f"- Universities processed: {len(output_data)}")
print(f"- Perfect matches: {success_count}")
print(f"- Errors detected: {len(mismatches)}")
print(f"  → Content mismatches: {len([m for m in mismatches if m['Type'] == 'Content Mismatch'])}")
print(f"  → Read errors: {len([m for m in mismatches if m['Type'] == 'Read Error'])}")
print(f"  → Other issues: {len([m for m in mismatches if m['Type'] not in ['Content Mismatch', 'Read Error']])}")