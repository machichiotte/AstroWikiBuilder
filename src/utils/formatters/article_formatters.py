# src/utils/formatters/article_formatters.py
import locale
from typing import Optional, Dict
from src.models.reference import DataPoint


class ArticleUtils:
    """
    Classe utilitaire pour le formatage des valeurs dans les articles Wikipedia
    """

    def __init__(self):
        locale.setlocale(locale.LC_ALL, "fr_FR.UTF-8")

    def format_numeric_value(self, value: Optional[float], precision: int = 2) -> str:
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

        return locale.format_string(f"%.{precision}f", fval, grouping=True).rstrip("0").rstrip(".")

    def format_year_value(self, value: Optional[float]) -> str:
        """
        Formate une valeur d'année (date) sans décimale.
        """
        if value is None:
            return ""
        if isinstance(value, (int, float)) and float(value).is_integer():
            return str(int(value))
        return str(value)

    def format_parsecs_to_lightyears(self, parsecs: float) -> float:
        """Convertit les parsecs en années-lumière."""
        return parsecs * 3.26156

    def format_datapoint(
        self,
        datapoint: DataPoint,
        exoplanet_name: str,
        template_refs: Dict[str, str],
        add_reference_func,
    ) -> str:
        """
        Formate un DataPoint pour l'affichage dans l'article
        """
        if not datapoint or not datapoint.value:
            return ""

        # Essayer de convertir la valeur en nombre si possible
        try:
            value = float(datapoint.value)
            value_str = self.format_numeric_value(value)
        except (ValueError, TypeError):
            # Si la conversion échoue, utiliser la valeur telle quelle
            value_str = str(datapoint.value)

        if datapoint.reference:
            # Standardized ref_name derivation
            ref_name = (
                str(datapoint.reference.source.value)
                if hasattr(datapoint.reference.source, "value")
                else str(datapoint.reference.source)
            )
            # Pass templates and exoplanet name to to_wiki_ref
            ref_content_full = datapoint.reference.to_wiki_ref(exoplanet_name)
            return f"{value_str} {add_reference_func(ref_name, ref_content_full)}"

        return value_str

    def format_right_ascension(self, rastr_val: str) -> str:
        """
        Formats a right ascension string by replacing 'h', 'm', 's'
        with '/' as needed for Wikipedia formatting.

        Example: "12h34m56s" becomes "12/34/56"
        """
        if not isinstance(rastr_val, str):
            # Handle cases where it might not be a string (e.g., NaN, other types)
            # Or raise an error, or return a default value
            return str(rastr_val)

        formatted_ra = rastr_val.replace(
            "h", "/").replace("m", "/").replace("s", "")
        return formatted_ra
