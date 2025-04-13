import os
import csv
from datetime import datetime

# ===== Configuration =====
wave3_path = "/Users/helanwang/PycharmProjects/divHelan/Wave3/2021UniversityFiles"
output_csv_name = "university_links.csv"  # Fixed filename
strict_validation = True
overwrite_existing = True  # Set to True to overwrite existing file

# ===== Initialize =====
output_data = []
mismatches = []

# Validate directory
if not os.path.exists(wave3_path):
    raise FileNotFoundError(f"Directory not found: {wave3_path}")

# Check if output file exists
if os.path.exists(output_csv_name) and not overwrite_existing:
    raise FileExistsError(
        f"Output file {output_csv_name} already exists. "
        "Set overwrite_existing=True to overwrite or change output_csv_name."
    )

# ===== Process Folders =====
folder_names = sorted([f for f in os.listdir(wave3_path) if os.path.isdir(os.path.join(wave3_path, f))])

# Calculate max links needed
max_links = max(
    len([f for f in os.listdir(os.path.join(wave3_path, folder))
         if f.endswith('.txt') and os.path.isfile(os.path.join(wave3_path, folder, f))])
    for folder in folder_names
)

for idx, folder_name in enumerate(folder_names, 1):
    folder_path = os.path.join(wave3_path, folder_name)
    txt_files = sorted(
        [f for f in os.listdir(folder_path) if f.endswith(".txt") and os.path.isfile(os.path.join(folder_path, f))])

    if not txt_files:
        print(f"⚠️ No text files in {folder_name}")
        continue

    row = {"W4.Num": idx, "Code": folder_name}

    for i, txt_file in enumerate(txt_files, 1):
        file_path = os.path.join(folder_path, txt_file)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                row[f"UniversityLink{i}"] = content
        except Exception as e:
            error_msg = f"Error reading {file_path}: {str(e)}"
            print(error_msg)
            row[f"UniversityLink{i}"] = "ERROR_READING_FILE"
            mismatches.append({
                "Folder": folder_name,
                "File": txt_file,
                "Error": error_msg,
                "Type": "Read Error"
            })

    output_data.append(row)

# ===== Write Main CSV =====
fieldnames = ["W4.Num", "Code"] + [f"UniversityLink{i}" for i in range(1, max_links + 1)]

with open(output_csv_name, mode="w", newline="", encoding="utf-8") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(output_data)

print(f"\n✅ Data saved to: {output_csv_name}")
print(f"Total universities processed: {len(output_data)}")

# ===== Strict Verification Phase =====
print("\n🔍 Starting STRICT verification...")
for row in output_data:
    folder_name = row["Code"]
    folder_path = os.path.join(wave3_path, folder_name)
    txt_files = sorted(
        [f for f in os.listdir(folder_path) if f.endswith(".txt") and os.path.isfile(os.path.join(folder_path, f))])

    for i, txt_file in enumerate(txt_files, 1):
        file_path = os.path.join(folder_path, txt_file)
        csv_value = row.get(f"UniversityLink{i}", "")

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                file_content = f.read().strip()

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
    for issue in mismatches[:5]:
        print(f"\n→ Folder: {issue['Folder']}/{issue['File']}")
        print(f"   Error Type: {issue['Type']}")
        if 'CSV Value' in issue:
            print(f"   CSV Value: {issue['CSV Value']}")
            print(f"   File Content: {issue['File Content']}")
        print(f"   Error: {issue['Error']}")

    # Save mismatches to a separate file with timestamp
    mismatch_log_path = f"mismatches_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with open(mismatch_log_path, mode='w', newline='', encoding='utf-8') as log_file:
        writer = csv.DictWriter(log_file, fieldnames=["Folder", "File", "CSV Value", "File Content", "Error", "Type"])
        writer.writeheader()
        writer.writerows(mismatches)
    print(f"\n📝 Mismatch details saved to: {mismatch_log_path}")

# ===== Final Stats =====
success_count = len(output_data) - len([m for m in mismatches if m["Type"] != "Read Error"])
print(f"\n📊 Final stats:")
print(f"- Universities processed: {len(output_data)}")
print(f"- Perfect matches: {success_count}")
print(f"- Errors detected: {len(mismatches)}")
print(f"  → Content mismatches: {len([m for m in mismatches if m['Type'] == 'Content Mismatch'])}")
print(f"  → Read errors: {len([m for m in mismatches if m['Type'] == 'Read Error'])}")
print(f"  → Other issues: {len([m for m in mismatches if m['Type'] not in ['Content Mismatch', 'Read Error']])}")