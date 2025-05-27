from src.constants.field_mappings import CONSTELLATION_GENDER
from src.models.exoplanet import Exoplanet
from .comparison_utils import ComparisonUtils
from .planet_type_utils import PlanetTypeUtils
from .star_utils import StarUtils
from .format_utils import FormatUtils


class IntroductionGenerator:
    """
    Classe pour générer l'introduction des articles d'exoplanètes
    """

    def __init__(self, comparison_utils: ComparisonUtils, format_utils: FormatUtils):
        self.comparison_utils = comparison_utils
        self.format_utils = format_utils
        self.planet_type_utils = PlanetTypeUtils()
        self.star_utils = StarUtils(self.format_utils)

    def generate_introduction(self, exoplanet: Exoplanet) -> str:
        """
        Génère l'introduction pour une exoplanète
        """

        # Obtenir le type de planète
        planet_type = self.planet_type_utils.get_planet_type(exoplanet)

        # Obtenir la description de l'étoile
        star_desc = self.star_utils.get_spectral_type_formatted_description(
            exoplanet.spectral_type.value if exoplanet.spectral_type else None
        )

        introduction = (
            f"'''{exoplanet.name}''' est une exoplanète de type [[{planet_type}]]"
        )

        # Ajout de l'étoile hôte
        if exoplanet.host_star and exoplanet.host_star.value:
            if star_desc:
                introduction += (
                    f" en orbite autour de la {star_desc} {exoplanet.host_star.value}"
                )
            else:
                introduction += (
                    f" en orbite autour de l'étoile {exoplanet.host_star.value}"
                )

        # Ajout de la distance
        if exoplanet.distance and exoplanet.distance.value:
            distance_ly = self.format_utils.parsecs_to_lightyears(
                exoplanet.distance.value
            )
            if distance_ly:
                introduction += f", située à environ {self.format_utils.format_numeric_value(distance_ly)} [[année-lumière|années-lumière]] de la [[Terre]]"

        # Ajout de la constellation
        if exoplanet.constellation and exoplanet.constellation.value:
            const = self.star_utils.get_constellation(exoplanet.constellation.value)
            introduction += f" {self.get_constellation_phrase(const)}"

        introduction += "."
        print("intro" + introduction)
        return introduction

    def get_constellation_phrase(nom_fr: str) -> str:
        genre = CONSTELLATION_GENDER.get(nom_fr, "m")  # défaut masculin
        preposition = "de la" if genre == "f" else "du"

        # Si la constellation commence par une voyelle et est masculine : contraction en "de l'"
        if genre == "m" and nom_fr[0].lower() in "aeiouéèêëàâäîïôöùûü":
            preposition = "de l'"
        return (
            f"dans la constellation {preposition} {nom_fr}"
            if not preposition.endswith("'")
            else f"dans la constellation {preposition}{nom_fr}"
        )
