# src/utils/formatters/article_formatters.py
import locale
from typing import Optional
from src.models.entities.exoplanet import ValueWithUncertainty


class ArticleUtils:
    """
    Classe utilitaire pour le formatage des valeurs dans les articles Wikipedia
    """

    def __init__(self):
        locale.setlocale(locale.LC_ALL, "fr_FR.UTF-8")

    def format_number_as_french_string(
        self, value: Optional[float], precision: int = 2
    ) -> str:
        """
        Formate une valeur numérique avec le format français, sans décimale inutile.
        """
        if value is None:
            return ""

        # Si c'est un float ou int et entier, on affiche sans décimale
        try:
            fval = float(value)
        except Exception:
            return str(value)

        if fval.is_integer():
            return str(int(fval))

        return (
            locale.format_string(f"%.{precision}f", fval, grouping=True)
            .rstrip("0")
            .rstrip(".")
        )

    def format_year_without_decimals(self, value: Optional[float]) -> str:
        """
        Formate une valeur d'année (date) sans décimale.
        """
        if value is None:
            return ""
        if isinstance(value, (int, float)) and float(value).is_integer():
            return str(int(value))
        return str(value)

    def convert_parsecs_to_lightyears(self, parsecs: float) -> float:
        """Convertit les parsecs en années-lumière."""
        return parsecs * 3.26156

    def format_uncertain_value_for_article(
        self,
        value_with_uncertainty: ValueWithUncertainty,
    ) -> str:
        """
        Formate une valeur avec incertitude pour l'affichage dans l'article
        """
        if not value_with_uncertainty or not value_with_uncertainty.value:
            return ""

        # Essayer de convertir la valeur en nombre si possible
        try:
            value = float(value_with_uncertainty.value)
            value_str: str = self.format_number_as_french_string(value)
        except (ValueError, TypeError):
            # Si la conversion échoue, utiliser la valeur telle quelle
            value_str = str(value_with_uncertainty.value)

        # Ajouter les incertitudes si présentes
        if (
            value_with_uncertainty.error_positive
            or value_with_uncertainty.error_negative
        ):
            error_str: str = None
            if value_with_uncertainty.error_positive:
                error_str += f"+{self.format_number_as_french_string(value_with_uncertainty.error_positive)}"
            if value_with_uncertainty.error_negative:
                error_str += f"-{self.format_number_as_french_string(value_with_uncertainty.error_negative)}"
            value_str = f"{value_str} {error_str}"

        # Ajouter le signe si présent
        if value_with_uncertainty.sign:
            value_str = f"{value_with_uncertainty.sign}{value_str}"

        return value_str
