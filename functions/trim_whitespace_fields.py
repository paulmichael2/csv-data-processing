import pandas as pd

def trim_whitespace_fields(df):
    """
    Trims leading and trailing whitespace from all string fields.
    
    Args:
        df (pandas.DataFrame): Input DataFrame
        
    Returns:
        pandas.DataFrame: DataFrame with trimmed whitespace
    """
    # Apply strip to all object (string) columns
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].str.strip()
    
    print("  Trimmed whitespace from all string fields")
    return df