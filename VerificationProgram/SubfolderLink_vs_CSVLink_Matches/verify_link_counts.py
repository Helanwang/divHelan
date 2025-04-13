import os
import csv
import sys


def count_txt_files_in_folder(folder_path):
    """Counts the number of .txt files in a given folder."""
    if not os.path.exists(folder_path):
        return 0
    return len([
        f for f in os.listdir(folder_path)
        if f.endswith(".txt")
    ])


def verify_link_counts(csv_file, base_dir):
    """Checks if each university's link count matches its folder's .txt files."""
    csv.field_size_limit(sys.maxsize)  # Handle large CSV fields
    mismatches = []

    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            code = row['Code']
            folder_path = os.path.join(base_dir, code)

            # Count links in CSV (non-empty UniversityLink columns)
            link_count = sum(
                1 for key in row.keys()
                if key.startswith("UniversityLink") and row[key].strip()
            )

            # Count .txt files in folder
            txt_count = count_txt_files_in_folder(folder_path)

            if link_count != txt_count:
                mismatches.append((code, link_count, txt_count))

    return mismatches


if __name__ == "__main__":
    # Paths (modify if needed)
    csv_file = "../../outputCvs/output_wave3_content_ordered.csv"
    base_dir = "/Users/helanwang/PycharmProjects/divHelan/Wave3/2021UniversityFiles"

    mismatches = verify_link_counts(csv_file, base_dir)

    if not mismatches:
        print("✅ **VERIFICATION PASSED**: All universities have the correct number of links!")
    else:
        print(f"❌ **VERIFICATION FAILED**: {len(mismatches)} mismatches found!")
        print("\nMismatched universities (Code, Links in CSV, .txt files in folder):")
        for code, csv_links, folder_txt in mismatches:
            print(f"- {code}: {csv_links} links (CSV) vs {folder_txt} .txt files (folder)")