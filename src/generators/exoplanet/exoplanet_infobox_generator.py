# src/generators/exoplanet_infobox_generator.py

from src.generators.base_infobox_generator import InfoboxBaseGenerator
from src.models.data_source_exoplanet import DataSourceExoplanet
from src.models.infobox_fields import InfoboxMapper, FieldMapping
from src.constants.field_mappings import (
    FIELD_DEFAULT_UNITS_EXOPLANET,
    NOTES_FIELDS_EXOPLANET,
)


class ExoplanetInfoboxGenerator(InfoboxBaseGenerator):
    def get_field_mappings(self) -> list[FieldMapping]:
        return InfoboxMapper.get_exoplanet_field_mappings()

    def get_infobox_header(self) -> str:
        return "{{Infobox Exoplanète"

    def get_notes_fields(self) -> list[str]:
        return NOTES_FIELDS_EXOPLANET

    def is_valid_object(self, obj) -> bool:
        return isinstance(obj, DataSourceExoplanet)

    @property
    def default_mapping(self):
        return FIELD_DEFAULT_UNITS_EXOPLANET
