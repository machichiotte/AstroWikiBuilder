# src/models/references/reference.py
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


# Métadonnées et modèles d'URL pour chaque source
SOURCE_DETAILS = {
    SourceType.NEA: {
        "display_title": "NASA Exoplanet Archive",
        "url_pattern_star": "https://exoplanetarchive.ipac.caltech.edu/overview/{star_id}",
        "url_pattern_exo": "https://exoplanetarchive.ipac.caltech.edu/overview/{star_id}#planet_{planet_id}_collapsible",
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
    star_id: Optional[str] = None
    planet_id: Optional[str] = None

    def to_url(self) -> str:
        details: dict[str, str] | None = SOURCE_DETAILS.get(self.source)
        if not details:
            raise ValueError(f"Unknown source: {self.source}")

        if self.source == SourceType.NEA:
            star_id: str = slugify(self.star_id or "")
            planet_id: str = slugify(self.planet_id or "")
            if not star_id and not planet_id:
                raise ValueError(
                    "Both star name and planet identifier are required for NEA"
                )
            elif not planet_id:
                return details["url_pattern_star"].format(star_id=star_id)

            return details["url_pattern_exo"].format(
                star_id=star_id, planet_id=planet_id
            )

        if not planet_id:
            raise ValueError("Identifier is required for generating the URL")
        return details["url_pattern"].format(planet_id=planet_id)

    def to_wiki_ref(self, short: bool = True) -> str:
        """Convertit la référence en format wiki, avec option pour version courte"""
        details: dict[str, str] | None = SOURCE_DETAILS.get(self.source)
        if not details:
            return f'<ref name="{self.source.value}">Unknown source</ref>'

        name_str: str = ""
        if self.planet_id:
            name_str = self.planet_id
        else:
            name_str = self.star_id

        url: str = self.to_url()
        title: str = f"{details['display_title']}{' - ' + name_str if name_str else ''}"

        if short:
            return f'<ref name="{self.source.value}" />'

        tpl: str = details["template"].format(
            title=title,
            url=url,
            update_date=self.update_date.strftime("%Y-%m-%d"),
            consultation_date=self.consultation_date.strftime("%Y-%m-%d"),
        )

        return f'<ref name="{self.source.value}">{tpl}</ref>'
