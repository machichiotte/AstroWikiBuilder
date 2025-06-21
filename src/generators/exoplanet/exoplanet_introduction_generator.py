# src/generators/exoplanet/exoplanet_introduction_generator.py
from typing import List, Optional

from src.constants.field_mappings import (
    CONSTELLATION_GENDER,
)
from src.models.entities.exoplanet import Exoplanet
from src.utils.astro.constellation_utils import ConstellationUtils
from src.utils.formatters.article_formatters import ArticleUtils
from src.utils.astro.classification.star_type_utils import StarTypeUtils

from src.utils.astro.classification.exoplanet_comparison_utils import (
    ExoplanetComparisonUtils,
)
from src.utils.astro.classification.exoplanet_type_utils import ExoplanetTypeUtils


class ExoplanetIntroductionGenerator:
    """
    Classe pour générer l'introduction des articles d'exoplanètes.
    """

    # ============================================================================
    # INITIALISATION
    # ============================================================================
    def __init__(
        self, comparison_utils: ExoplanetComparisonUtils, article_utils: ArticleUtils
    ):
        self.comparison_utils: ExoplanetComparisonUtils = comparison_utils
        self.article_utils: ArticleUtils = article_utils
        self.planet_type_utils = ExoplanetTypeUtils()
        self.constellation_utils = ConstellationUtils()
        self.star_type_utils = StarTypeUtils()

    # ============================================================================
    # COMPOSITION DES SEGMENTS DE PHRASE
    # ============================================================================
    def compose_host_star_phrase(self, exoplanet: Exoplanet) -> Optional[str]:
        """Construit le segment de phrase concernant l'étoile hôte."""
        if not exoplanet.st_name:
            return None

        st_name: str = exoplanet.st_name
        star_type_descriptions: List[str] = (
            self.star_type_utils.determine_star_types_from_properties(exoplanet)
        )

        if star_type_descriptions:
            desc = star_type_descriptions[0].strip()
            desc_lower = desc.lower()

            # Déterminer l'article correct
            first_letter = desc_lower[0]
            voyelles = {"a", "e", "é", "i", "o", "u", "y", "h"}  # inclut h muet
            genre = self.guess_grammatical_gender(desc_lower)  # <- fonction à créer

            if genre == "f":
                article = "de l'" if first_letter in voyelles else "de la "
            elif genre == "m":
                article = "de l'" if first_letter in voyelles else "du "
            else:
                article = "de "
            desc = desc[0].lower() + desc[1:]

            return f" en orbite autour {article}[[{desc}]] [[{st_name}]]"
        else:
            return f" en orbite autour de son étoile hôte [[{st_name}]]"

    @staticmethod
    def guess_grammatical_gender(type_description: str) -> str:
        """
        Essaie de deviner le genre grammatical d’un type d’étoile.
        """
        feminine_keywords = ["naine", "étoile", "géante", "brune"]
        masculine_keywords = ["nain", "géant", "sous-nain", "subdwarf"]

        for f in feminine_keywords:
            if f in type_description:
                return "f"
        for m in masculine_keywords:
            if m in type_description:
                return "m"
        return "?"  # inconnu

    def compose_distance_phrase(self, exoplanet: Exoplanet) -> Optional[str]:
        """Construit le segment de phrase concernant la distance."""
        if not exoplanet.st_distance or not exoplanet.st_distance.value:
            return None

        try:
            distance_pc = float(exoplanet.st_distance.value)
            distance_ly: float = self.article_utils.convert_parsecs_to_lightyears(
                distance_pc
            )
            if distance_ly is not None:
                formatted_distance_ly = (
                    self.article_utils.format_number_as_french_string(distance_ly)
                )
                return f", située à environ {formatted_distance_ly} [[année-lumière|années-lumière]] de la [[Terre]]"
        except (ValueError, TypeError):
            # Gère les cas où distance.value n'est pas un nombre valide.
            return None
        return None

    def format_constellation_locative_phrase(
        self, constellation_french_name: str
    ) -> str:
        """Formate la partie de phrase "dans la constellation de/du/de l' X"."""
        genre = CONSTELLATION_GENDER.get(
            constellation_french_name, "m"
        )  # défaut masculin
        preposition = "de la" if genre == "f" else "du"

        if (
            genre == "m"
            and constellation_french_name
            and constellation_french_name[0].lower() in "aeiouéèêëàâäîïôöùûü"
        ):
            preposition = "de l'"

        if preposition.endswith("'"):
            return f"dans la constellation {preposition}{constellation_french_name}"
        else:
            return f"dans la constellation {preposition} {constellation_french_name}"

    def compose_constellation_phrase(self, exoplanet: Exoplanet) -> Optional[str]:
        """Construit le segment de phrase concernant la constellation."""
        if not exoplanet.sy_constellation:
            return None

        constellation_name_fr = exoplanet.sy_constellation
        if constellation_name_fr:
            return self.format_constellation_locative_phrase(constellation_name_fr)
        return None

    # ============================================================================
    # GÉNÉRATION DE L'INTRODUCTION
    # ============================================================================
    def compose_exoplanet_introduction(self, exoplanet: Exoplanet) -> str:
        """
        Génère l'introduction pour une exoplanète.
        """
        planet_type = self.planet_type_utils.determine_exoplanet_classification(
            exoplanet
        )
        # planet_type est supposé être une chaîne comme "Jupiter chaud", pour être utilisé dans "[[Jupiter chaud]]"

        planet_name_str = exoplanet.pl_name or "Nom inconnu"

        planet_type = planet_type[0].lower() + planet_type[1:]

        base_intro = (
            f"'''{planet_name_str}''' est une exoplanète de type [[{planet_type}]]"
        )

        parts = [base_intro]

        host_star_segment = self.compose_host_star_phrase(exoplanet)
        if host_star_segment:
            parts.append(host_star_segment)

        distance_segment = self.compose_distance_phrase(exoplanet)
        if distance_segment:
            parts.append(distance_segment)

        constellation_segment = self.compose_constellation_phrase(exoplanet)
        if constellation_segment:
            parts.append(
                f" {constellation_segment}"
            )  # Espace initial comme dans la concaténation originale

        return "".join(parts) + "."
