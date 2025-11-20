# src/generators/articles/exoplanet/parts/exoplanet_infobox_generator.py

from src.generators.base.base_infobox_generator import InfoboxBaseGenerator
from src.models.entities.exoplanet_model import Exoplanet
from src.models.infobox_fields import InfoboxMapper, FieldMapping
from src.constants.wikipedia_field_config import (
    DEFAULT_WIKIPEDIA_UNITS_EXOPLANET,
    IS_NOTES_FIELDS_EXOPLANET,
)


class ExoplanetInfoboxGenerator(InfoboxBaseGenerator):
    def retrieve_field_mappings(self) -> list[FieldMapping]:
        return InfoboxMapper.convert_exoplanet_to_infobox()

    def fetch_infobox_header(self) -> str:
        return "{{Infobox Exoplanète"

    def retrieve_noted_fields(self) -> list[str]:
        return IS_NOTES_FIELDS_EXOPLANET

    def is_supported_entity(self, obj) -> bool:
        return isinstance(obj, Exoplanet)

    @property
    def default_field_mapping(self):
        return DEFAULT_WIKIPEDIA_UNITS_EXOPLANET
