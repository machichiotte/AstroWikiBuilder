# src/generators/articles/exoplanet/sections/host_star_section.py

from collections.abc import Callable

from src.models.entities.exoplanet_entity import Exoplanet
from src.utils.formatters.article_formatter import ArticleFormatter


class HostStarSection:
    def __init__(self, article_util: ArticleFormatter):
        self.article_util = article_util

        self.extractors: dict[str, Callable[[Exoplanet], str | None]] = {
            "spectral_type": self._extract_spectral_type,
            "mass": self._extract_mass,
            "metallicity": self._extract_metallicity,
            "age": self._extract_age,
        }

    def generate(self, exoplanet: Exoplanet) -> str:
        if not exoplanet.st_name:
            return ""

        content = ["== Étoile =="]

        # Description de l'étoile - adapter selon le type de système
        if exoplanet.sy_snum and exoplanet.sy_snum > 1 and exoplanet.cb_flag == 0:
            # Système multiple, planète non-circumbinaire
            intro = f"L'exoplanète orbite autour de l'une des étoiles du système [[{exoplanet.st_name}]]"
        else:
            # Système simple ou planète circumbinaire
            intro = f"L'exoplanète orbite autour de l'étoile [[{exoplanet.st_name}]]"

        characteristics = [
            extractor(exoplanet) for extractor in self.extractors.values() if extractor(exoplanet)
        ]

        if characteristics:
            if len(characteristics) == 1:
                intro += f", {characteristics[0]}"
            else:
                intro += f", {', '.join(characteristics[:-1])} et {characteristics[-1]}"

        intro += "."
        content.append(f"\n{intro}\n")

        return "\n".join(content)

    # ----- Extractors -----

    def _extract_spectral_type(self, exoplanet: Exoplanet) -> str | None:
        if exoplanet.st_spectral_type:
            return f"une étoile de type spectral {exoplanet.st_spectral_type}"
        return None

    def _extract_mass(self, exoplanet: Exoplanet) -> str | None:
        if exoplanet.st_mass and exoplanet.st_mass.value:
            mass_str = self.article_util.format_uncertain_value_for_article(exoplanet.st_mass)
            if mass_str:
                return f"d'une masse de {mass_str} [[Masse solaire|''M''{{{{ind|☉}}}}]]"
        return None

    def _extract_metallicity(self, exoplanet: Exoplanet) -> str | None:
        if exoplanet.st_metallicity and exoplanet.st_metallicity.value:
            met_str = self.article_util.format_uncertain_value_for_article(exoplanet.st_metallicity)
            if met_str:
                return f"d'une métallicité de {met_str} [Fe/H]"
        return None

    def _extract_age(self, exoplanet: Exoplanet) -> str | None:
        if exoplanet.st_age and exoplanet.st_age.value:
            age_str = self.article_util.format_uncertain_value_for_article(exoplanet.st_age)
            if age_str:
                return f"âgée de {age_str} [[milliard]]s d'années"
        return None
