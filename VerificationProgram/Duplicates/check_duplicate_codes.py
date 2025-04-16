"""
This script checks for duplicate university 'Code' entries in a CSV file
(e.g., output_wave3_content_ordered.csv). It prints a summary of any codes
that appear more than once.
"""

import csv     # Module for reading CSV files
import sys     # Used to increase the maximum CSV field size (for large text cells)

def find_duplicate_codes(csv_file):
    """
    Returns a set of duplicate 'Code' values in the CSV file.
    This helps detect if any university code appears more than once in the dataset.
    """
    csv.field_size_limit(sys.maxsize)  # Handle large text fields (some cells may exceed default limits)

    codes = set()        # To track unique codes seen so far
    duplicates = set()   # To collect any codes that appear more than once

    # Open the CSV file and read it using DictReader for column-based access
    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            code = row['Code']  # Get the university code from the current row

            if code in codes:
                duplicates.add(code)  # Already seen? Add to duplicates
            codes.add(code)          # Track this code

    return duplicates  # Return the set of duplicates (if any)


# Only run this block if the script is executed directly
if __name__ == "__main__":
    # Path to the output CSV file that needs checking
    csv_file = "../../outputCvs/output_wave3_content_ordered.csv"

    # Call the duplicate checker function
    duplicates = find_duplicate_codes(csv_file)

    # Output results
    if duplicates:
        print(f"❌ **DUPLICATE CODES FOUND**: {len(duplicates)}")
        print("Duplicates:", ", ".join(sorted(duplicates)))
    else:
        print("✅ **NO DUPLICATE CODES FOUND**")