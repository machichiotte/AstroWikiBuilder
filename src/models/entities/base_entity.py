from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class BaseEntity:
    """Classe de base pour toutes les entités"""

    name: Optional[str] = None
    alt_names: List[str] = field(default_factory=list)

    def get_primary_name(self) -> str:
        """Retourne le nom principal de l'entité"""
        return self.name

    def get_all_names(self) -> List[str]:
        """Retourne tous les noms de l'entité"""
        return [self.name] + self.alt_names
