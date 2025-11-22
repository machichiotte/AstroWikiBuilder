from src.constants.wikipedia_field_config import (
    DEFAULT_WIKIPEDIA_UNITS_STAR,
    IS_NOTES_FIELDS_STAR,
)
from src.models.entities.star_entity import Star
from src.models.infobox_fields import InfoboxMapper
from src.services.processors.reference_manager import ReferenceManager
from src.utils.formatters.infobox_field_formatter import InboxFieldFormatter


class InfoboxSection:
    """
    Génère l'infobox pour les articles d'étoiles.
    """

    def __init__(self, reference_manager: ReferenceManager):
        self.reference_manager = reference_manager
        self.inbox_field_formatter = InboxFieldFormatter()

    def generate(self, star: Star) -> str:
        """Génère le code wiki de l'infobox."""
        lines = ["{{Infobox Étoile"]

        wiki_reference = star.reference.to_wiki_ref() if star.reference else None

        # Récupération des mappings spécifiques aux étoiles
        mappings = InfoboxMapper.convert_star_to_infobox()

        for mapping in mappings:
            value = getattr(star, mapping.source_attribute, None)

            field_block = self.inbox_field_formatter.process_field(
                value=value,
                mapping=mapping,
                notes_fields=IS_NOTES_FIELDS_STAR,
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
        return DEFAULT_WIKIPEDIA_UNITS_STAR
