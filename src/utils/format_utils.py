import locale
import datetime
from typing import Optional

class FormatUtils:
    """
    Classe utilitaire pour le formatage des valeurs dans les articles Wikipedia
    """
    def __init__(self):
        locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')

    def format_numeric_value(self, value: Optional[float], precision: int = 2) -> str:
        """
        Formate une valeur numérique avec le format français
        """
        if value is None:
            return ""
        return locale.format_string(f"%.{precision}f", value, grouping=True)
    
    def format_value_with_unit(self, value: Optional[float], unit: str, precision: int = 2) -> str:
        """
        Formate une valeur avec son unité, gère les valeurs None
        """
        if value is None:
            return ""
        return f"{self.format_numeric_value(value, precision)} {unit}"
    
    def format_year_field(self, value: Optional[str]) -> str:
        """
        Formate une année ou une date complète
        """
        if not value:
            return ""

        # Nettoyer la valeur
        cleaned_value = str(value).replace("\u202F", "").replace(" ", "")
        if ',' in cleaned_value and '.' not in cleaned_value:
            cleaned_value = cleaned_value.replace(",", ".")

        try:
            numeric_value = float(cleaned_value)
            if numeric_value.is_integer():
                year_int = int(numeric_value)
                if 1000 <= year_int <= (datetime.datetime.now().year + 10):
                    return str(year_int)
            return str(value)
        except (ValueError, TypeError):
            return str(value)

    def parsecs_to_lightyears(self, parsecs: float) -> float:
        """Convertit les parsecs en années-lumière."""
        return parsecs * 3.26156 