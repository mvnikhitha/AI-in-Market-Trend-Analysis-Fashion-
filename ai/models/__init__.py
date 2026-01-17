"""AI Models Package"""

try:
    from .trend_analyzer import TrendAnalyzer, analyze_trends
except ImportError:
    from .trend_analysis import TrendAnalyzer, analyze_trends

from .color_analyzer import ColorAnalyzer

__all__ = ['TrendAnalyzer', 'analyze_trends', 'ColorAnalyzer']