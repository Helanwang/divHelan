# University Data Extractor

This script provides structured organization of university research data for the Stanford Stark Lab. It systematically processes directories containing university-specific text files and generates a standardized CSV output where:

- Each row corresponds to a university (identified by its folder code)
- Columns represent sequentially numbered text files (`1.txt`, `2.txt`, etc.) from each university's directory
- Original file hierarchy and sorting order are preserved

---

# Limitations

* Google Sheets: Cells truncate at 50,000 characters
* Fixed Structure: Folders must match exact hierarchy
* Max Files: Processes only 1.txt to 6.txt per university

---
## 📁 Input Directory Structure

The input data **must** follow a specific folder structure for the script to work properly:

<pre lang="nohighlight"><code>
```
.
├── Wave3/
└── └── 2021UniversityFiles/
    ├── ├── adelphi/
    ├── │   ├── 1.txt
    ├── │   ├── 2.txt
    ├── ├── albany/
    ├── │   ├── 1.txt
    ├── │   └── 2.txt
    └── └── alliant/
        └── └── 1.txt
```
</code></pre>


---

## 📄 CSV Output

The script outputs a `.csv` file with the following structure:

- `W4.Num`: Sequential index for each unique university
- `Code`: Folder name (university code)
- `UniversityLink 1~N`: Content of each corresponding text file

---

## 🛠 Requirements

- Python 3.x  
- Standard Python libraries:
  - `os`
  - `csv`

---

## 🚀 Installation & Execution

### 1. Clone the Repository

bash:
git clone git@github.com:Helanwang/divHelan.git




# Configuration

Edit these variables:
wave3_path = "/Users/helanwang/PycharmProjects/divHelan/Wave3/2021UniversityFiles"
output_csv_path = "/Users/helanwang/PycharmProjects/divHelan/outputCvs/output_wave3_content_ordered.csv"


# Execute the Code in Terminal:
python university_data_extractor.py

# Reusability

The data MUST follow the certain folder structure to make sure the program process. 

Data will NOT be processed if the following tree hierarchy structure is not followed. Name of the files can be modified. 

<pre lang="nohighlight"><code>
```
.
├── WaveName/   # Root Directory
└── └── University File/  # Parent directory/
    ├── ├── STANFORD/         # University folder (code)
    ├── │   ├── 1.txt         
    ├── │   ├── 2.txt         
    ├── │   └── ...  
    ├── ├── MIT/
    ├── │   ├── 1.txt
    ├── │   └── ...
    └── └── ...
```
</code></pre>


# Verification Program:

✅  The script includes built-in checks for:
* Duplicate entries
* Mismatch between input folders and output rows
* Inconsistent .txt file counts between folders and output columns

# Known Issues

When importing the generated .csv into Google Sheets, long text entries may exceed the cell limit of 50,000 characters. If a cell exceeds this, Google Sheets will skip the content.

Example:

If a file like msu/2.txt has:
* 39 pages
* 22,931 words
* 153,522 characters

Google Sheets will skip that cell, as it exceeds the limit.


# Contributors 👩‍💻
* Helan Wang 
* Christylan1121@gmail.com