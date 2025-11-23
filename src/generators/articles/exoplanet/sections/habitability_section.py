# src/generators/articles/exoplanet/sections/habitability_section.py

from src.models.entities.exoplanet_entity import Exoplanet
from src.utils.formatters.article_formatter import ArticleFormatter


class HabitabilitySection:
    """Génère la section habitabilité pour les articles d'exoplanètes."""

    def __init__(self, article_util: ArticleFormatter):
        self.article_util = article_util

    def _get_value_or_none_if_nan(self, data_point) -> float | int | None:
        """Extrait la valeur d'un data point ou retourne None si NaN."""
        if data_point and hasattr(data_point, "value") and data_point.value is not None:
            value = data_point.value
            if isinstance(value, str) and value.lower() == "nan":
                return None
            return value
        return None

    def generate(self, exoplanet: Exoplanet) -> str:
        """Génère la section sur l'habitabilité basée sur la température d'équilibre."""
        section = "== Habitabilité ==\n"

        temp = self._get_value_or_none_if_nan(exoplanet.pl_temperature)

        if temp is None:
            section += "Les conditions d'habitabilité de cette exoplanète ne sont pas déterminées ou ne sont pas connues.\n"
            return section

        try:
            temp_val = float(temp)
        except (ValueError, TypeError):
            section += "Les conditions d'habitabilité de cette exoplanète ne sont pas déterminées ou ne sont pas connues.\n"
            return section

        temp_str = self.article_util.format_uncertain_value_for_article(
            exoplanet.pl_temperature
        )

        if temp_val > 395:
            section += (
                f"Avec une température d'équilibre estimée à {temp_str} [[Kelvin|K]], "
                "cette exoplanète est considérée comme trop chaude pour abriter de l'eau liquide en surface.\n"
            )
        elif temp_val < 180:
            section += (
                f"Avec une température d'équilibre estimée à {temp_str} [[Kelvin|K]], "
                "cette exoplanète est considérée comme trop froide pour abriter de l'eau liquide en surface.\n"
            )
        else:
            section += (
                f"Avec une température d'équilibre estimée à {temp_str} [[Kelvin|K]], "
                "cette exoplanète se situe théoriquement dans la zone habitable de son étoile, "
                "permettant potentiellement la présence d'eau liquide en surface sous réserve d'une atmosphère adéquate.\n"
            )

        return section
