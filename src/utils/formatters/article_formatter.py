# src/utils/formatters/article_formatter.py
import locale

from src.models.entities.exoplanet_entity import ValueWithUncertainty


class ArticleFormatter:
    """
    Classe utilitaire pour le formatage des valeurs dans les articles Wikipedia
    """

    def __init__(self):
        # Liste des locales à essayer pour la compatibilité (Linux/Mac vs Windows)
        locales_to_try = ["fr_FR.UTF-8", "fr_FR", "fra", "French_France.1252", "French"]

        for loc in locales_to_try:
            try:
                locale.setlocale(locale.LC_ALL, loc)
                break
            except locale.Error:
                continue

    def format_number_as_french_string(self, value: float | None, precision: int = 2) -> str:
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

        formatted = locale.format_string(f"%.{precision}f", fval, grouping=True)

        # Fallback : si le formatage locale n'a pas mis de virgule (ex: locale non dispo),
        # on force le remplacement du point par la virgule pour le format français
        if "." in formatted and "," not in formatted:
            formatted = formatted.replace(".", ",")

        return formatted.rstrip("0").rstrip(",")

    def format_year_without_decimals(self, value: float | None) -> str:
        """
        Formate une valeur d'année (date) sans décimale.
        """
        if value is None:
            return ""
        if isinstance(value, int | float) and float(value).is_integer():
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
        if value_with_uncertainty.error_positive or value_with_uncertainty.error_negative:
            # CORRECTION ICI : Initialisation à une chaîne vide au lieu de None
            error_str: str = ""

            if value_with_uncertainty.error_positive:
                error_str += (
                    f"+{self.format_number_as_french_string(value_with_uncertainty.error_positive)}"
                )
            if value_with_uncertainty.error_negative:
                error_str += (
                    f"-{self.format_number_as_french_string(value_with_uncertainty.error_negative)}"
                )

            # On n'ajoute l'espace que si error_str n'est pas vide
            if error_str:
                value_str = f"{value_str} {error_str}"

        # Ajouter le signe si présent
        if value_with_uncertainty.sign:
            value_str = f"{value_with_uncertainty.sign}{value_str}"

        return value_str
