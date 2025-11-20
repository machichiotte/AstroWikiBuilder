# src/services/reference_manager.py
from datetime import datetime

from src.models.references.reference import SOURCE_DETAILS, Reference, SourceType


class ReferenceManager:
    """
    Gère la création et le suivi des Reference.
    """

    def __init__(self):
        # Pour gérer les références répétées
        self._reference_registry: set[str] = set()
        self._ref_contents: dict[str, str] = {}
        self.template_refs: dict[str, str] = {
            src.value: details["template"] for src, details in SOURCE_DETAILS.items()
        }

    def create_reference(
        self,
        source: SourceType,
        update_date: datetime,
        planet_id: str | None = None,
        star_id: str | None = None,
    ) -> Reference:
        """
        Crée et renvoie une Reference avec date de consultation actuelle.
        """
        return Reference(
            source=source,
            update_date=update_date,
            consultation_date=datetime.now(),
            planet_id=planet_id,
            star_id=star_id,
        )

    def format_or_reuse_reference(self, reference_key: str, content: str) -> str:
        """
        Retourne la balise <ref> complète la première fois,
        ou la référence courte (<ref name="..." />) ensuite.
        """
        if reference_key not in self._reference_registry:
            self._reference_registry.add(reference_key)
            if content.startswith("<ref") and content.endswith("</ref>"):
                return content
            return f'<ref name="{reference_key}" >{content}</ref>'
        return f'<ref name="{reference_key}" />'

    def clear_all(self) -> None:
        """
        Réinitialise l’état du manager (utile entre deux articles).
        """
        self._used_reference_keys.clear()
        self._reference_registry.clear()

    @property
    def all_registered_references(self) -> dict[str, str]:
        """
        Expose le dictionnaire ref_name → contenu complet de chaque référence,
        tel que stocké dans _ref_contents.
        """
        return self._ref_contents
