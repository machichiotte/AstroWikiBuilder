# src/generators/exoplanet_infobox_generator_v2.py

import unicodedata
# re module no longer needed for the simplified _is_valid_value
from typing import Optional, Any
from src.models.data_source_exoplanet import DataSourceExoplanet, DataPoint
from src.mappers.infobox_mapper import (
    InfoboxMapper,
    FieldMapping,
    FieldType,
)
from src.utils.formatters.field_formatters import FieldFormatter
from src.utils.formatters.article_utils import ArticleUtils
from src.utils.constellation_utils import ConstellationUtils
from src.services.reference_manager import ReferenceManager


class ExoplanetInfoboxGenerator:
    def __init__(self, reference_manager: ReferenceManager):
        self.reference_manager = reference_manager
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
        #self.reference_manager.reset_references()

        infobox_lines = ["{{Infobox exoplanet"]  # start infobox

        for mapping in InfoboxMapper.get_exoplanet_field_mappings():
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
        #    Attempt to retrieve the DataPoint object via mapping.source_attribute
        datapoint: Optional[DataPoint] = getattr(
            exoplanet, mapping.source_attribute, None
        )
       # TODO print(f"exoplanet {exoplanet.mass}")
       # print(f"mapping {mapping}")
       # print(f"Processing field '{mapping.infobox_field}' with source '{mapping.source_attribute}'")
       # print(f"_process_field exoplanet '{exoplanet.spectral_type}'")
        print(f"_process_field datapoint '{datapoint}'")
        print(f"exoplanet  '{exoplanet}'")

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

        # Determine the exoplanet's name as a string, with a fallback.
        current_exoplanet_name_str = "unknown_exoplanet"  # Default fallback
        if exoplanet.name and hasattr(exoplanet.name, 'value') and exoplanet.name.value is not None:
            current_exoplanet_name_str = str(exoplanet.name.value)
        elif exoplanet.name and hasattr(exoplanet.name, 'value') and exoplanet.name.value is None:
             # Case where exoplanet.name is a DataPoint but its value is None
             # Decide if to_wiki_ref can handle None or needs a placeholder.
             # For now, let's keep current_exoplanet_name_str as "unknown_exoplanet" or pass None.
             # Let's assume to_wiki_ref might not need the name or handles None.
             # If it strictly needs a name, this might need adjustment based on to_wiki_ref's contract.
             pass # current_exoplanet_name_str remains "unknown_exoplanet"
        elif exoplanet.name: # If exoplanet.name is a DataPoint but .value is not present or None
             current_exoplanet_name_str = str(exoplanet.name) # Fallback to string of DataPoint obj itself

        # Attempt to obtain the full ref wikitext
        try:
            # Pass the string name to to_wiki_ref.
            # This assumes to_wiki_ref expects/handles a string name.
            # If it expected the DataPoint object exoplanet.name, this is a change.
            full_ref_wikitext = reference_obj.to_wiki_ref(current_exoplanet_name_str)
        except Exception as e:
            # Optional: log the error with more context for debugging
            # print(f"Error calling to_wiki_ref for '{current_exoplanet_name_str}' with reference '{reference_obj}': {e}")
            return None

        if not full_ref_wikitext:
            return None

        # Determine a source name string for the <ref name="..."> identifier
        # Default to the exoplanet's name string if no specific source is found on the reference object.
        source_name_str = current_exoplanet_name_str

        if hasattr(reference_obj, "source") and reference_obj.source:
            # If .source has a .value attribute, use it; otherwise fallback to string repr of source object
            if hasattr(reference_obj.source, "value") and reference_obj.source.value is not None:
                source_name_str = str(reference_obj.source.value)
            else:
                source_name_str = str(reference_obj.source)
        # If no explicit source on reference_obj, source_name_str remains current_exoplanet_name_str (set above)

        # Ensure source_name_str is a string (it should be by this point, but as a safeguard)
        if not isinstance(source_name_str, str):
            source_name_str = str(source_name_str) # Final fallback to string conversion

        # Register the reference in ReferenceManager.
        # ReferenceManager is responsible for creating a valid XML attribute for 'name' from source_name_str.
        ref_tag = self.reference_manager.add_reference(source_name_str, full_ref_wikitext)
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
