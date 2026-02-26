import pytest
import pandas as pd
import os
import sys

# Add the project root to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import functions with CORRECT filenames (NO func_ prefix)
from functions.remove_duplicate_records import remove_duplicate_records
from functions.trim_whitespace_fields import trim_whitespace_fields
from functions.fill_missing_values import fill_missing_values
from functions.standardize_date_formats import standardize_date_formats
from functions.sanitize_special_characters import sanitize_special_characters


class TestRemoveDuplicates:
    def test_remove_duplicates(self):
        """Test that duplicate rows are removed"""
        test_data = {'A': [1, 2, 2, 3], 'B': ['x', 'y', 'y', 'z']}
        df = pd.DataFrame(test_data)
        
        result = remove_duplicate_records(df)
        assert len(result) == 3  # Should remove 1 duplicate
        
    def test_no_duplicates(self):
        """Test that data with no duplicates remains unchanged"""
        test_data = {'A': [1, 2, 3], 'B': ['x', 'y', 'z']}
        df = pd.DataFrame(test_data)
        
        result = remove_duplicate_records(df)
        assert len(result) == 3


class TestTrimWhitespace:
    def test_trim_whitespace(self):
        """Test that leading/trailing whitespace is removed"""
        test_data = {'Name': ['  John  ', 'Mary ', ' Bob'], 'Age': [25, 30, 35]}
        df = pd.DataFrame(test_data)
        
        result = trim_whitespace_fields(df)
        assert result['Name'][0] == 'John'
        assert result['Name'][1] == 'Mary'
        assert result['Name'][2] == 'Bob'
    
    def test_whitespace_with_empty_strings(self):
        """Test whitespace trimming with empty strings"""
        test_data = {'Name': ['  ', 'Mary', '']}
        df = pd.DataFrame(test_data)
        
        result = trim_whitespace_fields(df)
        assert result['Name'][0] == ''
        assert result['Name'][1] == 'Mary'


class TestFillMissingValues:
    def test_fill_numeric_missing(self):
        """Test that numeric missing values are filled with mean"""
        test_data = {'A': [1, 2, None, 4], 'B': [5, 6, 7, 8]}
        df = pd.DataFrame(test_data)
        
        result = fill_missing_values(df)
        assert result['A'].isnull().sum() == 0
        
    def test_fill_categorical_missing(self):
        """Test that categorical missing values are filled with mode"""
        test_data = {'Name': ['John', None, 'John', 'Bob']}
        df = pd.DataFrame(test_data)
        
        result = fill_missing_values(df)
        assert result['Name'].isnull().sum() == 0
        assert result['Name'][1] == 'John'  # mode
    
    def test_fill_all_missing(self):
        """Test filling when all values in a column are missing"""
        test_data = {'A': [None, None, None]}
        df = pd.DataFrame(test_data)
        
        result = fill_missing_values(df)
        assert result['A'].isnull().sum() == 0


class TestStandardizeDates:
    def test_standardize_dates(self):
        """Test that dates are standardized to YYYY-MM-DD format"""
        test_data = {'join_date': ['01/15/2023', '02/20/2023', '03/25/2023']}
        df = pd.DataFrame(test_data)
        
        result = standardize_date_formats(df)
        # All dates should be in YYYY-MM-DD format
        assert result['join_date'][0] == '2023-01-15'
        assert result['join_date'][1] == '2023-02-20'
        assert result['join_date'][2] == '2023-03-25'
    
    def test_date_column_detection(self):
        """Test that function detects date columns by name"""
        test_data = {
            'join_date': ['01/15/2023', '02/20/2023'],
            'name': ['John', 'Jane']
        }
        df = pd.DataFrame(test_data)
        
        result = standardize_date_formats(df)
        # join_date should be standardized
        assert result['join_date'][0] == '2023-01-15'
        # name should remain unchanged
        assert result['name'][0] == 'John'


class TestSanitizeSpecialCharacters:
    def test_sanitize_special_chars(self):
        """Test that special characters are removed from text"""
        test_data = {'Text': ['Hello@World!', 'Test#123$', 'Normal']}
        df = pd.DataFrame(test_data)
        
        result = sanitize_special_characters(df)
        assert result['Text'][0] == 'HelloWorld'
        assert result['Text'][1] == 'Test123'
        assert result['Text'][2] == 'Normal'
    
    def test_exclude_columns(self):
        """Test that excluded columns (like email) are not sanitized"""
        test_data = {
            'Name': ['John@Doe', 'Jane#Smith'],
            'Email': ['john@email.com', 'jane@email.com']
        }
        df = pd.DataFrame(test_data)
        
        result = sanitize_special_characters(df, exclude_cols=['Email'])
        assert result['Name'][0] == 'JohnDoe'
        assert result['Email'][0] == 'john@email.com'  # Should keep @
    
    def test_preserve_basic_punctuation(self):
        """Test that basic punctuation is preserved"""
        test_data = {'Text': ['Hello, World!', 'Test-123', 'Name.O\'Connor']}
        df = pd.DataFrame(test_data)
        
        result = sanitize_special_characters(df)
        assert 'Hello' in result['Text'][0]
        assert 'World' in result['Text'][0]
        assert 'Test-123' in result['Text'][1]