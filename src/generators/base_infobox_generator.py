# src/generators/base_infobox_generator.py

from abc import ABC, abstractmethod
from typing import Any
from src.models.entities.exoplanet import Exoplanet
from src.models.entities.star import Star
from src.models.infobox_fields import FieldMapping
from src.utils.formatters.infobox_field_formatters import FieldFormatter
from src.utils.formatters.article_formatters import ArticleUtils
from src.utils.astro.constellation_utils import ConstellationUtils
from src.services.processors.reference_manager import ReferenceManager


class InfoboxBaseGenerator(ABC):
    def __init__(self, reference_manager: ReferenceManager):
        self.reference_manager = reference_manager
        self.field_formatter = FieldFormatter()
        self.article_utils = ArticleUtils()
        self.constellation_utils = ConstellationUtils()

    def generate(self, obj: Exoplanet | Star) -> str:
        if not self.is_valid_object(obj):
            raise TypeError("Invalid data source object.")

        lines = [self.get_infobox_header()]

        for mapping in self.retrieve_infobox_field_mappings():
            value = getattr(obj, mapping.source_attribute, None)

            field_block = self.field_formatter.process_field(
                value=value,
                mapping=mapping,
                notes_fields=self.get_notes_fields(),
                entity_reference=obj.reference,
            )
            if field_block:
                lines.append(field_block)

        for full_ref in self.reference_manager.registered.values():
            lines.append(full_ref)

        lines.append("}}")
        return "\n".join(lines)

    @abstractmethod
    def retrieve_infobox_field_mappings(self) -> list[FieldMapping]:
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

    @property
    @abstractmethod
    def default_mapping(self) -> dict:
        pass
