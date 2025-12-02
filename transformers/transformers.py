"""
Transformation function definitions with descriptions.

This module defines all available transformation functions that can be applied
to data columns through the GUI.
"""
from functions.helper_functions import fix_name_values, fix_date_values, fix_state_values

TRANSFORMATION_FUNCTIONS = {
    "fix_name_values": {
        "name": "Fix Name Values",
        "description": "Transforms string values in a column (title case, uppercase, lowercase, strip whitespace, capitalize).",
        "function": fix_name_values,
        "requires_param": True,
        "param_options": {
            "title": "Title Case - Converts text to Title Case (e.g., 'john doe' -> 'John Doe')",
            "upper": "Uppercase - Converts all text to UPPERCASE (e.g., 'john doe' -> 'JOHN DOE')",
            "lower": "Lowercase - Converts all text to lowercase (e.g., 'John Doe' -> 'john doe')",
            "capitalize": "Capitalize - Capitalizes only the first letter (e.g., 'john doe' -> 'John doe')"
        }
    },
    "fix_date_values": {
        "name": "Fix Date Values",
        "description": "Parses and formats date values in a column. Can standardize dates to datetime format or format them as strings in various date formats (YYYY-MM-DD, MM/DD/YYYY, DD/MM/YYYY, etc.).",
        "function": fix_date_values,
        "requires_param": True,
        "param_options": {
            "standardize": "Standardize - Parse dates and convert to datetime64 format (default)",
            "yyyy-mm-dd": "YYYY-MM-DD - Format dates as 'YYYY-MM-DD' string (e.g., '2024-12-25')",
            "mm/dd/yyyy": "MM/DD/YYYY - Format dates as 'MM/DD/YYYY' string (e.g., '12/25/2024')",
            "dd/mm/yyyy": "DD/MM/YYYY - Format dates as 'DD/MM/YYYY' string (e.g., '25/12/2024')",
            "yyyy/mm/dd": "YYYY/MM/DD - Format dates as 'YYYY/MM/DD' string (e.g., '2024/12/25')",
            "dd-mm-yyyy": "DD-MM-YYYY - Format dates as 'DD-MM-YYYY' string (e.g., '25-12-2024')"
        }
    },
    "fix_state_values": {
        "name": "Fix State Values",
        "description": "Standardizes US state values in a column. Converts state codes to full names, full names to codes (ie. 'New York' -> 'NY'), or standardizes to proper case format (ie. 'new york' -> 'New York') using the US states dictionary.",
        "function": fix_state_values,
        "requires_param": True,
        "param_options": {
            "standardize": "Standardize - Convert to full state names with proper case (e.g., 'NY' -> 'New York', 'new york' -> 'New York')",
            "state_name": "State Name - Convert to full state name format (e.g., 'NY' -> 'New York', 'california' -> 'California')",
            "state_code": "State Code - Convert to two-letter state code (e.g., 'New York' -> 'NY', 'California' -> 'CA')"
        }
    }
}

