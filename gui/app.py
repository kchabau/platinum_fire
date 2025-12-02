"""
Main GUI application class for Platinum Fire.

Tkinter-based GUI that lets users select one or multiple data files and upload
them into the project's data_folder. Uploaded files are copied (not moved) so
the originals are preserved. The UI also prints lightweight column/type
previews for common tabular formats.

Multi-page application:
- Page 1: File Management (upload, delete, inspect files)
- Page 2: Data Inspection & Type Adjustment (inspect columns, adjust data types)
"""

from pathlib import Path
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter.scrolledtext import ScrolledText

import pandas as pd

from config.constants import DATA_FOLDER, FILE_TYPES, PANDAS_DTYPES
from themes.themes import THEMES
from transformers.transformers import TRANSFORMATION_FUNCTIONS
from functions.helper_functions import fix_column_names


class UploadApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Platinum Fire - Data Management")
        self.geometry("1200x700")
        self.resizable(True, True)
        
        # Application state
        self.selected_files: list[str] = []
        self.data_folder_files: list[str] = []
        self.current_dataframe: pd.DataFrame | None = None
        self.current_file_path: Path | None = None
        self.current_selected_column: str | None = None  # Store selected column name
        self.current_theme: str = "Light"  # Current theme
        self.theme_var = tk.StringVar(value=self.current_theme)
        self.style = ttk.Style(self)
        
        # Create page frames
        self.file_management_page = None
        self.data_inspection_page = None
        
        self._build_ui()
        self._apply_theme(self.current_theme)
        self.show_file_management_page()

    def _build_ui(self) -> None:
        """Build the main UI structure with navigation."""
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        
        # Navigation bar
        nav_frame = ttk.Frame(self)
        nav_frame.grid(row=0, column=0, sticky="ew", padx=12, pady=(12, 6))
        nav_frame.columnconfigure(0, weight=1)
        nav_frame.columnconfigure(2, weight=0)
        
        self.nav_label = ttk.Label(
            nav_frame, 
            text="File Management", 
            font=("Arial", 12, "bold")
        )
        self.nav_label.grid(row=0, column=0, sticky="w")
        
        ttk.Label(nav_frame, text="Theme:", font=("Arial", 10)).grid(row=0, column=1, padx=(12, 6), sticky="e")
        self.theme_selector = ttk.Combobox(
            nav_frame,
            values=list(THEMES.keys()),
            state="readonly",
            textvariable=self.theme_var,
            width=16
        )
        self.theme_selector.grid(row=0, column=2, sticky="e")
        self.theme_selector.bind("<<ComboboxSelected>>", self._on_theme_change)
        
        # Container for pages
        self.page_container = ttk.Frame(self)
        self.page_container.grid(row=1, column=0, sticky="nsew", padx=12, pady=6)
        self.page_container.columnconfigure(0, weight=1)
        self.page_container.rowconfigure(0, weight=1)
        
        # Build pages
        self._build_file_management_page()
        self._build_data_inspection_page()

    def _build_file_management_page(self) -> None:
        """Build the file management page (Page 1)."""
        self.file_management_page = ttk.Frame(self.page_container)
        self.file_management_page.columnconfigure(0, weight=1)
        self.file_management_page.rowconfigure(2, weight=1)
        
        header = ttk.Label(
            self.file_management_page,
            text="Inspect, upload, and remove files in data_folder",
            font=("Arial", 14, "bold"),
        )
        header.grid(row=0, column=0, padx=12, pady=(12, 6), sticky="w")
        
        lists_frame = ttk.Frame(self.file_management_page)
        lists_frame.grid(row=1, column=0, padx=12, pady=6, sticky="nsew")
        lists_frame.columnconfigure(0, weight=1)
        lists_frame.columnconfigure(1, weight=1)
        lists_frame.rowconfigure(1, weight=1)
        
        upload_label = ttk.Label(lists_frame, text="Selected files to upload")
        upload_label.grid(row=0, column=0, padx=(0, 8), pady=(0, 4), sticky="w")
        data_label = ttk.Label(lists_frame, text="Files currently in data_folder")
        data_label.grid(row=0, column=1, padx=(8, 0), pady=(0, 4), sticky="w")
        
        upload_frame = ttk.Frame(lists_frame)
        upload_frame.grid(row=1, column=0, padx=(0, 8), sticky="nsew")
        upload_frame.columnconfigure(0, weight=1)
        upload_frame.rowconfigure(0, weight=1)
        
        self.files_list = tk.Listbox(
            upload_frame,
            selectmode=tk.BROWSE,
            activestyle="none",
        )
        self.files_list.grid(row=0, column=0, sticky="nsew")
        upload_scroll = ttk.Scrollbar(upload_frame, orient="vertical", command=self.files_list.yview)
        self.files_list.configure(yscrollcommand=upload_scroll.set)
        upload_scroll.grid(row=0, column=1, sticky="ns")
        
        data_frame = ttk.Frame(lists_frame)
        data_frame.grid(row=1, column=1, padx=(8, 0), sticky="nsew")
        data_frame.columnconfigure(0, weight=1)
        data_frame.rowconfigure(0, weight=1)
        
        self.data_list = tk.Listbox(
            data_frame,
            selectmode=tk.EXTENDED,
            activestyle="none",
        )
        self.data_list.grid(row=0, column=0, sticky="nsew")
        self.data_list.bind("<<ListboxSelect>>", self._on_data_list_selection)
        data_scroll = ttk.Scrollbar(data_frame, orient="vertical", command=self.data_list.yview)
        self.data_list.configure(yscrollcommand=data_scroll.set)
        data_scroll.grid(row=0, column=1, sticky="ns")
        
        btn_frame = ttk.Frame(self.file_management_page)
        btn_frame.grid(row=2, column=0, padx=12, pady=6, sticky="ew")
        for i in range(7):
            btn_frame.columnconfigure(i, weight=1)
        
        ttk.Button(btn_frame, text="Choose files", command=self.choose_files).grid(row=0, column=0, padx=4, pady=4, sticky="ew")
        ttk.Button(btn_frame, text="Clear selected list", command=self.clear_files).grid(row=0, column=1, padx=4, pady=4, sticky="ew")
        ttk.Button(btn_frame, text="Upload to data_folder", command=self.upload_files).grid(row=0, column=2, padx=4, pady=4, sticky="ew")
        ttk.Button(btn_frame, text="Refresh folder view", command=self.refresh_data_folder_list).grid(row=0, column=3, padx=4, pady=4, sticky="ew")
        ttk.Button(btn_frame, text="Inspect selected in data_folder", command=self.inspect_selected_data_file).grid(row=0, column=4, padx=4, pady=4, sticky="ew")
        ttk.Button(btn_frame, text="Delete selected from data_folder", command=self.delete_selected_data_file).grid(row=0, column=5, padx=4, pady=4, sticky="ew")
        
        # Next Section button - initially hidden
        self.next_section_btn = ttk.Button(
            btn_frame, 
            text="Next Section →", 
            command=self.show_data_inspection_page,
            state="disabled"
        )
        self.next_section_btn.grid(row=0, column=6, padx=4, pady=4, sticky="ew")
        
        log_label = ttk.Label(self.file_management_page, text="Activity log")
        log_label.grid(row=3, column=0, padx=12, pady=(8, 0), sticky="w")
        
        self.log = ScrolledText(
            self.file_management_page,
            wrap=tk.WORD,
            height=10,
            state="disabled",
        )
        self.log.grid(row=4, column=0, padx=12, pady=(2, 12), sticky="nsew")
        self.file_management_page.rowconfigure(4, weight=1)
        
        data_folder_label = ttk.Label(self.file_management_page, text=f"Files will be copied to: {DATA_FOLDER}")
        data_folder_label.grid(row=5, column=0, padx=12, pady=(0, 12), sticky="w")
        
        self.refresh_data_folder_list()

    def _build_data_inspection_page(self) -> None:
        """Build the data inspection and type adjustment page (Page 2)."""
        self.data_inspection_page = ttk.Frame(self.page_container)
        self.data_inspection_page.columnconfigure(0, weight=1)
        self.data_inspection_page.rowconfigure(2, weight=1)
        
        # Header with back button
        header_frame = ttk.Frame(self.data_inspection_page)
        header_frame.grid(row=0, column=0, sticky="ew", padx=12, pady=(12, 6))
        header_frame.columnconfigure(1, weight=1)
        
        ttk.Button(
            header_frame, 
            text="← Back to File Management", 
            command=self.show_file_management_page
        ).grid(row=0, column=0, padx=(0, 12), sticky="w")
        
        ttk.Label(
            header_frame,
            text="Data Inspection & Type Adjustment",
            font=("Arial", 14, "bold"),
        ).grid(row=0, column=1, sticky="w")
        
        # File selection and info
        file_selection_frame = ttk.LabelFrame(self.data_inspection_page, text="Select File to Inspect", padding=10)
        file_selection_frame.grid(row=1, column=0, sticky="ew", padx=12, pady=6)
        file_selection_frame.columnconfigure(1, weight=1)
        
        ttk.Label(file_selection_frame, text="File:").grid(row=0, column=0, padx=(0, 8), sticky="w")
        self.file_selector = ttk.Combobox(file_selection_frame, state="readonly", width=50)
        self.file_selector.grid(row=0, column=1, sticky="ew", padx=(0, 8))
        self.file_selector.bind("<<ComboboxSelected>>", self._on_file_selected)
        
        ttk.Button(
            file_selection_frame, 
            text="Load File", 
            command=self._load_selected_file
        ).grid(row=0, column=2, padx=(0, 8))
        
        ttk.Button(
            file_selection_frame, 
            text="Refresh File List", 
            command=self._refresh_file_selector
        ).grid(row=0, column=3)
        
        # Data info display
        info_frame = ttk.Frame(self.data_inspection_page)
        info_frame.grid(row=2, column=0, sticky="nsew", padx=12, pady=6)
        info_frame.columnconfigure(0, weight=1)
        info_frame.rowconfigure(0, weight=1)
        
        # Create notebook for tabs
        notebook = ttk.Notebook(info_frame)
        notebook.grid(row=0, column=0, sticky="nsew")
        
        # Tab 1: Column Information & Type Adjustment
        columns_frame = ttk.Frame(notebook, padding=10)
        notebook.add(columns_frame, text="Columns & Data Types")
        columns_frame.columnconfigure(0, weight=1)
        columns_frame.rowconfigure(1, weight=1)
        
        # Column list with scrollbar
        list_container = ttk.Frame(columns_frame)
        list_container.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        list_container.columnconfigure(0, weight=1)
        
        label_frame = ttk.Frame(list_container)
        label_frame.grid(row=0, column=0, sticky="ew", pady=(0, 4))
        label_frame.columnconfigure(1, weight=1)
        
        ttk.Label(label_frame, text="Columns (select to view details):", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w")
        
        # Label to show currently selected column for type change
        self.selected_column_label = ttk.Label(
            label_frame, 
            text="", 
            font=("Arial", 9, "italic")
        )
        self.selected_column_label.grid(row=0, column=1, sticky="e", padx=(10, 0))
        
        col_list_frame = ttk.Frame(list_container)
        col_list_frame.grid(row=1, column=0, sticky="ew")
        col_list_frame.columnconfigure(0, weight=1)
        col_list_frame.rowconfigure(0, weight=1)
        
        self.columns_listbox = tk.Listbox(
            col_list_frame,
            height=8,
            activestyle="none",
            exportselection=False  # Prevent deselection when losing focus
        )
        self.columns_listbox.grid(row=0, column=0, sticky="ew")
        self.columns_listbox.bind("<<ListboxSelect>>", self._on_column_selected)
        # Bind focus events to maintain selection
        self.columns_listbox.bind("<FocusOut>", self._on_listbox_focus_out)
        self.columns_listbox.bind("<FocusIn>", self._on_listbox_focus_in)
        col_scroll = ttk.Scrollbar(col_list_frame, orient="vertical", command=self.columns_listbox.yview)
        self.columns_listbox.configure(yscrollcommand=col_scroll.set)
        col_scroll.grid(row=0, column=1, sticky="ns")
        
        # Column details and type adjustment
        details_frame = ttk.LabelFrame(columns_frame, text="Column Details & Type Adjustment", padding=10)
        details_frame.grid(row=1, column=0, sticky="nsew")
        details_frame.columnconfigure(1, weight=1)
        
        self.column_info_text = ScrolledText(
            details_frame,
            wrap=tk.WORD,
            height=8,
            state="disabled",
        )
        self.column_info_text.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        ttk.Label(details_frame, text="Change data type to:").grid(row=1, column=0, padx=(0, 8), sticky="w")
        self.dtype_selector = ttk.Combobox(details_frame, values=PANDAS_DTYPES, state="readonly", width=20)
        self.dtype_selector.grid(row=1, column=1, sticky="w", padx=(0, 8))
        
        ttk.Button(
            details_frame, 
            text="Apply Type Change", 
            command=self._apply_type_change
        ).grid(row=1, column=2, padx=(0, 8))
        
        ttk.Button(
            details_frame, 
            text="Reset All Types", 
            command=self._reset_types
        ).grid(row=1, column=3, padx=(0, 8))
        
        ttk.Button(
            details_frame, 
            text="Save Changes", 
            command=self._save_dataframe_changes
        ).grid(row=1, column=4)
        
        # Transformation function section
        transformation_frame = ttk.LabelFrame(details_frame, text="Value Transformation", padding=10)
        transformation_frame.grid(row=2, column=0, columnspan=5, sticky="ew", pady=(15, 0))
        transformation_frame.columnconfigure(1, weight=1)
        transformation_frame.columnconfigure(3, weight=1)
        
        ttk.Label(transformation_frame, text="Transformation Function:").grid(row=0, column=0, padx=(0, 8), sticky="w")
        self.transformation_func_selector = ttk.Combobox(
            transformation_frame, 
            values=list(TRANSFORMATION_FUNCTIONS.keys()),
            state="readonly",
            width=25
        )
        self.transformation_func_selector.grid(row=0, column=1, sticky="w", padx=(0, 12))
        self.transformation_func_selector.bind("<<ComboboxSelected>>", self._on_transformation_func_selected)
        
        ttk.Label(transformation_frame, text="Transformation Type:").grid(row=0, column=2, padx=(0, 8), sticky="w")
        self.transformation_param_selector = ttk.Combobox(
            transformation_frame,
            state="readonly",
            width=20
        )
        self.transformation_param_selector.grid(row=0, column=3, sticky="w", padx=(0, 12))
        
        ttk.Button(
            transformation_frame,
            text="Apply Transformation",
            command=self._apply_transformation
        ).grid(row=0, column=4, padx=(0, 0))
        
        # Description label for transformation function
        self.transformation_desc_label = ttk.Label(
            transformation_frame,
            text="Select a transformation function to see its description.",
            font=("Arial", 11),
            wraplength=700
        )
        self.transformation_desc_label.grid(row=1, column=0, columnspan=5, sticky="w", pady=(8, 0))
        
        # Tab 2: Data Preview
        preview_frame = ttk.Frame(notebook, padding=10)
        notebook.add(preview_frame, text="Data Preview")
        preview_frame.columnconfigure(0, weight=1)
        preview_frame.rowconfigure(0, weight=1)
        
        self.preview_text = ScrolledText(
            preview_frame,
            wrap=tk.NONE,
            state="disabled",
            font=("Courier", 11),
        )
        self.preview_text.grid(row=0, column=0, sticky="nsew")
        
        # Tab 3: Statistics
        stats_frame = ttk.Frame(notebook, padding=10)
        notebook.add(stats_frame, text="Statistics")
        stats_frame.columnconfigure(0, weight=1)
        stats_frame.rowconfigure(0, weight=1)
        
        self.stats_text = ScrolledText(
            stats_frame,
            wrap=tk.WORD,
            state="disabled",
        )
        self.stats_text.grid(row=0, column=0, sticky="nsew")
        
        # Action buttons at bottom
        action_frame = ttk.Frame(self.data_inspection_page)
        action_frame.grid(row=3, column=0, sticky="ew", padx=12, pady=6)
        
        ttk.Button(
            action_frame, 
            text="Apply Helper Functions (fix_column_names)", 
            command=self._apply_helper_functions
        ).grid(row=0, column=0, padx=4, pady=4)
        
        ttk.Label(
            action_frame, 
            text=f"Working with: {DATA_FOLDER}", 
            font=("Arial", 9)
        ).grid(row=0, column=1, padx=12, sticky="w")

    def _on_data_list_selection(self, event=None) -> None:
        """Enable/disable Next Section button based on selection."""
        selected = self.data_list.curselection()
        if selected:
            self.next_section_btn.config(state="normal")
        else:
            self.next_section_btn.config(state="disabled")

    def show_file_management_page(self) -> None:
        """Show the file management page."""
        if self.data_inspection_page:
            self.data_inspection_page.grid_remove()
        if self.file_management_page:
            self.file_management_page.grid(row=0, column=0, sticky="nsew")
        self.nav_label.config(text="File Management")

    def show_data_inspection_page(self) -> None:
        """Show the data inspection page."""
        selected = self.data_list.curselection()
        if not selected:
            messagebox.showwarning("No selection", "Select at least one file in data_folder to proceed.")
            return
        
        if self.file_management_page:
            self.file_management_page.grid_remove()
        if self.data_inspection_page:
            self.data_inspection_page.grid(row=0, column=0, sticky="nsew")
        self.nav_label.config(text="Data Inspection & Type Adjustment")
        
        # Refresh file selector and load first selected file
        self._refresh_file_selector()
        if self.file_selector['values']:
            first_selected = self.data_list.get(selected[0])
            if first_selected in self.file_selector['values']:
                self.file_selector.set(first_selected)
                self._load_selected_file()

    def _refresh_file_selector(self) -> None:
        """Refresh the file selector combobox with current data_folder files."""
        self.data_folder_files = sorted([p.name for p in DATA_FOLDER.iterdir() if p.is_file()])
        self.file_selector['values'] = self.data_folder_files

    def _on_file_selected(self, event=None) -> None:
        """Handle file selection from combobox - auto-load the file."""
        # Auto-load when a file is selected from the dropdown
        if self.file_selector.get():
            self._load_selected_file()

    def _load_selected_file(self) -> None:
        """Load the selected file into a dataframe."""
        filename = self.file_selector.get()
        if not filename:
            return
        
        file_path = DATA_FOLDER / filename
        if not file_path.exists():
            messagebox.showerror("Error", f"File not found: {file_path}")
            return
        
        try:
            suffix = file_path.suffix.lower()
            if suffix == ".csv":
                self.current_dataframe = pd.read_csv(file_path)
            elif suffix in {".xlsx", ".xls"}:
                self.current_dataframe = pd.read_excel(file_path)
            elif suffix == ".json":
                self.current_dataframe = pd.read_json(file_path)
            elif suffix == ".parquet":
                self.current_dataframe = pd.read_parquet(file_path)
            else:
                messagebox.showerror("Error", f"Unsupported file type: {suffix}")
                return
            
            self.current_file_path = file_path
            self._update_column_list()
            self._update_preview()
            self._update_statistics()
            messagebox.showinfo("Success", f"Loaded {filename} with {len(self.current_dataframe)} rows and {len(self.current_dataframe.columns)} columns.")
        except Exception as exc:
            messagebox.showerror("Error", f"Failed to load file: {exc}")

    def _update_column_list(self) -> None:
        """Update the columns listbox with current dataframe columns."""
        if self.current_dataframe is None:
            return
        
        # Store current selection
        selected_col = self.current_selected_column
        
        self.columns_listbox.delete(0, tk.END)
        for col in self.current_dataframe.columns:
            dtype = str(self.current_dataframe[col].dtype)
            self.columns_listbox.insert(tk.END, f"{col} ({dtype})")
        
        # Restore selection if column still exists
        if selected_col and selected_col in self.current_dataframe.columns:
            for i in range(self.columns_listbox.size()):
                if self.columns_listbox.get(i).startswith(f"{selected_col} ("):
                    self.columns_listbox.selection_clear(0, tk.END)
                    self.columns_listbox.selection_set(i)
                    self.columns_listbox.see(i)
                    break

    def _on_listbox_focus_out(self, event=None) -> None:
        """Maintain selection when listbox loses focus."""
        # Don't clear selection when losing focus - keep it visible
        if self.current_selected_column and self.current_dataframe is not None:
            # Restore selection after a brief delay to ensure it persists
            self.after(10, self._restore_column_selection)
    
    def _on_listbox_focus_in(self, event=None) -> None:
        """Restore selection when listbox gains focus."""
        self._restore_column_selection()
    
    def _restore_column_selection(self) -> None:
        """Restore the visual selection in the listbox."""
        if self.current_selected_column and self.current_dataframe is not None:
            if self.current_selected_column in self.current_dataframe.columns:
                for i in range(self.columns_listbox.size()):
                    if self.columns_listbox.get(i).startswith(f"{self.current_selected_column} ("):
                        self.columns_listbox.selection_clear(0, tk.END)
                        self.columns_listbox.selection_set(i)
                        self.columns_listbox.see(i)
                        break
    
    def _on_column_selected(self, event=None) -> None:
        """Handle column selection - show details and current type."""
        selected = self.columns_listbox.curselection()
        if not selected or self.current_dataframe is None:
            self.current_selected_column = None
            if hasattr(self, 'selected_column_label'):
                self.selected_column_label.config(text="")
            return
        
        col_name = self.columns_listbox.get(selected[0]).split(" (")[0]
        self.current_selected_column = col_name  # Store column name
        
        # Update the label to show selected column
        if hasattr(self, 'selected_column_label'):
            self.selected_column_label.config(text=f"Selected: {col_name}")
        
        col = self.current_dataframe[col_name]
        
        # Display column information
        info = f"Column: {col_name}\n"
        info += f"Current Type: {col.dtype}\n"
        info += f"Non-null count: {col.notna().sum()} / {len(col)}\n"
        info += f"Null count: {col.isna().sum()}\n"
        info += f"Unique values: {col.nunique()}\n\n"
        
        if col.dtype == 'object':
            info += f"Sample values:\n{col.head(10).tolist()}\n"
        else:
            info += f"Min: {col.min()}\n" if col.notna().any() else "Min: N/A\n"
            info += f"Max: {col.max()}\n" if col.notna().any() else "Max: N/A\n"
            info += f"Mean: {col.mean():.2f}\n" if col.dtype in ['int64', 'float64'] and col.notna().any() else ""
        
        self.column_info_text.configure(state="normal")
        self.column_info_text.delete(1.0, tk.END)
        self.column_info_text.insert(1.0, info)
        self.column_info_text.configure(state="disabled")
        
        # Set current dtype in selector
        current_dtype = str(col.dtype)
        if current_dtype in PANDAS_DTYPES:
            self.dtype_selector.set(current_dtype)
        else:
            self.dtype_selector.set("")

    def _apply_type_change(self) -> None:
        """Apply data type change to selected column."""
        if not self.current_selected_column or self.current_dataframe is None:
            messagebox.showwarning("No selection", "Select a column first.")
            return
        
        new_dtype = self.dtype_selector.get()
        if not new_dtype:
            messagebox.showwarning("No type selected", "Select a data type first.")
            return
        
        col_name = self.current_selected_column  # Use stored column name
        
        try:
            if new_dtype == "datetime64":
                self.current_dataframe[col_name] = pd.to_datetime(self.current_dataframe[col_name], errors='coerce')
            elif new_dtype == "category":
                self.current_dataframe[col_name] = self.current_dataframe[col_name].astype("category")
            else:
                self.current_dataframe[col_name] = self.current_dataframe[col_name].astype(new_dtype)
            
            self._update_column_list()
            # Re-select the column and refresh details
            self._restore_column_selection()
            self._on_column_selected()  # Refresh details
            messagebox.showinfo("Success", f"Changed {col_name} to {new_dtype}")
        except Exception as exc:
            messagebox.showerror("Error", f"Failed to change type: {exc}")

    def _on_transformation_func_selected(self, event=None) -> None:
        """Handle transformation function selection - update parameter options and description."""
        func_key = self.transformation_func_selector.get()
        if not func_key or func_key not in TRANSFORMATION_FUNCTIONS:
            self.transformation_param_selector['values'] = []
            self.transformation_param_selector.set("")
            self.transformation_desc_label.config(text="Select a transformation function to see its description.")
            return
        
        func_info = TRANSFORMATION_FUNCTIONS[func_key]
        
        # Update description
        self.transformation_desc_label.config(text=func_info["description"])
        
        # Update parameter selector if function requires parameters
        if func_info.get("requires_param", False) and "param_options" in func_info:
            param_keys = list(func_info["param_options"].keys())
            self.transformation_param_selector['values'] = param_keys
            if param_keys:
                self.transformation_param_selector.set(param_keys[0])
        else:
            self.transformation_param_selector['values'] = []
            self.transformation_param_selector.set("")

    def _apply_transformation(self) -> None:
        """Apply the selected transformation function to the selected column."""
        if not self.current_selected_column or self.current_dataframe is None:
            messagebox.showwarning("No selection", "Select a column first.")
            return
        
        func_key = self.transformation_func_selector.get()
        if not func_key or func_key not in TRANSFORMATION_FUNCTIONS:
            messagebox.showwarning("No function selected", "Select a transformation function first.")
            return
        
        func_info = TRANSFORMATION_FUNCTIONS[func_key]
        func = func_info["function"]
        col_name = self.current_selected_column
        
        try:
            # Get the column
            column = self.current_dataframe[col_name]
            
            # Apply transformation based on whether it requires parameters
            if func_info.get("requires_param", False):
                param = self.transformation_param_selector.get()
                if not param:
                    messagebox.showwarning("No parameter selected", "Select a transformation type first.")
                    return
                
                # Apply function with parameter
                result = func(column, param)
            else:
                # Apply function without parameter
                result = func(column)
            
            # Update the dataframe with transformed column
            self.current_dataframe[col_name] = result
            
            # Refresh the UI
            self._update_column_list()
            self._restore_column_selection()
            self._on_column_selected()  # Refresh details
            self._update_preview()
            
            param_text = f" with '{self.transformation_param_selector.get()}'" if func_info.get("requires_param", False) else ""
            messagebox.showinfo("Success", f"Applied {func_info['name']}{param_text} to column '{col_name}'")
            
        except Exception as exc:
            messagebox.showerror("Error", f"Failed to apply transformation: {exc}")

    def _reset_types(self) -> None:
        """Reset all data types by reloading the file."""
        if self.current_file_path is None:
            return
        
        confirm = messagebox.askyesno("Reset Types", "Reload file to reset all type changes?")
        if confirm:
            self._load_selected_file()

    def _save_dataframe_changes(self) -> None:
        """Save the current dataframe back to file."""
        if self.current_dataframe is None or self.current_file_path is None:
            messagebox.showwarning("No data", "No file loaded.")
            return
        
        try:
            suffix = self.current_file_path.suffix.lower()
            if suffix == ".csv":
                self.current_dataframe.to_csv(self.current_file_path, index=False)
            elif suffix in {".xlsx", ".xls"}:
                self.current_dataframe.to_excel(self.current_file_path, index=False)
            elif suffix == ".json":
                self.current_dataframe.to_json(self.current_file_path, orient="records")
            elif suffix == ".parquet":
                self.current_dataframe.to_parquet(self.current_file_path, index=False)
            
            messagebox.showinfo("Success", f"Saved changes to {self.current_file_path.name}")
            self._load_selected_file()  # Reload to refresh
        except Exception as exc:
            messagebox.showerror("Error", f"Failed to save: {exc}")

    def _apply_helper_functions(self) -> None:
        """Apply helper functions from helper_functions.py."""
        if self.current_dataframe is None:
            messagebox.showwarning("No data", "Load a file first.")
            return
        
        try:
            # Apply fix_column_names function
            result = fix_column_names(self.current_dataframe)
            if result is not None:
                self.current_dataframe = result
                self._update_column_list()
                # Clear column selection since names changed
                self.current_selected_column = None
                self.columns_listbox.selection_clear(0, tk.END)
                messagebox.showinfo("Success", "Applied fix_column_names() - column names converted to snake_case.")
            else:
                messagebox.showerror("Error", "fix_column_names() returned None.")
        except Exception as exc:
            messagebox.showerror("Error", f"Failed to apply helper functions: {exc}")

    def _update_preview(self) -> None:
        """Update the data preview tab."""
        if self.current_dataframe is None:
            return
        
        self.preview_text.configure(state="normal")
        self.preview_text.delete(1.0, tk.END)
        
        # Show first 100 rows for better visibility
        preview_df = self.current_dataframe.head(100)
        preview_str = preview_df.to_string()
        self.preview_text.insert(1.0, preview_str)
        self.preview_text.configure(state="disabled")

    def _update_statistics(self) -> None:
        """Update the statistics tab."""
        if self.current_dataframe is None:
            return
        
        self.stats_text.configure(state="normal")
        self.stats_text.delete(1.0, tk.END)
        
        stats = f"DataFrame Shape: {self.current_dataframe.shape[0]} rows × {self.current_dataframe.shape[1]} columns\n\n"
        stats += "Column Information:\n"
        stats += str(self.current_dataframe.info())
        stats += "\n\nDescriptive Statistics:\n"
        stats += str(self.current_dataframe.describe(include='all'))
        
        self.stats_text.insert(1.0, stats)
        self.stats_text.configure(state="disabled")

    # File management methods (existing functionality)
    def choose_files(self) -> None:
        paths = filedialog.askopenfilenames(title="Select one or more files", filetypes=FILE_TYPES)
        if not paths:
            return
        self.selected_files = list(paths)
        self._refresh_listbox()
        self._log(f"Selected {len(self.selected_files)} file(s).")
        self._log('-'*50)

    def clear_files(self) -> None:
        self.selected_files = []
        self._refresh_listbox()
        self._log("Cleared selected files.")
        self._log('-'*50)

    def upload_files(self) -> None:
        if not self.selected_files:
            messagebox.showwarning("No files", "Pick at least one file to upload.")
            return

        successes = 0
        for path_str in self.selected_files:
            source = Path(path_str)
            destination = DATA_FOLDER / source.name
            try:
                shutil.copy2(source, destination)
                successes += 1
                self._log(f"Copied {source.name} -> {destination}")
                self._log('-'*50)
                self._preview_types(destination)
                self._log('-'*50)
            except Exception as exc:
                self._log(f"Failed to copy {source}: {exc}")

        messagebox.showinfo("Upload complete", f"Finished processing {len(self.selected_files)} file(s). Success: {successes}.")
        self.refresh_data_folder_list()

    def refresh_data_folder_list(self) -> None:
        """Populate list of files currently in data_folder."""
        self.data_folder_files = sorted([p.name for p in DATA_FOLDER.iterdir() if p.is_file()])
        self.data_list.delete(0, tk.END)
        for name in self.data_folder_files:
            self.data_list.insert(tk.END, name)
        self._log(f"Refreshed data_folder view: {len(self.data_folder_files)} file(s).")
        self._log('-'*50)

    def inspect_selected_data_file(self) -> None:
        """Inspect/preview the currently selected file in data_folder."""
        selected = self.data_list.curselection()
        if not selected:
            messagebox.showwarning("No selection", "Select a file in data_folder to inspect.")
            return
        name = self.data_list.get(selected[0])
        file_path = DATA_FOLDER / name
        if not file_path.exists():
            self._log(f"File not found: {file_path}")
            self.refresh_data_folder_list()
            return
        self._preview_types(file_path)

    def delete_selected_data_file(self) -> None:
        """Remove the selected file(s) from data_folder after confirmation."""
        selected = self.data_list.curselection()
        if not selected:
            messagebox.showwarning("No selection", "Select one or more files in data_folder to delete.")
            return
        
        selected_names = [self.data_list.get(idx) for idx in selected]
        
        if len(selected_names) == 1:
            confirm_msg = f"Delete {selected_names[0]} from data_folder?"
        else:
            confirm_msg = f"Delete {len(selected_names)} files from data_folder?\n\nFiles:\n" + "\n".join(f"  • {name}" for name in selected_names)
        
        confirm = messagebox.askyesno("Delete file(s)", confirm_msg)
        if not confirm:
            return
        
        successes = 0
        failures = 0
        for name in selected_names:
            file_path = DATA_FOLDER / name
            if not file_path.exists():
                self._log(f"File not found: {file_path}")
                failures += 1
                continue
            try:
                file_path.unlink()
                self._log(f"Deleted {name} from data_folder.")
                successes += 1
                self._log('-'*50)
            except Exception as exc:
                self._log(f"Failed to delete {name}: {exc}")
                failures += 1
        
        if failures == 0:
            messagebox.showinfo("Delete complete", f"Successfully deleted {successes} file(s).")
        else:
            messagebox.showwarning("Delete complete", f"Deleted {successes} file(s). Failed to delete {failures} file(s).")
        
        self.refresh_data_folder_list()

    def _preview_types(self, file_path: Path) -> None:
        """Print lightweight dtypes preview for tabular files."""
        suffix = file_path.suffix.lower()
        try:
            if suffix == ".csv":
                df = pd.read_csv(file_path, nrows=20)
            elif suffix in {".xlsx", ".xls"}:
                df = pd.read_excel(file_path, nrows=20)
            elif suffix == ".json":
                df = pd.read_json(file_path)
            elif suffix == ".parquet":
                df = pd.read_parquet(file_path)
            else:
                self._log(f"Preview skipped for unsupported preview type: {file_path.name}")
                return

            preview = ", ".join(f"{col} ({dtype})" for col, dtype in df.dtypes.items())
            self._log(f"Preview for {file_path.name}: {preview}")
        except Exception as exc:
            self._log(f"Could not preview {file_path.name}: {exc}")

    def _refresh_listbox(self) -> None:
        self.files_list.delete(0, tk.END)
        for path_str in self.selected_files:
            self.files_list.insert(tk.END, path_str)

    def _log(self, message: str) -> None:
        self.log.configure(state="normal")
        self.log.insert(tk.END, f"{message}\n")
        self.log.see(tk.END)
        self.log.configure(state="disabled")

    def _on_theme_change(self, event=None) -> None:
        """Handle theme selection change from combobox."""
        new_theme = self.theme_var.get()
        if new_theme in THEMES:
            self._apply_theme(new_theme)

    def _apply_theme(self, theme: str) -> None:
        """Apply theme colors to all widgets."""
        self.current_theme = theme
        colors = THEMES[theme]
        
        # Configure ttk.Style for ttk widgets
        style = ttk.Style()
        style.theme_use('clam')  # Use a theme that supports customization
        
        # Configure ttk widget styles
        style.configure('TFrame', background=colors["secondary_bg"])
        style.configure('TLabel', background=colors["secondary_bg"], foreground=colors["fg"])
        style.configure('TButton', background=colors["button_bg"], foreground=colors["button_fg"])
        style.map('TButton',
                  background=[('active', colors["accent_hover"])],
                  foreground=[('active', colors["button_fg"])])
        style.configure('TCombobox', fieldbackground=colors["text_bg"], foreground=colors["fg"])
        style.configure('TNotebook', background=colors["secondary_bg"])
        style.configure('TNotebook.Tab', background=colors["secondary_bg"], foreground=colors["fg"])
        style.map('TNotebook.Tab',
                  background=[('selected', colors["bg"])],
                  foreground=[('selected', colors["fg"])])
        style.configure('TLabelFrame', background=colors["secondary_bg"], foreground=colors["fg"])
        style.configure('TScrollbar', background=colors["border"], troughcolor=colors["secondary_bg"])
        
        # Update theme selector
        if hasattr(self, 'theme_var'):
            self.theme_var.set(theme)
        
        # Apply to main window
        self.config(bg=colors["bg"])
        
        # Apply to all frames recursively
        for widget in self.winfo_children():
            self._apply_theme_to_widget(widget, colors)
        
        # Apply to specific widgets we know about
        if hasattr(self, 'files_list'):
            self.files_list.config(
                bg=colors["listbox_bg"],
                fg=colors["listbox_fg"],
                selectbackground=colors["listbox_select"],
                selectforeground=colors["bg"]
            )
        
        if hasattr(self, 'data_list'):
            self.data_list.config(
                bg=colors["listbox_bg"],
                fg=colors["listbox_fg"],
                selectbackground=colors["listbox_select"],
                selectforeground=colors["bg"]
            )
        
        if hasattr(self, 'columns_listbox'):
            self.columns_listbox.config(
                bg=colors["listbox_bg"],
                fg=colors["listbox_fg"],
                selectbackground=colors["listbox_select"],
                selectforeground=colors["bg"]
            )
        
        if hasattr(self, 'log'):
            self.log.config(
                bg=colors["text_bg"],
                fg=colors["text_fg"],
                insertbackground=colors["fg"]
            )
        
        if hasattr(self, 'column_info_text'):
            self.column_info_text.config(
                bg=colors["text_bg"],
                fg=colors["text_fg"],
                insertbackground=colors["fg"]
            )
        
        if hasattr(self, 'preview_text'):
            self.preview_text.config(
                bg=colors["text_bg"],
                fg=colors["text_fg"],
                insertbackground=colors["fg"]
            )
        
        if hasattr(self, 'stats_text'):
            self.stats_text.config(
                bg=colors["text_bg"],
                fg=colors["text_fg"],
                insertbackground=colors["fg"]
            )
        
        # Update selected column label
        if hasattr(self, 'selected_column_label'):
            style.configure('SelectedCol.TLabel', 
                          background=colors["secondary_bg"], 
                          foreground=colors["text_secondary"])
            self.selected_column_label.config(style='SelectedCol.TLabel')
        
        # Update transformation description label
        if hasattr(self, 'transformation_desc_label'):
            style.configure('TransDesc.TLabel',
                          background=colors["secondary_bg"],
                          foreground=colors["text_secondary"])
            self.transformation_desc_label.config(style='TransDesc.TLabel')

    def _apply_theme_to_widget(self, widget, colors: dict) -> None:
        """Recursively apply theme to widget and its children."""
        widget_type = widget.winfo_class()
        
        # Apply to frames
        if widget_type in ('Frame', 'TFrame'):
            try:
                widget.config(bg=colors["secondary_bg"])
            except:
                pass
        
        # Apply to labels
        if widget_type in ('Label', 'TLabel'):
            try:
                widget.config(bg=colors["secondary_bg"], fg=colors["fg"])
            except:
                pass
        
        # Recursively apply to children
        for child in widget.winfo_children():
            self._apply_theme_to_widget(child, colors)

