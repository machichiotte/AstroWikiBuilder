# src/generators/articles/star/sections/infobox_section.py

from src.constants.wikipedia_field_config import (
    DEFAULT_WIKIPEDIA_UNITS_STAR,
    IS_NOTES_FIELDS_STAR,
)
from src.generators.base.base_infobox_generator import InfoboxBaseGenerator
from src.models.entities.star_entity import Star
from src.models.infobox_fields import FieldMapping, InfoboxMapper


class InfoboxSection(InfoboxBaseGenerator):
    def retrieve_field_mappings(self) -> list[FieldMapping]:
        return InfoboxMapper.convert_star_to_infobox()

    def fetch_infobox_header(self) -> str:
        return "{{Infobox Étoile"

    def retrieve_noted_fields(self) -> list[str]:
        return IS_NOTES_FIELDS_STAR

    def is_supported_entity(self, obj) -> bool:
        return isinstance(obj, Star)

    @property
    def default_field_mapping(self):
        return DEFAULT_WIKIPEDIA_UNITS_STAR
