from dataclasses import dataclass
from typing import Optional, Any
from src.models.references.reference import Reference


@dataclass
class DataPoint:
    """Classe pour stocker une valeur et sa référence"""

    value: Any
    reference: Optional[Reference] = None
    unit: Optional[str] = None  # Unité de mesure (ex: M_J, R_J, K, etc.)

    def to_wiki_value(self) -> str:
        """Convertit la valeur en format wiki avec sa référence"""
        if self.value is None:
            return None
        if self.reference:
            # Pour les noms alternatifs, on ne retourne que la valeur
            if hasattr(self, "_is_alternate_name") and self._is_alternate_name:
                return str(self.value)
            return f"{self.value} {self.reference.to_wiki_ref()}"
        return str(self.value)
