import locale
import datetime
from typing import Optional, Dict
from src.models.reference import DataPoint
from src.models.exoplanet import Exoplanet

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
            
        # Si c'est une date (année), on ne garde pas de décimales
        if isinstance(value, (int, float)) and value.is_integer() and 1000 <= value <= 2100:
            return str(int(value))
            
        # Si c'est une température avec des décimales nulles, on affiche en entier
        if isinstance(value, float) and value.is_integer():
            return str(int(value))
            
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

    def format_datapoint(self, datapoint: DataPoint, exoplanet_name: str, template_refs: Dict[str, str], add_reference_func) -> str:
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
            ref_name = str(datapoint.reference.source.value) if hasattr(datapoint.reference.source, 'value') else str(datapoint.reference.source)
            # Pass templates and exoplanet name to to_wiki_ref
            ref_content_full = datapoint.reference.to_wiki_ref(template_refs, exoplanet_name) 
            return f"{value_str} {add_reference_func(ref_name, ref_content_full)}"
            
        return value_str

    def format_year_field_with_ref(self, datapoint: Optional[DataPoint], exoplanet_name: str, template_refs: Dict[str, str], add_reference_func) -> str:
        """
        Formate un champ d'année avec sa référence
        """
        if not datapoint or datapoint.value is None:
            return ""

        value_str = self.format_year_field(datapoint.value)

        if datapoint.reference:
            ref_name = str(datapoint.reference.source.value) if hasattr(datapoint.reference.source, 'value') else str(datapoint.reference.source)
            ref_content_full = datapoint.reference.to_wiki_ref(template_refs, exoplanet_name)
            if ref_content_full:
                 return f"{value_str} {add_reference_func(ref_name, ref_content_full)}"
        
        return value_str 

    def _format_references(self, exoplanet: Exoplanet) -> str:
        """Formate les références pour l'article."""
        references = []
        if exoplanet.source == "exoplanet_eu":
            references.append(
                f'<ref>{{{{Lien web |langue=en |nom1=EPE |titre={exoplanet.name} |url=https://exoplanet.eu/catalog/{exoplanet.name.lower().replace(" ", "_")}/ |site=exoplanet.eu |date=2024-8-1 |consulté le=2025-1-3 }}}}</ref>'
            )
        if exoplanet.source == "nasa":
            references.append(
                f'<ref>{{{{Lien web |langue=en |nom1=NEA |titre={exoplanet.name} |url=https://science.nasa.gov/exoplanet-catalog/{exoplanet.name.lower().replace(" ", "-")}/ |site=science.nasa.gov |date=2024-11-1 |consulté le=2025-1-3 }}}}</ref>'
            )
        return " ".join(references) 

    def format_value(value, field_type):
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
