# src/data/country_mapping.py
import pandas as pd
import numpy as np
import pycountry
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

class CountryMapper:
    def __init__(self):
        # Manual mappings for common variations
        def __init__(self):
            self.manual_map = {
                'USA': 'USA', 'United States': 'USA', 'United States of America': 'USA',
                'Korea, Rep.': 'KOR', 'South Korea': 'KOR',
                'Czech Republic': 'CZE', 'Czechia': 'CZE',
                'Russia': 'RUS', 'Russian Federation': 'RUS',
                'Iran': 'IRN', 'Iran, Islamic Rep.': 'IRN',
                'Venezuela': 'VEN', 'Venezuela, RB': 'VEN',
                'Bolivia': 'BOL', 'Vietnam': 'VNM', 'Viet Nam': 'VNM',
                'Tanzania': 'TZA', 'Syria': 'SYR', 'Syrian Arab Republic': 'SYR',
                'Laos': 'LAO', 'Moldova': 'MDA',
                'Egypt, Arab Rep.': 'EGY', 'Egypt': 'EGY',
                'Yemen, Rep.': 'YEM', 'Yemen': 'YEM',
                'Congo, Dem. Rep.': 'COD', 'Congo, Rep.': 'COG',
                'Hong Kong SAR, China': 'HKG', 'Hong Kong': 'HKG',
                'Macao SAR, China': 'MAC', 'Macau': 'MAC',
                'West Bank and Gaza': 'PSE', 'Palestine': 'PSE',
                'Slovak Republic': 'SVK', 'Slovakia': 'SVK',
                'Türkiye': 'TUR', 'Turkey': 'TUR',
            }
            
    def get_iso3(self, country_name):
        """Convert country name to ISO3 code"""
        if pd.isna(country_name):
            return None
        
        country_name = str(country_name).strip()
        
        # Check manual map first
        if country_name in self.manual_map:
            return self.manual_map[country_name]
        
        # Try pycountry lookup
        try:
            country = pycountry.countries.search_fuzzy(country_name)[0]
            return country.alpha_3
        except:
            print(f"Warning: Could not map '{country_name}'")
            return None
    
    def create_mapping_table(self, country_names):
        """Create a DataFrame of country name -> ISO3"""
        unique_names = list(set(country_names))
        mappings = [(name, self.get_iso3(name)) for name in unique_names]
        return pd.DataFrame(mappings, columns=['country_name', 'iso3'])

# Usage
mapper = CountryMapper()