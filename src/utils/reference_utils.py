from typing import Set, List
from src.models.reference import DataPoint
from src.models.exoplanet import Exoplanet
from src.models.reference import SourceType

class ReferenceUtils:
    """
    Classe utilitaire pour la gestion des références dans les articles Wikipedia
    """
    def __init__(self):
        self.template_refs = {
            'nasa': "{{Lien web |langue=en |nom1=NEA |titre={title} |url=https://science.nasa.gov/exoplanet-catalog/{id}/ |site=science.nasa.gov |date=2024-11-1 |consulté le=2025-1-3 }}",
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

    def reset_references(self):
        """Réinitialise les références pour un nouvel article"""
        self._used_refs = set()
        self._has_grouped_notes = False
        
    def get_used_references(self, exoplanet: Exoplanet) -> List[str]:
        """
        Retourne la liste des références utilisées pour l'exoplanète
        """
        refs = set()
        
        # Parcourir tous les attributs de l'exoplanète
        for field_name in exoplanet.__dataclass_fields__:
            if field_name == 'name' or field_name == 'other_names':
                continue
                
            value = getattr(exoplanet, field_name)
            if value and hasattr(value, 'reference') and value.reference:
                if isinstance(value.reference.source, SourceType):
                    refs.add(value.reference.source.value)
        
        # Si aucune référence n'a été trouvée, ajouter au moins NEA par défaut
        # Ne rien ajouter si pas de référence
            
        return list(refs)
