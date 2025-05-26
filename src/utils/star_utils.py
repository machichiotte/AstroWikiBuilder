# src/utils/star_utils.py
from typing import Dict
from src.constants.field_mappings import CONSTELLATION_FR, SPECTRAL_TYPE_DESCRIPTIONS, SPECTRAL_TYPE_LINKS
from src.models.exoplanet import Exoplanet
from .format_utils import FormatUtils

from astropy.coordinates import SkyCoord
import astropy.units as u

class StarUtils:
    """
    Classe utilitaire pour décrire et caractériser les étoiles hôtes des exoplanètes,
    avec descriptions et liens Wikipedia en français vers le type d'astre correspondant.
    """

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
        if spectral in SPECTRAL_TYPE_DESCRIPTIONS:
            desc += SPECTRAL_TYPE_DESCRIPTIONS[spectral]
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

    # ne semble pas utilisé
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
            if spectral in SPECTRAL_TYPE_LINKS:
                chars["Type d'astre"] = SPECTRAL_TYPE_LINKS[spectral]

        if exoplanet.apparent_magnitude and exoplanet.apparent_magnitude.value is not None:
            chars["Magnitude apparente"] = self.format_utils.format_numeric_value(exoplanet.apparent_magnitude.value)
        if exoplanet.distance and exoplanet.distance.value is not None:
            ly = self.format_utils.parsecs_to_lightyears(exoplanet.distance.value)
            if ly is not None:
                chars["Distance"] = f"{self.format_utils.format_numeric_value(ly)} années‑lumière"
        if exoplanet.constellation and exoplanet.constellation.value:
            chars["Constellation"] = exoplanet.constellation.value
        return chars

    def get_spectral_type_formatted_description(self, spectral_type: str) -> str:
        """Génère une description de l'étoile avec le type spectral."""
        if not spectral_type:
            return "son étoile hôte"
            
        spectral_class = spectral_type[0].upper()
        description = SPECTRAL_TYPE_DESCRIPTIONS.get(spectral_class, "son étoile hôte")
        
        return f"[[{description}]]"
    
    def get_constellation(self, exoplanet: Exoplanet) -> str:
        """Trouve la constellation"""
        right_ascension = exoplanet.right_ascension.value.replace('/', ' ')
        declination = exoplanet.declination.value.replace('/', ' ')
        
        coord = SkyCoord(ra=right_ascension, dec=declination, unit=(u.hourangle, u.deg), frame='icrs')
        constellation_en = coord.get_constellation()
    
        return CONSTELLATION_FR.get(constellation_en, constellation_en)
    
    def get_constellation_formatted(self, exoplanet: Exoplanet) -> str:
        """
        Génère le lien formaté pour la constellation de l'étoile hôte.
        Ex: [[Cygne (constellation)|Cygne]]
        This method now internally calls get_constellation to determine the name.
        """
        # Use the astropy-based get_constellation to get the French constellation name
        constellation_name = self.get_constellation(exoplanet) # This calls the user's new method
        
        if constellation_name and constellation_name != "son étoile hôte": # Check if a valid constellation was found
            # Assuming the French Wikipedia convention for constellations is "Name (constellation)"
            
            print(f"[[{constellation_name} (constellation)|{constellation_name}]]")
            return f"[[{constellation_name} (constellation)|{constellation_name}]]"
        return "" # Return empty string if no constellation or if it's the default "son étoile hôte"
    