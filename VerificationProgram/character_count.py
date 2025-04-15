import os
import csv

# Configuration
wave3_path = "/Users/helanwang/PycharmProjects/divHelan/Wave3/2021UniversityFiles"
check_results_path = "/Users/helanwang/PycharmProjects/divHelan/outputCvs/wave3_character_check_results.csv"  # NEW output file
CHARACTER_LIMIT = 50000  # Google Sheets cell character limit


def check_character_counts():
    # Get all folders and sort them
    folder_names = sorted([f for f in os.listdir(wave3_path) if os.path.isdir(os.path.join(wave3_path, f))])

    results = []  # Will store ALL universities, not just flagged ones

    for folder_name in folder_names:
        folder_path = os.path.join(wave3_path, folder_name)
        txt_files = sorted([f for f in os.listdir(folder_path) if f.endswith(".txt")])

        university_data = {
            "UniversityCode": folder_name,
            "TotalFiles": len(txt_files),
            "FilesOverLimit": 0,
            "MaxCharacterCount": 0,
            "Flagged": "No",  # Default to "No"
            "ProblemFiles": "None"  # Default to "None"
        }

        problem_files = []

        for txt_file in txt_files:
            file_path = os.path.join(folder_path, txt_file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    char_count = len(content)

                    # Update max character count
                    if char_count > university_data["MaxCharacterCount"]:
                        university_data["MaxCharacterCount"] = char_count

                    # Check against limit
                    if char_count > CHARACTER_LIMIT:
                        university_data["FilesOverLimit"] += 1
                        problem_files.append(f"{txt_file} ({char_count} chars)")
            except Exception as e:
                problem_files.append(f"{txt_file} (ERROR: {str(e)})")

        # Update flagged status if any problems found
        if university_data["FilesOverLimit"] > 0:
            university_data["Flagged"] = "YES"
            university_data["ProblemFiles"] = "; ".join(problem_files)

        results.append(university_data)

    # Write FULL results to the NEW CSV file
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

    # Print summary
    flagged_count = sum(1 for uni in results if uni["Flagged"] == "YES")
    print(f"Character check completed. Results saved to: {check_results_path}")
    print(f"Total universities processed: {len(results)}")
    print(f"Universities with files > {CHARACTER_LIMIT} chars: {flagged_count}")


if __name__ == "__main__":
    check_character_counts()