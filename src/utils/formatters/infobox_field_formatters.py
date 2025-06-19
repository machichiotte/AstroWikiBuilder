# src/utils/formatters/infobox_field_formatters.py
from enum import Enum
import logging
from typing import Any

from src.constants.field_mappings import DISCOVERY_FACILITY_MAPPING, METHOD_NAME_MAPPING
from src.models.entities.exoplanet import ValueWithUncertainty
from src.utils.validators import infobox_validators
from src.models.infobox_fields import FieldMapping
from src.models.references.reference import Reference

logger = logging.getLogger(__name__)


class InfoboxField(str, Enum):
    """Enumération des champs d'infobox"""

    LOCATION = "lieu"
    METHOD = "méthode"
    AGE = "âge"
    DESIGNATIONS = "désignations"
    UAI_MAP = "carte UAI"
    CONSTELLATION = "constellation"
    EPOCH = "test_epoch"


def _format_error_number(value: ValueWithUncertainty) -> str:
    """Formate une valeur avec incertitude pour l'infobox"""
    if not value or value.value is None:
        return ""

    try:
        formatted_value = f"{float(value.value):.2f}"

        pos_error = (
            f"{float(value.error_positive):.2f}"
            if value.error_positive is not None
            else ""
        )
        neg_error = (
            f"{float(value.error_negative):.2f}"
            if value.error_negative is not None
            else ""
        )

        if pos_error and neg_error:
            error_part = f"{{{{±|{pos_error}|{neg_error}}}}}"
        elif pos_error:
            error_part = f"{{{{±|{pos_error}|}}}}"
        elif neg_error:
            error_part = f"{{{{±||{neg_error}}}}}"
        else:
            error_part = ""
        return formatted_value + error_part

    except (ValueError, TypeError) as e:
        logger.error(f"Erreur lors du formatage de la valeur {value}: {str(e)}")
        return str(value)


class FieldFormatter:
    """Formatters pour différents types de champs"""

    @staticmethod
    def _format_discovery_facility(value: str) -> str:
        """Formate le lieu de découverte"""
        try:
            mapped: str | None = DISCOVERY_FACILITY_MAPPING.get(value)
            return f"[[{mapped}]]" if mapped else str(value)
        except Exception as e:
            logger.error(
                f"Erreur lors du formatage du lieu de découverte {value}: {str(e)}"
            )
            return str(value)

    @staticmethod
    def _format_discovery_method(value: str) -> str:
        """Formate la méthode de découverte"""
        try:
            method_key: str = str(value).strip().lower()
            mapped: str | None = METHOD_NAME_MAPPING.get(method_key)
            return (
                f"[[{mapped['article']}|{mapped['display']}]]" if mapped else str(value)
            )
        except Exception as e:
            logger.error(f"Erreur lors du formatage de la méthode {value}: {str(e)}")
            return str(value)

    @staticmethod
    def _format_designations(value: str) -> str:
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
                formatted_designations = []
                for v in value:
                    if v and str(v).strip():
                        formatted: str = format_single_designation(str(v))
                        if formatted:
                            formatted_designations.append(formatted)
                return (
                    ", ".join(formatted_designations) if formatted_designations else ""
                )
            return format_single_designation(str(value).strip())
        except Exception as e:
            logger.error(f"Erreur lors du formatage des désignations {value}: {str(e)}")
            return str(value)

    def _format_field_value(
        self, value: str | ValueWithUncertainty | None, field_name: str
    ) -> str:
        """Formate la valeur principale du champ."""
        try:
            # Si c'est une ValueWithUncertainty, on la formate d'abord
            if isinstance(value, ValueWithUncertainty):
                formatted_value = _format_error_number(value)
                return formatted_value

            # Pour les autres types, on applique le formatter normalement
            formatter = _FORMATTERS.get(field_name)
            return formatter(value) if formatter else value
        except Exception as e:
            logger.error(
                f"Erreur lors du formatage de la valeur {value} pour le champ {field_name}: {str(e)}"
            )
            return str(value)

    def process_field(
        self,
        value: str | list | ValueWithUncertainty,
        mapping: FieldMapping,
        notes_fields: list[str],
        wiki_reference: str = None,
    ) -> str:
        """Traite un champ complet avec sa valeur, unité et notes."""
        if not value:
            return ""

        reference: str | None = wiki_reference if wiki_reference else None

        try:
            # Extraction des valeurs brutes
            if (
                isinstance(value, str)
                | isinstance(value, list)
                | isinstance(value, ValueWithUncertainty)
            ):
                raw_value = value
            else:
                raw_value = None

        except AttributeError as e:
            logger.error(
                f"Erreur lors de l'extraction des attributs de la valeur: {str(e)}"
            )
            return ""

        # Vérification de la validité de la valeur
        if not raw_value:
            return ""

        # Formatage de la valeur principale
        formatted_value: str = self._format_field_value(
            raw_value, mapping.infobox_field
        )

        # Construction du champ complet
        field: str = f" | {mapping.infobox_field} = {formatted_value}"

        # Ajout des notes si nécessaire
        if reference and infobox_validators.is_valid_infobox_note(
            mapping.infobox_field, notes_fields
        ):
            field += f"\n | {mapping.infobox_field} notes = {reference}"

        return field


# Dictionnaire des formatters spécifiques
_FORMATTERS = {
    InfoboxField.LOCATION: FieldFormatter._format_discovery_facility,
    InfoboxField.METHOD: FieldFormatter._format_discovery_method,
    InfoboxField.AGE: lambda v: f"{v}×10<sup>9</sup>",
    InfoboxField.DESIGNATIONS: FieldFormatter._format_designations,
    InfoboxField.UAI_MAP: lambda v: v,
    InfoboxField.CONSTELLATION: lambda v: f"[[{v} (constellation)|{v}]]",
}
