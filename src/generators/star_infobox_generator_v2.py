# src/generators/star_infobox_generator_v2.py
from typing import Optional, Any
from src.models.star import Star, DataPoint
from src.mappers.star_mapping import StarMappingConfig, FieldMapping, FieldType
from src.formatters.field_formatters import FieldFormatter
from src.utils.star.star_utils import StarUtils
from src.formatters.format_utils import FormatUtils


class StarInfoboxGenerator:
    """Générateur d'infobox pour les étoiles - Version refactorisée"""

    def __init__(self):
        self.format_utils = FormatUtils()
        self.star_utils = StarUtils(self.format_utils)
        self.field_formatter = FieldFormatter()
        self.mapping_config = StarMappingConfig()

    def generate_star_infobox(self, star: Star) -> str:
        """Génère le contenu de l'infobox Wikipédia pour une étoile"""
        if not isinstance(star, Star):
            raise TypeError("Input must be a Star object.")

        infobox = "{{Infobox Étoile\n"

        # Traiter tous les champs selon leur configuration
        for mapping in self.mapping_config.get_field_mappings():
            field_content = self._process_field(star, mapping)
            if field_content:
                infobox += field_content

        infobox += "}}\n"
        return infobox

    def _process_field(self, star: Star, mapping: FieldMapping) -> str:
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
        self, star: Star, attribute_name: str
    ) -> tuple[Any, Optional[str]]:
        """Extrait la valeur et l'unité d'un attribut Star"""
        attr_dp = getattr(star, attribute_name, None)

        if attr_dp is None:
            return None, None

        if isinstance(attr_dp, DataPoint):
            return attr_dp.value, attr_dp.unit

        return attr_dp, None

    def _is_valid_value(self, value: Any) -> bool:
        """Vérifie si une valeur est valide pour l'affichage"""
        if value is None:
            return False
        if isinstance(value, str) and not value.strip():
            return False
        if isinstance(value, list) and not any(str(v).strip() for v in value):
            return False
        return True

    def _format_by_type(
        self, value: Any, unit: Optional[str], infobox_field: str, field_type: FieldType
    ) -> str:
        """Formate une valeur selon son type de champ"""
        formatters = {
            FieldType.SIMPLE: lambda: self.field_formatter.format_simple_field(
                value, unit, infobox_field
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

    def _handle_constellation_field(self, star: Star) -> str:
        """Gère le champ constellation calculé"""
        if not (star.right_ascension and star.declination):
            return ""

        constellation = self.star_utils.get_constellation_UAI(
            star.right_ascension.value, star.declination.value
        )
        return f" | constellation = {constellation}\n"

    def _handle_carte_uai_field(self, star: Star) -> str:
        """Gère le champ carte UAI calculé"""
        if not (star.right_ascension and star.declination):
            return ""

        carte_uai = self.star_utils.get_constellation_name(
            star.right_ascension.value, star.declination.value
        )
        return f" | carte UAI = {carte_uai}\n"
