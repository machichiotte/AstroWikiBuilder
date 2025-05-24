# src/models/reference.py
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, Optional

class SourceType(Enum):
    NEA = "NEA" # Nasa Exoplanet Archive
    EPE = "EPE"  # Exoplanet.eu
    OEC = "OEC"  # Open Exoplanet Catalogue

@dataclass
class Reference:
    source: SourceType
    update_date: datetime  # Date de mise à jour des données
    consultation_date: datetime  # Date de consultation/génération
    url: Optional[str] = None
    identifier: Optional[str] = None

    def to_wiki_ref(self, template_refs: Optional[Dict[str, str]] = None, exoplanet_name: Optional[str] = None) -> str:
        """
        Convertit la référence en format wiki.
        Si un template et un nom d'exoplanète sont fournis, utilise le template.
        Sinon, utilise le format {{Lien web}} par défaut.
        """
        if template_refs and exoplanet_name:
            template = template_refs.get(str(self.source.value).lower(), "")
            if template:
                return template.format(
                    title=f"NASA Exoplanet Archive - {exoplanet_name}",
                    id=exoplanet_name.lower().replace(" ", "-"),
                    update_date=self.update_date.strftime("%Y-%m-%d"),
                    consultation_date=self.consultation_date.strftime("%Y-%m-%d")
                )
        
        # Format par défaut avec {{Lien web}}
        ref_content = f"""{{{{Lien web |langue=en |nom1=NEA|titre=NASA Exoplanet Archive{f" - {exoplanet_name}" if exoplanet_name else ""}
  |url=https://science.nasa.gov/exoplanet-catalog/{exoplanet_name.lower().replace(" ", "-") if exoplanet_name else ""} |site=science.nasa.gov
  |date={self.update_date.strftime("%Y-%m-%d")} |consulté le={self.consultation_date.strftime("%Y-%m-%d")} }}}}"""
        
        # Encapsuler dans les balises ref
        return f'<ref name="{self.source.value}" >{ref_content}</ref>'

@dataclass
class DataPoint:
    """Classe pour stocker une valeur et sa référence"""
    value: any
    reference: Reference = None
    unit: str = None  # Unité de mesure (ex: M_J, R_J, K, etc.)

    def to_wiki_value(self) -> str:
        """Convertit la valeur en format wiki avec sa référence"""
        if self.value is None:
            return None
        if self.reference:
            # Pour les noms alternatifs, on ne retourne que la valeur
            if hasattr(self, '_is_alternate_name') and self._is_alternate_name:
                return str(self.value)
            return f"{self.value} {self.reference.to_wiki_ref()}"
        return str(self.value) 