# src/models/reference.py
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, Optional

class SourceType(Enum):
    NASA = "NasaGov"
    EPE = "EPE"  # Exoplanet.eu
    OEC = "OEC"  # Open Exoplanet Catalogue

@dataclass
class Reference:
    source: SourceType
    update_date: datetime  # Date de mise à jour des données
    consultation_date: datetime  # Date de consultation/génération
    url: Optional[str] = None
    identifier: Optional[str] = None

    def to_wiki_ref(self, template_refs: Dict[str, str] = None, exoplanet_name: str = None) -> str:
        """Convertit la référence en format wiki"""
        if template_refs and exoplanet_name:
            template = template_refs.get(str(self.source.value).lower(), "")
            if template:
                # Formater les dates pour le template
                update_date_str = self.update_date.strftime("%Y-%m-%d")
                consultation_date_str = self.consultation_date.strftime("%Y-%m-%d")
                
                content = template.format(
                    title=exoplanet_name,
                    id=exoplanet_name.lower().replace(" ", "-"),
                    update_date=update_date_str,
                    consultation_date=consultation_date_str
                )
                return f"<ref name=\"{self.source.value}\">{content}</ref>"
        return f"<ref name=\"{self.source.value}\"/>"

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