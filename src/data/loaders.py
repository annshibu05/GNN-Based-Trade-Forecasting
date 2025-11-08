# src/data/loaders.py
import pandas as pd
import numpy as np
from .country_mapping import CountryMapper

def load_comtrade(file_path, mapper):
    """Load and clean UN Comtrade data"""
    print(f"Loading Comtrade from {file_path}...")
    
    # Load with appropriate encoding
    df = pd.read_csv(file_path, low_memory=False, encoding='latin1')
    
    print(f"Raw shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    
    # Rename columns for consistency
    column_map = {
        'reporterDesc': 'source_country',
        'partnerDesc': 'target_country',
        'refYear': 'year',
        'refMonth': 'month',
        'flowDesc': 'flow',
        'cmdCode': 'hs_code',
        'cmdDesc': 'product_desc',
        'primaryValue': 'trade_value'
    }
    df = df.rename(columns=column_map)
    
    # Map to ISO3
    df['source_iso3'] = df['source_country'].apply(mapper.get_iso3)
    df['target_iso3'] = df['target_country'].apply(mapper.get_iso3)
    
    # Remove rows with unmapped countries
    before = len(df)
    df = df.dropna(subset=['source_iso3', 'target_iso3'])
    print(f"Dropped {before - len(df)} rows with unmapped countries")
    
    # Filter to exports only (imports are just reverse edges)
    df = df[df['flow'] == 'Export'].copy()
    
    # Handle missing trade values
    df['trade_value'] = pd.to_numeric(df['trade_value'], errors='coerce')
    df = df.dropna(subset=['trade_value'])
    df = df[df['trade_value'] > 0]  # Remove zero/negative trade
    
    # Add log transform
    df['trade_value_log'] = np.log1p(df['trade_value'])
    
    # Filter to pharmaceuticals and textiles (optional, can filter later)
    pharma_codes = ['3004', '3001', '3002', '3003', '3005', '3006']
    textile_chapters = [str(i) for i in range(50, 64)]  # HS 50-63
    
    # For now, keep all products (you can filter later by hs_code)
    
    print(f"Cleaned shape: {df.shape}")
    return df

def load_world_bank_indicator(file_path, indicator_name):
    """Load and melt World Bank indicator"""
    print(f"Loading World Bank {indicator_name} from {file_path}...")
    
    # World Bank CSVs have 4 header rows
    df = pd.read_csv(file_path, skiprows=4)
    
    # Columns: Country Name, Country Code, Indicator Name, Indicator Code, 1960, 1961, ..., 2023
    # We want: Country Name, Year, Value
    
    # Get year columns (numeric columns)
    year_cols = [col for col in df.columns if col.isdigit()]
    
    # Melt to long format
    df_long = df.melt(
        id_vars=['Country Name', 'Country Code'],
        value_vars=year_cols,
        var_name='year',
        value_name=indicator_name
    )
    
    df_long['year'] = pd.to_numeric(df_long['year'], errors='coerce')
    df_long[indicator_name] = pd.to_numeric(df_long[indicator_name], errors='coerce')
    
    # Map to ISO3
    mapper = CountryMapper()
    df_long['iso3'] = df_long['Country Name'].apply(mapper.get_iso3)
    df_long = df_long.dropna(subset=['iso3'])
    
    # Select relevant columns
    df_long = df_long[['iso3', 'year', indicator_name]]
    
    print(f"Loaded {indicator_name}: {len(df_long)} rows")
    return df_long

def load_cepii(file_path, mapper):
    """Load CEPII distance data"""
    print(f"Loading CEPII from {file_path}...")
    
    df = pd.read_csv(file_path)
    
    # Typical columns: iso_o, iso_d, dist, distw, contig, comlang_off, ...
    # Keep: iso_o (source), iso_d (target), dist (distance), contig (border), comlang_off (language)
    
    required_cols = ['iso_o', 'iso_d', 'dist', 'contig', 'comlang_off']
    missing = set(required_cols) - set(df.columns)
    if missing:
        print(f"Warning: Missing CEPII columns: {missing}")
    
    # Rename
    df = df.rename(columns={
        'iso_o': 'source_iso3',
        'iso_d': 'target_iso3',
        'dist': 'distance_km',
        'contig': 'shared_border',
        'comlang_off': 'shared_lang'
    })
    
    # Convert boolean columns
    df['shared_border'] = df['shared_border'].astype(bool)
    df['shared_lang'] = df['shared_lang'].astype(bool)
    
    # Log transform distance
    df['distance_log'] = np.log1p(df['distance_km'])
    
    print(f"Loaded CEPII: {len(df)} country pairs")
    return df[['source_iso3', 'target_iso3', 'distance_km', 'distance_log', 'shared_border', 'shared_lang']]

def load_rta(file_path, mapper):
    """Load and parse RTA (Free Trade Agreements)"""
    print(f"Loading RTAs from {file_path}...")
    
    df = pd.read_csv(file_path)
    
    # Typical structure: RTA Name, Date of entry into force, Current signatories
    # Current signatories is a semicolon or comma-separated list
    
    print(f"RTA columns: {df.columns.tolist()}")
    
    # Parse signatories
    all_pairs = []
    
    for idx, row in df.iterrows():
        if pd.notna(row.get('Current signatories')):
            # Split by semicolon or comma
            signatories = str(row['Current signatories']).replace(';', ',').split(',')
            signatories = [s.strip() for s in signatories if s.strip()]
            
            # Map to ISO3
            iso_codes = [mapper.get_iso3(s) for s in signatories]
            iso_codes = [c for c in iso_codes if c is not None]
            
            # Create pairs (directed: all combinations)
            for i in range(len(iso_codes)):
                for j in range(len(iso_codes)):
                    if i != j:
                        all_pairs.append({
                            'source_iso3': iso_codes[i],
                            'target_iso3': iso_codes[j],
                            'rta_name': row.get('RTA Name', 'Unknown'),
                            'fta_binary': 1
                        })
    
    fta_df = pd.DataFrame(all_pairs)
    
    # Remove duplicates (a pair might be in multiple RTAs)
    fta_df = fta_df.drop_duplicates(subset=['source_iso3', 'target_iso3'])
    
    print(f"Loaded {len(fta_df)} FTA pairs from {len(df)} agreements")
    return fta_df[['source_iso3', 'target_iso3', 'fta_binary']]