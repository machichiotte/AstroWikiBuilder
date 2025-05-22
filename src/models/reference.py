# src/models/reference.py
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict

class SourceType(Enum):
    NASA = "NasaGov"
    EPE = "EPE"  # Exoplanet.eu
    OEC = "OEC"  # Open Exoplanet Catalogue

@dataclass
class Reference:
    source: SourceType
    date: datetime
    url: str = None
    identifier: str = None

    def to_wiki_ref(self, template_refs: Dict[str, str] = None, exoplanet_name: str = None) -> str:
        """Convertit la référence en format wiki"""
        if template_refs and exoplanet_name:
            template = template_refs.get(str(self.source.value).lower(), "")
            if template:
                content = template.format(title=exoplanet_name, id=exoplanet_name.lower().replace(" ", "-"))
                return f"<ref name=\"{self.source.value}\">{content}</ref>"
        return f"<ref name=\"{self.source.value}\"/>"

@dataclass
class DataPoint:
    """Classe pour stocker une valeur et sa référence"""
    value: any
    reference: Reference = None

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