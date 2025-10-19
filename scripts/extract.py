#!/usr/bin/env python3
"""
Data extraction module for this project.
Handles reading, cleaning, and preparing data from CSV sources.
All logic in extract_data_source() function.
"""

import pandas as pd
import os
from typing import Dict, Any, Optional, Union, List
from datetime import datetime


def extract_data_source(source_config: Dict[str, Any]) -> pd.DataFrame:
    # ========================================================================
    # STEP 1: Parse Configuration
    # ========================================================================
    source_type = source_config.get('type', '').lower()
    filename = source_config.get('filename', '')
    base_path = source_config.get('base_path', '../data')
    prepare_records = source_config.get('prepare', False)
    get_summary = source_config.get('get_summary', False)
    
    # Validate source type
    if source_type not in ['disasters', 'hdi']:
        print(f"✗ Unknown source type: {source_type}")
        print(f"   Supported types: 'disasters', 'hdi'")
        return None
    
    # ========================================================================
    # STEP 2: Set Default Filenames
    # ========================================================================
    if not filename:
        if source_type == 'disasters':
            filename = 'EMDATCSV.csv'
        elif source_type == 'hdi':
            filename = 'hdi_data_transformed.csv'
    
    # ========================================================================
    # STEP 3: Resolve File Path
    # ========================================================================
    if not os.path.isabs(base_path):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        base_path = os.path.join(script_dir, base_path)
        base_path = os.path.normpath(base_path)
    
    csv_path = os.path.join(base_path, filename)
    
    # ========================================================================
    # STEP 4: Read CSV File
    # ========================================================================
    print(f"Extracting {source_type.upper()} data...")
    print(f"  File: {csv_path}")
    
    if not os.path.exists(csv_path):
        print(f"  ✗ File not found!\n")
        return None
    
    try:
        df = pd.read_csv(csv_path)
        print(f"  ✓ Loaded {len(df):,} records\n")
    except Exception as e:
        print(f"  ✗ Error reading file: {e}\n")
        return None
    
    # ========================================================================
    # STEP 5: Return Summary if Requested
    # ========================================================================
    if get_summary:
        summary = {
            'name': source_type.capitalize(),
            'rows': len(df),
            'columns': len(df.columns),
            'column_names': list(df.columns),
            'memory_usage': f"{df.memory_usage(deep=True).sum() / 1024**2:.2f} MB",
            'null_counts': df.isnull().sum().to_dict()
        }
        return summary
    
    # ========================================================================
    # STEP 6: Prepare Records if Requested
    # ========================================================================
    if prepare_records:
        print(f"Preparing {len(df):,} {source_type} records...")
        
        if source_type == 'disasters':
            # Prepare disaster records
            records = []
            for _, row in df.iterrows():
                record = {
                    'disNo': row.get('DisNo.'),
                    'iso': row.get('ISO'),
                    'country': row.get('Country'),
                    'region': row.get('Region'),
                    'subregion': row.get('Subregion'),
                    'disasterGroup': row.get('Disaster Group'),
                    'disasterType': row.get('Disaster Type'),
                    'disasterSubtype': row.get('Disaster Subtype'),
                    'eventName': row.get('Event Name'),
                    'location': row.get('Location'),
                    'riverBasin': row.get('River Basin'),
                    'startYear': int(row['Start Year']) if pd.notna(row.get('Start Year')) else None,
                    'startMonth': int(row['Start Month']) if pd.notna(row.get('Start Month')) else None,
                    'startDay': int(row['Start Day']) if pd.notna(row.get('Start Day')) else None,
                    'endYear': int(row['End Year']) if pd.notna(row.get('End Year')) else None,
                    'endMonth': int(row['End Month']) if pd.notna(row.get('End Month')) else None,
                    'endDay': int(row['End Day']) if pd.notna(row.get('End Day')) else None,
                    'totalDeaths': int(row['Total Deaths']) if pd.notna(row.get('Total Deaths')) else None,
                    'injured': int(row['No. Injured']) if pd.notna(row.get('No. Injured')) else None,
                    'affected': int(row['No. Affected']) if pd.notna(row.get('No. Affected')) else None,
                    'homeless': int(row['No. Homeless']) if pd.notna(row.get('No. Homeless')) else None,
                    'totalAffected': int(row['Total Affected']) if pd.notna(row.get('Total Affected')) else None,
                    'totalDamage': float(row["Total Damage ('000 US$)"]) if pd.notna(row.get("Total Damage ('000 US$)")) else None,
                    'magnitude': float(row['Magnitude']) if pd.notna(row.get('Magnitude')) else None,
                    'magnitudeScale': row.get('Magnitude Scale'),
                    'latitude': float(row['Latitude']) if pd.notna(row.get('Latitude')) else None,
                    'longitude': float(row['Longitude']) if pd.notna(row.get('Longitude')) else None,
                }
                records.append(record)
            
            print(f"  ✓ Prepared {len(records):,} records\n")
            return records
        
        elif source_type == 'hdi':
            # Prepare HDI records
            records = []
            for _, row in df.iterrows():
                record = {
                    'iso': row.get('ISO'),
                    'country': row.get('country'),
                    'year': int(row['year']) if pd.notna(row.get('year')) else None,
                    'region': row.get('region'),
                    'hdiCode': row.get('hdicode'),
                    'hdiRank2023': int(row['hdi_rank_2023']) if pd.notna(row.get('hdi_rank_2023')) else None,
                    'hdi': float(row['hdi']) if pd.notna(row.get('hdi')) else None,
                    'le': float(row['le']) if pd.notna(row.get('le')) else None,
                    'le_f': float(row['le_f']) if pd.notna(row.get('le_f')) else None,
                    'le_m': float(row['le_m']) if pd.notna(row.get('le_m')) else None,
                    'gnipc': float(row['gnipc']) if pd.notna(row.get('gnipc')) else None,
                    'gni_pc_m': float(row['gni_pc_m']) if pd.notna(row.get('gni_pc_m')) else None,
                    'gni_pc_f': float(row['gni_pc_f']) if pd.notna(row.get('gni_pc_f')) else None,
                    'mys': float(row['mys']) if pd.notna(row.get('mys')) else None,
                    'mys_m': float(row['mys_m']) if pd.notna(row.get('mys_m')) else None,
                    'mys_f': float(row['mys_f']) if pd.notna(row.get('mys_f')) else None,
                    'eys': float(row['eys']) if pd.notna(row.get('eys')) else None,
                    'eys_m': float(row['eys_m']) if pd.notna(row.get('eys_m')) else None,
                    'eys_f': float(row['eys_f']) if pd.notna(row.get('eys_f')) else None,
                    'gii': float(row['gii']) if pd.notna(row.get('gii')) else None,
                    'gii_rank': int(row['gii_rank']) if pd.notna(row.get('gii_rank')) else None,
                    'mmr': float(row['mmr']) if pd.notna(row.get('mmr')) else None,
                    'abr': float(row['abr']) if pd.notna(row.get('abr')) else None,
                    'pop_total': float(row['pop_total']) if pd.notna(row.get('pop_total')) else None,
                    'co2_prod': float(row['co2_prod']) if pd.notna(row.get('co2_prod')) else None,
                    'ineq_edu': float(row['ineq_edu']) if pd.notna(row.get('ineq_edu')) else None,
                    'ineq_inc': float(row['ineq_inc']) if pd.notna(row.get('ineq_inc')) else None,
                    'ineq_le': float(row['ineq_le']) if pd.notna(row.get('ineq_le')) else None,
                }
                records.append(record)
            
            print(f"  ✓ Prepared {len(records):,} records\n")
            return records
    
    # ========================================================================
    # STEP 7: Return Raw DataFrame (Default)
    # ========================================================================
    return df


def main():
    """Main execution function for testing extraction."""
    print("=" * 70)
    print("DATA EXTRACTION TEST")
    print("=" * 70)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    print("Testing extract_data_source() function with different configurations:\n")
    
    # Test 1: Extract raw disasters DataFrame
    print("1. Extract raw disasters DataFrame:")
    config1 = {'type': 'disasters', 'base_path': '../data'}
    disasters_df = extract_data_source(config1)
    if disasters_df is not None:
        print(f"   ✓ Got DataFrame with {len(disasters_df):,} rows\n")
    
    # Test 2: Extract and prepare disaster records
    print("2. Extract and prepare disaster records:")
    config2 = {'type': 'disasters', 'base_path': '../data', 'prepare': True}
    disaster_records = extract_data_source(config2)
    if disaster_records is not None:
        print(f"   ✓ Got {len(disaster_records):,} prepared records")
        print(f"   Sample record keys: {list(disaster_records[0].keys())[:5]}...\n")
    
    # Test 3: Extract disasters with summary
    print("3. Extract disasters with summary:")
    config3 = {'type': 'disasters', 'base_path': '../data', 'get_summary': True}
    summary = extract_data_source(config3)
    if summary is not None:
        print(f"   ✓ Summary:")
        print(f"      Rows: {summary['rows']:,}")
        print(f"      Columns: {summary['columns']}")
        print(f"      Memory: {summary['memory_usage']}\n")
    
    # Test 4: Extract raw HDI DataFrame
    print("4. Extract raw HDI DataFrame:")
    config4 = {'type': 'hdi', 'base_path': '../data'}
    hdi_df = extract_data_source(config4)
    if hdi_df is not None:
        print(f"   ✓ Got DataFrame with {len(hdi_df):,} rows\n")
    
    # Test 5: Extract and prepare HDI records
    print("5. Extract and prepare HDI records:")
    config5 = {'type': 'hdi', 'base_path': '../data', 'prepare': True}
    hdi_records = extract_data_source(config5)
    if hdi_records is not None:
        print(f"   ✓ Got {len(hdi_records):,} prepared records")
        print(f"   Sample record keys: {list(hdi_records[0].keys())[:5]}...\n")
    
    # Test 6: Extract HDI with summary
    print("6. Extract HDI with summary:")
    config6 = {'type': 'hdi', 'base_path': '../data', 'get_summary': True}
    summary = extract_data_source(config6)
    if summary is not None:
        print(f"   ✓ Summary:")
        print(f"      Rows: {summary['rows']:,}")
        print(f"      Columns: {summary['columns']}")
        print(f"      Memory: {summary['memory_usage']}\n")
    
    # Test 7: Invalid source type
    print("7. Test invalid source type:")
    config7 = {'type': 'invalid_type', 'base_path': '../data'}
    result = extract_data_source(config7)
    print()
    
    print("=" * 70)
    print("✓ EXTRACTION TEST COMPLETE!")
    print("=" * 70)
    print("\nThe extract_data_source() function supports:")
    print("  - type: 'disasters' or 'hdi' (required)")
    print("  - filename: CSV filename (optional, uses defaults)")
    print("  - base_path: Base data directory (optional, default: '../data')")
    print("  - prepare: True to get prepared records (default: False)")
    print("  - get_summary: True to get summary stats (default: False)")
    print("\nExample usage:")
    print("  config = {'type': 'disasters', 'prepare': True}")
    print("  records = extract_data_source(config)")


if __name__ == "__main__":
    main()