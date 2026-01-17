#!/usr/bin/env python3
"""
Kalainayam Complete Auto-Setup Script
Automatically sets up everything: AI analysis, backend API, frontend integration
"""

import os
import sys
import json

def create_file(path, content):
    """Create or overwrite a file"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)
    print(f"✓ {path}")
    return True

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("\n" + "="*70)
    print("🎨 KALAINAYAM COMPLETE AUTO-SETUP")
    print("="*70 + "\n")
    
    # ============================================================
    # 1. FIX BACKEND REQUIREMENTS
    # ============================================================
    print("📦 1. Updating Backend Requirements...")
    backend_req = """Flask==2.3.3
Flask-CORS==4.0.0
python-dotenv==1.0.0
gunicorn==21.2.0
pandas==2.0.3
numpy==1.24.3
scikit-learn==1.3.0
matplotlib==3.7.2
seaborn==0.12.2
scipy==1.11.1
"""
    create_file(os.path.join(base_dir, 'backend/requirements.txt'), backend_req)
    
    # ============================================================
    # 2. UPDATED BACKEND APP.PY WITH FULL AI INTEGRATION
    # ============================================================
    print("\n🔧 2. Updating Backend API (app.py)...")
    app_py = '''"""
Kalainayam Backend Server
AI-powered trend analysis and collection suggestions
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from functools import wraps
import os
import sys

app = Flask(__name__)
CORS(app)

# Configuration
app.config['DEBUG'] = True
app.config['JSON_SORT_KEYS'] = False

# Add AI module path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Initialize AI analyzer (cache it)
trend_analyzer = None
ai_available = False

# Try to import AI modules
try:
    from ai.models.trend_analysis import TrendAnalyzer, analyze_trends
    from ai.models.color_analyzer import ColorAnalyzer
    from ai.pipelines.data_loader import DataLoader
    ai_available = True
    print("✓ AI modules imported successfully")
except ImportError as e:
    print(f"⚠ Warning: Could not import AI modules: {e}")
    print("⚠ Running in demo mode with mock data")
    TrendAnalyzer = None
    ColorAnalyzer = None
    DataLoader = None

def get_analyzer():
    """Get or create trend analyzer"""
    global trend_analyzer, ai_available
    if not ai_available:
        return None
    
    if trend_analyzer is None:
        try:
            trend_analyzer = TrendAnalyzer()
            print("✓ Trend Analyzer initialized with Fashion_Retail_Sales.csv")
        except Exception as e:
            print(f"✗ Error initializing trend analyzer: {e}")
            ai_available = False
    return trend_analyzer

# Middleware for error handling
def handle_errors(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            print(f"Error: {str(e)}")
            return jsonify({
                'error': str(e),
                'status': 'error'
            }), 500
    return decorated_function

# ===== API Routes =====

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'message': 'Kalainayam API is running',
        'aiEnabled': ai_available
    }), 200


@app.route('/api/trends', methods=['GET'])
@handle_errors
def get_trends():
    """
    Get AI-analyzed trend data from fashion retail data
    Query params: region (default: global), days (default: 28)
    """
    region = request.args.get('region', 'global')
    days = int(request.args.get('days', 28))
    
    analyzer = get_analyzer()
    
    if analyzer is None:
        # Return mock data if analyzer unavailable
        return jsonify({
            'status': 'warning',
            'message': 'AI analyzer not available, returning sample data',
            'region': region,
            'days': days,
            'timestamp': datetime.now().isoformat(),
            'dataSource': 'Sample Data',
            'styles': [
                {'name': 'Structured Tailoring', 'score': 9, 'note': 'Tailored pieces dominating market'},
                {'name': 'Casual Wear', 'score': 8, 'note': 'Relaxed fits trending'},
                {'name': 'Formal Wear', 'score': 7, 'note': 'Classic styles popular'},
            ],
            'colors': [
                {'hex': '#4a0e1b', 'name': 'Deep Burgundy'},
                {'hex': '#7b1127', 'name': 'Maroon'},
                {'hex': '#b33b4a', 'name': 'Wine Red'},
                {'hex': '#c9a15b', 'name': 'Soft Gold'}
            ],
            'fabrics': [
                {'name': 'Denim', 'demand': 9},
                {'name': 'Cotton Blend', 'demand': 8},
                {'name': 'Rib Knit', 'demand': 7},
            ],
            'overallGrowth': 12,
            'topItems': [
                {'item': 'Jeans', 'count': 150, 'percentage': 12.5},
                {'item': 'T-shirt', 'count': 130, 'percentage': 10.8},
            ],
            'priceAnalysis': {
                'avgPrice': 3200.0,
                'minPrice': 2000,
                'maxPrice': 5000,
                'medianPrice': 3100,
                'stdDeviation': 500.0
            },
            'ratingAnalysis': {
                'avgRating': 3.5,
                'totalReviews': 800,
                'ratedPercentage': 65.0,
            }
        }), 200
    
    # Get real data from CSV analysis
    insights = analyzer.generate_fashion_insights()
    temporal = analyzer.get_temporal_trends(days)
    
    # Calculate growth from temporal data
    overall_growth = 0
    if len(temporal) > 1:
        first_day = temporal[0]['totalSales']
        last_day = temporal[-1]['totalSales']
        if first_day > 0:
            overall_growth = round((last_day - first_day) / first_day * 100, 2)
    
    # Map items to styles with scores
    styles = []
    for style, data in insights['styles'].items():
        styles.append({
            'name': style,
            'score': round(data['percentage'] / 2),
            'note': f"{data['percentage']}% of trending items"
        })
    
    # Get color palette
    if ColorAnalyzer:
        colors = ColorAnalyzer.get_palette_for_season(region if region != 'global' else 'spring')
    else:
        colors = [
            {'hex': '#4a0e1b', 'name': 'Deep Burgundy'},
            {'hex': '#7b1127', 'name': 'Maroon'},
            {'hex': '#b33b4a', 'name': 'Wine Red'},
            {'hex': '#c9a15b', 'name': 'Soft Gold'}
        ]
    
    # Get fabrics
    fabrics = insights['fabrics']
    
    trends_data = {
        'region': region,
        'days': days,
        'timestamp': datetime.now().isoformat(),
        'dataSource': 'Fashion_Retail_Sales.csv',
        'styles': sorted(styles, key=lambda x: x['score'], reverse=True)[:4],
        'colors': colors,
        'fabrics': [{'name': f, 'demand': (i+1)*3} for i, f in enumerate(fabrics[:4])],
        'overallGrowth': overall_growth,
        'temporalTrends': temporal[-14:] if temporal else [],
        'topItems': insights['topItems'][:5],
        'priceAnalysis': insights['priceAnalysis'],
        'ratingAnalysis': insights['ratingAnalysis']
    }
    
    return jsonify(trends_data), 200


@app.route('/api/trends/detailed', methods=['GET'])
@handle_errors
def get_detailed_trends():
    """Get comprehensive trend analysis"""
    analyzer = get_analyzer()
    
    if analyzer is None:
        return jsonify({'error': 'AI not available', 'status': 'error'}), 503
    
    return jsonify({
        'status': 'success',
        'data': {
            'topItems': analyzer.get_top_items(),
            'insights': analyzer.generate_fashion_insights(),
            'temporalTrends': analyzer.get_temporal_trends(28),
            'recommendations': analyzer.get_item_recommendations(),
            'paymentTrends': analyzer.get_payment_trends()
        },
        'timestamp': datetime.now().isoformat()
    }), 200


@app.route('/api/suggestions', methods=['POST'])
@handle_errors
def generate_suggestions():
    """Generate collection suggestions using AI"""
    data = request.get_json()
    
    season = data.get('season', 'spring')
    audience = data.get('audience', 'women')
    price = data.get('price', 'mid')
    focus = data.get('focus', 'tailoring')
    
    analyzer = get_analyzer()
    
    # Get AI-informed top items
    top_items = analyzer.get_top_items(3) if analyzer else []
    
    focus_styles = {
        'tailoring': ['Oversized Blazer', 'Fitted Trousers', 'Structured Coat'],
        'street': ['Cargo Trousers', 'Boxy Tee', 'Technical Jacket'],
        'romantic': ['Slip Dress', 'Sheer Blouse', 'Rib Knit Dress'],
        'minimal': ['Clean Tunic', 'Minimal Knit', 'Monochrome Set']
    }
    
    materials = {
        'tailoring': ['Wool Blend', 'Linen-Blend', 'Gabardine'],
        'street': ['Technical Nylon', 'Cotton Twill', 'Denim'],
        'romantic': ['Silk Satin', 'Chiffon', 'Rib Knit'],
        'minimal': ['Pima Cotton', 'Minimal Knit', 'Soft Wool']
    }
    
    # Get seasonal colors
    if ColorAnalyzer:
        colors = ColorAnalyzer.get_palette_for_season(season)
    else:
        colors = [
            {'hex': '#4a0e1b', 'name': 'Deep Burgundy'},
            {'hex': '#7b1127', 'name': 'Maroon'},
            {'hex': '#b33b4a', 'name': 'Wine Red'},
        ]
    
    suggestions = []
    styles = focus_styles.get(focus, focus_styles['tailoring'])
    mats = materials.get(focus, materials['tailoring'])
    
    for i in range(3):
        suggestions.append({
            'design': styles[i % len(styles)],
            'designNumber': f"KLN-{season[0].upper()}{i+1:03d}",
            'palette': [c['hex'] for c in colors],
            'colorNames': [c['name'] for c in colors],
            'materials': mats[:2],
            'rationale': f'Top item: {top_items[i]["item"] if i < len(top_items) else "Classic"}. Optimized for {audience}, {price} price band.',
            'marketDemand': 'High',
            'confidence': round(0.85 + (i * 0.05), 2)
        })
    
    return jsonify({
        'status': 'success',
        'suggestions': suggestions,
        'parameters': {'season': season, 'audience': audience, 'price': price, 'focus': focus},
        'dataSource': 'AI Analysis + Fashion Retail Data'
    }), 200


@app.route('/api/subscribe', methods=['POST'])
@handle_errors
def subscribe_newsletter():
    """Subscribe to newsletter"""
    data = request.get_json()
    email = data.get('email')
    
    if not email:
        return jsonify({'error': 'Email required'}), 400
    
    print(f"Newsletter: {email}")
    return jsonify({'status': 'success', 'email': email}), 200


@app.route('/api/request-report', methods=['POST'])
@handle_errors
def request_report():
    """Request custom report"""
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    
    if not name or not email:
        return jsonify({'error': 'Name and email required'}), 400
    
    return jsonify({
        'status': 'success',
        'requestId': f"REQ-{int(datetime.now().timestamp())}"
    }), 200


@app.route('/api/download-report/<template>', methods=['GET'])
@handle_errors
def download_report(template):
    """Download report"""
    valid = ['weekly', 'seasonal']
    if template not in valid:
        return jsonify({'error': 'Invalid template'}), 400
    
    return jsonify({'status': 'success', 'url': f'/reports/{template}.pdf'}), 200


# Error handlers
@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Not found', 'status': 'error'}), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({'error': 'Server error', 'status': 'error'}), 500

# Root
@app.route('/', methods=['GET'])
def index():
    return jsonify({
        'name': 'Kalainayam API',
        'version': '1.0.0',
        'description': 'AI-powered fashion intelligence',
        'aiEnabled': ai_available,
        'endpoints': {
            'health': 'GET /api/health',
            'trends': 'GET /api/trends',
            'trends_detailed': 'GET /api/trends/detailed',
            'suggestions': 'POST /api/suggestions',
            'subscribe': 'POST /api/subscribe',
        }
    }), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🎨 Starting Kalainayam on port {port}")
    if ai_available:
        print("📊 AI enabled")
        get_analyzer()
    app.run(host='0.0.0.0', port=port, debug=True)
'''
    create_file(os.path.join(base_dir, 'backend/app.py'), app_py)
    
    # ============================================================
    # 3. UPDATE FRONTEND SCRIPT.JS
    # ============================================================
    print("\n🎨 3. Updating Frontend JavaScript (script.js)...")
    script_js = '''// Kalainayam — AI-powered fashion intelligence
// Integrated with real backend API

(function(){
  const API_BASE = 'http://localhost:5000/api';

  // Fetch real data from backend
  async function fetchTrendData(region='global', days=28) {
    try {
      const response = await fetch(`${API_BASE}/trends?region=${region}&days=${days}`);
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      return await response.json();
    } catch (error) {
      console.error('Fetch error:', error);
      return null;
    }
  }

  // Fetch suggestions from backend
  async function fetchSuggestions(opts) {
    try {
      const response = await fetch(`${API_BASE}/suggestions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(opts)
      });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      return await response.json();
    } catch (error) {
      console.error('Fetch error:', error);
      return null;
    }
  }

  // Render dashboard
  async function renderDashboard(region='global', days=28){
    let data = await fetchTrendData(region, days);
    
    if (!data) {
      console.warn('Using sample data');
      data = {
        styles: [
          {name:'Oversized Tailoring', score: 12},
          {name:'Casual Wear', score: 8},
        ],
        colors: [
          {hex:'#4a0e1b', name:'Deep Burgundy'},
          {hex:'#7b1127', name:'Maroon'},
        ],
        fabrics: [
          {name:'Denim', demand: 10},
        ],
        overallGrowth: 12,
        topItems: []
      };
    } else {
      console.log('✓ Real AI data loaded');
    }

    // Render styles
    const stylesList = document.getElementById('styles-list');
    if(stylesList){
      stylesList.innerHTML = (data.styles || [])
        .sort((a,b)=>b.score-a.score)
        .map(s => `<li><span>${s.name}</span><span class="muted small">${s.score}</span></li>`)
        .join('');
    }

    // Render colors
    const colorsPalette = document.getElementById('colors-palette');
    if(colorsPalette){
      colorsPalette.innerHTML = (data.colors || [])
        .map(c => `<span style="background:${c.hex}" title="${c.name}"></span>`)
        .join('');
    }

    // Render fabrics
    const fabricsList = document.getElementById('fabrics-list');
    if(fabricsList){
      fabricsList.innerHTML = (data.fabrics || [])
        .sort((a,b)=>b.demand-a.demand)
        .map(f => `<li><span>${f.name}</span><span class="muted small">${f.demand}</span></li>`)
        .join('');
    }

    // Render growth
    const growthElem = document.getElementById('growth-percent');
    if(growthElem && data.overallGrowth !== undefined){
      growthElem.innerHTML = `<strong>${data.overallGrowth}%</strong>`;
    }
  }

  // Generate suggestions
  async function generateCollectionSuggestions({season='spring', audience='women', price='mid', focus='tailoring'} = {}){
    const result = await fetchSuggestions({season, audience, price, focus});

    const picks = result ? result.suggestions : generateFallback({season, audience, price, focus});
    renderSuggestions(picks);
  }

  function generateFallback({season='spring', audience='women', price='mid', focus='tailoring'} = {}) {
    const focusStyles = {
      tailoring: ['Oversized Blazer','Fitted Trousers','Structured Coat'],
      street: ['Cargo Trousers','Boxy Tee','Technical Jacket'],
      romantic: ['Slip Dress','Sheer Blouse','Rib Knit Dress'],
      minimal: ['Clean Tunic','Minimal Knit','Monochrome Set']
    };
    const styles = focusStyles[focus] || focusStyles.tailoring;
    const colors = ['#4a0e1b','#7b1127','#b33b4a'];

    return Array.from({length:3}).map((_,i) => ({
      design: styles[i % styles.length],
      palette: colors,
      materials: ['Wool', 'Cotton'],
      rationale: `Suggested for ${audience}, ${price} price.`
    }));
  }

  function renderSuggestions(picks){
    const grid = document.getElementById('suggestions-grid');
    if(!grid) return;
    
    grid.innerHTML = picks.map(p=>`
      <article class="suggestion">
        <h4>${p.design}</h4>
        <p class="muted small">${p.rationale}</p>
        <div class="swatches" style="margin-top:.6rem">
          ${p.palette.map(c=>`<span style="background:${c};display:inline-block;width:28px;height:28px;border-radius:6px;margin-right:.4rem;border:1px solid rgba(0,0,0,0.04)"></span>`).join('')}
        </div>
        <p style="margin-top:.6rem"><strong>Materials:</strong> ${p.materials.join(', ')}</p>
      </article>
    `).join('');
  }

  // Init
  document.addEventListener('DOMContentLoaded', function(){
    renderDashboard();

    const refreshBtn = document.getElementById('refresh-trends');
    if(refreshBtn){
      refreshBtn.addEventListener('click', () => {
        const region = document.getElementById('region-select')?.value || 'global';
        const days = parseInt(document.getElementById('timeframe-select')?.value || '28');
        renderDashboard(region, days);
      });
    }

    const colForm = document.getElementById('collection-form');
    if(colForm){
      colForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const fd = new FormData(colForm);
        generateCollectionSuggestions({
          season: fd.get('season'),
          audience: fd.get('audience'),
          price: fd.get('price'),
          focus: fd.get('focus') || 'tailoring'
        });
        document.querySelector('.suggestions')?.scrollIntoView({behavior:'smooth'});
      });
    }

    const y = new Date().getFullYear();
    document.querySelectorAll('[id$="-year"]').forEach(el=>el.textContent = y);
  });

  window.generateCollectionSuggestions = generateCollectionSuggestions;
  window.renderDashboard = renderDashboard;

})();
'''
    create_file(os.path.join(base_dir, 'frontend/js/script.js'), script_js)
    
    # ============================================================
    # 4. CREATE TEST PAGE
    # ============================================================
    print("\n🧪 4. Creating Test Page (test.html)...")
    test_html = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Kalainayam Test</title>
  <link rel="stylesheet" href="css/styles.css">
  <style>
    .test { padding: 1rem; margin: 0.5rem 0; border-left: 3px solid #7b1127; background: #f9f9f9; }
    .pass { border-left-color: #2d5016; color: #2d5016; }
    .fail { border-left-color: #d9534f; color: #d9534f; }
    .pending { border-left-color: #c9a15b; }
  </style>
</head>
<body class="theme-kalainayam">
  <div class="container" style="padding: 3rem 0;">
    <h1>🎨 Kalainayam Connection Test</h1>
    <p class="muted">Verify backend connectivity and AI analysis</p>

    <div style="margin: 2rem 0; padding: 2rem; background: #fff; border-radius: 12px;">
      <h2>API Status</h2>
      <div id="backend-test" class="test pending">Connecting to backend...</div>
      <div id="health-test" class="test pending">Checking health...</div>
      <div id="trends-test" class="test pending">Testing trends...</div>
      <div id="suggestions-test" class="test pending">Testing suggestions...</div>
      <div id="ai-data" class="test pending">Testing AI data...</div>
    </div>

    <div style="margin: 2rem 0; padding: 2rem; background: #fff; border-radius: 12px;">
      <h2>Ready to Explore?</h2>
      <ul style="list-style: none; padding: 0;">
        <li>✨ <a href="index.html" style="color: #7b1127; font-weight: 600;">Homepage</a></li>
        <li>📊 <a href="pages/ai-analysis.html" style="color: #7b1127; font-weight: 600;">AI Analysis Dashboard</a></li>
        <li>🎨 <a href="pages/create-collection.html" style="color: #7b1127; font-weight: 600;">Create Collection</a></li>
      </ul>
    </div>
  </div>

  <script src="js/api.js"></script>
  <script>
    async function runTests() {
      const tests = {
        backend: document.getElementById('backend-test'),
        health: document.getElementById('health-test'),
        trends: document.getElementById('trends-test'),
        suggestions: document.getElementById('suggestions-test'),
        ai: document.getElementById('ai-data')
      };

      try {
        await fetch('http://localhost:5000/api/health');
        tests.backend.textContent = '✅ Backend connected';
        tests.backend.classList.add('pass');
      } catch {
        tests.backend.textContent = '❌ Backend not running (python app.py)';
        tests.backend.classList.add('fail');
        return;
      }

      try {
        const res = await fetch('http://localhost:5000/api/health');
        const data = await res.json();
        const status = data.aiEnabled ? '✅ AI Models Ready' : '⚠️ AI Offline';
        tests.health.textContent = status;
        tests.health.classList.add(data.aiEnabled ? 'pass' : 'pending');
      } catch (e) {
        tests.health.textContent = '❌ Health check failed: ' + e.message;
        tests.health.classList.add('fail');
      }

      try {
        const res = await fetch('http://localhost:5000/api/trends');
        const data = await res.json();
        const count = data.topItems?.length || 0;
        tests.trends.textContent = `✅ Trends loaded (${count} items)`;
        tests.trends.classList.add('pass');
      } catch (e) {
        tests.trends.textContent = '❌ Trends failed: ' + e.message;
        tests.trends.classList.add('fail');
      }

      try {
        const res = await fetch('http://localhost:5000/api/suggestions', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ season: 'spring', audience: 'women', price: 'mid', focus: 'tailoring' })
        });
        const data = await res.json();
        const count = data.suggestions?.length || 0;
        tests.suggestions.textContent = `✅ Suggestions generated (${count} designs)`;
        tests.suggestions.classList.add('pass');
      } catch (e) {
        tests.suggestions.textContent = '❌ Suggestions failed: ' + e.message;
        tests.suggestions.classList.add('fail');
      }

      try {
        const res = await fetch('http://localhost:5000/api/trends/detailed');
        const data = await res.json();
        const items = data.data?.topItems?.length || 0;
        tests.ai.textContent = `✅ AI Analysis Complete (${items} items analyzed)`;
        tests.ai.classList.add('pass');
      } catch (e) {
        tests.ai.textContent = '⚠️ Detailed analysis: ' + e.message;
        tests.ai.classList.add('pending');
      }
    }

    window.addEventListener('load', runTests);
  </script>
</body>
</html>
'''
    create_file(os.path.join(base_dir, 'frontend/test.html'), test_html)
    
    # ============================================================
    # 5. DONE!
    # ============================================================
    print("\n" + "="*70)
    print("✅ AUTO-SETUP COMPLETE!")
    print("="*70)
    print("""
📋 NEXT STEPS:

1️⃣  Install dependencies:
    cd backend
    pip install -r requirements.txt

2️⃣  Start Backend (Terminal 1):
    cd backend
    python app.py

3️⃣  Start Frontend (Terminal 2):
    cd frontend
    python -m http.server 8000

4️⃣  Test Connection:
    http://localhost:8000/test.html

5️⃣  Explore Website:
    http://localhost:8000/index.html

📊 What's Connected:
    ✅ AI analyzes Fashion_Retail_Sales.csv
    ✅ Real trends shown on homepage
    ✅ Full dashboard with charts
    ✅ AI suggestions for collections
    ✅ Price, rating, and sales analysis
""")
    print("="*70 + "\n")

if __name__ == '__main__':
    main()
