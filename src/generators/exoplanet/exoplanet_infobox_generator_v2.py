# src/generators/exoplanet_infobox_generator_v2.py

import unicodedata
# re module no longer needed for the simplified _is_valid_value
from typing import Optional, Any
from src.models.data_source_exoplanet import DataSourceExoplanet, DataPoint
from src.mappers.exoplanet_infobox_mapper import (
    ExoplanetInfoboxMapper,
    FieldMapping,
    FieldType,
)
from src.utils.formatters.field_formatters import FieldFormatter
from src.utils.formatters.article_utils import ArticleUtils
from src.utils.constellation_utils import ConstellationUtils
from src.services.reference_manager import ReferenceManager


class ExoplanetInfoboxGenerator:
    def __init__(self):
        self.exoplanet_mapping = ExoplanetInfoboxMapper()
        self.reference_manager = ReferenceManager()
        self.field_formatter = FieldFormatter()
        self.article_utils = ArticleUtils()
        self.constellation_utils = ConstellationUtils()

    def generate_exoplanet_infobox(self, exoplanet: DataSourceExoplanet) -> str:
        """
        Main entry point to build the infobox wikitext for a given Exoplanet.
        Loops over FieldMappings, calls _process_field(), and then injects
        all stored reference contents at the end.
        """
        if not isinstance(exoplanet, DataSourceExoplanet):
            raise TypeError("Input must be an Exoplanet object.")

        # Réinitialise les références pour cet exoplanète
        self.reference_manager.reset_references()

        infobox_lines = ["{{Infobox exoplanet"]  # start infobox

        for mapping in self.exoplanet_mapping.get_field_mappings():
            field_block = self._process_field(exoplanet, mapping)
            if field_block:
                infobox_lines.append(field_block)

        # After all fields, append full <ref>…</ref> contents from ReferenceManager
        for (
            tag_name,
            full_ref,
        ) in self.reference_manager.registered.items():
            # full_ref should be the complete <ref name="…">…</ref> string
            infobox_lines.append(full_ref)

        infobox_lines.append("}}")  # close infobox
        return "\n".join(infobox_lines)

    def _process_field(self, exoplanet: DataSourceExoplanet, mapping: FieldMapping) -> str:
        """
        Processes a single field mapping:
        1. Checks condition (if provided).
        2. If field_type is CONSTELLATION or CARTE_UAI, delegates to special handlers.
        3. Otherwise, extracts DataPoint, obtains (value, unit), formats it, and
           appends a 'notes' sub‐line if a reference is present.
        Returns a chunk of wikitext (with leading '| ') or empty string.
        """
        # 1. Condition filter
        if mapping.condition and not mapping.condition(exoplanet):
            return ""

        # 2. Special, computed fields
        if mapping.field_type == FieldType.CONSTELLATION:
            return self._handle_constellation_field(exoplanet)
        elif mapping.field_type == FieldType.CARTE_UAI:
            return self._handle_carte_uai_field(exoplanet)

        # 3. Standard DataPoint fields
        #    Attempt to retrieve the DataPoint object via mapping.star_attribute
        datapoint: Optional[DataPoint] = getattr(
            exoplanet, mapping.star_attribute, None
        )
        if datapoint is None:
            return ""

        # 3.a Extract raw value and unit
        value, unit = self._extract_field_value(datapoint)
        if not self._is_valid_value(value):
            return ""

        # 3.b Apply unit override if provided
        if mapping.unit_override:
            unit = mapping.unit_override

        # 3.c Apply custom formatter if defined
        if mapping.formatter:
            # Custom formatter is expected to return a complete "| field = …" string
            # including any notes if needed; skip default note‐injection below.
            return mapping.formatter(value).strip()

        # 3.d Format standard/simple or separate‐unit fields
        formatted_value = self._format_by_type(
            value, unit, mapping.infobox_field, mapping.field_type
        )

        # formatted_value now contains the full " | field_name = value_content"
        # (potentially multi-line for fields with separate units from FieldFormatter)
        infobox_block = formatted_value

        # 4. Attempt to extract a reference (notes) from datapoint
        notes_ref = self._extract_notes(datapoint, exoplanet)
        if notes_ref:   
            # Append notes as a new, correctly formatted line
            infobox_block += f"\n| {mapping.infobox_field} notes = {notes_ref}"
        
        return infobox_block # The calling function (generate_exoplanet_infobox) joins blocks with newlines

    def _extract_field_value(
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

    def _is_valid_value(self, value: Any) -> bool:
        """
        Checks if the extracted value should be rendered.
        Returns False if value is None, empty string, or otherwise invalid.
        """
        if value is None:
            return False  # Step 1: Handle None directly

        if value is None:
            return False

        try:
            # Get the string representation using format(), which is closer to f-string behavior
            s_representation = format(value)
        except Exception:
            # If formatting fails for some reason, treat as invalid
            return False

        # Normalize Unicode characters
        normalized_s_value = unicodedata.normalize('NFKD', s_representation)
        
        # Strip whitespace from the normalized string representation
        s_value_stripped = normalized_s_value.strip()

        # If, after stripping, the string is empty, it's invalid
        if not s_value_stripped:
            return False
        
        # Convert the stripped string to lowercase for case-insensitive comparison
        s_value_lower = s_value_stripped.lower()
        
        # Check if the lowercase, stripped, normalized string is "nan"
        # OR starts with "nan{{" (to catch "nan{{±...}}")
        if s_value_lower == "nan" or s_value_lower.startswith("nan{{"):
            return False # If it's "nan" or "nan{{...", it's invalid
            
        # Otherwise, the value is considered valid
        return True

    def _format_by_type(
        self,
        value: Any,
        unit: Optional[str],
        infobox_field: str,
        field_type: FieldType,
    ) -> str:
        """
        Delegates to FieldFormatter based on field_type.
        - SIMPLE: just wrap/escape value
        - SEPARATE_UNIT: handle value and unit separately
        For any additional custom types, extend here or rely on mapping.formatter.
        """
        if field_type == FieldType.SIMPLE:
            return self.field_formatter.format_simple_field(value, infobox_field)
        elif field_type == FieldType.SEPARATE_UNIT:
            return self.field_formatter.format_separate_unit_field(
                value, unit, infobox_field
            )
        else:
            # Fallback: treat as SIMPLE
            return self.field_formatter.format_simple_field(value, infobox_field)

    def _extract_notes(
        self, datapoint: DataPoint, exoplanet: DataSourceExoplanet
    ) -> Optional[str]:
        """
        If datapoint.reference exists and provides to_wiki_ref(exoplanet_name),
        register it in ReferenceManager and return the short <ref name="TAG"/> tag.
        Otherwise, return None.
        """
        reference_obj = getattr(datapoint, "reference", None)
        if reference_obj is None:
            return None

        # Attempt to obtain the full ref wikitext (e.g., '<ref name="Smith2024">Smith et al. 2024</ref>')
        try:
            full_ref_wikitext = reference_obj.to_wiki_ref(exoplanet.name)
        except Exception:
            return None

        if not full_ref_wikitext:
            return None

        # Determine a source name to use as the <ref name="..."> identifier
        source_name = None
        if hasattr(reference_obj, "source") and reference_obj.source:
            # If .source has a .value attribute, use it; otherwise fallback to string repr
            source_name = getattr(
                reference_obj.source, "value", str(reference_obj.source)
            )
        else:
            source_name = str(exoplanet.name)  # fallback to exoplanet.name as tag base

        # Register the reference in ReferenceManager, which returns the short tag '<ref name="..."/>'
        ref_tag = self.reference_manager.add_reference(source_name, full_ref_wikitext)
        return ref_tag

    def _handle_constellation_field(self, exoplanet: DataSourceExoplanet) -> str:
        """
        Handles the CONSTELLATION field_type.
        Returns a line '| constellation = <value>' if RA and Dec exist.
        """
        if not (exoplanet.right_ascension and exoplanet.declination):
            return ""
        constellation = self.constellation_utils.get_constellation_UAI(
            exoplanet.right_ascension.value, exoplanet.declination.value
        )
        return f"| constellation = {constellation}"

    def _handle_carte_uai_field(self, exoplanet: DataSourceExoplanet) -> str:
        """
        Handles the CARTE_UAI field_type.
        Returns a line '| carte UAI = <value>' if RA and Dec exist.
        """
        if not (exoplanet.right_ascension and exoplanet.declination):
            return ""
        carte_uai = self.constellation_utils.get_constellation_name(
            exoplanet.right_ascension.value, exoplanet.declination.value
        )
        return f"| carte UAI = {carte_uai}"
