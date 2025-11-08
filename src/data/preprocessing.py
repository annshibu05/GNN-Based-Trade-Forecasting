# src/data/preprocessing.py
import pandas as pd
import numpy as np
from .loaders import *
from .country_mapping import CountryMapper

class TradeDataPreprocessor:
    def __init__(self, data_dir='data/raw'):
        self.data_dir = data_dir
        self.mapper = CountryMapper()
        
    def load_all_data(self):
        """Load all raw datasets"""
        print("=" * 60)
        print("LOADING ALL DATASETS")
        print("=" * 60)
        
        # Load trade data
        self.trade_df = load_comtrade(
            f'{self.data_dir}/comtrade/TradeData_6_18_2025_13_36_12.csv',
            self.mapper
        )
        
        # Load World Bank indicators
        self.gdp_df = load_world_bank_indicator(
            f'{self.data_dir}/world-bank/API_NY.GDP.MKTP.CD_DS2_en_csv_v2_75934.csv',
            'gdp_usd'
        )
        
        self.pop_df = load_world_bank_indicator(
            f'{self.data_dir}/world-bank/API_SP.POP.TOTL_DS2_en_csv_v2_76034.csv',
            'population'
        )
        
        self.cpi_df = load_world_bank_indicator(
            f'{self.data_dir}/world-bank/API_FP.CPI.TOTL.ZG_DS2_en_csv_v2_73483.csv',
            'cpi'
        )
        
        # Load CEPII
        self.cepii_df = load_cepii(
            f'{self.data_dir}/cepii/dist_cepii.csv',
            self.mapper
        )
        
        # Load RTAs
        self.rta_df = load_rta(
            f'{self.data_dir}/rta/AllRTAs.csv',
            self.mapper
        )
        
        # Load GDELT sentiment (if you have historical)
        try:
            self.gdelt_df = pd.read_csv(f'{self.data_dir}/sentiment/sentiment.csv')
            print(f"Loaded GDELT sentiment: {len(self.gdelt_df)} rows")
        except:
            print("Warning: No GDELT sentiment file found, will skip for now")
            self.gdelt_df = None
        
        print("\n" + "=" * 60)
        print("DATA LOADING COMPLETE")
        print("=" * 60)
    
    def create_node_features(self, year=2022):
        """Create node feature matrix for a given year"""
        print(f"\nCreating node features for year {year}...")
        
        # Merge GDP, population, CPI
        nodes = self.gdp_df[self.gdp_df['year'] == year].copy()
        nodes = nodes.merge(
            self.pop_df[self.pop_df['year'] == year][['iso3', 'population']],
            on='iso3',
            how='outer'
        )
        nodes = nodes.merge(
            self.cpi_df[self.cpi_df['year'] == year][['iso3', 'cpi']],
            on='iso3',
            how='outer'
        )
        
        # Add log transforms
        nodes['gdp_log'] = np.log1p(nodes['gdp_usd'].fillna(0))
        nodes['pop_log'] = np.log1p(nodes['population'].fillna(0))
        
        # Normalize CPI (Z-score)
        nodes['cpi_norm'] = (nodes['cpi'] - nodes['cpi'].mean()) / nodes['cpi'].std()
        nodes['cpi_norm'] = nodes['cpi_norm'].fillna(0)
        
        # Create country_id (sequential integer)
        nodes = nodes.reset_index(drop=True)
        nodes['country_id'] = nodes.index
        
        print(f"Created {len(nodes)} nodes with features")
        
        self.nodes = nodes
        return nodes
    
    def create_edges(self, year=2022):
        """Create edge list with features for a given year"""
        print(f"\nCreating edges for year {year}...")
        
        # Filter trade data to year
        edges = self.trade_df[self.trade_df['year'] == year].copy()
        
        # For multiple monthly records, aggregate to yearly
        edges = edges.groupby(['source_iso3', 'target_iso3', 'hs_code'], as_index=False).agg({
            'trade_value': 'sum',
            'trade_value_log': 'mean'  # Or re-compute: np.log1p(sum)
        })
        
        # Add CEPII features
        edges = edges.merge(
            self.cepii_df,
            on=['source_iso3', 'target_iso3'],
            how='left'
        )
        
        # Add FTA
        edges = edges.merge(
            self.rta_df[['source_iso3', 'target_iso3', 'fta_binary']],
            on=['source_iso3', 'target_iso3'],
            how='left'
        )
        edges['fta_binary'] = edges['fta_binary'].fillna(0).astype(int)
        
        # Add GDELT sentiment (if available)
        if self.gdelt_df is not None:
            # Assuming gdelt_df has: source_iso3, target_iso3, year, month, avg_tone
            gdelt_yearly = self.gdelt_df[self.gdelt_df['year'] == year].groupby(
                ['source_iso3', 'target_iso3'], as_index=False
            )['avg_tone'].mean()
            
            edges = edges.merge(
                gdelt_yearly,
                on=['source_iso3', 'target_iso3'],
                how='left'
            )
            
            # Normalize sentiment from [-10, 10] to [0, 1]
            edges['sentiment_norm'] = (edges['avg_tone'] + 10) / 20
            edges['sentiment_norm'] = edges['sentiment_norm'].fillna(0.5)  # Neutral if missing
        else:
            edges['sentiment_norm'] = 0.5  # Default neutral
        
        # Fill missing values
        edges['distance_km'] = edges['distance_km'].fillna(edges['distance_km'].median())
        edges['distance_log'] = np.log1p(edges['distance_km'])
        edges['shared_border'] = edges['shared_border'].fillna(False).astype(int)
        edges['shared_lang'] = edges['shared_lang'].fillna(False).astype(int)
        
        print(f"Created {len(edges)} edges with features")
        
        self.edges = edges
        return edges
    
    def create_train_mask(self):
        """Create mask for India -> partner edges"""
        india_mask = (self.edges['source_iso3'] == 'IND')
        self.edges['is_india_export'] = india_mask
        
        print(f"India export edges: {india_mask.sum()} out of {len(self.edges)}")
        
        return india_mask
    
    def save_processed_data(self, output_dir='data/processed'):
        """Save processed nodes and edges"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        self.nodes.to_csv(f'{output_dir}/nodes_2022.csv', index=False)
        self.edges.to_csv(f'{output_dir}/edges_2022.csv', index=False)
        
        print(f"\nSaved processed data to {output_dir}/")
        print(f"  - nodes_2022.csv: {len(self.nodes)} rows")
        print(f"  - edges_2022.csv: {len(self.edges)} rows")

# Usage
if __name__ == "__main__":
    preprocessor = TradeDataPreprocessor()
    preprocessor.load_all_data()
    preprocessor.create_node_features(year=2022)
    preprocessor.create_edges(year=2022)
    preprocessor.create_train_mask()
    preprocessor.save_processed_data()