# src/generators/exoplanet/exoplanet_introduction_generator.py
from typing import Optional  # Ajouté Optional

from src.constants.field_mappings import (
    CONSTELLATION_GENDER,
    SPECTRAL_TYPE_DESCRIPTIONS,
)
from src.models.data_source_exoplanet import DataSourceExoplanet
from src.utils.constellation_utils import ConstellationUtils
from src.utils.formatters.article_formatters import ArticleUtils

from src.utils.exoplanet_comparison_utils import ExoplanetComparisonUtils
from src.utils.exoplanet_type_utils import ExoplanetTypeUtils


class ExoplanetIntroductionGenerator:
    """
    Classe pour générer l'introduction des articles d'exoplanètes.
    """

    def __init__(
        self, comparison_utils: ExoplanetComparisonUtils, article_utils: ArticleUtils
    ):
        self.comparison_utils = comparison_utils
        self.article_utils = article_utils
        self.planet_type_utils = ExoplanetTypeUtils()
        self.constellation_utils = ConstellationUtils()

    def _get_exoplanet_spectral_type_formatted_description(
        self, spectral_type: Optional[str]
    ) -> str:
        """
        Génère une description formatée de l'étoile avec le type spectral.
        Retourne "[[description]]" ou "son étoile hôte" comme placeholder.
        """
        if not isinstance(spectral_type, str) or not spectral_type.strip():
            return "son étoile hôte"  # Placeholder if no spectral type

        spectral_class = spectral_type[0].upper()
        description = SPECTRAL_TYPE_DESCRIPTIONS.get(spectral_class)

        if description:
            return f"[[{description}]]"
        # Placeholder if spectral class not in map or description is None
        return "son étoile hôte"

    def _build_host_star_segment(self, exoplanet: DataSourceExoplanet) -> Optional[str]:
        """Construit le segment de phrase concernant l'étoile hôte."""
        if not (
            exoplanet.st_name
            and hasattr(exoplanet.st_name, "value")
            and exoplanet.st_name.value
        ):
            return None

        host_star_name = exoplanet.st_name.value

        star_type_description = self._get_exoplanet_spectral_type_formatted_description(
            exoplanet.st_spectral_type.value
            if exoplanet.st_spectral_type and hasattr(exoplanet.st_spectral_type, "value")
            else None
        )

        if star_type_description != "son étoile hôte":
            # Suppose que star_type_description (ex: "[[naine jaune]]") est grammaticalement féminin
            # pour que "de la" soit correct, correspondant à l'hypothèse implicite du code original.
            return f" en orbite autour de la {star_type_description} {host_star_name}"
        else:
            # Gère correctement le placeholder "son étoile hôte".
            return f" en orbite autour de {star_type_description} {host_star_name}"

    def _build_distance_segment(self, exoplanet: DataSourceExoplanet) -> Optional[str]:
        """Construit le segment de phrase concernant la distance."""
        if not (
            exoplanet.st_distance
            and hasattr(exoplanet.st_distance, "value")
            and exoplanet.st_distance.value is not None
        ):
            return None

        try:
            distance_pc = float(exoplanet.st_distance.value)
            distance_ly = self.article_utils.format_parsecs_to_lightyears(
                distance_pc)
            if distance_ly is not None:
                formatted_distance_ly = self.article_utils.format_numeric_value(
                    distance_ly
                )
                return f", située à environ {formatted_distance_ly} [[année-lumière|années-lumière]] de la [[Terre]]"
        except (ValueError, TypeError):
            # Gère les cas où distance.value n'est pas un nombre valide.
            return None
        return None

    def _format_constellation_locative_phrase(
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

    def _build_constellation_segment(self, exoplanet: DataSourceExoplanet) -> Optional[str]:
        """Construit le segment de phrase concernant la constellation."""
        if not (
            exoplanet.st_constellation
            and hasattr(exoplanet.st_constellation, "value")
            and exoplanet.st_constellation.value
        ):
            return None

        constellation_name_fr = self.constellation_utils.get_constellation_name(
            exoplanet.st_constellation.value
        )
        if constellation_name_fr:
            return self._format_constellation_locative_phrase(constellation_name_fr)
        return None

    def generate_exoplanet_introduction(self, exoplanet: DataSourceExoplanet) -> str:
        """
        Génère l'introduction pour une exoplanète.
        """
        planet_type = self.planet_type_utils.get_exoplanet_planet_type(
            exoplanet)
        # planet_type est supposé être une chaîne comme "Jupiter chaud", pour être utilisé dans "[[Jupiter chaud]]"

        planet_name_str = "Nom inconnu"
        if exoplanet.pl_name and hasattr(exoplanet.pl_name, "value") and exoplanet.pl_name.value:
            planet_name_str = exoplanet.pl_name.value
        elif isinstance(exoplanet.pl_name, str):  # Fallback if name is already a string
            planet_name_str = exoplanet.pl_name

        base_intro = (
            f"'''{planet_name_str}''' est une exoplanète de type [[{planet_type}]]"
        )

        parts = [base_intro]

        host_star_segment = self._build_host_star_segment(exoplanet)
        if host_star_segment:
            parts.append(host_star_segment)

        distance_segment = self._build_distance_segment(exoplanet)
        if distance_segment:
            parts.append(distance_segment)

        constellation_segment = self._build_constellation_segment(exoplanet)
        if constellation_segment:
            parts.append(
                f" {constellation_segment}"
            )  # Espace initial comme dans la concaténation originale

        return "".join(parts) + "."
