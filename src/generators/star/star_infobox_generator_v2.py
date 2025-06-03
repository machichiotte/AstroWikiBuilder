# src/generators/star_infobox_generator_v2.py
import math
from typing import Optional, Any
from src.models.data_source_star import DataSourceStar, DataPoint
from src.mappers.star_mapping_infobox import StarMappingInfobox, FieldMapping, FieldType
from src.utils.constellation_utils import ConstellationUtils
from src.utils.formatters.article_utils import ArticleUtils
from src.utils.formatters.field_formatters import FieldFormatter


class StarInfoboxGenerator:
    """Générateur d'infobox pour les étoiles"""

    def __init__(self):
        self.article_utils = ArticleUtils()
        self.constellation_utils = ConstellationUtils()
        self.field_formatter = FieldFormatter()
        self.mapping_config = StarMappingInfobox()

    def generate_star_infobox(self, star: DataSourceStar) -> str:
        """Génère le contenu de l'infobox Wikipédia pour une étoile"""

        print("generateeeeeeeeee " + str(star))
        if not isinstance(star, DataSourceStar):
            raise TypeError("Input must be a Star object.")

        infobox = "{{Infobox Étoile\n"

        # Traiter tous les champs selon leur configuration
        for mapping in self.mapping_config.get_field_mappings():
            field_content = self._process_field(star, mapping)
            if field_content:
                infobox += field_content

        infobox += "}}\n"
        return infobox

    def _process_field(self, star: DataSourceStar, mapping: FieldMapping) -> str:
        """Traite un champ selon sa configuration de mapping"""
        # Vérifier la condition si elle existe
        if mapping.condition and not mapping.condition(star):
            return ""

        # Gérer les champs calculés spéciaux
        if mapping.field_type == FieldType.CONSTELLATION:
            return self._handle_constellation_field(star)
        elif mapping.field_type == FieldType.CARTE_UAI:
            return self._handle_carte_uai_field(star)

        # Récupérer la valeur du champ
        value, unit = self._extract_field_value(star, mapping.star_attribute)

        if not self._is_valid_value(value):
            return ""

        # Appliquer l'override d'unité si défini
        if mapping.unit_override:
            unit = mapping.unit_override

        # Appliquer le formatter personnalisé si défini
        if mapping.formatter:
            return mapping.formatter(value)

        # Formater selon le type de champ
        return self._format_by_type(
            value, unit, mapping.infobox_field, mapping.field_type
        )

    def _extract_field_value(
        self, star: DataSourceStar, attribute_name: str
    ) -> tuple[Any, Optional[str]]:
        """Extrait la valeur et l'unité d'un attribut Star"""
        attr_dp = getattr(star, attribute_name, None)

        if attr_dp is None:
            return None, None

        if isinstance(attr_dp, DataPoint):
            return attr_dp.value, attr_dp.unit

        return attr_dp, None

    def _is_valid_value(self, value: Any) -> bool:
        """
        Checks if the extracted value should be rendered.
        Returns False if value is None, an empty string, a string representation of 'nan',
        or the float NaN.
        """
        if value is None:
            return False

        # Check for float NaN
        if isinstance(value, float) and math.isnan(value):
            return False

        # Check for string representations of NaN or empty/whitespace strings
        if isinstance(value, str):
            if value.strip() == "":
                return False
            if value.strip().lower() == "nan":
                return False

        # Add any other specific invalid checks if needed, e.g. for other types

        return True

    def _format_by_type(
        self, value: Any, unit: Optional[str], infobox_field: str, field_type: FieldType
    ) -> str:
        """Formate une valeur selon son type de champ"""
        formatters = {
            FieldType.SIMPLE: lambda: self.field_formatter.format_simple_field(
                value, infobox_field
            ),
            FieldType.DESIGNATIONS: lambda: self.field_formatter.format_designations(
                value, infobox_field
            ),
            FieldType.AGE: lambda: self.field_formatter.format_age_field(
                value, infobox_field
            ),
            FieldType.SEPARATE_UNIT: lambda: self.field_formatter.format_separate_unit_field(
                value, unit, infobox_field
            ),
        }

        formatter = formatters.get(field_type, formatters[FieldType.SIMPLE])
        return formatter()

    def _handle_constellation_field(self, star: DataSourceStar) -> str:
        """Gère le champ constellation calculé"""
        if not (star.right_ascension and star.declination):
            return ""

        constellation = self.constellation_utils.get_constellation_UAI(
            star.right_ascension.value, star.declination.value
        )
        return f" | constellation = {constellation}\n"

    def _handle_carte_uai_field(self, star: DataSourceStar) -> str:
        """Gère le champ carte UAI calculé"""
        if not (star.right_ascension and star.declination):
            return ""
        carte_uai = self.constellation_utils.get_constellation_name(
            star.right_ascension.value, star.declination.value
        )
        return f" | carte UAI = {carte_uai}\n"
