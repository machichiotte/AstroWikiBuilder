from typing import Optional
from src.models.exoplanet import Exoplanet
from .comparison_utils import ComparisonUtils
from .format_utils import FormatUtils

class IntroductionGenerator:
    """
    Classe pour générer l'introduction des articles d'exoplanètes
    """
    def __init__(self, comparison_utils: ComparisonUtils, format_utils: FormatUtils):
        self.comparison_utils = comparison_utils
        self.format_utils = format_utils

    def generate_introduction(self, exoplanet: Exoplanet) -> str:
        """
        Génère l'introduction pour une exoplanète
        """
        intro = f"{exoplanet.name} est une exoplanète"
        
        # Ajout des caractéristiques physiques
        if exoplanet.mass and exoplanet.mass.value:
            mass_comparison = self.comparison_utils.get_mass_comparison(exoplanet)
            if mass_comparison:
                intro += f" {mass_comparison}"
        
        if exoplanet.radius and exoplanet.radius.value:
            radius_comparison = self.comparison_utils.get_radius_comparison(exoplanet)
            if radius_comparison:
                intro += f" {radius_comparison}"
        
        # Ajout de la distance orbitale
        if exoplanet.semi_major_axis and exoplanet.semi_major_axis.value:
            orbital_comparison = self.comparison_utils.get_orbital_comparison(exoplanet)
            if orbital_comparison:
                intro += f" {orbital_comparison}"
        
        # Ajout de l'étoile hôte
        if exoplanet.host_star and exoplanet.host_star.value:
            intro += f" en orbite autour de l'étoile {exoplanet.host_star.value}"
            
            if exoplanet.spectral_type and exoplanet.spectral_type.value:
                intro += f" de type spectral {exoplanet.spectral_type.value}"
        
        # Ajout de la distance
        if exoplanet.distance and exoplanet.distance.value:
            distance_ly = self.format_utils.parsecs_to_lightyears(exoplanet.distance.value)
            if distance_ly:
                intro += f", située à environ {self.format_utils.format_numeric_value(distance_ly)} années-lumière"
        
        # Ajout de la constellation
        if exoplanet.constellation and exoplanet.constellation.value:
            intro += f" dans la constellation de {exoplanet.constellation.value}"
        
        # Ajout de la découverte
        if exoplanet.discovery_date and exoplanet.discovery_date.value:
            intro += f". Elle a été découverte en {self.format_utils.format_year_field(exoplanet.discovery_date.value)}"
            
            if exoplanet.discovery_method and exoplanet.discovery_method.value:
                intro += f" par la méthode de {exoplanet.discovery_method.value}"
        
        intro += "."
        return intro 