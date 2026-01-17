"""Kalainayam AI Module"""

# Import from trend_analysis (or trend_analyzer - both point to same code)
try:
    from .models.trend_analyzer import TrendAnalyzer, analyze_trends
except ImportError:
    from .models.trend_analysis import TrendAnalyzer, analyze_trends

from .models.color_analyzer import ColorAnalyzer
from .pipelines.data_loader import DataLoader

__all__ = ['TrendAnalyzer', 'analyze_trends', 'ColorAnalyzer', 'DataLoader']