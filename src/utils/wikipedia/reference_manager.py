# src/utils/reference_manager.py
from datetime import datetime
from typing import Optional, Dict
from src.models.reference import SOURCE_DETAILS, Reference, SourceType


class ReferenceManager:
    """
    Gère la création et le suivi des Reference.
    """

    def __init__(self):
        # Pour gérer les références répétées
        self._used_refs: set[str] = set()
        # Templates MediaWiki unifiées (clé = valeur de SourceType)
        self.template_refs: Dict[str, str] = {
            src.value: details["template"] for src, details in SOURCE_DETAILS.items()
        }

    def create_reference(
        self,
        source: SourceType,
        update_date: datetime,
        planet_identifier: Optional[str] = None,
        star_identifier: Optional[str] = None,
    ) -> Reference:
        """
        Crée et renvoie une Reference avec date de consultation actuelle.
        """
        return Reference(
            source=source,
            update_date=update_date,
            consultation_date=datetime.now(),
            planet_identifier=planet_identifier,
            star_identifier=star_identifier,
        )

    def add_reference(self, ref_name: str, ref_content: str) -> str:
        """
        Retourne la balise <ref> complète la première fois,
        ou la référence courte (<ref name="..." />) ensuite.
        """
        if ref_name not in self._used_refs:
            self._used_refs.add(ref_name)
            if ref_content.startswith("<ref") and ref_content.endswith("</ref>"):
                return ref_content
            return f'<ref name="{ref_name}" >{ref_content}</ref>'
        return f'<ref name="{ref_name}" />'

    def reset_references(self):
        """
        Réinitialise le suivi des références.
        """
        self._used_refs.clear()
