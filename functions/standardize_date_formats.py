import pandas as pd

def standardize_date_formats(df):
    """
    Standardizes all date columns to YYYY-MM-DD format.
    
    Args:
        df (pandas.DataFrame): Input DataFrame
        
    Returns:
        pandas.DataFrame: DataFrame with standardized date formats
    """
    date_columns = []
    
    # Identify potential date columns (common names)
    date_keywords = ['date', 'time', 'join', 'created', 'updated']
    potential_date_cols = [col for col in df.columns 
                          if any(keyword in col.lower() for keyword in date_keywords)]
    
    # Also try all object columns
    for col in df.select_dtypes(include=['object']).columns:
        try:
            # Try parsing as date
            parsed = pd.to_datetime(df[col], errors='coerce', dayfirst=False)
            # If successful, format to standard
            if parsed.notna().any():
                df[col] = parsed.dt.strftime('%Y-%m-%d')
                date_columns.append(col)
        except:
            pass  # Not a date column, skip
    
    print(f"  Standardized date formats in columns: {date_columns}")
    return df