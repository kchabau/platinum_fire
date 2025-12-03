## Platinum Fire - Data Management Tool

A Tkinter-based GUI application for managing and transforming data files. Upload files to `data_folder`, inspect data structures, adjust data types, and apply transformation functions to clean and standardize your data.

### Quick Start - How to Use

Watch this quick demo video to see Platinum Fire in action:

https://github.com/kchabau/platinum_fire/blob/main/Screen%20Recording%202025-12-02%20at%207.48.54%20PM.mov

The video demonstrates:
- Uploading files to the application
- Inspecting data structure and types
- Applying transformations to clean and standardize data
- Saving your cleaned datasets

### Background

**The Problem:**

Before you can analyze data, you often need to clean and transform it. Common issues include:

- Inconsistent column names (spaces, special characters, mixed case)
- Mixed data formats (dates as strings, numbers with currency symbols, phone numbers in various formats)
- Inconsistent text formatting (names in different cases, state codes vs. full names)
- Wrong data types (numbers stored as strings, dates not recognized)
- Messy values (extra whitespace, inconsistent formatting)

Traditional solutions require writing Python scripts with pandas, which can be time-consuming and requires programming knowledge. Excel can help but lacks the power and flexibility of Python-based transformations.

**The Solution:**

Platinum Fire bridges this gap by providing a user-friendly GUI that combines the power of Python/pandas with an intuitive interface. It allows you to:

- **Quickly upload files** in multiple formats (CSV, Excel, JSON, Parquet)
- **Inspect your data** visually without writing code
- **Transform values** using pre-built functions for common data cleaning tasks
- **Adjust data types** with a simple dropdown interface
- **Save cleaned data** back to files in `data_folder` for further analysis

Whether you're a data analyst, researcher, or business professional, the program helps you get from raw, messy data to clean, analysis-ready datasets in minutes instead of hours.

### Features

- **File Management**: Select, upload, inspect, and delete files in `data_folder`
- **Data Inspection**: View column information, data types, and statistics
- **Type Adjustment**: Change column data types with a user-friendly interface
- **Data Transformations**: Apply helper functions to standardize:
  - Column names (snake_case conversion)
  - Name values (title case, uppercase, lowercase, capitalize)
  - Date values (parse and format in various date formats)
  - State values (standardize US state names/codes)
  - Numeric values (format as currency, percentage, phone numbers, IDs, or standardize)
- **Theme Support**: Switch between Light, Dark, and Warm Tones themes
- **Multi-format Support**: Works with CSV, Excel, JSON, and Parquet files

### Prerequisites

- Python 3.11 or higher
- Tkinter (usually included with Python)

### Setup Instructions

**It is recommended to use a virtual environment before starting the project.**

#### 1. Create a Virtual Environment

```bash
# Create virtual environment
python3 -m venv .venv

# On macOS/Linux, activate it:
source .venv/bin/activate

# On Windows, activate it:
# .venv\Scripts\activate
```

#### 2. Install Dependencies

```bash
# Make sure your virtual environment is activated, then:
pip install -r requirements.txt
```

#### 3. Run the Application

```bash
# With virtual environment activated:
python main.py
```

### Project Structure

```
platinum_fire/
├── main.py                    # Main entry point - runs the application
├── gui/
│   └── app.py                # Main GUI application class
├── config/
│   └── constants.py           # Application constants (DATA_FOLDER, FILE_TYPES, etc.)
├── themes/
│   └── themes.py             # Theme color definitions (Light, Dark, Warm Tones)
├── transformers/
│   └── transformers.py       # Transformation function configurations
├── functions/
│   └── helper_functions.py   # Data transformation functions
├── dependencies/
│   └── dependencies.py       # Color palettes and US states dictionary
├── data_folder/              # Directory for uploaded data files
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

### How to Use

#### Starting the Application

1. **Activate your virtual environment** (if using one):

   ```bash
   source .venv/bin/activate  # macOS/Linux
   # or
   .venv\Scripts\activate     # Windows
   ```

2. **Run the application**:

   ```bash
   python main.py
   ```

3. The application window will open with the **File Management** page.

---

#### Page 1: File Management

The File Management page allows you to upload, inspect, and manage data files.

**Uploading Files:**

1. Click **"Choose files"** to select one or more data files from your computer
2. Selected files will appear in the "Selected files to upload" list
3. Click **"Upload to data_folder"** to copy files to the project's `data_folder`
4. Files are copied (not moved), so your originals remain safe

**Managing Files:**

- **Refresh folder view**: Updates the list of files in `data_folder`
- **Inspect selected in data_folder**: Preview column types for a selected file
- **Delete selected from data_folder**: Remove one or more files (with confirmation)
- **Clear selected list**: Clear the upload queue without uploading

**Navigation:**

- Click **"Next Section →"** to proceed to Data Inspection (no file selection required)

---

#### Page 2: Data Inspection & Type Adjustment

This page provides tools to inspect and transform your data.

**Loading a File:**

1. Select a file from the **"File"** dropdown (shows all files in `data_folder`)
2. Click **"Load File"** or the file will auto-load when selected
3. The file loads into memory for inspection and transformation

**Viewing Data Information:**

The page has three tabs:

1. **Columns & Data Types Tab:**

   - **Column List**: Shows all columns with their current data types
   - **Column Details**: Select a column to see:
     - Current data type
     - Non-null/null counts
     - Unique value count
     - Sample values or min/max/mean (for numeric columns)

2. **Data Preview Tab:**

   - Displays the first 100 rows of data
   - Useful for seeing the actual data values

3. **Statistics Tab:**
   - Shows DataFrame shape and column information
   - Displays descriptive statistics

**Changing Data Types:**

1. Select a column from the column list
2. Choose a new data type from the **"Change data type to"** dropdown
3. Click **"Apply Type Change"** to convert the column
4. Common types: `int64`, `float64`, `object`, `datetime64`, `category`, `string`

**Applying Transformations:**

The application includes several transformation functions:

1. **Fix Name Values** - Transform string text:

   - **Title Case**: "john doe" → "John Doe"
   - **Uppercase**: "john doe" → "JOHN DOE"
   - **Lowercase**: "John Doe" → "john doe"
   - **Capitalize**: "john doe" → "John doe"

2. **Fix Date Values** - Parse and format dates:

   - **Standardize**: Convert to datetime64 format
   - **YYYY-MM-DD**: Format as "2024-12-25"
   - **MM/DD/YYYY**: Format as "12/25/2024"
   - **DD/MM/YYYY**: Format as "25/12/2024"
   - And other date formats

3. **Fix State Values** - Standardize US state names/codes:

   - **Standardize**: Convert to full state names (e.g., "NY" → "New York")
   - **State Name**: Convert to full state name format
   - **State Code**: Convert to two-letter code (e.g., "New York" → "NY")

4. **Fix Numeric Values** - Transform numeric data:
   - **Standardize**: Extract numbers from strings, convert to float64 (e.g., "$1,000" → 1000.0)
   - **Format**: Round to 2 decimal places as float64
   - **Percentage**: Format as percentage string (e.g., 0.5 → "50.00%")
   - **Money**: Format as currency (e.g., 100000 → "$100,000.00")
   - **Phone**: Format as phone number with + prefix (e.g., "1234567890" → "+1234567890")
   - **ID**: Convert to integer (e.g., 123456.78 → 123456)

**To Apply a Transformation:**

1. Select a column from the column list
2. Choose a transformation function from the **"Transformation Function"** dropdown
3. Select a transformation type from the **"Transformation Type"** dropdown (if applicable)
4. Read the description that appears below the dropdowns
5. Click **"Apply Transformation"** to transform the column

**Saving Changes:**

- Click **"Save Changes"** to write modifications back to the original file
- Click **"Reset All Types"** to reload the file and discard all changes

**Other Features:**

- **Apply Helper Functions**: Automatically applies `fix_column_names()` to convert all column names to snake_case
- **Theme Selector**: Change the application theme (Light, Dark, Warm Tones) from the top navigation bar

---

#### Common Workflows

**Workflow 1: Clean Column Names**

1. Upload your file
2. Go to Data Inspection page
3. Click **"Apply Helper Functions (fix_column_names)"**
4. All column names are converted to snake_case

**Workflow 2: Standardize Phone Numbers**

1. Load a file with phone number column
2. Select the phone number column
3. Choose **"Fix Numeric Values"** → **"Phone"**
4. Click **"Apply Transformation"**
5. All phone numbers formatted as "+1234567890"

**Workflow 3: Fix Date Formats**

1. Load a file with date column (may be strings)
2. Select the date column
3. Choose **"Fix Date Values"** → **"Standardize"**
4. Click **"Apply Transformation"**
5. Dates converted to datetime64 format
6. Optionally format as string: Choose **"YYYY-MM-DD"** or other format

**Workflow 4: Clean State Names**

1. Load a file with state column (mixed formats: "NY", "New York", "new york")
2. Select the state column
3. Choose **"Fix State Values"** → **"Standardize"**
4. Click **"Apply Transformation"**
5. All states converted to proper case full names

---

#### Tips

- **Preview Before Saving**: Use the Data Preview tab to verify transformations before saving
- **Check Statistics**: Use the Statistics tab to understand your data distribution
- **Multiple Transformations**: You can apply multiple transformations to the same column
- **Undo Changes**: Use "Reset All Types" to reload the file and start over
- **CLI Logging**: Check your terminal/console for detailed transformation logs and progress

### Dependencies

The project requires the following Python packages (install via `requirements.txt`):

- **pandas** - Data manipulation and analysis
- **numpy** - Numerical operations
- **openpyxl** - Excel file support (.xlsx, .xls)
- **pyarrow** - Parquet file support

**Note:** `scikit-learn` was removed from requirements as it's not used in the application.

Most Python installs ship with Tkinter; if not available, install `python-tk` via your system package manager (e.g., `brew install python-tk@3.11` on macOS).

---

### Troubleshooting

**Issue: ModuleNotFoundError for pandas/numpy**

- Solution: Make sure your virtual environment is activated and run `pip install -r requirements.txt`

**Issue: Tkinter not found**

- macOS: Install via Homebrew: `brew install python-tk@3.11`
- Linux: Install via package manager: `sudo apt-get install python3-tk` (Ubuntu/Debian)
- Windows: Usually included with Python installation

**Issue: Can't load Excel files**

- Solution: Ensure `openpyxl` is installed: `pip install openpyxl`

**Issue: Can't load Parquet files**

- Solution: Ensure `pyarrow` is installed: `pip install pyarrow`

---

### Contributing

This is an open-source project. Feel free to:

- Report issues
- Suggest new features
- Submit pull requests
- Add new transformation functions

---

### License

This project is open source and available for anyone to use, modify, and distribute freely. No formal license restrictions - use it however you'd like!
