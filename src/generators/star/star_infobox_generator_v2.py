# src/generators/star_infobox_generator.py

from src.generators.base_infobox_generator import InfoboxBaseGenerator
from src.models.data_source_star import DataSourceStar
from src.models.infobox_fields import InfoboxMapper, FieldMapping, FieldType
from src.constants.field_mappings import FIELD_DEFAULT_UNITS_STAR, NOTES_FIELDS_STAR


class StarInfoboxGenerator(InfoboxBaseGenerator):
    def get_field_mappings(self) -> list[FieldMapping]:
        return InfoboxMapper.get_star_field_mappings()

    def get_infobox_header(self) -> str:
        return "{{Infobox Étoile"

    def get_notes_fields(self) -> list[str]:
        return NOTES_FIELDS_STAR

    def is_valid_object(self, obj) -> bool:
        return isinstance(obj, DataSourceStar)

    def handle_special_field(self, star: DataSourceStar, mapping: FieldMapping) -> str:
        if mapping.field_type == FieldType.CONSTELLATION:
            if not (star.right_ascension and star.declination):
                return ""
            constellation = self.constellation_utils.get_constellation_UAI(
                star.right_ascension.value, star.declination.value
            )
            return f"| constellation = {constellation}"

        elif mapping.field_type == FieldType.CARTE_UAI:
            if not (star.right_ascension and star.declination):
                return ""
            carte_uai = self.constellation_utils.get_constellation_name(
                star.right_ascension.value, star.declination.value
            )
            return f"| carte UAI = {carte_uai}"

        return ""

    @property
    def default_mapping(self):
        return FIELD_DEFAULT_UNITS_STAR