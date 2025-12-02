"""
Application constants and configuration.
"""
from pathlib import Path

# Resolve data folder relative to project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FOLDER = PROJECT_ROOT / "data_folder"
DATA_FOLDER.mkdir(parents=True, exist_ok=True)

# File filters shown in the picker dialog
FILE_TYPES = [
    ("Data files", "*.csv *.xlsx *.xls *.json *.parquet *.txt"),
    ("All files", "*.*"),
]

# Available data types for conversion
PANDAS_DTYPES = [
    "object", "int64", "float64", "bool", "datetime64",
    "category", "string", "Int64", "Float64", "boolean"
]

