# src/generators/star_infobox_generator.py
from src.generators.base_infobox_generator import InfoboxBaseGenerator
from src.models.data_source_star import DataSourceStar
from src.models.infobox_fields import InfoboxMapper, FieldMapping
from src.constants.field_mappings import (
    FIELD_DEFAULT_UNITS_STAR,
    NOTES_FIELDS_STAR,
)


class StarInfoboxGenerator(InfoboxBaseGenerator):
    def get_field_mappings(self) -> list[FieldMapping]:
        return InfoboxMapper.get_star_field_mappings()

    def get_infobox_header(self) -> str:
        return "{{Infobox Étoile"

    def get_notes_fields(self) -> list[str]:
        return NOTES_FIELDS_STAR

    def is_valid_object(self, obj) -> bool:
        return isinstance(obj, DataSourceStar)

    @property
    def default_mapping(self):
        return FIELD_DEFAULT_UNITS_STAR
