# src/generators/star_infobox_generator.py
from src.generators.base_infobox_generator import InfoboxBaseGenerator
from src.models.entities.star import Star
from src.models.infobox_fields import InfoboxMapper, FieldMapping
from src.constants.field_mappings import (
    FIELD_DEFAULT_UNITS_STAR,
    NOTES_FIELDS_STAR,
)


class StarInfoboxGenerator(InfoboxBaseGenerator):
    def retrieve_infobox_field_mappings(self) -> list[FieldMapping]:
        return InfoboxMapper.convert_star_to_infobox()

    def get_infobox_header(self) -> str:
        return "{{Infobox Étoile}"

    def get_notes_fields(self) -> list[str]:
        return NOTES_FIELDS_STAR

    def is_valid_object(self, obj) -> bool:
        return isinstance(obj, Star)

    @property
    def default_mapping(self):
        return FIELD_DEFAULT_UNITS_STAR
