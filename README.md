## Platinum Fire Uploader

A Tkinter GUI to manage files in `data_folder`: select and upload, inspect, and delete. The app gives quick column/type previews for common tabular formats (CSV, Excel, JSON, Parquet) and logs actions in-app.

### How to run

```bash
python main.py
```

### What it does
- Select multiple files via the dialog
- Copy them into `data_folder` (originals stay untouched)
- Inspect files already in `data_folder` with lightweight dtype previews
- Delete files from `data_folder` with confirmation
- Log successes/errors in the UI
- Switch between Light, Dark, and High Contrast themes from the dropdown for better visibility

### Dependencies
Install Python packages:
```bash
pip install -r requirements.txt
```

Most Python installs ship Tkinter; `tk` is also listed in requirements for environments that need pip installation.
