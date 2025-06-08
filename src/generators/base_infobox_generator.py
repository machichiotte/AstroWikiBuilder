# src/generators/base_infobox_generator.py

from abc import ABC, abstractmethod
from typing import Optional, Any
from src.utils.formatters.infobox_fields import FieldMapping, FieldType
from src.utils.formatters.infobox_field_formatters import FieldFormatter
from src.utils.formatters.article_formatters import ArticleUtils
from src.utils.constellation_utils import ConstellationUtils
from src.services.reference_manager import ReferenceManager
from src.utils.validators import infobox_validators

class InfoboxBaseGenerator(ABC):
    def __init__(self, reference_manager: ReferenceManager):
        self.reference_manager = reference_manager
        self.field_formatter = FieldFormatter()
        self.article_utils = ArticleUtils()
        self.constellation_utils = ConstellationUtils()

    def generate(self, obj: Any) -> str:
        if not self.is_valid_object(obj):
            raise TypeError("Invalid data source object.")

        lines = [self.get_infobox_header()]

        for mapping in self.get_field_mappings():
            field_block = self._process_field(obj, mapping)
            if field_block:
                lines.append(field_block)

        for full_ref in self.reference_manager.registered.values():
            lines.append(full_ref)

        lines.append("}}")
        return "\n".join(lines)

    def _process_field(self, obj: Any, mapping: FieldMapping) -> str:
        if mapping.condition and not mapping.condition(obj):
            return ""

        if mapping.field_type in {FieldType.CONSTELLATION, FieldType.CARTE_UAI}:
            return self.handle_special_field(obj, mapping)

        datapoint = getattr(obj, mapping.source_attribute, None)
        if datapoint is None:
            return ""

        value, unit = self.field_formatter.extract_field_value(datapoint)
        value_part = ""

        if infobox_validators.is_valid_infobox_value(value):
            if mapping.unit_override:
                unit = mapping.unit_override

            unit_to_use = unit if infobox_validators.is_needed_infobox_unit(
                mapping.infobox_field, unit, self.default_mapping) else None

            if mapping.formatter:
                value_part = mapping.formatter(value).strip()
            else:
                value_part = self.field_formatter.format_by_type(
                    value, unit_to_use, mapping.infobox_field, mapping.field_type
                )

        if not value_part:
            return ""

        parts = [value_part]

        if infobox_validators.is_valid_infobox_note(mapping.infobox_field, self.get_notes_fields()):
            notes_ref = self._extract_notes(datapoint, obj)
            if notes_ref:
                parts.append(f"| {mapping.infobox_field} notes = {notes_ref}")

        return "\n".join(parts)

    def _extract_notes(self, datapoint: Any, obj: Any) -> Optional[str]:
        ref = getattr(datapoint, "reference", None)
        if ref is None:
            return None

        name_point = getattr(obj, "name", None)
        current_name = "unknown_object"
        if name_point and hasattr(name_point, "value") and name_point.value:
            current_name = str(name_point.value)
        elif name_point:
            current_name = str(name_point)

        try:
            full_ref = ref.to_wiki_ref(current_name)
        except Exception:
            return None

        if not full_ref:
            return None

        source_name = current_name
        if hasattr(ref, "source") and ref.source:
            source_val = getattr(ref.source, "value", None)
            source_name = str(source_val if source_val else ref.source)

        return self.reference_manager.add_reference(str(source_name), full_ref)

    @abstractmethod
    def get_field_mappings(self) -> list[FieldMapping]:
        pass

    @abstractmethod
    def get_infobox_header(self) -> str:
        pass

    @abstractmethod
    def get_notes_fields(self) -> list[str]:
        pass

    @abstractmethod
    def is_valid_object(self, obj: Any) -> bool:
        pass

    @abstractmethod
    def handle_special_field(self, obj: Any, mapping: FieldMapping) -> str:
        pass

    @property
    @abstractmethod
    def default_mapping(self) -> dict:
        pass
