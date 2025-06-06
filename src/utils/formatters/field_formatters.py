# src/utils/formatters/field_formatters.py
from typing import Any, Optional

from src.models.reference import DataPoint
from src.mappers.infobox_mapper import FieldType


class FieldFormatter:
    """Formatters pour différents types de champs"""

    @staticmethod
    def format_simple_field(value: Any, infobox_field: str = "") -> str:
        """Formate un champ simple avec valeur"""
        if not value or (isinstance(value, str) and not value.strip()):
            return ""

        output = f" | {infobox_field} = {value}"

        return output

    @staticmethod
    def format_simple_with_notes_field(value: Any, infobox_field: str = "", reference: str = "") -> str:
        """Formate un champ simple avec notes"""
        if not value or (isinstance(value, str) and not value.strip()):
            return ""

        output = f" | {infobox_field} = {value}  \n"

        if reference:
            output += f" | {infobox_field} notes = {reference}  \n"

        return output

    @staticmethod
    def format_designations(value: Any, infobox_field: str) -> str:
        """Formate le champ désignations (liste ou string)"""
        if isinstance(value, list):
            processed_list = [str(v) for v in value if str(v).strip()]
            if not processed_list:
                return ""
            return f" | {infobox_field} = {', '.join(processed_list)}"

        if value and str(value).strip():
            return f" | {infobox_field} = {value}"

        return ""

    @staticmethod
    def format_age_field(value: Any, infobox_field: str) -> str:
        """Formate le champ âge avec notation scientifique"""
        if not value:
            return ""
        return f" | {infobox_field} = {value}×10<sup>9</sup>"

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
            FieldType.DESIGNATIONS: lambda: FieldFormatter.format_designations(
                value, infobox_field
            ),
            FieldType.AGE: lambda: FieldFormatter.format_age_field(
                value, infobox_field
            ),
            FieldType.SEPARATE_UNIT: lambda: FieldFormatter.format_separate_unit_field(
                value, unit, infobox_field
            ),
        }

        print("iciiiii info", infobox_field)
        print("iciiiii value", value)
        print("iciiiii unit", unit)
        print("iciiiii field", field_type)

        formatter = formatters.get(field_type, formatters[FieldType.SIMPLE])

        print("formatter", formatter())
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
