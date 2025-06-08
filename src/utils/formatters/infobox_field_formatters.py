# src/utils/formatters/infobox_field_formatters.py
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
                value = ", ".join(
                    FieldFormatter._format_designation_with_template(str(v))
                    for v in value if str(v).strip()
                )
            else:
                value = FieldFormatter._format_designation_with_template(
                    str(value).strip())

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

    @staticmethod
    def _format_designation_with_template(designation: str) -> str:
        """Formate une désignation avec le modèle Wikipédia approprié si possible."""
        d = designation.strip()
        if d.lower().startswith("koi "):
            return f"{{{{StarKOI|{d.split(' ')[1]}}}}}"
        if d.lower().startswith("kic "):
            return f"{{{{StarKIC|{d.split(' ')[1]}}}}}"
        if d.lower().startswith("tic "):
            return f"{{{{StarTIC|{d.split(' ')[1]}}}}}"
        if d.lower().startswith("2mass j"):
            core = d[7:].strip()
            if "+" in core or "-" in core:
                for sep in ["+", "-"]:
                    if sep in core:
                        parts = core.split(sep)
                        if len(parts) == 2:
                            return f"{{{{Star2MASS|{parts[0]}|{sep}{parts[1]}}}}}"
        # Ajoute d'autres modèles si besoin
        return d

    def format_numeric_no_trailing_zeros(value):
        try:
            fval = float(value)
            return f"{fval:.5f}".rstrip("0").rstrip(".")
        except Exception:
            return str(value)
