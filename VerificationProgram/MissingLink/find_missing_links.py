"""
This script verifies whether the files listed under msu university code
in the CSV match the actual .txt files in that university's folder.

Use Case:
    Helps debug mismatches between the files actually present and what’s recorded
    in the output CSV, especially when working with large data exports like Wave3.

Output:
    - Lists files in the folder and corresponding CSV links
    - Prints any missing files (present in folder but missing in CSV)
    - Flags extra files listed in the CSV but not found in the folder
"""

import os
import csv
import sys


def list_txt_files(folder_path):
    """List all .txt files in a folder (recursively)."""
    txt_files = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".txt"):
                txt_files.append(os.path.join(root, file))
    return txt_files


def get_csv_links(csv_file, target_code):
    """Get all links for a specific university from the CSV."""
    # Increase field size limit to handle large fields
    csv.field_size_limit(sys.maxsize)

    links = []
    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Code'] == target_code:
                # Collect all fields that start with "UniversityLink" and are not empty
                links = [row[key] for key in row.keys()
                         if key.startswith("UniversityLink") and row[key].strip()]
                break
    return links


def compare_links_to_files(csv_file, base_dir, target_code):
    """Compare CSV links to actual .txt files in the folder."""
    # Get all .txt files in the university's folder
    university_folder = os.path.join(base_dir, target_code)
    if not os.path.exists(university_folder):
        print(f"❌ Folder not found: {university_folder}")
        return

    # List .txt files found in the folder
    txt_files = list_txt_files(university_folder)
    print(f"\n📁 Files in folder '{target_code}':")
    for file in sorted(txt_files):  # Sort for readability
        print(f"  - {os.path.basename(file)}")

    # Get list of links from the CSV
    csv_links = get_csv_links(csv_file, target_code)
    print(f"\n📄 Links in CSV for '{target_code}':")
    for i, link in enumerate(csv_links, 1):
        print(f"  - UniversityLink{i}: {link}")

    # Compare folder filenames vs CSV filenames
    folder_files = {os.path.basename(f) for f in txt_files}
    csv_files = set()

    for link in csv_links:
        if os.path.isfile(link):  # If link is a local file path
            csv_files.add(os.path.basename(link))
        elif link.startswith(('http://', 'https://')):  # If it's a URL
            csv_files.add(os.path.basename(link.split('/')[-1]))
        else:  # Plain string fallback (likely just file name)
            csv_files.add(link)

    # Detect mismatches
    missing_in_csv = folder_files - csv_files
    extra_in_csv = csv_files - folder_files

    # Print results
    if missing_in_csv:
        print(f"\n❌ Missing in CSV: {missing_in_csv}")
    else:
        print("\n✅ All folder files are present in CSV.")

    if extra_in_csv:
        print(f"\n⚠️ Extra in CSV (not in folder): {extra_in_csv}")


if __name__ == "__main__":
    # Configure file paths and target university code
    csv_file = "../../outputCvs/output_wave3_content_ordered.csv"
    base_dir = "/Users/helanwang/PycharmProjects/divHelan/Wave3/2021UniversityFiles"
    target_code = "msu"  # The university code you're debugging

    # Set the CSV field size limit again (in case it wasn't already done)
    csv.field_size_limit(sys.maxsize)

    # Run the comparison
    compare_links_to_files(csv_file, base_dir, target_code)