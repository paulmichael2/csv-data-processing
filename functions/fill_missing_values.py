import pandas as pd

def fill_missing_values(df):
    """
    Fills missing values - numeric columns with mean, 
    categorical with mode or 'Unknown'.
    
    Args:
        df (pandas.DataFrame): Input DataFrame
        
    Returns:
        pandas.DataFrame: DataFrame with missing values filled
    """
    # Count missing values before
    missing_before = df.isnull().sum().sum()
    
    # Fill numeric columns with mean
    numeric_cols = df.select_dtypes(include=['number']).columns
    for col in numeric_cols:
        mean_val = df[col].mean()
        df[col] = df[col].fillna(mean_val)
    
    # Fill object (string) columns with mode or 'Unknown'
    object_cols = df.select_dtypes(include=['object']).columns
    for col in object_cols:
        if df[col].mode().empty:
            df[col] = df[col].fillna('Unknown')
        else:
            mode_val = df[col].mode()[0]
            df[col] = df[col].fillna(mode_val)
    
    # Fill boolean columns with False
    bool_cols = df.select_dtypes(include=['bool']).columns
    df[bool_cols] = df[bool_cols].fillna(False)
    
    missing_after = df.isnull().sum().sum()
    print(f"  Filled {missing_before - missing_after} missing values")
    return df