# src/utils/formatters/infobox_field_formatters.py
from typing import Any, Optional

from src.constants.field_mappings import DISCOVERY_FACILITY_MAPPING, METHOD_NAME_MAPPING
from src.models.reference import DataPoint
from src.models.infobox_fields import FieldType


class FieldFormatter:
    """Formatters pour différents types de champs"""

    @staticmethod
    def format_simple_field(
        infobox_field: str, value: Any, unit: Optional[str] = None
    ) -> str:
        """Formate un champ simple avec valeur"""
        if not value or (isinstance(value, str) and not value.strip()):
            return ""

        print("infobox_field", infobox_field)
        print("value", value)
        print("unit", unit)

        # Mapping pour certains champs
        if infobox_field == "lieu":
            mapped = DISCOVERY_FACILITY_MAPPING.get(value)
            if mapped:
                value = f"[[{mapped}]]"
        elif infobox_field == "méthode":
            method_key = str(value).strip().lower()
            mapped = METHOD_NAME_MAPPING.get(method_key)
            if mapped:
                value = f"[[{mapped['article']}|{mapped['display']}]]"
        elif infobox_field == "âge":
            # Pour le champ âge, on utilise une notation scientifique
            value = f"{value}×10<sup>9</sup>"
        elif infobox_field == "désignations":
            # Pour le champ désignations, on formate en liste
            if isinstance(value, list):
                value = ", ".join(
                    FieldFormatter._format_designation_with_template(str(v))
                    for v in value
                    if str(v).strip()
                )
            else:
                value = FieldFormatter._format_designation_with_template(
                    str(value).strip()
                )

        output = f" | {infobox_field} = {value}"

        if unit:
            # Add newline here if unit exists
            output += f"\n | {infobox_field} unité = {unit}"

        return output

    @staticmethod
    def format_by_type(infobox_field: str, value: Any, unit: Optional[str]) -> str:
        """Formate une valeur selon son type de champ"""
        formatters = {
            FieldType.SIMPLE: lambda: FieldFormatter.format_simple_field(
                infobox_field, value, unit
            ),
        }

        formatter = formatters[FieldType.SIMPLE]

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
        if d.lower().startswith("hd "):
            return f"{{{{HD|{d.split(' ')[1]}}}}}"
        if d.lower().startswith("hip "):
            return f"{{{{HIP|{d.split(' ')[1]}}}}}"
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
