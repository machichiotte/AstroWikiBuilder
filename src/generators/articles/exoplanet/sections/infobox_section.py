# src/generators/articles/exoplanet/sections/infobox_section.py

from dataclasses import replace

from src.constants.wikipedia_field_config import (
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
        exoplanet_with_ids = self._add_alternative_identifiers(exoplanet)
        mappings = InfoboxMapper.convert_exoplanet_to_infobox()

        for mapping in mappings:
            value = getattr(exoplanet_with_ids, mapping.source_attribute, None)
            field_block = self.inbox_field_formatter.process_field(
                value=value,
                mapping=mapping,
                notes_fields=IS_NOTES_FIELDS_EXOPLANET,
                wiki_reference=wiki_reference,
            )
            if field_block:
                lines.append(field_block)

        lines.append("}}")
        return "\n".join(lines)

    def _add_alternative_identifiers(self, exoplanet: Exoplanet) -> Exoplanet:
        """Ajoute les identifiants alternatifs à pl_altname."""
        alt_names = list(exoplanet.pl_altname) if exoplanet.pl_altname else []

        identifiers = [
            exoplanet.hd_name,
            exoplanet.hip_name,
            exoplanet.tic_id,
            exoplanet.gaia_id,
        ]

        for identifier in identifiers:
            if identifier:
                alt_names.append(identifier)

        return replace(exoplanet, pl_altname=alt_names if alt_names else None)
