import pandas as pd 
import numpy as np
import re 

from datetime import datetime
from dependencies.dependencies import us_states


def fix_column_names(data: pd.DataFrame) -> pd.DataFrame:
    """
    Fix_column_names: This function will be used to transform the names of the columns 
    in the dataframe to fit snake_case naming conventions.

    Input: A DataFrame
    Output: A DataFrame with the names of the columns in snake_case
    
    This function replaces punctuation with underscores and converts to snake_case.
    """
    punctuation_list = ['!', '@', '#', '$', '%', '^', '&', '*', '+', '=', '<', '>', '?', ';', ':', '|', '\\', '/', '\"', '\'', '`', '~']
    
    # Create a copy to avoid modifying the original
    df = data.copy()
    
    try:   
        # Replace punctuation with underscores
        for punctuation in punctuation_list:
            df.columns = df.columns.str.replace(punctuation, '_', regex=False)
        
        # Convert to snake_case (lowercase with underscores)
        # Replace spaces and multiple underscores with single underscore
        df.columns = df.columns.str.replace(' ', '_', regex=False)
        df.columns = df.columns.str.replace('__+', '_', regex=True)  # Multiple underscores to single
        df.columns = df.columns.str.lower()  # Convert to lowercase
        df.columns = df.columns.str.strip('_')  # Remove leading/trailing underscores
        
        return df
    except Exception as e:
        print(f'Error fixing names: {e}')
        return data  # Return original on error


# Future functions can be added here:
# - fix_column_names(df)
# - fix_name_values(df)
# - convert_data_types(df, column_type_mapping)
# - handle_missing_values(df, strategy='drop'|'fill')
# - remove_duplicates(df, subset=None)
# - etc.

def fix_name_values(column: pd.Series, transformation: str = 'title') -> pd.Series:
    """
    Fix_name_values: This function transforms the values in a column based on the specified transformation.
    
    Supported transformations for string columns:
    - 'title': Convert to Title Case (e.g., "john doe" -> "John Doe")
    - 'upper': Convert to UPPERCASE (e.g., "john doe" -> "JOHN DOE")
    - 'lower': Convert to lowercase (e.g., "John Doe" -> "john doe")
    - 'strip': Remove leading/trailing whitespace
    - 'capitalize': Capitalize first letter only (e.g., "john doe" -> "John doe")
    
    Args:
        column: A pandas Series (column) to transform
        transformation: Type of transformation to apply (default: 'title')
    
    Returns:
        A Series with transformed values
    
    Example:
        >>> df['name'] = fix_name_values(df['name'], 'title')
    """
    try:
        # Create a copy to avoid modifying the original
        result = column.copy()
        
        # Only apply string transformations to object/string dtype columns
        if column.dtype == 'object' or column.dtype == 'string':
            transformation = transformation.lower()
            
            if transformation == 'title':
                result = result.str.strip().str.title()
            elif transformation == 'upper':
                result = result.str.strip().str.upper()
            elif transformation == 'lower':
                result = result.str.strip().str.lower()
            elif transformation == 'capitalize':
                result = result.str.strip().str.capitalize()
            else:
                print(f'Warning: Unknown transformation "{transformation}". Supported: title, upper, lower, strip, capitalize')
                return column  # Return original if unknown transformation
        
        return result
        
    except Exception as e:
        print(f'Error fixing name values: {e}')
        return column  # Return original on error


def fix_date_values(column: pd.Series, transformation: str = 'standardize') -> pd.Series:
    """
    Fix_date_values: This function transforms date values in a column by parsing and optionally formatting them.
    
    The function can:
    1. Parse string dates from various input formats
    2. Standardize dates to datetime objects
    3. Format datetime objects to specific string formats
    
    Args:
        column: A pandas Series (column) to transform (can be string or datetime)
        transformation: Type of transformation to apply:
            - 'standardize': Parse dates and convert to datetime64 (default)
            - 'yyyy-mm-dd': Format dates as 'YYYY-MM-DD' string
            - 'mm/dd/yyyy': Format dates as 'MM/DD/YYYY' string
            - 'dd/mm/yyyy': Format dates as 'DD/MM/YYYY' string
            - 'yyyy/mm/dd': Format dates as 'YYYY/MM/DD' string
            - 'dd-mm-yyyy': Format dates as 'DD-MM-YYYY' string
    
    Returns:
        A Series with transformed date values (datetime64 for 'standardize', string for format options)
    
    Example:
        >>> df['date'] = fix_date_values(df['date'], 'standardize')  # Parse to datetime
        >>> df['date'] = fix_date_values(df['date'], 'yyyy-mm-dd')  # Format as string
    """
    try:
        # Create a copy to avoid modifying the original
        result = column.copy()
        
        # First, try to parse dates if column is string/object type
        if column.dtype == 'object' or column.dtype == 'string':
            # Try to parse dates - pandas will attempt to infer format
            result = pd.to_datetime(result, errors='coerce', infer_datetime_format=True)
        
        # If already datetime or successfully parsed, proceed with transformation
        if pd.api.types.is_datetime64_any_dtype(result) or result.dtype == 'datetime64[ns]':
            transformation = transformation.lower()
            
            if transformation == 'standardize':
                # Already datetime, just return it
                return result
            elif transformation == 'yyyy-mm-dd':
                # Format as YYYY-MM-DD string
                return result.dt.strftime('%Y-%m-%d')
            elif transformation == 'mm/dd/yyyy':
                # Format as MM/DD/YYYY string
                return result.dt.strftime('%m/%d/%Y')
            elif transformation == 'dd/mm/yyyy':
                # Format as DD/MM/YYYY string
                return result.dt.strftime('%d/%m/%Y')
            elif transformation == 'yyyy/mm/dd':
                # Format as YYYY/MM/DD string
                return result.dt.strftime('%Y/%m/%d')
            elif transformation == 'dd-mm-yyyy':
                # Format as DD-MM-YYYY string
                return result.dt.strftime('%d-%m-%Y')
            else:
                print(f'Warning: Unknown transformation "{transformation}". Supported: standardize, yyyy-mm-dd, mm/dd/yyyy, dd/mm/yyyy, yyyy/mm/dd, dd-mm-yyyy')
                return column  # Return original if unknown transformation
        else:
            # If we couldn't parse dates, return original
            print(f'Warning: Could not parse dates from column. Column dtype: {column.dtype}')
            return column
        
    except Exception as e:
        print(f'Error fixing date values: {e}')
        return column  # Return original on error


def fix_state_values(column: pd.Series, transformation: str = 'standardize') -> pd.Series:
    """
    Fix_state_values: This function standardizes state values in a column using the US states dictionary.

    The function can:
    1. Convert state codes to full state names (e.g., "NY" -> "New York")
    2. Convert full state names to state codes (e.g., "New York" -> "NY")
    3. Standardize state names to proper case format (default)

    Args:
        column: A pandas Series (column) to transform
        transformation: Type of transformation to apply:
            - 'standardize': Standardize to full state names with proper case (default)
            - 'state_name': Convert to full state name (e.g., "NY" -> "New York", "new york" -> "New York")
            - 'state_code': Convert to state code (e.g., "New York" -> "NY", "new york" -> "NY")
    
    Returns:
        A Series with transformed state values
    
    Example:
        >>> df['state'] = fix_state_values(df['state'], 'standardize')  # Standardize to full names
        >>> df['state'] = fix_state_values(df['state'], 'state_code')  # Convert to codes
    """
    try:
        # Create a copy to avoid modifying the original
        result = column.copy()
        
        # Only process string/object columns
        if column.dtype != 'object' and column.dtype != 'string':
            print(f'Warning: Column is not string type. Cannot process state values.')
            return column
        
        # Create reverse mapping: code -> name
        code_to_name = {code: name for name, code in us_states.items()}
        
        # Process each value
        def transform_state(value):
            if pd.isna(value):
                return value
            
            value_str = str(value).strip()
            if not value_str:
                return value
            
            # Try to match as state code (case-insensitive)
            value_upper = value_str.upper()
            if value_upper in code_to_name:
                state_name = code_to_name[value_upper]
                if transformation == 'state_code':
                    return value_upper
                else:  # standardize or state_name
                    return state_name
            
            # Try to match as state name (case-insensitive, title case)
            value_title = value_str.title()
            if value_title in us_states:
                state_code = us_states[value_title]
                if transformation == 'state_code':
                    return state_code
                else:  # standardize or state_name
                    return value_title
            
            # Try partial matching (e.g., "New York" might be "new york" or "NEW YORK")
            for state_name, state_code in us_states.items():
                if value_title == state_name.title() or value_upper == state_code:
                    if transformation == 'state_code':
                        return state_code
                    else:
                        return state_name
            
            # If no match found, return original value (or try title case for standardize)
            if transformation in ['standardize', 'state_name']:
                return value_title
            elif transformation == 'state_code':
                return value_upper
            else:
                return value_str
        
        result = result.apply(transform_state)
        return result
        
    except Exception as e:
        print(f'Error fixing state values: {e}')
        return column  # Return original on error