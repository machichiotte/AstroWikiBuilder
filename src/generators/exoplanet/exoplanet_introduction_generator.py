# src/generators/exoplanet/exoplanet_introduction_generator.py
from typing import Optional

from src.constants.field_mappings import (
    CONSTELLATION_GENDER,
    SPECTRAL_TYPE_DESCRIPTIONS,
)
from src.models.entities.exoplanet import Exoplanet
from src.utils.astro.constellation_utils import ConstellationUtils
from src.utils.formatters.article_formatters import ArticleUtils

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

    # ============================================================================
    # UTILITAIRES DE DESCRIPTION ET FORMATAGE
    # ============================================================================
    def resolve_spectral_type_description(self, spectral_type: Optional[str]) -> str:
        """
        Génère une description formatée de l'étoile avec le type spectral.
        Retourne "[[description]]" ou "son étoile hôte" comme placeholder.
        """
        if not isinstance(spectral_type, str) or not spectral_type.strip():
            return "son étoile hôte"  # Placeholder if no spectral type

        spectral_class: str = spectral_type[0].upper()
        description: str | None = SPECTRAL_TYPE_DESCRIPTIONS.get(spectral_class)

        if description:
            return f"[[{description}]]"
        # Placeholder if spectral class not in map or description is None
        return "son étoile hôte"

    # ============================================================================
    # COMPOSITION DES SEGMENTS DE PHRASE
    # ============================================================================
    def compose_host_star_phrase(self, exoplanet: Exoplanet) -> Optional[str]:
        """Construit le segment de phrase concernant l'étoile hôte."""
        if not exoplanet.st_name:
            return None

        st_name: str = exoplanet.st_name

        star_type_description: str = self.resolve_spectral_type_description(
            exoplanet.st_spectral_type if exoplanet.st_spectral_type else None
        )

        if star_type_description != "son étoile hôte":
            # Suppose que star_type_description (ex: "[[naine jaune]]") est grammaticalement féminin
            # pour que "de la" soit correct, correspondant à l'hypothèse implicite du code original.
            return f" en orbite autour de la {star_type_description} {st_name}"
        else:
            # Gère correctement le placeholder "son étoile hôte".
            return f" en orbite autour de {star_type_description} {st_name}"

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
        if not exoplanet.st_constellation:
            return None

        constellation_name_fr = exoplanet.st_constellation
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
