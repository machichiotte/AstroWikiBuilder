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

    def _format_field_value(self, value: Any, field_name: str) -> str:
        """Formate la valeur principale du champ."""
        try:
            return FieldFormatter._apply_special_formatting(field_name, value)
        except Exception as e:
            logger.error(
                f"Erreur lors du formatage de la valeur {value} pour le champ {field_name}: {str(e)}"
            )
            return str(value)

    def _format_unit(
        self, unit: Optional[str], mapping: FieldMapping, default_mapping: dict
    ) -> Optional[str]:
        """Formate l'unité du champ si nécessaire."""
        unit_to_use = FieldFormatter._get_unit_to_use(unit, mapping, default_mapping)
        if not unit_to_use:
            return None
        return f"\n | {mapping.infobox_field} unité = {unit_to_use}"

    def _format_notes(
        self, datapoint: DataPoint, mapping: FieldMapping, notes_fields: list[str]
    ) -> Optional[str]:
        """Formate les notes de référence si présentes."""
        if not datapoint.reference or not infobox_validators.is_valid_infobox_note(
            mapping.infobox_field, notes_fields
        ):
            return None

        notes_ref = FieldFormatter._extract_notes(datapoint)
        if not notes_ref:
            return None

        return f"\n | {mapping.infobox_field} notes = {notes_ref}"

    def process_field(
        self,
        datapoint: DataPoint,
        mapping: FieldMapping,
        default_mapping: dict,
        notes_fields: list[str],
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

        Returns:
            str: Le champ formaté avec sa valeur, son unité et ses notes si présents
        """
        # Vérification des conditions préalables
        if not datapoint or not datapoint.value:
            return ""

        try:
            # Extraction des valeurs brutes
            raw_value = datapoint.value
            raw_unit = getattr(datapoint, "unit", None)
            raw_notes = getattr(datapoint, "notes", None)
        except AttributeError as e:
            logger.error(
                f"Erreur lors de l'extraction des attributs du DataPoint: {str(e)}"
            )
            return ""

        # Vérification de la validité de la valeur
        if raw_value is None or (isinstance(raw_value, str) and not raw_value.strip()):
            return ""

        # Construction du champ formaté
        try:
            # Formatage de la valeur principale
            formatted_value = self._format_field_value(raw_value, mapping.infobox_field)
            output = f" | {mapping.infobox_field} = {formatted_value}"

            # Ajout de l'unité si nécessaire
            unit_output = self._format_unit(raw_unit, mapping, default_mapping)
            if unit_output:
                output += unit_output

            # Ajout des notes si nécessaire
            notes_output = self._format_notes(datapoint, mapping, notes_fields)
            if notes_output:
                output += notes_output

            return output

        except Exception as e:
            logger.error(
                f"Erreur lors du formatage du champ {mapping.infobox_field}: {str(e)}"
            )
            return ""
