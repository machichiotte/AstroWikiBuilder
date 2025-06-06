# src/utils/formatters/field_formatters.py
from typing import Any, Optional

from src.constants.field_mappings import LIEU_NAME_MAPPING, METHOD_NAME_MAPPING
from src.models.reference import DataPoint
from src.mappers.infobox_mapper import FieldType


class FieldFormatter:
    """Formatters pour différents types de champs"""

    @staticmethod
    def format_simple_field(value: Any, infobox_field: str = "") -> str:
        """Formate un champ simple avec valeur"""
        if not value or (isinstance(value, str) and not value.strip()):
            return ""

         # Mapping pour certains champs
        if infobox_field == "lieu":
            mapped = LIEU_NAME_MAPPING.get(value)
            if mapped:
                value = f"[[{mapped}]]"
        elif infobox_field == "méthode":
            mapped = METHOD_NAME_MAPPING.get(value)
            if mapped:
                value = f"[[{mapped}]]"
        elif infobox_field == "âge":
            # Pour le champ âge, on utilise une notation scientifique
            value = f"{value}×10<sup>9</sup>"
        elif infobox_field == "désignations":
            # Pour le champ désignations, on formate en liste
            if isinstance(value, list):
                value = ", ".join(str(v) for v in value if str(v).strip())
            else:
                value = str(value).strip()
                
        output = f" | {infobox_field} = {value}"

        return output

    @staticmethod
    def format_separate_unit_field(
        value: Any, unit: Optional[str], infobox_field: str
    ) -> str:
        """Formate un champ avec unité sur ligne séparée"""
        if not value:
            return ""

        result = f" | {infobox_field} = {value}"

        if unit:
            unit_param = FieldFormatter._get_unit_param_name(infobox_field)
            # Add newline here if unit exists
            result += f"\n | {unit_param} = {unit}"

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

    @staticmethod
    def format_by_type(
        value: Any, unit: Optional[str], infobox_field: str, field_type: FieldType
    ) -> str:
        """Formate une valeur selon son type de champ"""
        formatters = {
            FieldType.SIMPLE: lambda: FieldFormatter.format_simple_field(
                value, infobox_field
            ),
            FieldType.SEPARATE_UNIT: lambda: FieldFormatter.format_separate_unit_field(
                value, unit, infobox_field
            ),
        }

        formatter = formatters.get(field_type, formatters[FieldType.SIMPLE])

        return formatter()

    def extract_field_value(
        self, datapoint: DataPoint
    ) -> tuple[Optional[Any], Optional[str]]:
        """
        Returns a tuple (value, unit) from the DataPoint.
        If the DataPoint has no value or it's invalid, returns (None, None).
        """
        # We assume DataPoint has .value and .unit attributes
        try:
            raw_value = datapoint.value
            raw_unit = getattr(datapoint, "unit", None)
        except AttributeError:
            return None, None

        # If the raw_value is None or empty, treat as invalid
        if raw_value is None or (
            isinstance(raw_value, str) and raw_value.strip() == ""
        ):
            return None, None

        return raw_value, raw_unit
