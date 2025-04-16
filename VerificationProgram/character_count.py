"""
This function checks each university folder and each .txt file inside it.
It records how many characters are in each file and flags files that exceed
the Google Sheets character limit (50,000 characters per cell).
"""

import os
import csv

# Configuration
wave3_path = "/Users/helanwang/PycharmProjects/divHelan/Wave3/2021UniversityFiles"
check_results_path = "/Users/helanwang/PycharmProjects/divHelan/outputCvs/wave3_character_check_results.csv"  # Output file to save results
CHARACTER_LIMIT = 50000  # Google Sheets cell character limit

def check_character_counts():
    # Get and sort all university folders
    folder_names = sorted([f for f in os.listdir(wave3_path) if os.path.isdir(os.path.join(wave3_path, f))])

    results = []  # Store data for all universities, including those with no issues

    for folder_name in folder_names:
        folder_path = os.path.join(wave3_path, folder_name)
        txt_files = sorted([f for f in os.listdir(folder_path) if f.endswith(".txt")])

        # Initialize data for the current university
        university_data = {
            "UniversityCode": folder_name,
            "TotalFiles": len(txt_files),
            "FilesOverLimit": 0,              # Counter for files exceeding character limit
            "MaxCharacterCount": 0,           # Longest file in the folder
            "Flagged": "No",                  # Default: not flagged
            "ProblemFiles": "None"            # Default: no problem files
        }

        problem_files = []  # Track problematic files in this folder

        for txt_file in txt_files:
            file_path = os.path.join(folder_path, txt_file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    char_count = len(content)

                    # Update the max character count for this university
                    if char_count > university_data["MaxCharacterCount"]:
                        university_data["MaxCharacterCount"] = char_count

                    # If file exceeds character limit, record it
                    if char_count > CHARACTER_LIMIT:
                        university_data["FilesOverLimit"] += 1
                        problem_files.append(f"{txt_file} ({char_count} chars)")
            except Exception as e:
                # Record the file as problematic if it can't be read
                problem_files.append(f"{txt_file} (ERROR: {str(e)})")

        # If any problem files found, update the university record
        if university_data["FilesOverLimit"] > 0:
            university_data["Flagged"] = "YES"
            university_data["ProblemFiles"] = "; ".join(problem_files)

        # Save results for this university
        results.append(university_data)

    # Write all results to the CSV file
    with open(check_results_path, mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = [
            'UniversityCode',
            'TotalFiles',
            'FilesOverLimit',
            'MaxCharacterCount',
            'Flagged',
            'ProblemFiles'
        ]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    # Print final summary to the console
    flagged_count = sum(1 for uni in results if uni["Flagged"] == "YES")
    print(f"Character check completed. Results saved to: {check_results_path}")
    print(f"Total universities processed: {len(results)}")
    print(f"Universities with files > {CHARACTER_LIMIT} chars: {flagged_count}")

# Run the check if this script is executed directly
if __name__ == "__main__":
    check_character_counts()