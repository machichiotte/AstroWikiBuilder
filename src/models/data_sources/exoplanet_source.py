from datetime import datetime
from typing import Dict, Any, Optional
from src.models.references.reference import Reference, SourceType


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

    def _parse_date(self, date_str: Optional[str]) -> Optional[datetime]:
        """Parse une date depuis une chaîne de caractères"""
        if not date_str:
            return None
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            return None
