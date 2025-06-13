from dataclasses import dataclass, field
from typing import Dict, Any
from datetime import datetime
from src.models.entities.star import Star
from src.models.references.reference import Reference, SourceType


@dataclass
class DataSourceStar:
    """Classe pour stocker les données brutes d'une étoile depuis une source"""

    name: str
    source_type: SourceType
    update_date: datetime
    consultation_date: datetime
    raw_data: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_star(self) -> Star:
        """Convertit les données brutes en objet Star"""
        star = Star(
            name=self.raw_data.get("st_name", ""),
            alt_names=self.raw_data.get("alt_names", []),
            spectral_type=self.raw_data.get("st_spectral_type"),
            metadata=self.metadata,
        )

        # Ajouter la référence
        reference = Reference(
            source=self.source_type,
            update_date=self.update_date,
            consultation_date=self.consultation_date,
            star_id=self.raw_data.get("star_id"),
        )
        star.add_reference(reference)

        return star
