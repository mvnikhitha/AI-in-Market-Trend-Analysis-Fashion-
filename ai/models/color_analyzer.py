# /Users/mvnikhitha/Desktop/Kalainayam/ai/models/color_analyzer.py
"""
Fashion Color Trend Analyzer
Derives color trends from item types
"""

class ColorAnalyzer:
    """Analyzes fashion colors based on trends"""
    
    # Color palette based on item categories
    COLOR_TRENDS = {
        'formal': [
            {'hex': '#4a0e1b', 'name': 'Deep Burgundy', 'mood': 'Sophisticated'},
            {'hex': '#1b1b1b', 'name': 'Black', 'mood': 'Classic'},
            {'hex': '#2d3142', 'name': 'Navy', 'mood': 'Elegant'}
        ],
        'casual': [
            {'hex': '#7b7b7b', 'name': 'Charcoal', 'mood': 'Contemporary'},
            {'hex': '#f7e9e6', 'name': 'Cream', 'mood': 'Neutral'},
            {'hex': '#5a6f7d', 'name': 'Blue-Grey', 'mood': 'Calm'}
        ],
        'fashion_forward': [
            {'hex': '#b33b4a', 'name': 'Wine Red', 'mood': 'Bold'},
            {'hex': '#c9a15b', 'name': 'Soft Gold', 'mood': 'Luxe'},
            {'hex': '#7b1127', 'name': 'Maroon', 'mood': 'Powerful'}
        ],
        'seasonal': {
            'spring': ['#f7e9e6', '#c9a15b', '#d4a5a5'],
            'summer': ['#f7e9e6', '#b3d9e8', '#f4d47f'],
            'autumn': ['#4a0e1b', '#c9a15b', '#8b6f47'],
            'winter': ['#4a0e1b', '#1b1b1b', '#b3d9e8']
        }
    }
    
    @staticmethod
    def get_palette_for_season(season='spring'):
        """Get color palette for a season"""
        seasonal_colors = ColorAnalyzer.COLOR_TRENDS['seasonal'].get(season, ColorAnalyzer.COLOR_TRENDS['seasonal']['spring'])
        return [
            {'hex': color, 'name': f'{season.title()} Palette Color'} 
            for color in seasonal_colors
        ]
    
    @staticmethod
    def get_palette_for_style(style='fashion_forward'):
        """Get color palette for a style"""
        palette = ColorAnalyzer.COLOR_TRENDS.get(style, ColorAnalyzer.COLOR_TRENDS['fashion_forward'])
        return palette
    
    @staticmethod
    def trending_colors():
        """Get current trending colors"""
        return ColorAnalyzer.COLOR_TRENDS['fashion_forward']