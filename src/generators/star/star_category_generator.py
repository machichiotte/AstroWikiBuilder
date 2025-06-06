# src/generators/star/star_category_generator.py

from typing import List, Dict, Optional, Set
from src.models.data_source_star import DataSourceStar
from src.utils.wikipedia.category_parser import parse_categories
import re

class StarCategoryGenerator:
    """
    Classe pour générer les catégories des articles d'étoiles.
    """

    def __init__(self):
        self.predefined_categories: Dict[str, List[str]] = parse_categories()
        self.base_categories: List[str] = ["[[Catégorie:Étoile]]"]

    def _get_constellation_category(self, star: DataSourceStar) -> Optional[str]:
        if (
            star.constellation
            and hasattr(star.constellation, "value")
            and star.constellation.value is not None
        ):
            constellation_name = str(star.constellation.value)
            available_constellations = self.predefined_categories.get("Constellations", [])
            for cat_string in available_constellations:
                match_cat_text = re.search(r"\[\[Catégorie:(.*?)\]\]", cat_string)
                if match_cat_text:
                    text_part = match_cat_text.group(1)
                    if re.search(r"\b" + re.escape(constellation_name) + r"\b", text_part, re.IGNORECASE):
                        return cat_string
        return None

    def _get_spectral_type_category(self, star: DataSourceStar) -> Optional[str]:
        if (
            star.spectral_type
            and hasattr(star.spectral_type, "value")
            and star.spectral_type.value is not None
        ):
            spectral_type = str(star.spectral_type.value)
            available_types = self.predefined_categories.get("Spectral Types", [])
            for cat_string in available_types:
                if spectral_type in cat_string:
                    return cat_string
        return None

    def _get_variable_star_category(self, star: DataSourceStar) -> Optional[str]:
        if hasattr(star, "variable_type") and star.variable_type and getattr(star.variable_type, "value", None):
            variable_type = str(star.variable_type.value)
            available_variables = self.predefined_categories.get("Variable Stars", [])
            for cat_string in available_variables:
                if variable_type in cat_string:
                    return cat_string
        return None

    def generate_categories(self, star: DataSourceStar) -> List[str]:
        categories: Set[str] = set(self.base_categories.copy())

        category_sources = [
            self._get_constellation_category,
            self._get_spectral_type_category,
            self._get_variable_star_category,
        ]

        for source_func in category_sources:
            category = source_func(star)
            if category:
                categories.add(category)

        return sorted(list(categories))
