# src/generators/exoplanet_infobox_generator.py

from src.generators.base_infobox_generator import InfoboxBaseGenerator
from src.models.data_source_exoplanet import DataSourceExoplanet
from src.mappers.infobox_mapper import InfoboxMapper, FieldMapping, FieldType
from src.constants.field_mappings import FIELD_DEFAULT_UNITS_EXOPLANET, NOTES_FIELDS_EXOPLANET


class ExoplanetInfoboxGenerator(InfoboxBaseGenerator):
    def get_field_mappings(self) -> list[FieldMapping]:
        return InfoboxMapper.get_exoplanet_field_mappings()

    def get_infobox_header(self) -> str:
        return "{{Infobox Exoplanète"

    def get_notes_fields(self) -> list[str]:
        return NOTES_FIELDS_EXOPLANET

    def is_valid_object(self, obj) -> bool:
        return isinstance(obj, DataSourceExoplanet)

    def handle_special_field(self, exoplanet: DataSourceExoplanet, mapping: FieldMapping) -> str:
        if mapping.field_type == FieldType.CONSTELLATION:
            if not (exoplanet.right_ascension and exoplanet.declination):
                return ""
            constellation = self.constellation_utils.get_constellation_UAI(
                exoplanet.right_ascension.value, exoplanet.declination.value
            )
            return f"| constellation = {constellation}"

        elif mapping.field_type == FieldType.CARTE_UAI:
            if not (exoplanet.right_ascension and exoplanet.declination):
                return ""
            carte_uai = self.constellation_utils.get_constellation_name(
                exoplanet.right_ascension.value, exoplanet.declination.value
            )
            return f"| carte UAI = {carte_uai}"

        return ""

    @property
    def default_mapping(self):
        return FIELD_DEFAULT_UNITS_EXOPLANET