# src/utils/reference_manager.py
from datetime import datetime
from typing import Optional
from src.models.reference import Reference, SourceType


class ReferenceManager:
    """
    Classe pour gérer les références et leurs dates de mise à jour
    """

    def __init__(self):
        self.template_refs = {
            "nasa": "{{Lien web |langue=en |nom1=NEA |titre={title} |url=https://science.nasa.gov/exoplanet-catalog/{id}/ |site=science.nasa.gov |date={update_date} |consulté le={consultation_date} }}",
            "exoplanet_eu": "{{Lien web |langue=en |nom1=EPE |titre={title} |url=https://exoplanet.eu/catalog/{id}/ |site=exoplanet.eu |date={update_date} |consulté le={consultation_date} }}",
            "open_exoplanet": "{{Lien web |langue=en |nom1=OEC |titre={title} |url=https://github.com/OpenExoplanetCatalogue/open_exoplanet_catalogue |site=Open Exoplanet Catalogue |date={update_date} |consulté le={consultation_date} }}",
            "article": "{{Article |langue= |auteur= |titre= |périodique= |année= |volume= |numéro= |pages= |lire en ligne= |consulté le={consultation_date} }}",
            "ouvrage": "{{Ouvrage |langue= |auteur= |titre= |éditeur= |année= |pages totales= |passage= |isbn= |lire en ligne= |consulté le={consultation_date} }}",
        }
        self._used_refs: set[str] = set()
        self._has_grouped_notes: bool = False
        self._unit_mapping = {
            "R_J": "M_J",  # Rayon jovien -> Masse jovienne
            "R_E": "M_E",  # Rayon terrestre -> Masse terrestre
            "R_S": "M_S",  # Rayon solaire -> Masse solaire
        }

    def get_mass_unit_from_radius_unit(self, radius_unit: str) -> str:
        """
        Retourne l'unité de masse correspondante à une unité de rayon
        """
        return self._unit_mapping.get(radius_unit, "M_J")  # Par défaut, on utilise M_J

    def create_reference(
        self,
        source: SourceType,
        update_date: datetime,
        url: Optional[str] = None,
        identifier: Optional[str] = None,
    ) -> Reference:
        """
        Crée une nouvelle référence avec les dates de mise à jour et de consultation
        """
        return Reference(
            source=source,
            update_date=update_date,
            consultation_date=datetime.now(),
            url=url,
            identifier=identifier,
        )

    def add_reference(self, ref_name: str, ref_content: str) -> str:
        """
        Ajoute une référence et retourne la balise de référence appropriée.
        Si c'est la première occurrence, retourne la référence complète.
        Sinon, retourne une référence courte.
        """
        if ref_name not in self._used_refs:
            self._used_refs.add(ref_name)
            # Vérifier si le contenu est déjà encapsulé dans une balise ref
            if ref_content.startswith("<ref") and ref_content.endswith("</ref>"):
                return ref_content
            # S'assurer que le contenu est correctement formaté avec les espaces
            return f'<ref name="{ref_name}" >{ref_content}</ref>'
        return f'<ref name="{ref_name}" />'

    def reset_references(self):
        """Réinitialise les références pour un nouvel article"""
        self._used_refs = set()
        self._has_grouped_notes = False

    def format_references_section(self) -> str:
        """
        Génère la section "Notes et références" avec les sous-sections
        "Notes" et "Références"
        """
        notes_section = ""
        if self._has_grouped_notes:
            notes_section = """=== Notes ===
{{références|groupe="note"}}
"""

        return f"""
== Notes et références ==
{notes_section}
=== Références ===
{{Références}}
"""
