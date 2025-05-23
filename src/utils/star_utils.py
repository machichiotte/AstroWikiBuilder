# src/utils/star_utils.py
from typing import Dict, Optional
from src.models.exoplanet import Exoplanet
from .format_utils import FormatUtils

class StarUtils:
    """
    Classe utilitaire pour décrire et caractériser les étoiles hôtes des exoplanètes,
    avec descriptions et liens Wikipedia en français vers le type d'astre correspondant.
    """
    # Descriptions des types spectraux selon Morgan-Keenan
    SPECTRAL_TYPE_DESCRIPTIONS: Dict[str, str] = {
        'O': "étoile bleue de la séquence principale",
        'B': "étoile bleu-blanc de la séquence principale",
        'A': "étoile blanche de la séquence principale",
        'F': "étoile blanc-jaune de la séquence principale",
        'G': "étoile jaune de la séquence principale",
        'K': "étoile orange de la séquence principale",
        'M': "étoile rouge de la séquence principale",
        'L': "naine brune de type L",
        'T': "naine brune de type T",
        'Y': "naine brune de type Y"
    }
    # Liens Wikipédia pour chaque "type d'astre" (en français)
    SPECTRAL_TYPE_LINKS: Dict[str, str] = {
        'O': 'https://fr.wikipedia.org/wiki/%C3%89toile_bleue_de_la_s%C3%A9quence_principale',
        'B': 'https://fr.wikipedia.org/wiki/%C3%89toile_bleu-blanc_de_la_s%C3%A9quence_principale',
        'A': 'https://fr.wikipedia.org/wiki/%C3%89toile_blanche_de_la_s%C3%A9quence_principale',
        'F': 'https://fr.wikipedia.org/wiki/%C3%89toile_blanc-jaune_de_la_s%C3%A9quence_principale',
        'G': 'https://fr.wikipedia.org/wiki/%C3%89toile_jaune_de_la_s%C3%A9quence_principale',
        'K': 'https://fr.wikipedia.org/wiki/%C3%89toile_orange_de_la_s%C3%A9quence_principale',
        'M': 'https://fr.wikipedia.org/wiki/%C3%89toile_rouge_de_la_s%C3%A9quence_principale',
        'L': 'https://fr.wikipedia.org/wiki/Naine_brunne_L',
        'T': 'https://fr.wikipedia.org/wiki/Naine_brune_T',
        'Y': 'https://fr.wikipedia.org/wiki/Naine_brune_Y'
    }

    spectral_type_descriptions = {
        'O': "étoile bleue très chaude",
        'B': "étoile bleue chaude",
        'A': "étoile blanche",
        'F': "étoile blanc-jaune",
        'G': "étoile jaune",
        'K': "étoile orange",
        'M': "étoile rouge"
    }

    def __init__(self, format_utils: FormatUtils):
        self.format_utils = format_utils

    def get_star_description(self, exoplanet: Exoplanet) -> str:
        """
        Génère une description complète de l'étoile hôte en français.
        """
        star_name = exoplanet.host_star.value if exoplanet.host_star and exoplanet.host_star.value else None
        if not star_name:
            return ""

        desc = f"L'étoile hôte, {star_name}, est "
        spectral = exoplanet.spectral_type.value[0] if exoplanet.spectral_type and exoplanet.spectral_type.value else None
        if spectral in self.SPECTRAL_TYPE_DESCRIPTIONS:
            desc += self.SPECTRAL_TYPE_DESCRIPTIONS[spectral]
        else:
            full = exoplanet.spectral_type.value or "inconnu"
            desc += f"de type spectral {full}"

        if exoplanet.apparent_magnitude and exoplanet.apparent_magnitude.value is not None:
            mag = self.format_utils.format_numeric_value(exoplanet.apparent_magnitude.value)
            desc += f", de magnitude apparente {mag}"

        if exoplanet.distance and exoplanet.distance.value is not None:
            ly = self.format_utils.parsecs_to_lightyears(exoplanet.distance.value)
            if ly is not None:
                desc += f", située à environ {self.format_utils.format_numeric_value(ly)} années‑lumière"

        if exoplanet.constellation and exoplanet.constellation.value:
            desc += f", dans la constellation de {exoplanet.constellation.value}"

        return desc + "."

    def get_star_characteristics(self, exoplanet: Exoplanet) -> Dict[str, str]:
        """
        Retourne un dictionnaire des caractéristiques de l'étoile hôte,
        dont le lien Wikipédia vers le "type d'astre" (ex : séquence principale, naine brune).
        Clés : Type spectral, Type d'astre (URL), Magnitude apparente, Distance, Constellation.
        """
        chars: Dict[str, str] = {}
        spectral = exoplanet.spectral_type.value[0] if exoplanet.spectral_type and exoplanet.spectral_type.value else None
        if spectral:
            chars["Type spectral"] = exoplanet.spectral_type.value
            if spectral in self.SPECTRAL_TYPE_LINKS:
                chars["Type d'astre"] = self.SPECTRAL_TYPE_LINKS[spectral]

        if exoplanet.apparent_magnitude and exoplanet.apparent_magnitude.value is not None:
            chars["Magnitude apparente"] = self.format_utils.format_numeric_value(exoplanet.apparent_magnitude.value)
        if exoplanet.distance and exoplanet.distance.value is not None:
            ly = self.format_utils.parsecs_to_lightyears(exoplanet.distance.value)
            if ly is not None:
                chars["Distance"] = f"{self.format_utils.format_numeric_value(ly)} années‑lumière"
        if exoplanet.constellation and exoplanet.constellation.value:
            chars["Constellation"] = exoplanet.constellation.value
        return chars