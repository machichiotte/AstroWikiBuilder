# src/utils/formatters/article_utils.py
import locale
from typing import Optional, Dict
from src.models.reference import DataPoint
import unicodedata


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

    # TODO check if utile or not
    def format_exoplanet_value(value, field_type):
        if value is None or value == "":
            return None
        try:
            value = float(value)
            if field_type == "distance":  # parsec
                return f"{value:.2f}"
            elif field_type == "mass":  # MJ
                if value < 0.1:
                    return f"{value:.3f}"
                elif value < 1:
                    return f"{value:.2f}"
                else:
                    return f"{value:.1f}"
            elif field_type == "radius":  # RJ
                if value < 0.1:
                    return f"{value:.3f}"
                elif value < 1:
                    return f"{value:.2f}"
                else:
                    return f"{value:.1f}"
            elif field_type == "temperature":  # K
                if value < 100:
                    return f"{value:.1f}"
                else:
                    return f"{value:.0f}"
            elif field_type == "semi_major_axis":  # UA
                if value < 0.1:
                    return f"{value:.3f}"
                elif value < 1:
                    return f"{value:.2f}"
                else:
                    return f"{value:.1f}"
            elif field_type == "period":  # jours
                if value < 1:
                    return f"{value:.3f}"
                elif value < 10:
                    return f"{value:.2f}"
                else:
                    return f"{value:.1f}"
            elif field_type == "eccentricity":
                return f"{value:.2f}"
            elif field_type == "inclination":  # degrés
                return f"{value:.1f}"
            elif field_type == "apparent_magnitude":
                return f"{value:.2f}"
            elif field_type in ["t_peri", "arg_péri", "date"]:  # valeurs entières
                return f"{value:.0f}"
            else:
                return str(value)
        except (ValueError, TypeError):
            return str(value)

    def is_valid_infobox_notes(self, field: str, notes_fields: list[str]) -> bool:
        return field.lower() in notes_fields

    def is_valid_infobox_value(self, value) -> bool:
        """
        Checks if the extracted value should be rendered.
        Returns False if value is None, empty string, or otherwise invalid.
        """
        if value is None:
            return False

        if value is None:
            return False

        try:
            s_representation = format(value)
        except Exception:
            return False

        normalized_s_value = unicodedata.normalize('NFKD', s_representation)

        s_value_stripped = normalized_s_value.strip()

        if not s_value_stripped:
            return False

        s_value_lower = s_value_stripped.lower()

        if s_value_lower == "nan" or s_value_lower.startswith("nan{{"):
            return False

        return True

    def is_needed_infobox_unit(self, field: str, unit: str, default_mapping: dict) -> bool:
        valid_units = default_mapping.get(field.lower(), None)
        return not valid_units == unit
