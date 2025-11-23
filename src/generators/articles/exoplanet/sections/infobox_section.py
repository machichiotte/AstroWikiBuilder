# src/generators/articles/exoplanet/sections/infobox_section.py

from src.constants.wikipedia_field_config import (
    DEFAULT_WIKIPEDIA_UNITS_EXOPLANET,
    IS_NOTES_FIELDS_EXOPLANET,
)
from src.models.entities.exoplanet_entity import Exoplanet
from src.models.infobox_fields import InfoboxMapper
from src.services.processors.reference_manager import ReferenceManager
from src.utils.astro.constellation_util import ConstellationUtil
from src.utils.formatters.article_formatter import ArticleFormatter
from src.utils.formatters.infobox_field_formatter import InboxFieldFormatter


class InfoboxSection:
    """Génère l'infobox pour les articles d'exoplanètes."""

    def __init__(self, reference_manager: ReferenceManager):
        self.reference_manager = reference_manager
        self.inbox_field_formatter = InboxFieldFormatter()
        self.article_util = ArticleFormatter()
        self.constellation_util = ConstellationUtil()

    def generate(self, exoplanet: Exoplanet) -> str:
        """Génère le code wiki de l'infobox."""
        lines = ["{{Infobox Exoplanète"]

        wiki_reference = exoplanet.reference.to_wiki_ref() if exoplanet.reference else None

        # Récupération des mappings spécifiques aux exoplanètes
        mappings = InfoboxMapper.convert_exoplanet_to_infobox()

        for mapping in mappings:
            value = getattr(exoplanet, mapping.source_attribute, None)

            field_block = self.inbox_field_formatter.process_field(
                value=value,
                mapping=mapping,
                notes_fields=IS_NOTES_FIELDS_EXOPLANET,
                wiki_reference=wiki_reference,
            )
            if field_block:
                lines.append(field_block)

        # Ajout des références globales
        for full_ref in self.reference_manager.all_registered_references.values():
            lines.append(full_ref)

        lines.append("}}")
        return "\n".join(lines)

    @property
    def default_field_mapping(self):
        return DEFAULT_WIKIPEDIA_UNITS_EXOPLANET
