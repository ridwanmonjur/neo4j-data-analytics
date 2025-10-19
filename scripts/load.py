#!/usr/bin/env python3
"""
- Four main functions: load_nodes, load_relationships, create_constraints, main
- Checks if data already exists before loading
- Handles batch processing for performance
- Uses extract_data_source() for data extraction
- Uses transform module for data cleaning and graph transformation
"""

from neo4j import GraphDatabase
import pandas as pd
import os
import time
from datetime import datetime
from typing import List, Dict, Optional
from dotenv import load_dotenv

# Import ETL modules
from extract import extract_data_source
from transform import clean_data, transform_for_graph

# Load environment variables from .env file (for local development)
# This will be ignored if running in Docker with environment variables already set
load_dotenv()

# Environment Configuration
# These will use Docker Compose env vars if available, otherwise fall back to .env file
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "ridwan-8-chars")
DATA_PATH = os.getenv("DATA_PATH", "../data")
BATCH_SIZE = int(os.getenv("BATCH_SIZE", "100"))

# Print configuration (for debugging)
print(f"Configuration:")
print(f"  NEO4J_URI: {NEO4J_URI}")
print(f"  NEO4J_USER: {NEO4J_USER}")
print(f"  DATA_PATH: {DATA_PATH}")
print()


def get_driver(uri: str = NEO4J_URI, user: str = NEO4J_USER, password: str = NEO4J_PASSWORD):
    """Create and return a Neo4j driver with connection retry logic."""
    max_retries = 5
    print(f"Connecting to Neo4j at {uri}...")
    
    for i in range(max_retries):
        try:
            driver = GraphDatabase.driver(uri, auth=(user, password))
            driver.verify_connectivity()
            print("✓ Connected to Neo4j successfully!\n")
            return driver
        except Exception as e:
            print(f"Connection attempt {i+1}/{max_retries} failed: {e}")
            if i < max_retries - 1:
                time.sleep(5)
    
    raise Exception("Could not connect to Neo4j after multiple attempts")


def create_constraints(driver):
    """Create constraints and indexes."""
    print("Creating constraints and indexes...")
    
    constraints = [
        {
            'name': 'disaster_id',
            'query': "CREATE CONSTRAINT disaster_id IF NOT EXISTS FOR (d:Disaster) REQUIRE d.disNo IS UNIQUE"
        },
        {
            'name': 'disaster_country_year_idx',
            'query': "CREATE INDEX disaster_country_year IF NOT EXISTS FOR (d:Disaster) ON (d.iso, d.startYear)"
        },
        {
            'name': 'hdi_country_year_idx',
            'query': "CREATE INDEX hdi_country_year IF NOT EXISTS FOR (h:HDI_Record) ON (h.iso, h.year)"
        },
        {
            'name': 'disaster_type_idx',
            'query': "CREATE INDEX disaster_type IF NOT EXISTS FOR (d:Disaster) ON (d.disasterType)"
        }
    ]
    
    with driver.session() as session:
        for constraint in constraints:
            try:
                session.run(constraint['query'])
                print(f"  ✓ {constraint['name']}")
            except Exception as e:
                if "already exists" in str(e).lower() or "equivalent" in str(e).lower():
                    print(f"  ↻ {constraint['name']} (already exists)")
                else:
                    print(f"  ✗ {constraint['name']}: {str(e)[:60]}")
    print()


def load_nodes(driver, nodes: List[Dict], node_type: str, batch_size: int = BATCH_SIZE) -> bool:
    """Load nodes into Neo4j with batch processing."""
    if not nodes:
        print(f"  ✗ No {node_type} nodes to load\n")
        return False
    
    total = len(nodes)
    start_time = time.time()
    
    print(f"Loading {total:,} {node_type} nodes...")
    
    try:
        with driver.session() as session:
            for i in range(0, total, batch_size):
                batch = nodes[i:i+batch_size]
                
                if node_type == 'Disaster':
                    session.execute_write(_insert_disaster_batch, batch)
                elif node_type == 'HDI_Record':
                    session.execute_write(_insert_hdi_batch, batch)
                else:
                    raise ValueError(f"Unknown node type: {node_type}")
                
                progress = min(i+batch_size, total)
                print(f"  Progress: {progress:,}/{total:,} ({progress/total*100:.1f}%)", end='\r')
        
        elapsed = time.time() - start_time
        print(f"\n  ✓ Loaded {total:,} {node_type} nodes in {elapsed:.1f}s\n")
        return True
        
    except Exception as e:
        print(f"\n  ✗ Error loading {node_type} nodes: {e}\n")
        return False


def _insert_disaster_batch(tx, records):
    """Insert a batch of Disaster nodes."""
    query = """
    UNWIND $records AS row
    MERGE (d:Disaster {disNo: row.disNo})
    ON CREATE SET
        d.iso = row.iso,
        d.country = row.country,
        d.region = row.region,
        d.subregion = row.subregion,
        d.disasterGroup = row.disasterGroup,
        d.disasterType = row.disasterType,
        d.disasterSubtype = row.disasterSubtype,
        d.eventName = row.eventName,
        d.location = row.location,
        d.startYear = row.startYear,
        d.startMonth = row.startMonth,
        d.startDay = row.startDay,
        d.endYear = row.endYear,
        d.endMonth = row.endMonth,
        d.endDay = row.endDay,
        d.totalDeaths = row.totalDeaths,
        d.injured = row.injured,
        d.affected = row.affected,
        d.homeless = row.homeless,
        d.totalAffected = row.totalAffected,
        d.totalDamage = row.totalDamage,
        d.magnitude = row.magnitude,
        d.magnitudeScale = row.magnitudeScale,
        d.latitude = row.latitude,
        d.longitude = row.longitude,
        d.riverBasin = row.riverBasin,
        d.createdAt = datetime()
    """
    tx.run(query, records=records)


def _insert_hdi_batch(tx, records):
    """Insert a batch of HDI_Record nodes."""
    query = """
    UNWIND $records AS row
    MERGE (h:HDI_Record {iso: row.iso, year: row.year})
    ON CREATE SET
        h.country = row.country,
        h.region = row.region,
        h.hdiCode = row.hdiCode,
        h.hdiRank2023 = row.hdiRank2023,
        h.hdi = row.hdi,
        h.lifeExpectancy = row.le,
        h.lifeExpectancyFemale = row.le_f,
        h.lifeExpectancyMale = row.le_m,
        h.gniPerCapita = row.gnipc,
        h.gniPerCapitaMale = row.gni_pc_m,
        h.gniPerCapitaFemale = row.gni_pc_f,
        h.meanYearsSchooling = row.mys,
        h.meanYearsSchoolingMale = row.mys_m,
        h.meanYearsSchoolingFemale = row.mys_f,
        h.expectedYearsSchooling = row.eys,
        h.expectedYearsSchoolingMale = row.eys_m,
        h.expectedYearsSchoolingFemale = row.eys_f,
        h.gii = row.gii,
        h.giiRank = row.gii_rank,
        h.mmr = row.mmr,
        h.abr = row.abr,
        h.populationTotal = row.pop_total,
        h.co2Production = row.co2_prod,
        h.inequalityEducation = row.ineq_edu,
        h.inequalityIncome = row.ineq_inc,
        h.inequalityLifeExpectancy = row.ineq_le,
        h.createdAt = datetime()
    """
    tx.run(query, records=records)


def load_relationships(driver, relationship_type: str = 'HAPPENED_IN_COUNTRY_YEAR') -> bool:
    """Create relationships between nodes."""
    print(f"Creating {relationship_type} relationships...")
    
    start_time = time.time()
    
    try:
        with driver.session() as session:
            result = session.run("""
                MATCH (d:Disaster), (h:HDI_Record)
                WHERE d.iso = h.iso AND d.startYear = h.year
                MERGE (d)-[r:HAPPENED_IN_COUNTRY_YEAR]->(h)
                ON CREATE SET r.createdAt = datetime()
                RETURN count(r) as links
            """)
            count = result.single()['links']
            elapsed = time.time() - start_time
            print(f"  ✓ Created {count:,} relationships in {elapsed:.1f}s\n")
            return True
            
    except Exception as e:
        print(f"  ✗ Error creating relationships: {e}\n")
        return False


def check_existing_data(driver) -> Dict[str, int]:
    """Check what data already exists in the database."""
    with driver.session() as session:
        result = session.run("""
            MATCH (n)
            RETURN labels(n)[0] as Type, count(*) as Count
            ORDER BY Count DESC
        """)
        node_counts = {record['Type']: record['Count'] for record in result}
        
        result = session.run("""
            MATCH ()-[r]->()
            RETURN type(r) as Type, count(*) as Count
        """)
        rel_counts = {record['Type']: record['Count'] for record in result}
        
        return {
            'nodes': node_counts,
            'relationships': rel_counts,
            'total_nodes': sum(node_counts.values()),
            'total_relationships': sum(rel_counts.values())
        }


def clear_database(driver, confirm: bool = True) -> bool:
    """Clear all data from database."""
    if confirm:
        response = input("⚠️  This will delete ALL data. Are you sure? (yes/no): ")
        if response.lower() != 'yes':
            print("Aborted.")
            return False
    
    print("\nClearing database...")
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")
        print("✓ Database cleared\n")
    return True


def extract_and_prepare_data(data_type: str, filename: str, base_path: str = DATA_PATH) -> Optional[List[Dict]]:
    """Extract, clean, and transform data using the ETL pipeline."""
    print(f"Extracting and preparing {data_type} data...")
    
    config = {
        'type': data_type,
        'filename': filename,
        'base_path': base_path,
        'prepare': True
    }
    
    records = extract_data_source(config)
    
    if records is None:
        print(f"  ✗ Failed to extract {data_type} data\n")
        return None
    
    print("  Converting to DataFrame...")
    df = pd.DataFrame(records)
    
    print("  Cleaning data...")
    df = clean_data(df)
    print(f"    ✓ Cleaned data: {len(df)} rows remaining")
    
    print("  Transforming data for graph...")
    records = transform_for_graph(df)
    print(f"    ✓ Transformed {len(records)} records for graph\n")
    
    return records


def show_summary(driver):
    """Display database summary and run sample query."""
    print("=" * 70)
    print("DATABASE SUMMARY")
    print("=" * 70)
    
    data_info = check_existing_data(driver)
    
    if data_info['nodes']:
        print("\nNode Counts:")
        for node_type, count in data_info['nodes'].items():
            print(f"  {node_type}: {count:,}")
    else:
        print("\n  ⚠️  Database is empty")
    
    if data_info['relationships']:
        print("\nRelationship Counts:")
        for rel_type, count in data_info['relationships'].items():
            print(f"  {rel_type}: {count:,}")
    
    print("\n" + "=" * 70 + "\n")
    
    if data_info['total_nodes'] > 0 and data_info['total_relationships'] > 0:
        print("=" * 70)
        print("SAMPLE QUERY: Top 5 Deadliest Disasters with HDI Context")
        print("=" * 70 + "\n")
        
        with driver.session() as session:
            result = session.run("""
                MATCH (d:Disaster)-[:HAPPENED_IN_COUNTRY_YEAR]->(h:HDI_Record)
                WHERE d.totalDeaths IS NOT NULL
                RETURN d.country as Country,
                       d.disasterType as Type,
                       d.startYear as Year,
                       d.totalDeaths as Deaths,
                       d.totalAffected as Affected,
                       h.hdi as HDI,
                       h.lifeExpectancy as LifeExp
                ORDER BY d.totalDeaths DESC
                LIMIT 5
            """)
            
            records = list(result)
            if records:
                for i, record in enumerate(records, 1):
                    print(f"{i}. {record['Country']} ({record['Year']}) - {record['Type']}")
                    print(f"   Deaths: {record['Deaths']:,}")
                    if record['Affected']:
                        print(f"   Affected: {record['Affected']:,}")
                    if record['HDI']:
                        print(f"   HDI: {record['HDI']:.3f}, Life Expectancy: {record['LifeExp']:.1f} years")
                    print()


def main():
    """Main execution function."""
    print("=" * 70)
    print("NEO4J DATABASE LOADER")
    print("=" * 70)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    driver = None
    
    try:
        driver = get_driver()
        
        existing_data = check_existing_data(driver)
        
        if existing_data['total_nodes'] > 0:
            print("⚠️  Database already contains data")
            print(f"  Nodes: {existing_data['total_nodes']:,}")
            print(f"  Relationships: {existing_data['total_relationships']:,}")
            print("\nOptions:")
            print("  1. Skip loading (data will be preserved)")
            print("  2. Clear and reload all data")
            choice = input("\nChoose (1/2): ").strip()
            
            if choice == '2':
                if not clear_database(driver, confirm=True):
                    return
            elif choice != '1':
                print("✗ Invalid choice, exiting")
                return
            print()
        
        create_constraints(driver)
        
        disaster_records = extract_and_prepare_data(
            data_type='disasters',
            filename='EMDATCSV.csv',
            base_path=DATA_PATH
        )
        
        hdi_records = extract_and_prepare_data(
            data_type='hdi',
            filename='hdi_data_transformed.csv',
            base_path=DATA_PATH
        )
        
        disasters_loaded = False
        hdi_loaded = False
        
        if disaster_records:
            disasters_loaded = load_nodes(driver, disaster_records, 'Disaster')
        
        if hdi_records:
            hdi_loaded = load_nodes(driver, hdi_records, 'HDI_Record')
        
        if disasters_loaded and hdi_loaded:
            load_relationships(driver)
        
        show_summary(driver)
        
        print("=" * 70)
        print("✓ LOADING COMPLETE!")
        print("=" * 70)
        print("\nAccess your data at:")
        print("  Neo4j Browser: http://localhost:7474")
        print("  NeoDash: http://localhost:5005")
        print(f"\nFinished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        if driver:
            driver.close()
            print("\n✓ Connection closed")


if __name__ == "__main__":
    main()