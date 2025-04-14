# University Data Extractor

This script provides structured organization of university research data for the `Stanford Univeristy Stark Lab`. It systematically processes directories containing university-specific text files and generates a standardized CSV output where:

- Each row corresponds to a university (identified by its folder code)
- Columns represent sequentially numbered text files (`1.txt`, `2.txt`, etc.) from each university's directory
- Original file hierarchy and sorting order are preserved

---

# Logic of the code
### 🧠 How the Script Works

This script reads university folders and extracts text content from `.txt` files to create a clean, organized `.csv` file.

#### Step-by-Step:

1. **Access the Input Folder**  
   The program looks inside the main directory that holds all the university folders.

2. **Identify All University Folders**  
   It finds each subfolder inside the input folder. Every subfolder represents a university (e.g., `adelphi`, `stanford`).

3. **Sort the Folders Alphabetically**  
   To keep the output consistent and easy to read, the university folders are processed in alphabetical order.

4. **Go Into Each University Folder**  
   Inside each university folder, the program finds all `.txt` files.

5. **Sort the Text Files**  
   These `.txt` files are sorted by filename (like `1.txt`, `2.txt`, etc.) so they appear in the right sequence in the CSV.

6. **Read Each Text File's Content**  
   The content of each `.txt` file is read and stored for that university.

7. **Create a Row of Data for Each University**  
   A new row is created that includes:
   - A sequential number (`W4.Num`)
   - The university’s folder name (`Code`)
   - The contents of each text file (`UniversityLink1`, `UniversityLink2`, ...)

8. **Repeat for All Universities**  
   This process continues for every university folder found in the input.

9. **Export the Data to a CSV File**  
   After collecting all the data, it's written to a `.csv` file using clearly labeled columns.

10. **Print the Result**  
    At the end, the script prints how many unique universities were processed and confirms the location of the saved CSV.

# Technical Mechanisms ⚙️
#### 1. **Directory Traversal and Filtering**

Lists and filters all university folders:

```python


folder_names = sorted([
    f for f in os.listdir(wave3_path)
    if os.path.isdir(os.path.join(wave3_path, f))
])

txt_files = sorted([
    f for f in os.listdir(folder_path)
    if f.endswith(".txt")
])
```


# Limitations

* Google Sheets: Cells truncate at `50,000 characters`
* Fixed Structure: Folders must match exact hierarchy
* Max Files: Processes only `1.txt` to `6.txt` per university

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

```bash
git clone git@github.com:Helanwang/divHelan.git
```

# Configuration

Edit these variables:
```python 
wave3_path = "/Users/helanwang/PycharmProjects/divHelan/Wave3/2021UniversityFiles"
output_csv_path = "/Users/helanwang/PycharmProjects/divHelan/outputCvs/output_wave3_content_ordered.csv"
```


# Execute the Code in Terminal:

``` bash
python university_data_extractor.py
```

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
* Inconsistent `.txt` file counts between folders and output columns

# Known Issues

When importing the generated .csv into Google Sheets, long text entries may exceed the cell limit of `50,000 characters`. If a cell exceeds this, Google Sheets will skip the content.

Example:

If a file like `msu/2.txt` has:
* 39 pages
* 22,931 words
* 153,522 characters

Google Sheets will skip that cell, as it exceeds the limit.


# Contributors 👩‍💻
* Helan Wang 
* Christylan1121@gmail.com

# Contact
* `Stanford University (Starks Lab)`