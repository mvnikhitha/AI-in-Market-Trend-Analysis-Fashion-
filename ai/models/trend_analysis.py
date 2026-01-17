# /Users/mvnikhitha/Desktop/Kalainayam/ai/models/trend_analyzer.py
"""
Fashion Retail Trend Analyzer
Analyzes Fashion_Retail_Sales.csv to extract market trends
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from collections import Counter
import os

class TrendAnalyzer:
    def __init__(self, csv_path=None):
        """Initialize with path to Fashion_Retail_Sales.csv"""
        if csv_path is None:
            # Default path relative to this file
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            csv_path = os.path.join(base_dir, 'ai', 'data', 'Fashion_Retail_Sales.csv')
        
        self.csv_path = csv_path
        self.df = None
        self.load_data()
    
    def load_data(self):
        """Load and preprocess the CSV data"""
        try:
            self.df = pd.read_csv(self.csv_path)
            # Convert date column
            self.df['Date Purchase'] = pd.to_datetime(self.df['Date Purchase'], format='%d-%m-%Y')
            print(f"✓ Loaded {len(self.df)} fashion records")
        except Exception as e:
            print(f"✗ Error loading data: {e}")
            raise
    
    def get_top_items(self, limit=10):
        """Get top selling items by frequency"""
        item_counts = self.df['Item Purchased'].value_counts().head(limit)
        return [{
            'item': item,
            'count': int(count),
            'percentage': round(count / len(self.df) * 100, 2)
        } for item, count in item_counts.items()]
    
    def get_price_analysis(self):
        """Analyze pricing trends"""
        return {
            'avgPrice': round(self.df['Purchase Amount (USD)'].mean(), 2),
            'minPrice': int(self.df['Purchase Amount (USD)'].min()),
            'maxPrice': int(self.df['Purchase Amount (USD)'].max()),
            'medianPrice': int(self.df['Purchase Amount (USD)'].median()),
            'stdDeviation': round(self.df['Purchase Amount (USD)'].std(), 2)
        }
    
    def get_rating_analysis(self):
        """Analyze customer satisfaction ratings"""
        ratings = self.df['Review Rating'].dropna()
        if len(ratings) == 0:
            return {'avgRating': 0, 'totalReviews': 0}
        
        return {
            'avgRating': round(ratings.mean(), 2),
            'totalReviews': int(len(ratings)),
            'ratedPercentage': round(len(ratings) / len(self.df) * 100, 2),
            'distribution': {
                'excellent': int((ratings >= 4.0).sum()),
                'good': int(((ratings >= 3.0) & (ratings < 4.0)).sum()),
                'average': int(((ratings >= 2.0) & (ratings < 3.0)).sum()),
                'poor': int((ratings < 2.0).sum())
            }
        }
    
    def get_payment_trends(self):
        """Analyze payment method preferences"""
        payment_counts = self.df['Payment Method'].value_counts()
        total = len(self.df)
        return [{
            'method': method,
            'count': int(count),
            'percentage': round(count / total * 100, 2)
        } for method, count in payment_counts.items()]
    
    def get_temporal_trends(self, days=28):
        """Analyze sales trends over time"""
        if self.df is None or len(self.df) == 0:
            return []
        
        # Get date range
        end_date = self.df['Date Purchase'].max()
        start_date = end_date - timedelta(days=days)
        
        # Filter data
        recent = self.df[self.df['Date Purchase'] >= start_date]
        
        # Group by date and aggregate
        daily = recent.groupby(recent['Date Purchase'].dt.date).agg({
            'Purchase Amount (USD)': ['sum', 'count', 'mean']
        }).reset_index()
        
        result = []
        for _, row in daily.iterrows():
            result.append({
                'date': row['Date Purchase'].isoformat(),
                'totalSales': round(float(row[('Purchase Amount (USD)', 'sum')]), 2),
                'transactions': int(row[('Purchase Amount (USD)', 'count')]),
                'avgTransactionValue': round(float(row[('Purchase Amount (USD)', 'mean')]), 2)
            })
        
        return sorted(result, key=lambda x: x['date'])
    
    def get_item_recommendations(self, limit=5):
        """Get items with best average ratings"""
        item_ratings = self.df[self.df['Review Rating'].notna()].groupby('Item Purchased').agg({
            'Review Rating': ['mean', 'count']
        }).reset_index()
        
        item_ratings.columns = ['Item', 'AvgRating', 'Count']
        # Filter items with at least 2 reviews
        item_ratings = item_ratings[item_ratings['Count'] >= 2]
        item_ratings = item_ratings.sort_values('AvgRating', ascending=False).head(limit)
        
        return [{
            'item': row['Item'],
            'avgRating': round(float(row['AvgRating']), 2),
            'reviewCount': int(row['Count'])
        } for _, row in item_ratings.iterrows()]
    
    def generate_fashion_insights(self):
        """Generate comprehensive fashion insights"""
        top_items = self.get_top_items(5)
        
        # Map items to fashion styles
        style_mapping = {
            'Jacket': 'Structured Tailoring',
            'Blazer': 'Formal Wear',
            'Jeans': 'Casual Wear',
            'Dress': 'Occasion Wear',
            'Tunic': 'Casual Wear',
            'Trousers': 'Formal Wear',
            'T-shirt': 'Basic Essentials',
            'Shoes': 'Footwear',
            'Boots': 'Footwear',
            'Loafers': 'Footwear',
            'Trench Coat': 'Outerwear',
            'Sweater': 'Knitwear',
            'Leggings': 'Basics',
            'Shorts': 'Casual Wear'
        }
        
        styles = {}
        for item_data in top_items:
            item_name = item_data['item']
            # Find matching style
            style = next((style for key, style in style_mapping.items() if key in item_name), 'Fashion Item')
            if style not in styles:
                styles[style] = {'count': 0, 'percentage': 0}
            styles[style]['count'] += item_data['count']
        
        # Calculate percentages
        total_items = sum(s['count'] for s in styles.values())
        for style in styles:
            styles[style]['percentage'] = round(styles[style]['count'] / total_items * 100, 2)
        
        # Extract fabrics from top items (heuristic)
        fabric_hints = {
            'Jeans': 'Denim',
            'Leather': 'Leather',
            'Wool': 'Wool',
            'Silk': 'Silk Satin',
            'Cotton': 'Pima Cotton',
            'Knit': 'Rib Knit'
        }
        
        trending_fabrics = ['Denim', 'Cotton Blend', 'Rib Knit', 'Linen Blend', 'Technical Jersey']
        
        return {
            'topItems': top_items,
            'styles': styles,
            'fabrics': trending_fabrics,
            'priceAnalysis': self.get_price_analysis(),
            'ratingAnalysis': self.get_rating_analysis()
        }


# Convenience function to get trends
def analyze_trends():
    """Quick function to get all trends"""
    analyzer = TrendAnalyzer()
    return {
        'topItems': analyzer.get_top_items(),
        'priceAnalysis': analyzer.get_price_analysis(),
        'ratingAnalysis': analyzer.get_rating_analysis(),
        'paymentTrends': analyzer.get_payment_trends(),
        'temporalTrends': analyzer.get_temporal_trends(28),
        'recommendations': analyzer.get_item_recommendations(),
        'insights': analyzer.generate_fashion_insights()
    }