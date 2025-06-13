from dataclasses import dataclass, field
from typing import Dict, Any
from datetime import datetime
from src.models.references.reference import SourceType


@dataclass
class DataSourceStar:
    """Classe pour stocker les données brutes d'une étoile depuis une source"""

    name: str
    source_type: SourceType
    update_date: datetime
    consultation_date: datetime
    raw_data: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
