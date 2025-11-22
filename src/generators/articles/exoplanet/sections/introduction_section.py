# src/generators/articles/exoplanet/sections/introduction_section.py

from src.models.entities.exoplanet_entity import Exoplanet
from src.utils.astro.classification.exoplanet_comparison_util import (
    ExoplanetComparisonUtil,
)
from src.utils.astro.classification.exoplanet_type_util import ExoplanetTypeUtil
from src.utils.astro.classification.star_type_util import StarTypeUtil
from src.utils.astro.constellation_util import ConstellationUtil
from src.utils.formatters.article_formatter import ArticleFormatter
from src.utils.lang.french_articles import (
    get_french_article_noun,
    guess_grammatical_gender,
)
from src.utils.lang.phrase.constellation import phrase_dans_constellation


class IntroductionSection:
    """Génère la section introduction pour les articles d'exoplanètes."""

    def __init__(self, comparison_util: ExoplanetComparisonUtil, article_util: ArticleFormatter):
        self.comparison_util = comparison_util
        self.article_util = article_util
        self.planet_type_util = ExoplanetTypeUtil()
        self.constellation_util = ConstellationUtil()
        self.star_type_util = StarTypeUtil()

    def _compose_host_star_phrase(self, exoplanet: Exoplanet) -> str | None:
        """Construit le segment de phrase concernant l'étoile hôte."""
        if not exoplanet.st_name:
            return None

        st_name: str = exoplanet.st_name
        star_type_descriptions: list[str] = (
            self.star_type_util.determine_star_types_from_properties(exoplanet)
        )

        if star_type_descriptions:
            desc = star_type_descriptions[0].strip()
            desc_clean = desc[0].lower() + desc[1:]
            genre = guess_grammatical_gender(desc_clean)
            article = get_french_article_noun(
                desc_clean, gender=genre, preposition="de", with_brackets=True
            )
            return f" en orbite autour {article} [[{st_name}]]"
        else:
            return f" en orbite autour de son étoile hôte [[{st_name}]]"

    def _compose_distance_phrase(self, exoplanet: Exoplanet) -> str | None:
        """Construit le segment de phrase concernant la distance."""
        if not exoplanet.st_distance or not exoplanet.st_distance.value:
            return None

        try:
            distance_pc = float(exoplanet.st_distance.value)
            distance_ly: float = self.article_util.convert_parsecs_to_lightyears(distance_pc)
            if distance_ly is not None:
                formatted_distance_ly = self.article_util.format_number_as_french_string(
                    distance_ly
                )
                return f", située à environ {formatted_distance_ly} [[année-lumière|années-lumière]] de la [[Terre]]"
        except (ValueError, TypeError):
            return None
        return None

    def _compose_constellation_phrase(self, exoplanet: Exoplanet) -> str | None:
        """Construit le segment de phrase concernant la constellation."""
        if not exoplanet.sy_constellation:
            return None

        constellation_name_fr = exoplanet.sy_constellation

        if constellation_name_fr:
            return phrase_dans_constellation(constellation_name_fr, True)

        return None

    def generate(self, exoplanet: Exoplanet) -> str:
        """Génère l'introduction pour une exoplanète."""
        planet_type = self.planet_type_util.determine_exoplanet_classification(exoplanet)
        planet_name_str = exoplanet.pl_name or "Nom inconnu"
        planet_type = planet_type[0].lower() + planet_type[1:]

        base_intro = f"'''{planet_name_str}''' est une exoplanète de type [[{planet_type}]]"

        parts = [base_intro]

        host_star_segment = self._compose_host_star_phrase(exoplanet)
        if host_star_segment:
            parts.append(host_star_segment)

        distance_segment = self._compose_distance_phrase(exoplanet)
        if distance_segment:
            parts.append(distance_segment)

        constellation_segment = self._compose_constellation_phrase(exoplanet)
        if constellation_segment:
            parts.append(f" {constellation_segment}")

        return "".join(parts) + "."
