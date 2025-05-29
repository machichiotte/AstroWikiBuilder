# src/models/reference.py
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional
import re


def slugify(name: str) -> str:
    """Convertit un nom d'exoplanète en identifiant d'URL propre"""
    return re.sub(r"\s+", "-", name.strip().lower())


class SourceType(Enum):
    NEA = "NEA"
    EPE = "EPE"
    OEC = "OEC"


# je me suis trompé d'url pour NEA
# https://exoplanetarchive.ipac.caltech.edu/overview/Kepler-100#planet_Kepler-100-b_collapsible
# https://exoplanetarchive.ipac.caltech.edu/overview/{star}#planet_{planet}_collapsible

# Métadonnées et modèles d'URL pour chaque source
SOURCE_DETAILS = {
    SourceType.NEA: {
        "display_title": "NASA Exoplanet Archive",
        # Modifié: retrait du slash final pour correspondre à l'URL désirée
        "url_pattern": "https://exoplanetarchive.ipac.caltech.edu/overview/{star_id}#planet_{planet_id}_collapsible",
        "site": "science.nasa.gov",
        "wiki_pipe": "nom1=NEA",
        "template": "{{{{Lien web|langue=en|nom1=NEA|titre={title}|url={url}|site=science.nasa.gov|date={update_date}|consulté le={consultation_date}}}}}",
    },
    SourceType.EPE: {
        "display_title": "Exoplanet.eu",
        "url_pattern": "http://exoplanet.eu/catalog/{planet_id}/",
        "site": "exoplanet.eu",
        "wiki_pipe": "nom1=EPE",
        "template": "{{{{Lien web|langue=en|nom1=EPE|titre={title}|url={url}|site=exoplanet.eu|date={update_date}|consulté le={consultation_date}}}}}",
    },
    SourceType.OEC: {
        "display_title": "Open Exoplanet Catalogue",
        "url_pattern": "http://www.openexoplanetcatalogue.com/planet/{planet_id}/",
        "site": "openexoplanetcatalogue.com",
        "wiki_pipe": "nom1=OEC",
        "template": "{{{{Lien web|langue=en|nom1=OEC|titre={title}|url={url}|site=openexoplanetcatalogue.com|date={update_date}|consulté le={consultation_date}}}}}",
    },
}


@dataclass
class Reference:
    source: SourceType
    update_date: datetime
    consultation_date: datetime
    planet_identifier: Optional[str] = None
    star_identifier: Optional[str] = None

    def to_url(self, fallback_name: Optional[str] = None) -> str:
        details = SOURCE_DETAILS.get(self.source)
        if not details:
            raise ValueError(f"Unknown source: {self.source}")

        if self.source == SourceType.NEA:
            star_id = slugify(self.star_identifier or fallback_name or "")
            planet_id = slugify(self.planet_identifier or fallback_name or "")
            if not star_id or not planet_id:
                raise ValueError(
                    "Both star name and planet identifier are required for NEA"
                )
            return details["url_pattern"].format(star_id=star_id, planet_id=planet_id)

        planet_id = self.identifier or (
            slugify(fallback_name) if fallback_name else None
        )
        if not planet_id:
            raise ValueError("Identifier is required for generating the URL")
        return details["url_pattern"].format(planet_id=planet_id)

    def to_wiki_ref(self, exoplanet_name: Optional[str] = None) -> str:
        details = SOURCE_DETAILS.get(self.source)
        if not details:
            return f'<ref name="{self.source.value}">Unknown source</ref>'

        url = self.to_url(fallback_name=exoplanet_name)
        title = f"{details['display_title']}{' - ' + exoplanet_name if exoplanet_name else ''}"

        tpl = details["template"].format(
            title=title,
            url=url,
            update_date=self.update_date.strftime("%Y-%m-%d"),
            consultation_date=self.consultation_date.strftime("%Y-%m-%d"),
        )

        return f'<ref name="{self.source.value}" >{tpl}</ref>'


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
            if hasattr(self, "_is_alternate_name") and self._is_alternate_name:
                return str(self.value)
            return f"{self.value} {self.reference.to_wiki_ref()}"
        return str(self.value)
