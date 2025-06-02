# src/generators/star_infobox_generator_v2.py
from typing import Optional, Any
from src.models.exoplanet import Exoplanet, DataPoint
from src.mappers.exoplanet_mapping import (
    ExoplanetMappingConfig,
    FieldMapping,
    FieldType,
)
from src.formatters.field_formatters import FieldFormatter
from src.utils.star.star_utils import StarUtils
from src.formatters.format_utils import FormatUtils


class ExoplanetInfoboxGenerator:
    """Générateur d'infobox pour les exoplanète"""

    def __init__(self):
        self.format_utils = FormatUtils()
        self.star_utils = StarUtils(self.format_utils)
        self.field_formatter = FieldFormatter()
        self.mapping_config = ExoplanetMappingConfig()

    def generate_exoplanet_infobox(self, exoplanet: Exoplanet) -> str:
        """Génère le contenu de l'infobox Wikipédia pour une exoplanète"""
        if not isinstance(exoplanet, Exoplanet):
            raise TypeError("Input must be an Exoplanet object.")

        infobox = "{{Infobox Exoplanète\n"

        # Traiter tous les champs selon leur configuration
        for mapping in self.mapping_config.get_field_mappings():
            field_content = self._process_field(exoplanet, mapping)
            if field_content:
                infobox += field_content

        infobox += "}}\n"
        return infobox

    def _process_field(self, exoplanet: Exoplanet, mapping: FieldMapping) -> str:
        """Traite un champ selon sa configuration de mapping"""
        # Vérifier la condition si elle existe
        if mapping.condition and not mapping.condition(exoplanet):
            return ""

        # Gérer les champs calculés spéciaux
        if mapping.field_type == FieldType.CONSTELLATION:
            return self._handle_constellation_field(exoplanet)
        elif mapping.field_type == FieldType.CARTE_UAI:
            return self._handle_carte_uai_field(exoplanet)

        # Récupérer la valeur du champ
        value, unit = self._extract_field_value(exoplanet, mapping.star_attribute)

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
        self, exoplanet: Exoplanet, attribute_name: str
    ) -> tuple[Any, Optional[str]]:
        """Extrait la valeur et l'unité d'un attribut Exoplanet"""
        attr_dp = getattr(exoplanet, attribute_name, None)

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
            FieldType.SEPARATE_UNIT: lambda: self.field_formatter.format_separate_unit_field(
                value, unit, infobox_field
            ),
        }

        formatter = formatters.get(field_type, formatters[FieldType.SIMPLE])
        return formatter()

    def _handle_constellation_field(self, exoplanet: Exoplanet) -> str:
        """Gère le champ constellation calculé"""
        if not (exoplanet.right_ascension and exoplanet.declination):
            return ""

        constellation = self.star_utils.get_constellation_UAI(
            exoplanet.right_ascension.value, exoplanet.declination.value
        )
        return f" | constellation = {constellation}\n"

    def _handle_carte_uai_field(self, exoplanet: Exoplanet) -> str:
        """Gère le champ carte UAI calculé"""
        if not (exoplanet.right_ascension and exoplanet.declination):
            return ""

        carte_uai = self.star_utils.get_constellation_name(
            exoplanet.right_ascension.value, exoplanet.declination.value
        )
        return f" | carte UAI = {carte_uai}\n"
