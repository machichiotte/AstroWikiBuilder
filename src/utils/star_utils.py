from typing import Optional, Dict
from src.models.exoplanet import Exoplanet
from .format_utils import FormatUtils

class StarUtils:
    """
    Classe pour gérer les informations sur les étoiles hôtes des exoplanètes
    """
    def __init__(self, format_utils: FormatUtils):
        self.format_utils = format_utils
        self.spectral_type_descriptions = {
            'O': "étoile bleue très chaude",
            'B': "étoile bleue chaude",
            'A': "étoile blanche",
            'F': "étoile blanc-jaune",
            'G': "étoile jaune",
            'K': "étoile orange",
            'M': "étoile rouge"
        }

    def get_star_description(self, exoplanet: Exoplanet) -> str:
        """
        Génère une description de l'étoile hôte
        """
        if not exoplanet.host_star or not exoplanet.host_star.value:
            return ""

        description = f"L'étoile hôte, {exoplanet.host_star.value}, est "
        
        # Type spectral
        if exoplanet.spectral_type and exoplanet.spectral_type.value:
            spectral_type = exoplanet.spectral_type.value[0]  # Prend la première lettre
            if spectral_type in self.spectral_type_descriptions:
                description += f"une {self.spectral_type_descriptions[spectral_type]}"
            else:
                description += f"de type spectral {exoplanet.spectral_type.value}"

        # Magnitude apparente
        if exoplanet.apparent_magnitude and exoplanet.apparent_magnitude.value:
            description += f" avec une magnitude apparente de {self.format_utils.format_value(exoplanet.apparent_magnitude.value)}"

        # Distance
        if exoplanet.distance and exoplanet.distance.value:
            distance_ly = self.format_utils.parsec_to_light_years(exoplanet.distance.value)
            if distance_ly:
                description += f", située à environ {self.format_utils.format_value(distance_ly)} années-lumière"

        # Constellation
        if exoplanet.constellation and exoplanet.constellation.value:
            description += f" dans la constellation de {exoplanet.constellation.value}"

        description += "."
        return description

    def get_star_characteristics(self, exoplanet: Exoplanet) -> Dict[str, str]:
        """
        Retourne un dictionnaire des caractéristiques de l'étoile
        """
        characteristics = {}
        
        if exoplanet.spectral_type and exoplanet.spectral_type.value:
            characteristics["Type spectral"] = exoplanet.spectral_type.value
            
        if exoplanet.apparent_magnitude and exoplanet.apparent_magnitude.value:
            characteristics["Magnitude apparente"] = self.format_utils.format_value(exoplanet.apparent_magnitude.value)
            
        if exoplanet.distance and exoplanet.distance.value:
            distance_ly = self.format_utils.parsec_to_light_years(exoplanet.distance.value)
            if distance_ly:
                characteristics["Distance"] = f"{self.format_utils.format_value(distance_ly)} années-lumière"
                
        if exoplanet.constellation and exoplanet.constellation.value:
            characteristics["Constellation"] = exoplanet.constellation.value
            
        return characteristics 