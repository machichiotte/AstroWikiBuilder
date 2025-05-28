# src/models/reference.py
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, Optional


class SourceType(Enum):
    NEA = "NEA"  # Nasa Exoplanet Archive
    EPE = "EPE"  # Exoplanet.eu
    OEC = "OEC"  # Open Exoplanet Catalogue


SOURCE_DETAILS = {
    SourceType.NEA: {
        "name": "NEA",
        "display_title": "NASA Exoplanet Archive",
        "base_url": "https://science.nasa.gov/exoplanet-catalog/",
        "site": "science.nasa.gov",
    },
    SourceType.EPE: {
        "name": "EPE",
        "display_title": "Exoplanet.eu",
        "base_url": "http://exoplanet.eu/catalog/",  # Fictional URL, replace with actual
        "site": "exoplanet.eu",
    },
    SourceType.OEC: {
        "name": "OEC",
        "display_title": "Open Exoplanet Catalogue",
        "base_url": "http://www.openexoplanetcatalogue.com/planet/",  # Fictional URL
        "site": "openexoplanetcatalogue.com",
    },
}


@dataclass
class Reference:
    source: SourceType
    update_date: datetime  # Date de mise à jour des données
    consultation_date: datetime  # Date de consultation/génération
    url: Optional[str] = None
    identifier: Optional[str] = None

    def to_wiki_ref(
        self,
        template_refs: Optional[Dict[str, str]] = None,
        exoplanet_name: Optional[str] = None,
    ) -> str:
        source_info = SOURCE_DETAILS.get(self.source)
        if not source_info:
            # Fallback or error for unknown source
            return (
                f'<ref name="{self.source.value}">Error: Unknown source details</ref>'
            )

        # Construct URL; this might need to be more flexible based on source
        # For NEA, it's exoplanet_name.lower().replace(" ", "-")
        # Other sources might have different ID formats.
        # You might need a specific URL formatting function or pattern per source.
        specific_id_part = (
            exoplanet_name.lower().replace(" ", "-") if exoplanet_name else ""
        )
        if self.source == SourceType.EPE and exoplanet_name:
            specific_id_part = exoplanet_name  # E.g., EPE might use the name directly
        # Add more conditions for other sources if their URL structure for identifiers differs

        full_url = (
            f"{source_info['base_url']}{specific_id_part}"
            if exoplanet_name
            else source_info["base_url"]
        )
        if self.url:  # If a specific URL is already provided in the Reference object
            full_url = self.url

        title_suffix = f" - {exoplanet_name}" if exoplanet_name else ""
        full_title = f"{source_info['display_title']}{title_suffix}"

        if template_refs and exoplanet_name:
            template_key = str(self.source.value).lower()
            template = template_refs.get(template_key, "")
            if template:
                # Ensure your templates can handle dynamic titles, ids, etc.
                # The current template example is hardcoded for NEA title.
                # You might need to adjust what {title} and {id} mean in the template context.
                return template.format(
                    # This title is still NEA specific in your original example template
                    # You'd need to make the template itself more generic or have source-specific templates
                    title=full_title,  # Use the dynamically generated title
                    id=self.identifier
                    if self.identifier
                    else specific_id_part,  # Use provided ID or generate one
                    update_date=self.update_date.strftime("%Y-%m-%d"),
                    consultation_date=self.consultation_date.strftime("%Y-%m-%d"),
                )

        # Default format with {{Lien web}}
        ref_content = f"""{{{{Lien web |langue=en |nom1={source_info["name"]}|titre={full_title}
 |url={full_url} |site={source_info["site"]}
 |date={self.update_date.strftime("%Y-%m-%d")} |consulté le={self.consultation_date.strftime("%Y-%m-%d")} }}}}"""

        ref_name_attr = self.identifier if self.identifier else self.source.value
        # If you want to include exoplanet_name in ref name for uniqueness:
        # ref_name_attr = f"{self.source.value}_{exoplanet_name.replace(' ','_')}" if exoplanet_name else self.source.value

        return f'<ref name="{ref_name_attr}" >{ref_content}</ref>'


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
