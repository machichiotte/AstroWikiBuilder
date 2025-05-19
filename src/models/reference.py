from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class SourceType(Enum):
    NASA = "NASA"
    EPE = "EPE"  # Exoplanet.eu
    OEP = "OEP"  # Open Exoplanet Catalogue

@dataclass
class Reference:
    source: SourceType
    date: datetime
    url: str = None
    identifier: str = None

    def to_wiki_ref(self) -> str:
        """Convertit la référence en format wiki"""
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