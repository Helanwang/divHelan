import os
import csv
import sys


def count_subfolders(directory):
    """Count the number of subfolders in a given directory."""
    subfolders = [
        f for f in os.listdir(directory)
        if os.path.isdir(os.path.join(directory, f))
    ]
    return len(subfolders)


def count_csv_rows(csv_file):
    """Count the number of university entries in the CSV (excluding header)."""
    # Increase CSV field size limit to handle large fields
    csv.field_size_limit(sys.maxsize)  # Set to maximum possible limit

    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        return sum(1 for row in reader) - 1  # Subtract header row


def main():
    # Paths (modify these if needed)
    wave3_path = "/Users/helanwang/PycharmProjects/divHelan/Wave3/2021UniversityFiles"
    csv_file = "../../outputCvs/output_wave3_content_ordered.csv"

    # Count subfolders (input)
    subfolder_count = count_subfolders(wave3_path)
    print(f"Number of subfolders (input): {subfolder_count}")

    # Count CSV rows (output)
    csv_count = count_csv_rows(csv_file)
    print(f"Number of universities in CSV (output): {csv_count}")

    # Verify match
    if subfolder_count == csv_count:
        print("✅ **VERIFICATION PASSED**: Input and output counts match!")
    else:
        print(f"❌ **VERIFICATION FAILED**: Mismatch detected!")
        print(f"   - Input folders: {subfolder_count}")
        print(f"   - CSV entries: {csv_count}")


if __name__ == "__main__":
    main()