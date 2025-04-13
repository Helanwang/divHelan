import csv
import sys

def find_duplicate_codes(csv_file):
    """Returns a set of duplicate 'Code' values in the CSV."""
    csv.field_size_limit(sys.maxsize)  # Handle large fields
    codes = set()
    duplicates = set()

    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            code = row['Code']
            if code in codes:
                duplicates.add(code)
            codes.add(code)

    return duplicates

if __name__ == "__main__":
    csv_file = "../../outputCvs/output_wave3_content_ordered.csv"
    duplicates = find_duplicate_codes(csv_file)

    if duplicates:
        print(f"❌ **DUPLICATE CODES FOUND**: {len(duplicates)}")
        print("Duplicates:", ", ".join(sorted(duplicates)))
    else:
        print("✅ **NO DUPLICATE CODES FOUND**")