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
                # Remove extra spaces
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

def fix_numeric_values(column: pd.Series, transformation: str = 'standardize') -> pd.Series:
    """
    Fix_numeric_values: This function transforms numeric values in a column. It can handle both
    numeric and string columns that contain numeric values (e.g., "$1,000", "50%", "1,234.56").
    
    The function first extracts numeric values from strings (removing currency symbols, commas, 
    percentage signs, etc.), then applies the specified transformation.

    Args:
        column: A pandas Series (column) to transform (can be numeric or string containing numbers)
        transformation: Type of transformation to apply:
            - 'standardize': Convert to numeric float64 format (default) - removes formatting and converts to pure numbers
            - 'format': Convert to float64 with 2 decimal places (e.g., 100000.456 -> 100000.46)
            - 'percentage': Convert to percentage format as string/object (e.g., 0.5 -> "50.00%")
            - 'money': Format as currency with dollar sign as string/object (e.g., 100000 -> "$100,000.00")
            - 'phone': Format as phone number with plus sign prefix (e.g., "1234567890" -> "+1234567890", extracts digits and adds + prefix)
            - 'id': Convert to integer as int64 if whole number, or keep as float64 if has decimals for manual inspection (e.g., 123456.0 -> 123456, 1234.56 -> 1234.56)
    
    Returns:
        A Series with transformed numeric values. Returns float64 for 'standardize' and 'format'. 
        Returns int64 (Int64 nullable) for 'id' if all values are whole numbers, or float64 if any have decimals. 
        Returns object (string) for 'percentage', 'money', and 'phone' transformations.
    
    Example:
        >>> df['price'] = fix_numeric_values(df['price'], 'standardize')  # Convert "$1,000" -> 1000.0
        >>> df['price'] = fix_numeric_values(df['price'], 'money')  # Format as "$1,000.00"
    """
    print(f"\n[FIX_NUMERIC_VALUES] Applying transformation: '{transformation}'")
    print(f"  Column dtype: {column.dtype}")
    print(f"  Total values: {len(column)}, Non-null: {column.notna().sum()}, Null: {column.isna().sum()}")
    
    try: 
        # Create a copy to avoid modifying the original
        result = column.copy()
        
        # Helper function to extract numeric value from string
        def extract_numeric(value):
            """Extract numeric value from string, handling currency, percentages, commas, etc."""
            if pd.isna(value):
                return np.nan
            
            # If already numeric, return as is
            if pd.api.types.is_number(value):
                return float(value)
            
            # Convert to string and clean
            value_str = str(value).strip()
            if not value_str or value_str.lower() in ['nan', 'none', 'null', '']:
                return np.nan
            
            # Remove currency symbols ($, €, £, etc.)
            value_str = re.sub(r'[$€£¥₹]', '', value_str)
            
            # Handle percentages - if ends with %, divide by 100
            is_percentage = value_str.endswith('%')
            if is_percentage:
                value_str = value_str.rstrip('%').strip()
            
            # Remove commas and other formatting characters
            value_str = re.sub(r'[,\s]', '', value_str)
            
            # Try to convert to float
            try:
                numeric_value = float(value_str)
                # If it was a percentage, convert from percentage to decimal
                if is_percentage:
                    numeric_value = numeric_value / 100.0
                return numeric_value
            except (ValueError, TypeError):
                # If conversion fails, try to extract first number found
                numbers = re.findall(r'-?\d+\.?\d*', value_str)
                if numbers:
                    try:
                        return float(numbers[0])
                    except (ValueError, TypeError):
                        pass
                return np.nan
        
        # Step 1: Convert all values to numeric (handling strings)
        if column.dtype in ['int64', 'float64', 'Int64', 'Float64']:
            # Already numeric, convert to float
            print(f"  → Column is already numeric, converting to float...")
            result = result.astype(float)
            print(f"  ✓ Converted {result.notna().sum()} values to numeric")
        elif column.dtype in ['object', 'string']:
            # Extract numeric values from strings
            print(f"  → Extracting numeric values from strings (removing currency symbols, commas, percentages, etc.)...")
            result = result.apply(extract_numeric)
            result = pd.to_numeric(result, errors='coerce')
            extracted_count = result.notna().sum()
            print(f"  ✓ Successfully extracted {extracted_count} out of {len(column)} numeric values")
        else:
            print(f'  ⚠ WARNING: Column dtype "{column.dtype}" may not contain numeric values. Attempting conversion...')
            result = pd.to_numeric(result, errors='coerce')
            converted_count = result.notna().sum()
            print(f"  ✓ Converted {converted_count} out of {len(column)} values to numeric")
        
        # Step 2: Apply transformation
        transformation = transformation.lower()
        
        if transformation == 'standardize':
            # Return as float64 numeric values (no formatting)
            print(f"  ✓ Standardized to float64 (pure numeric values)")
            final_result = result.astype('float64')
        elif transformation == 'format':
            # Return as float64 numeric values (round to 2 decimals)
            print(f"  ✓ Formatted to float64 with 2 decimal places")
            final_result = result.round(2).astype('float64')
        elif transformation == 'percentage':
            # Convert to percentage format as string (object type)
            print(f"  ✓ Formatting as percentage strings (e.g., '50.00%')")
            final_result = result.apply(lambda x: f'{x:.2%}' if pd.notna(x) else '')
            final_result = final_result.astype('object')
        elif transformation == 'money':
            # Format as currency with dollar sign as string (object type)
            print(f"  ✓ Formatting as currency strings (e.g., '$1,000.00')")
            final_result = result.apply(lambda x: f'${x:,.2f}' if pd.notna(x) else '')
            final_result = final_result.astype('object')
        elif transformation == 'phone':
            # Format as phone number string with plus sign prefix (object type)
            print(f"  → Formatting as phone numbers...")
            def format_phone(value):
                """Format phone number to international format: +1234567890"""
                if pd.isna(value) or np.isnan(value):
                    return ''
                
                # Convert to string and extract only digits
                value_str = str(value).strip()
                if not value_str:
                    return ''
                
                # Extract all digits
                digits = re.sub(r'\D', '', value_str)
                
                if not digits:
                    return ''
                
                # Format with plus sign prefix
                # If already starts with +, remove it first
                if value_str.startswith('+'):
                    # Already has plus, just extract digits and add plus back
                    return f"+{digits}"
                else:
                    # Add plus sign prefix
                    return f"+{digits}"
            
            final_result = result.apply(format_phone)
            final_result = final_result.astype('object')
            print(f"  ✓ Formatted phone numbers (e.g., '+1234567890')")
        elif transformation == 'id':
            # Convert to integer as int64, but preserve values with decimals for manual inspection
            print(f"  → Converting to ID format (preserving decimals for inspection)...")
            def convert_to_id(value):
                if pd.isna(value) or np.isnan(value):
                    return np.nan
                # Check if value has decimal places (not a whole number)
                # Use a small epsilon to handle floating point precision issues
                if abs(value - int(value)) > 1e-10:
                    # Has decimals, keep as float64 for manual inspection
                    return float(value)
                else:
                    # Whole number, convert to integer
                    return int(value)
            
            final_result = result.apply(convert_to_id)
            # Check if any values have decimals (not whole numbers)
            has_decimals = final_result.apply(lambda x: pd.notna(x) and abs(x - int(x)) > 1e-10 if pd.notna(x) else False).any()
            if has_decimals:
                # Some values have decimals, return as float64 to preserve them
                print(f"  ✓ Some values have decimals - returning as float64 for manual inspection")
                final_result = final_result.astype('float64')
            else:
                # All whole numbers, return as nullable int64
                print(f"  ✓ All values are whole numbers - returning as int64")
                final_result = final_result.astype('Int64')
        else:
            print(f'  ⚠ WARNING: Unknown transformation "{transformation}". Supported: standardize, format, percentage, money, phone, id')
            print(f"  → Returning original column unchanged\n")
            return column
        
        # Show sample of transformed values
        sample = final_result.dropna().head(5).tolist()
        if sample:
            print(f"  Sample transformed values: {sample}")
        print(f"  Final dtype: {final_result.dtype}")
        print(f"  ✓ Transformation complete\n")
        return final_result
    
    except Exception as e:
        print(f'  ✗ ERROR: Failed to fix numeric values: {e}')
        print(f"  → Returning original column\n")
        return column  # Return original on error