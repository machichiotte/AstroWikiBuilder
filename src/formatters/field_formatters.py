# src/utils/formatting/field_formatters.py
from typing import Any, Optional


class FieldFormatter:
    """Formatters pour différents types de champs"""

    @staticmethod
    def format_simple_field(value: Any, infobox_field: str = "") -> str:
        """Formate un champ simple avec valeur"""
        if not value or (isinstance(value, str) and not value.strip()):
            return ""

        output = f" | {infobox_field} = {value}"

        return output + "\n"

    @staticmethod
    def format_designations(value: Any, infobox_field: str) -> str:
        """Formate le champ désignations (liste ou string)"""
        if isinstance(value, list):
            processed_list = [str(v) for v in value if str(v).strip()]
            if not processed_list:
                return ""
            return f" | {infobox_field} = {', '.join(processed_list)}\n"

        if value and str(value).strip():
            return f" | {infobox_field} = {value}\n"

        return ""

    @staticmethod
    def format_age_field(value: Any, infobox_field: str) -> str:
        """Formate le champ âge avec notation scientifique"""
        if not value:
            return ""
        return f" | {infobox_field} = {value}×10<sup>9</sup>\n"

    @staticmethod
    def format_separate_unit_field(
        value: Any, unit: Optional[str], infobox_field: str
    ) -> str:
        """Formate un champ avec unité sur ligne séparée"""
        if not value:
            return ""

        result = f" | {infobox_field} = {value}\n"

        if unit:
            unit_param = FieldFormatter._get_unit_param_name(infobox_field)
            result += f" | {unit_param} = {unit}\n"

        return result

    @staticmethod
    def _should_skip_unit(infobox_field: str) -> bool:
        """Détermine si l'unité doit être omise pour ce champ"""
        skip_patterns = [
            "métallicité",
            "type spectral",
            "époque",
            "constellation",
            "magnitude apparente",
            "magnitude absolue",
            "indice ",
        ]
        return any(pattern in infobox_field for pattern in skip_patterns)

    @staticmethod
    def _get_unit_param_name(infobox_field: str) -> str:
        """Retourne le nom du paramètre d'unité pour un champ donné"""
        overrides = {
            "longitude du nœud ascendant (Ω)": "longitude nœud ascendant unité",
            "argument du périastre (ω)": "argument périastre unité",
        }
        return overrides.get(infobox_field, f"{infobox_field} unité")
