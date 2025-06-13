# src/utils/formatters/infobox_field_formatters.py
from enum import Enum
import logging
from typing import Any, Optional

from src.constants.field_mappings import DISCOVERY_FACILITY_MAPPING, METHOD_NAME_MAPPING
from src.models.reference import DataPoint
from src.utils.validators import infobox_validators
from src.models.infobox_fields import FieldMapping

logger = logging.getLogger(__name__)


class InfoboxField(str, Enum):
    """Enumération des champs d'infobox"""

    LOCATION = "lieu"
    METHOD = "méthode"
    AGE = "âge"
    DESIGNATIONS = "désignations"
    UAI_MAP = "carte UAI"
    CONSTELLATION = "constellation"


class FieldFormatter:
    """Formatters pour différents types de champs"""

    @staticmethod
    def _apply_special_formatting(infobox_field: str, value: Any) -> str:
        """Applique le formatage spécial selon le type de champ"""
        try:
            formatter = FieldFormatter._FORMATTERS.get(infobox_field)
            return formatter(value) if formatter else value
        except Exception as e:
            logger.error(f"Erreur lors du formatage du champ {infobox_field}: {str(e)}")
            return str(value)

    @staticmethod
    def _format_discovery_facility(value: Any) -> str:
        """Formate le lieu de découverte"""
        try:
            mapped = DISCOVERY_FACILITY_MAPPING.get(value)
            return f"[[{mapped}]]" if mapped else str(value)
        except Exception as e:
            logger.error(
                f"Erreur lors du formatage du lieu de découverte {value}: {str(e)}"
            )
            return str(value)

    @staticmethod
    def _format_discovery_method(value: Any) -> str:
        """Formate la méthode de découverte"""
        try:
            method_key = str(value).strip().lower()
            mapped = METHOD_NAME_MAPPING.get(method_key)
            return (
                f"[[{mapped['article']}|{mapped['display']}]]" if mapped else str(value)
            )
        except Exception as e:
            logger.error(f"Erreur lors du formatage de la méthode {value}: {str(e)}")
            return str(value)

    @staticmethod
    def _format_designations(value: Any) -> str:
        """Formate les désignations en liste avec les modèles Wikipédia appropriés."""
        try:

            def format_single_designation(d: str) -> str:
                try:
                    d = d.strip()
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
                    return d
                except Exception as e:
                    logger.error(
                        f"Erreur lors du formatage de la désignation {d}: {str(e)}"
                    )
                    return d

            if isinstance(value, list):
                return ", ".join(
                    format_single_designation(str(v)) for v in value if str(v).strip()
                )
            return format_single_designation(str(value).strip())
        except Exception as e:
            logger.error(f"Erreur lors du formatage des désignations {value}: {str(e)}")
            return str(value)

    _FORMATTERS = {
        InfoboxField.LOCATION: _format_discovery_facility,
        InfoboxField.METHOD: _format_discovery_method,
        InfoboxField.AGE: lambda v: f"{v}×10<sup>9</sup>",
        InfoboxField.DESIGNATIONS: _format_designations,
        InfoboxField.UAI_MAP: lambda v: v,
        InfoboxField.CONSTELLATION: lambda v: f"[[{v} (constellation)|{v}]]",
    }

    @staticmethod
    def _extract_field_value(
        datapoint: DataPoint,
    ) -> tuple[Optional[Any], Optional[str], Optional[Any]]:
        """
        Returns a tuple (value, unit) from the DataPoint.
        If the DataPoint has no value or it's invalid, returns (None, None).
        """
        try:
            raw_value = datapoint.value
            raw_unit = getattr(datapoint, "unit", None)
            raw_ref: Any | None = getattr(datapoint, "notes", None)
        except AttributeError:
            return None, None

        # If the raw_value is None or empty, treat as invalid
        if raw_value is None or (
            isinstance(raw_value, str) and raw_value.strip() == ""
        ):
            return None, None, None

        return raw_value, raw_unit, raw_ref

    @staticmethod
    def _get_unit_to_use(
        unit: Optional[str], mapping: FieldMapping, default_mapping: dict
    ) -> Optional[str]:
        """Détermine l'unité à utiliser pour le champ."""
        if mapping.unit_override:
            return mapping.unit_override

        if not unit:
            return None

        return (
            unit
            if infobox_validators.is_needed_infobox_unit(
                mapping.infobox_field, unit, default_mapping
            )
            else None
        )

    @staticmethod
    def _extract_notes(datapoint: DataPoint) -> Optional[str]:
        """Extrait les notes d'un DataPoint."""
        ref = datapoint.reference
        if not ref:
            return None

        try:
            full_ref = ref.to_wiki_ref()
            if not full_ref:
                return None
            return full_ref
        except Exception:
            return None

    def process_field(
        self,
        datapoint: DataPoint | None,
        mapping: FieldMapping,
        default_mapping: dict,
        notes_fields: list[str],
        obj: Any,
    ) -> str:
        """Traite un champ complet avec sa valeur, unité et notes.

        Cette méthode gère le formatage complet d'un champ d'infobox en :
        1. Vérifiant les conditions préalables
        2. Extrayant et formatant la valeur principale
        3. Ajoutant l'unité si nécessaire
        4. Ajoutant les notes de référence si présentes

        Args:
            datapoint: Le point de données contenant la valeur et potentiellement une référence
            mapping: La configuration de mapping du champ
            default_mapping: Le mapping par défaut pour les unités
            notes_fields: Liste des champs qui peuvent avoir des notes
            obj: L'objet source pour la vérification des conditions

        Returns:
            str: Le champ formaté avec sa valeur, son unité et ses notes si présents
        """
        if mapping.condition and not mapping.condition(obj):
            return ""

        if not datapoint or not datapoint.value:
            return ""

        value, unit, ref = FieldFormatter._extract_field_value(datapoint)
        if not value:
            return ""

        formatted_value = FieldFormatter._apply_special_formatting(
            mapping.infobox_field, value
        )

        output = f" | {mapping.infobox_field} = {formatted_value}"

        # Ajout du champ unité si nécessaire
        unit_to_use = FieldFormatter._get_unit_to_use(unit, mapping, default_mapping)
        if unit_to_use:
            output += f"\n | {mapping.infobox_field} unité = {unit_to_use}"

        # Ajoute les notes au champ si nécessaire
        if ref and infobox_validators.is_valid_infobox_note(
            mapping.infobox_field, notes_fields
        ):
            notes_ref = FieldFormatter._extract_notes(datapoint)
            if notes_ref:
                output += f"\n | {mapping.infobox_field} notes = {notes_ref}"

        return output
