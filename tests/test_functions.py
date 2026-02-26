import pytest
import pandas as pd
import os
import sys

# Add the functions directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'functions'))

from functions.func_remove_duplicates import remove_duplicate_records
from functions.func_trim_whitespace import trim_whitespace_fields
from functions.func_fill_missing_values import fill_missing_values
from functions.func_standardize_date_formats import standardize_date_formats
from functions.func_sanitize_special_characters import sanitize_special_characters


class TestRemoveDuplicates:
    def test_remove_duplicates(self):
        # Create test data with duplicates
        test_data = {'A': [1, 2, 2, 3], 'B': ['x', 'y', 'y', 'z']}
        df = pd.DataFrame(test_data)
        
        result = remove_duplicate_records(df)
        assert len(result) == 3  # Should remove 1 duplicate
        
    def test_no_duplicates(self):
        test_data = {'A': [1, 2, 3], 'B': ['x', 'y', 'z']}
        df = pd.DataFrame(test_data)
        
        result = remove_duplicate_records(df)
        assert len(result) == 3


class TestTrimWhitespace:
    def test_trim_whitespace(self):
        test_data = {'Name': ['  John  ', 'Mary ', ' Bob'], 'Age': [25, 30, 35]}
        df = pd.DataFrame(test_data)
        
        result = trim_whitespace_fields(df)
        assert result['Name'][0] == 'John'
        assert result['Name'][1] == 'Mary'
        assert result['Name'][2] == 'Bob'


class TestFillMissingValues:
    def test_fill_numeric_missing(self):
        test_data = {'A': [1, 2, None, 4], 'B': [5, 6, 7, 8]}
        df = pd.DataFrame(test_data)
        
        result = fill_missing_values(df)
        assert result['A'].isnull().sum() == 0
        assert result['A'][2] == 2.33  # mean of 1, 2, 4
        
    def test_fill_categorical_missing(self):
        test_data = {'Name': ['John', None, 'John', 'Bob']}
        df = pd.DataFrame(test_data)
        
        result = fill_missing_values(df)
        assert result['Name'].isnull().sum() == 0
        assert result['Name'][1] == 'John'  # mode


class TestStandardizeDates:
    def test_standardize_dates(self):
        test_data = {'Date': ['01/15/2023', '2023-02-20', '03-25-2023']}
        df = pd.DataFrame(test_data)
        
        result = standardize_date_formats(df)
        # All dates should be in YYYY-MM-DD format
        assert result['Date'][0] == '2023-01-15'
        assert result['Date'][1] == '2023-02-20'


class TestSanitizeSpecialCharacters:
    def test_sanitize_special_chars(self):
        test_data = {'Text': ['Hello@World!', 'Test#123$', 'Normal']}
        df = pd.DataFrame(test_data)
        
        result = sanitize_special_characters(df)
        assert result['Text'][0] == 'HelloWorld'
        assert result['Text'][1] == 'Test123'
        assert result['Text'][2] == 'Normal'
    
    def test_exclude_columns(self):
        test_data = {
            'Name': ['John@Doe', 'Jane#Smith'],
            'Email': ['john@email.com', 'jane@email.com']
        }
        df = pd.DataFrame(test_data)
        
        result = sanitize_special_characters(df, exclude_cols=['Email'])
        assert result['Name'][0] == 'JohnDoe'
        assert result['Email'][0] == 'john@email.com'  # Should keep @