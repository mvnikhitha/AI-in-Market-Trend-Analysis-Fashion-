import os
import pandas as pd
import numpy as np
from typing import List, Dict, Any
from collections import defaultdict

try:
    from .color_analyzer import ColorAnalyzer
except Exception:
    # fallback if relative import fails when module used directly
    from ai.models.color_analyzer import ColorAnalyzer


class CollectionRecommender:
    """
    Lightweight recommender for creating smart collections using
    `ai/data/Womens Clothing E-Commerce Reviews.csv`.
    """

    def __init__(self, csv_path: str = None):
        if csv_path is None:
            base = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            csv_path = os.path.join(base, "ai", "data", "Womens Clothing E-Commerce Reviews.csv")

        self.csv_path = csv_path
        self.df = None
        self.item_stats = None
        self._load()

    def _load(self):
        df = pd.read_csv(self.csv_path, low_memory=False)
        # rename / normalize columns if necessary
        df.columns = [c.strip() for c in df.columns]
        # required columns in this dataset:
        # 'Clothing ID', 'Rating', 'Recommended IND', 'Positive Feedback Count', 'Department Name', 'Class Name'
        # convert types
        for col in ['Rating', 'Recommended IND', 'Positive Feedback Count']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        # keep useful columns and drop rows without Clothing ID
        df = df[df['Clothing ID'].notna()].copy()
        self.df = df

        # build item-level stats
        grp = df.groupby('Clothing ID').agg({
            'Rating': ['mean', 'count'],
            'Recommended IND': 'mean',
            'Positive Feedback Count': 'sum',
            'Department Name': lambda s: s.mode().iat[0] if not s.mode().empty else '',
            'Class Name': lambda s: s.mode().iat[0] if not s.mode().empty else ''
        })
        grp.columns = ['avg_rating', 'review_count', 'recommend_rate', 'positive_feedback', 'department', 'class_name']
        grp = grp.reset_index()

        # score for ranking: combine popularity and quality
        grp['score'] = grp['review_count'] * (grp['avg_rating'].fillna(0) / 5.0) + (grp['positive_feedback'].fillna(0) * 0.05)

        # sort descending
        grp = grp.sort_values('score', ascending=False).reset_index(drop=True)
        self.item_stats = grp

    def get_top_products(self, n: int = 10) -> pd.DataFrame:
        return self.item_stats.head(n)

    def _choose_materials(self, class_name: str, price_band: str) -> List[str]:
        # simple heuristics
        mapping = {
            'Dresses': ['Cotton', 'Silk', 'Polyester'],
            'Tops': ['Cotton', 'Viscose', 'Linen'],
            'Blouses': ['Viscose', 'Silk'],
            'Pants': ['Denim', 'Cotton'],
            'Outerwear': ['Wool Blend', 'Polyester'],
            'Intimates': ['Modal', 'Cotton'],
            'Skirts': ['Cotton', 'Poly Blend'],
            'Knits': ['Wool', 'Acrylic', 'Cotton'],
            'Default': ['Cotton Blend', 'Polyester']
        }
        base = mapping.get(class_name, mapping['Default']).copy()
        if price_band == 'premium':
            base = ['Silk Blend'] + base
        elif price_band == 'budget':
            base = base + ['Polyester']
        return base[:3]

    def _style_candidates(self, focus: str) -> List[str]:
        mapping = {
            'tailoring': ['Dresses', 'Blazers', 'Trousers', 'Outerwear'],
            'street': ['Tops', 'Bottoms', 'Knits', 'Skirts'],
            'romantic': ['Dresses', 'Blouses', 'Skirts'],
            'minimal': ['Tops', 'Trousers', 'Knits']
        }
        return mapping.get(focus, mapping['tailoring'])
    def _audience_context(self, audience: str) -> str:
        """Return audience-specific context for rationale"""
        mapping = {
            'women': 'contemporary women',
            'premium': 'premium/luxury women 30+',
            'petite': 'petite-fit women',
            'plus': 'plus-size women'
        }
        return mapping.get(audience, 'women')
    def generate_suggestions(self,
                             season: str = 'spring',
                             audience: str = 'women',
                             price: str = 'mid',
                             focus: str = 'tailoring',
                             top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Generate `top_k` collection suggestions using item stats and simple heuristics.
        Returns list of dicts with keys:
          - design, designNumber, palette (list of hex), colorNames, materials, rationale, marketDemand, confidence
        """
        if self.item_stats is None:
            self._load()

        candidates = self.item_stats.copy()

        # filter by class_name candidates for focus
        focus_classes = self._style_candidates(focus)
        candidates = candidates[candidates['class_name'].isin(focus_classes)]
        if candidates.empty:
            candidates = self.item_stats.copy()

        # seasonal palette from ColorAnalyzer
        palette = [p['hex'] for p in ColorAnalyzer.get_palette_for_season(season)]

        results = []
        used_classes = set()
        i = 0
        idx = 0
        while i < top_k and idx < len(candidates):
            row = candidates.iloc[idx]
            idx += 1
            class_name = str(row.get('class_name', 'Other')) or 'Other'
            if class_name in used_classes and len(candidates) > top_k:
                continue
            used_classes.add(class_name)

            design_label = f"{class_name} Edit"
            top_review_count = int(row['review_count']) if not np.isnan(row['review_count']) else 0
            avg_rating = float(row['avg_rating']) if not np.isnan(row['avg_rating']) else 0.0

            materials = self._choose_materials(class_name, price)
            audience_ctx = self._audience_context(audience)
            rationale = (
                f"Based on {int(row['review_count'])} reviews (avg rating {avg_rating:.1f}), "
                f"popular in {row['department']} / {class_name}. Optimized for {audience_ctx}, {price} price band."
)

            confidence = min(0.95, 0.6 + (avg_rating / 5.0) * 0.4 + min(0.2, top_review_count / 1000.0))
            market_demand = 'High' if row['score'] >= candidates['score'].quantile(0.75) else 'Moderate'

            suggestion = {
                'design': design_label,
                'designNumber': f"KLN-{season[0].upper()}{i+1:03d}",
                'palette': palette,
                'colorNames': [f"{season.title()} Color {j+1}" for j in range(len(palette))],
                'materials': materials,
                'rationale': rationale,
                'marketDemand': market_demand,
                'confidence': round(confidence, 2),
                'sourceClothingID': int(row['Clothing ID'])
            }
            results.append(suggestion)
            i += 1

        # If not enough candidates, fill with generic designs
        j = 0
        while i < top_k:
            j += 1
            results.append({
                'design': f"Classic {focus.title()} {j}",
                'designNumber': f"KLN-{season[0].upper()}X{j:02d}",
                'palette': palette,
                'colorNames': [f"{season.title()} Color {k+1}" for k in range(len(palette))],
                'materials': self._choose_materials('Default', price),
                'rationale': f"Fallback suggestion for {audience} / {price}",
                'marketDemand': 'Moderate',
                'confidence': 0.5,
                'sourceClothingID': None
            })
            i += 1

        return results


if __name__ == "__main__":
    # quick smoke test
    rec = CollectionRecommender()
    s = rec.generate_suggestions(season='autumn', audience='women', price='premium', focus='tailoring', top_k=3)
    import json
    print(json.dumps(s, indent=2))