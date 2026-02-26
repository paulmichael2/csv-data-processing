import pandas as pd

def standardize_date_formats(df):
    """
    Standardizes all date columns to YYYY-MM-DD format.
    """
    date_columns = []
    
    # Common date column names to target
    date_keywords = ['date', 'time', 'join', 'created', 'updated', 'birth']
    
    # Make a copy to avoid modifying original
    df = df.copy()
    
    for col in df.select_dtypes(include=['object']).columns:
        # Check if column name suggests it's a date column
        is_date_column = any(keyword in col.lower() for keyword in date_keywords)
        
        if is_date_column:
            try:
                # Try parsing with multiple formats
                parsed = pd.to_datetime(df[col], errors='coerce', dayfirst=False)
                
                # If we successfully parsed some values, standardize the column
                if parsed.notna().any():
                    df[col] = parsed.dt.strftime('%Y-%m-%d')
                    date_columns.append(col)
            except Exception as e:
                print(f"  Warning: Could not parse date column '{col}': {e}")
                pass
    
    print(f"  Standardized date formats in columns: {date_columns}")
    return df