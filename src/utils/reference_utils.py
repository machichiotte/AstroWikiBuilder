from typing import Dict, Set
from src.models.reference import SourceType, DataPoint

class ReferenceUtils:
    """
    Classe utilitaire pour la gestion des références dans les articles Wikipedia
    """
    def __init__(self):
        self.template_refs = {
            'nasa': "{{Lien web |langue=en |nom1=NasaGov |titre={title} |url=https://science.nasa.gov/exoplanet-catalog/{id}/ |site=science.nasa.gov |date=2024-11-1 |consulté le=2025-1-3 }}",
            'exoplanet_eu': "{{Lien web |langue=en |nom1=EPE |titre={title} |url=https://exoplanet.eu/catalog/{id}/ |site=exoplanet.eu |date=2024-8-1 |consulté le=2025-1-3 }}",
            'open_exoplanet': "{{Lien web |langue=en |nom1=OEC |titre={title} |url=https://github.com/OpenExoplanetCatalogue/open_exoplanet_catalogue |site=Open Exoplanet Catalogue |date=2024-1-1 |consulté le=2025-1-3 }}",
            'article': "{{Article |langue= |auteur= |titre= |périodique= |année= |volume= |numéro= |pages= |lire en ligne= |consulté le= }}",
            'ouvrage': "{{Ouvrage |langue= |auteur= |titre= |éditeur= |année= |pages totales= |passage= |isbn= |lire en ligne= |consulté le= }}"
        }
        self._used_refs: Set[str] = set()
        self._has_grouped_notes: bool = False

    def get_reference(self, source: str, title: str, id: str) -> str:
        """
        Retourne la référence formatée pour une source donnée
        """
        template = self.template_refs.get(source, "")
        return template.format(title=title, id=id)

    def add_reference(self, ref_name: str, ref_content: str) -> str:
        """
        Ajoute une référence et retourne la balise de référence appropriée.
        """
        if ref_name not in self._used_refs:
            self._used_refs.add(ref_name)
            if isinstance(ref_content, str) and 'group="note"' in ref_content.lower():
                self._has_grouped_notes = True
            return ref_content 
        return f'<ref name="{ref_name}" />'

    def format_datapoint(self, datapoint: DataPoint, exoplanet_name: str) -> str:
        """Formate un DataPoint pour l'affichage dans l'article"""
        if not datapoint or not datapoint.value:
            return ""
            
        try:
            value = float(datapoint.value)
            value_str = f"{value:.2f}"
        except (ValueError, TypeError):
            value_str = str(datapoint.value)
        
        if datapoint.reference:
            ref_name = str(datapoint.reference.source.value) if hasattr(datapoint.reference.source, 'value') else str(datapoint.reference.source)
            ref_content_full = datapoint.reference.to_wiki_ref(self.template_refs, exoplanet_name) 
            return f"{value_str} {self.add_reference(ref_name, ref_content_full)}"
            
        return value_str

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

    def reset_references(self):
        """Réinitialise les références pour un nouvel article"""
        self._used_refs = set()
        self._has_grouped_notes = False 