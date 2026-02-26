import pandas as pd
import re

def sanitize_special_characters(df, exclude_cols=None):
    """
    Removes or replaces special characters from string fields.
    Keeps only alphanumeric, spaces, and basic punctuation.
    
    Args:
        df (pandas.DataFrame): Input DataFrame
        exclude_cols (list): List of column names to exclude from sanitization
        
    Returns:
        pandas.DataFrame: DataFrame with sanitized special characters
    """
    if exclude_cols is None:
        exclude_cols = []
    
    def clean_text(text):
        if pd.isna(text):
            return text
        # Remove special characters but keep letters, numbers, spaces, and basic punctuation
        return re.sub(r'[^a-zA-Z0-9\s\-\.\,\'\"]', '', str(text))
    
    # Apply to all object (string) columns EXCEPT excluded ones
    sanitized_columns = []
    for col in df.select_dtypes(include=['object']).columns:
        if col not in exclude_cols:
            df[col] = df[col].apply(clean_text)
            sanitized_columns.append(col)
    
    print(f"  Sanitized special characters in columns: {sanitized_columns}")
    if exclude_cols:
        print(f"  Excluded columns from sanitization: {exclude_cols}")
    return df