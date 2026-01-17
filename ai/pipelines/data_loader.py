# /Users/mvnikhitha/Desktop/Kalainayam/ai/pipelines/data_loader.py
"""
Data Loading and Preprocessing Pipeline
"""

import pandas as pd
import os

class DataLoader:
    """Load and preprocess fashion retail data"""
    
    @staticmethod
    def load_fashion_data(csv_path=None):
        """Load Fashion_Retail_Sales.csv"""
        if csv_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            csv_path = os.path.join(base_dir, 'ai', 'data', 'Fashion_Retail_Sales.csv')
        
        df = pd.read_csv(csv_path)
        df['Date Purchase'] = pd.to_datetime(df['Date Purchase'], format='%d-%m-%Y')
        return df
    
    @staticmethod
    def get_summary_stats(df):
        """Get basic summary statistics"""
        return {
            'totalRecords': len(df),
            'dateRange': {
                'start': df['Date Purchase'].min().isoformat(),
                'end': df['Date Purchase'].max().isoformat()
            },
            'uniqueItems': df['Item Purchased'].nunique(),
            'uniqueCustomers': df['Customer Reference ID'].nunique()
        }