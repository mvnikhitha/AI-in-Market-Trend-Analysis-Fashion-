"""
Kalainayam Backend Server - Simplified
AI-powered trend analysis for fashion retail
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import os
import sys
import pandas as pd
import numpy as np

app = Flask(__name__)
CORS(app)

app.config['DEBUG'] = True
app.config['JSON_SORT_KEYS'] = False

# Global analyzer
analyzer_data = None

def load_analyzer():
    """Load and analyze the CSV data"""
    global analyzer_data
    
    try:
        csv_path = os.path.join(os.path.dirname(__file__), '..', 'ai', 'data', 'Fashion_Retail_Sales.csv')
        
        df = pd.read_csv(csv_path)
        
        # Rename columns for easier access
        df.columns = ['Customer ID', 'Item Purchased', 'Purchase Amount', 'Date', 'Review Rating', 'Payment Method']
        
        # Convert types
        df['Purchase Amount'] = pd.to_numeric(df['Purchase Amount'], errors='coerce')
        df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y', errors='coerce')
        df['Review Rating'] = pd.to_numeric(df['Review Rating'], errors='coerce')
        
        # Remove rows with NaN in critical columns
        df_clean = df.dropna(subset=['Purchase Amount', 'Date'])
        
        # Calculate stats
        top_items = df_clean['Item Purchased'].value_counts().head(10)
        
        analyzer_data = {
            'df': df_clean,
            'top_items': [{
                'item': item,
                'count': int(count),
                'percentage': round(count / len(df_clean) * 100, 2)
            } for item, count in top_items.items()],
            'price_analysis': {
                'avgPrice': float(df_clean['Purchase Amount'].mean()),
                'medianPrice': float(df_clean['Purchase Amount'].median()),
                'minPrice': float(df_clean['Purchase Amount'].min()),
                'maxPrice': float(df_clean['Purchase Amount'].max()),
                'stdDeviation': float(df_clean['Purchase Amount'].std())
            },
            'total_records': len(df_clean),
            'unique_items': df_clean['Item Purchased'].nunique(),
            'unique_customers': df_clean['Customer ID'].nunique(),
            'date_range': {
                'start': df_clean['Date'].min().isoformat(),
                'end': df_clean['Date'].max().isoformat()
            }
        }
        
        print(f"✓ Analyzer loaded with {len(df_clean)} records")
        return True
        
    except Exception as e:
        print(f"✗ Error loading analyzer: {e}")
        return False

# Load on startup
if load_analyzer():
    print("✓ AI analyzer ready")
else:
    print("⚠ Running in demo mode")

# ===== API Routes =====

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'aiEnabled': analyzer_data is not None
    }), 200

@app.route('/api/trends/detailed', methods=['GET'])
def get_detailed_trends():
    """Get comprehensive trend analysis"""
    if analyzer_data is None:
        return jsonify({'error': 'Data not loaded'}), 503
    
    df = analyzer_data['df']
    
    # Rating analysis
    excellent = len(df[df['Review Rating'] >= 4.5])
    good = len(df[(df['Review Rating'] >= 3.5) & (df['Review Rating'] < 4.5)])
    average = len(df[(df['Review Rating'] >= 2.5) & (df['Review Rating'] < 3.5)])
    poor = len(df[df['Review Rating'] < 2.5])
    
    # Style categories
    style_mapping = {
        'Casual': ['T-Shirt', 'T-shirt', 'Jeans', 'Shorts', 'Casual Jacket', 'Sneakers'],
        'Formal': ['Dress Shirt', 'Trousers', 'Blazer', 'Formal Dress'],
        'Athletic': ['Athletic Shoes', 'Sports Bra', 'Running Shorts', 'Yoga Pants'],
        'Accessories': ['Sunglasses', 'Hat', 'Belt', 'Scarf', 'Watch', 'Handbag'],
        'Footwear': ['Boots', 'Sandals', 'Loafers', 'Heels', 'Flats', 'Flip-Flops'],
        'Outerwear': ['Winter Coat', 'Cardigan', 'Hoodie', 'Rain Jacket', 'Sweater', 'Jacket', 'Trench Coat', 'Poncho']
    }
    
    def get_style(item):
        for category, items in style_mapping.items():
            if item in items:
                return category
        return 'Other'
    
    df['Style'] = df['Item Purchased'].apply(get_style)
    styles = df.groupby('Style').agg({
        'Purchase Amount': ['mean', 'count'],
        'Review Rating': 'mean'
    })
    
    styles_data = {}
    for style in styles.index:
        styles_data[style] = {
            'percentage': round(styles.loc[style, ('Purchase Amount', 'count')] / len(df) * 100, 1),
            'avgPrice': round(styles.loc[style, ('Purchase Amount', 'mean')], 2),
            'avgRating': round(styles.loc[style, ('Review Rating', 'mean')], 2)
        }
    
    # Temporal trends
    max_date = df['Date'].max()
    start_date = max_date - timedelta(days=27)
    df_28 = df[(df['Date'] >= start_date) & (df['Date'] <= max_date)]
    
    daily = df_28.groupby('Date').agg({
        'Purchase Amount': 'sum',
        'Customer ID': 'count'
    }).rename(columns={'Purchase Amount': 'totalSales', 'Customer ID': 'transactions'})
    
    temporal = [{
        'date': idx.isoformat(),
        'totalSales': float(row['totalSales']),
        'transactions': int(row['transactions'])
    } for idx, row in daily.iterrows()]
    
    # Payment methods
    payments = df['Payment Method'].value_counts()
    payment_data = []
    for method, count in payments.items():
        revenue = df[df['Payment Method'] == method]['Purchase Amount'].sum()
        payment_data.append({
            'method': method,
            'count': int(count),
            'percentage': round(count / len(df) * 100, 1),
            'revenue': float(revenue),
            'avgPerTransaction': float(revenue / count)
        })
    
    return jsonify({
        'status': 'success',
        'data': {
            'topItems': analyzer_data['top_items'],
            'insights': {
                'topItems': analyzer_data['top_items'],
                'styles': styles_data,
                'priceAnalysis': analyzer_data['price_analysis'],
                'ratingAnalysis': {
                    'avgRating': round(df['Review Rating'].mean(), 2),
                    'excellent': excellent,
                    'good': good,
                    'average': average,
                    'poor': poor,
                    'distribution': {
                        'excellent': excellent,
                        'good': good,
                        'average': average,
                        'poor': poor
                    }
                }
            },
            'temporalTrends': temporal,
            'paymentMethods': payment_data,
            'overview': {
                'totalRecords': analyzer_data['total_records'],
                'uniqueItems': analyzer_data['unique_items'],
                'uniqueCustomers': analyzer_data['unique_customers'],
                'dateRange': analyzer_data['date_range'],
                'totalRevenue': float(df['Purchase Amount'].sum()),
                'avgTransaction': float(df['Purchase Amount'].mean())
            }
        },
        'timestamp': datetime.now().isoformat()
    }), 200

@app.route('/api/suggestions', methods=['POST'])
def api_suggestions():
    """Generate collection suggestions using womens clothing dataset"""
    try:
        from ai.models.collection_recommender import CollectionRecommender
    except ImportError as e:
        print(f"⚠ CollectionRecommender import failed: {e}")
        return jsonify({'status': 'error', 'message': 'Recommender module not available'}), 503

    # Parse request payload FIRST
    payload = request.get_json() or {}
    season = payload.get('season', 'spring')
    audience = payload.get('audience', 'women')
    price = payload.get('price', 'mid')
    focus = payload.get('focus', 'tailoring')

    try:
        # Initialize recommender and generate suggestions
        rec = CollectionRecommender()
        suggestions = rec.generate_suggestions(
            season=season,
            audience=audience,
            price=price,
            focus=focus,
            top_k=3
        )
        
        return jsonify({
            'status': 'success',
            'suggestions': suggestions,
            'parameters': {'season': season, 'audience': audience, 'price': price, 'focus': focus}
        }), 200
        
    except Exception as e:
        print(f"✗ Error generating suggestions: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500
    
@app.route('/api/style-insights', methods=['GET'])
def get_style_insights():
    """Get style insights from womens clothing analysis"""
    try:
        import traceback
        
        womens_csv = os.path.join(os.path.dirname(__file__), '..', 'ai', 'data', 'Womens Clothing E-Commerce Reviews.csv')
        print(f"📖 Loading CSV from: {womens_csv}")
        
        # Load womens data
        df = pd.read_csv(womens_csv, low_memory=False)
        print(f"✓ Loaded {len(df)} rows")
        
        # Normalize columns
        df.columns = [c.strip() for c in df.columns]
        
        # Convert numeric columns
        numeric_cols = ['Rating', 'Recommended IND', 'Positive Feedback Count', 'Age']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        df = df[df['Clothing ID'].notna()].copy()
        print(f"✓ After cleaning: {len(df)} rows")
        
        # Top classes by review count
        top_classes = df['Class Name'].value_counts().head(5)
        print(f"✓ Top classes: {list(top_classes.index)}")
        
        # Trending classes
        trending = df['Class Name'].value_counts().head(5)
        trending_data = []
        for class_name, count in trending.items():
            avg_rating = float(df[df['Class Name'] == class_name]['Rating'].mean())
            trending_data.append({
                'class': str(class_name),
                'reviews': int(count),
                'avg_rating': round(avg_rating, 2)
            })
        print(f"✓ Trending data created: {len(trending_data)} items")
        
        # Satisfaction metrics (top rated)
        class_ratings = df.groupby('Class Name').agg({
            'Rating': ['mean', 'count'],
            'Recommended IND': lambda x: (x.sum() / len(x) * 100) if len(x) > 0 else 0
        }).round(2)
        
        # Filter classes with at least 10 reviews
        class_ratings = class_ratings[class_ratings[('Rating', 'count')] >= 10]
        class_ratings = class_ratings.nlargest(5, ('Rating', 'mean'))
        
        top_rated = []
        for class_name in class_ratings.index:
            top_rated.append({
                'class': str(class_name),
                'rating': float(class_ratings.loc[class_name, ('Rating', 'mean')]),
                'recommendation_rate': float(class_ratings.loc[class_name, ('Recommended IND', '')])
            })
        print(f"✓ Top rated styles: {len(top_rated)} items")
        
        # Summary stats
        response_data = {
            'status': 'success',
            'insights': {
                'dataset_stats': {
                    'total_reviews': int(len(df)),
                    'unique_products': int(df['Clothing ID'].nunique()),
                    'unique_classes': int(df['Class Name'].nunique()),
                    'avg_rating': round(float(df['Rating'].mean()), 2),
                    'recommendation_rate': round(float((df['Recommended IND'].sum() / len(df) * 100)), 1),
                    'age_range': f"{int(df['Age'].min())} - {int(df['Age'].max())}"
                },
                'trending_styles': trending_data,
                'top_rated_styles': top_rated
            },
            'timestamp': datetime.now().isoformat()
        }
        
        print(f"✓ Response ready: {len(response_data)} keys")
        return jsonify(response_data), 200
        
    except Exception as e:
        error_msg = f"✗ Error: {str(e)}\n{traceback.format_exc()}"
        print(error_msg)
        return jsonify({
            'status': 'error', 
            'message': str(e),
            'type': type(e).__name__
        }), 500
    
    
@app.route('/', methods=['GET'])
def index():
    return jsonify({
        'name': 'Kalainayam API',
        'status': 'running',
        'aiEnabled': analyzer_data is not None
    }), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"\n🎨 Starting Kalainayam on port {port}")
    app.run(host='0.0.0.0', port=port, debug=True)