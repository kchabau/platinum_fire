## Platinum Fire - Data Management Tool

A Tkinter-based GUI application for managing and transforming data files. Upload files to `data_folder`, inspect data structures, adjust data types, and apply transformation functions to clean and standardize your data.

### Features

- **File Management**: Select, upload, inspect, and delete files in `data_folder`
- **Data Inspection**: View column information, data types, and statistics
- **Type Adjustment**: Change column data types with a user-friendly interface
- **Data Transformations**: Apply helper functions to standardize:
  - Column names (snake_case conversion)
  - Name values (title case, uppercase, lowercase, etc.)
  - Date values (various date formats)
  - State values (standardize state names/codes)
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

### Usage

1. **File Management Page**:

   - Select files to upload using "Choose files"
   - Upload files to `data_folder`
   - Inspect or delete files from `data_folder`
   - Click "Next Section →" to proceed to data inspection

2. **Data Inspection Page**:
   - Select a file from the dropdown
   - View columns and their data types
   - Select a column to see detailed information
   - Change data types using the dropdown
   - Apply transformation functions to clean your data
   - Save changes back to the file

### Dependencies

The project requires the following Python packages (install via `requirements.txt`):

- pandas
- numpy
- scikit-learn
- openpyxl
- pyarrow

Most Python installs ship with Tkinter; if not available, install `python-tk` via your system package manager.
