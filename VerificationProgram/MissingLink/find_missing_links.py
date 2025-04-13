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

    txt_files = list_txt_files(university_folder)
    print(f"\n📁 Files in folder '{target_code}':")
    for file in sorted(txt_files):  # Sort files for better readability
        print(f"  - {os.path.basename(file)}")

    # Get links from CSV
    csv_links = get_csv_links(csv_file, target_code)
    print(f"\n📄 Links in CSV for '{target_code}':")
    for i, link in enumerate(csv_links, 1):
        print(f"  - UniversityLink{i}: {link}")

    # Find missing files
    folder_files = {os.path.basename(f) for f in txt_files}
    csv_files = set()

    for link in csv_links:
        if os.path.isfile(link):  # If links are file paths
            csv_files.add(os.path.basename(link))
        elif link.startswith(('http://', 'https://')):  # If links are URLs
            # Try to extract filename from URL
            csv_files.add(os.path.basename(link.split('/')[-1]))
        else:  # If plain text
            csv_files.add(link)

    missing_in_csv = folder_files - csv_files
    extra_in_csv = csv_files - folder_files

    if missing_in_csv:
        print(f"\n❌ Missing in CSV: {missing_in_csv}")
    else:
        print("\n✅ All folder files are present in CSV.")

    if extra_in_csv:
        print(f"\n⚠️ Extra in CSV (not in folder): {extra_in_csv}")


if __name__ == "__main__":
    # Configure paths
    csv_file = "../../outputCvs/output_wave3_content_ordered.csv"
    base_dir = "/Users/helanwang/PycharmProjects/divHelan/Wave3/2021UniversityFiles"
    target_code = "msu"  # The university code you're debugging

    # Fix CSV field size limit
    csv.field_size_limit(sys.maxsize)

    compare_links_to_files(csv_file, base_dir, target_code)