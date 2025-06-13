from datetime import datetime
from typing import Dict, Any
from src.models.references.reference import SourceType


class DataSourceExoplanet:
    """Classe pour stocker les données brutes d'une exoplanète depuis une source"""

    def __init__(
        self,
        name: str,
        source_type: SourceType,
        update_date: datetime,
        consultation_date: datetime,
        raw_data: Dict[str, Any],
        metadata: Dict[str, Any] = None,
    ):
        self.name = name
        self.source_type = source_type
        self.update_date = update_date
        self.consultation_date = consultation_date
        self.raw_data = raw_data
        self.metadata = metadata or {}
