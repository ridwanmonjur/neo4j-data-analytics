"""
Data transformation module for this project.
"""
import pandas as pd
from typing import List, Dict
from datetime import datetime


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and preprocess raw data.
    
    Args:
        df: Raw DataFrame to be cleaned
        
    Returns:
        Cleaned DataFrame with duplicates removed, missing values handled,
        and data types normalized
    """
    cleaned_df = df.copy()
    
    cleaned_df = cleaned_df.drop_duplicates()
    
    # Handle missing values - fill numeric columns with 0 or appropriate defaults
    numeric_columns = cleaned_df.select_dtypes(include=['float64', 'int64']).columns
    for col in numeric_columns:
        if cleaned_df[col].isna().sum() > 0:
            cleaned_df[col] = cleaned_df[col].fillna(0)
    
    # Strip whitespace from string columns
    string_columns = cleaned_df.select_dtypes(include=['object']).columns
    for col in string_columns:
        if cleaned_df[col].dtype == 'object':
            cleaned_df[col] = cleaned_df[col].astype(str).str.strip()
            # Replace 'nan' string with empty string
            cleaned_df[col] = cleaned_df[col].replace('nan', '')
    
    # Remove rows with critical missing data (e.g., no country or year)
    if 'iso' in cleaned_df.columns:
        cleaned_df = cleaned_df[cleaned_df['iso'].notna() & (cleaned_df['iso'] != '')]
    
    return cleaned_df


def transform_for_graph(df: pd.DataFrame) -> List[Dict]:
    """
    Transform data into graph format for Neo4j.
    
    Converts DataFrame into a list of dictionaries with Neo4j-compatible
    data types, handling NaN values, datetime objects, and numpy types.
    
    Args:
        df: Cleaned DataFrame to be transformed
        
    Returns:
        List of dictionaries ready for Neo4j insertion
    """
    # Convert DataFrame to list of dictionaries
    records = df.to_dict('records')
    
    # Transform each record for Neo4j compatibility
    transformed_records = []
    for record in records:
        transformed = {}
        for key, value in record.items():
            # Handle NaN, None, and empty values
            if pd.isna(value) or value == '' or value == 'nan':
                transformed[key] = None
            # Convert numpy types to Python native types
            elif hasattr(value, 'item'):
                transformed[key] = value.item()
            # Handle datetime objects
            elif isinstance(value, (pd.Timestamp, datetime)):
                transformed[key] = value.isoformat()
            else:
                transformed[key] = value
        
        transformed_records.append(transformed)
    
    return transformed_records


if __name__ == "__main__":
    print("Running data transformation...")
    print("This module provides:")
    print("  - clean_data(df): Clean and preprocess raw data")
    print("  - transform_for_graph(df): Transform data for Neo4j")
    print("\nImport these functions in your loader script.")