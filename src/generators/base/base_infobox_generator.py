# src/generators/base/base_infobox_generator.py

from abc import ABC, abstractmethod
from typing import Any

from src.utils.formatters.article_formatter import ArticleFormatter

from src.models.entities.exoplanet_entity import Exoplanet
from src.models.entities.star_entity import Star
from src.models.infobox_fields import FieldMapping
from src.services.processors.reference_manager import ReferenceManager
from src.utils.astro.constellation_util import ConstellationUtil
from src.utils.formatters.infobox_field_formatter import InboxFieldFormatter


class InfoboxBaseGenerator(ABC):
    def __init__(self, reference_manager: ReferenceManager):
        self.reference_manager: ReferenceManager = reference_manager
        self.inbox_field_formatter = InboxFieldFormatter()
        self.article_util = ArticleFormatter()
        self.constellation_util = ConstellationUtil()

    def build_infobox(self, obj: Exoplanet | Star) -> str:
        if not self.is_supported_entity(obj):
            raise TypeError("Invalid data source object.")

        lines: list[str] = [self.fetch_infobox_header()]

        wiki_reference: str | None = obj.reference.to_wiki_ref() if obj.reference else None

        for mapping in self.retrieve_field_mappings():
            value = getattr(obj, mapping.source_attribute, None)

            field_block: str = self.inbox_field_formatter.process_field(
                value=value,
                mapping=mapping,
                notes_fields=self.retrieve_noted_fields(),
                wiki_reference=wiki_reference,
            )
            if field_block:
                lines.append(field_block)

        for full_ref in self.reference_manager.all_registered_references.values():
            lines.append(full_ref)

        lines.append("}}")
        return "\n".join(lines)

    # --- Méthodes à spécialiser par les classes filles ---

    @abstractmethod
    def retrieve_field_mappings(self) -> list[FieldMapping]:
        pass

    @abstractmethod
    def fetch_infobox_header(self) -> str:
        pass

    @abstractmethod
    def retrieve_noted_fields(self) -> list[str]:
        pass

    @abstractmethod
    def is_supported_entity(self, obj: Any) -> bool:
        pass

    @property
    @abstractmethod
    def default_field_mapping(self) -> dict:
        pass
