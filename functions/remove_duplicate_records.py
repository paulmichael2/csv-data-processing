import pandas as pd

def remove_duplicate_records(df):
    """
    Removes duplicate records from the DataFrame.
    
    Args:
        df (pandas.DataFrame): Input DataFrame
        
    Returns:
        pandas.DataFrame: DataFrame with duplicates removed
    """
    initial_count = len(df)
    df_cleaned = df.drop_duplicates()
    final_count = len(df_cleaned)
    print(f"  Removed {initial_count - final_count} duplicate records")
    return df_cleaned