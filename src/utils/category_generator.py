from typing import List
from src.models.exoplanet import Exoplanet

class CategoryGenerator:
    """
    Classe pour générer les catégories des articles d'exoplanètes
    """
    def __init__(self):
        self.base_categories = [
            "Exoplanète"
        ]

    def generate_categories(self, exoplanet: Exoplanet) -> List[str]:
        """Génère les catégories pour l'article."""
        categories = ["Exoplanète"]
        
        # Catégorie par constellation
        if exoplanet.constellation and exoplanet.constellation.value:
            categories.append(f"Exoplanète de la constellation du {exoplanet.constellation.value}")
            
        # Catégorie par type spectral
        if exoplanet.spectral_type and exoplanet.spectral_type.value:
            spectral_class = exoplanet.spectral_type.value[0]
            categories.append(f"Exoplanète orbitant une étoile de type {spectral_class}")
            
        # Catégorie par méthode de découverte
        if exoplanet.discovery_method and exoplanet.discovery_method.value:
            method = exoplanet.discovery_method.value
            if method == "Transit":
                categories.append("Exoplanète découverte par la méthode du transit")
            elif method == "Radial Velocity":
                categories.append("Exoplanète découverte par la méthode des vitesses radiales")
            elif method == "Imaging":
                categories.append("Exoplanète découverte par imagerie directe")
            else:
                categories.append(f"Exoplanète découverte par {method.lower()}")
                
        # Catégorie par année de découverte
        if exoplanet.discovery_date and exoplanet.discovery_date.value:
            year = exoplanet.discovery_date.value.year if hasattr(exoplanet.discovery_date.value, 'year') else str(exoplanet.discovery_date.value)
            categories.append(f"Exoplanète découverte en {year}")
            
        # Catégorie par type de planète (basée sur la masse)
        if exoplanet.mass and exoplanet.mass.value is not None:
            mass = exoplanet.mass.value
            if mass < 0.1:
                categories.append("Sous-Terre")
            elif mass < 1:
                categories.append("Super-Terre")
            elif mass < 13:
                categories.append("Jupiter")
            else:
                categories.append("Naine brune")
                
        # Catégorie par température et distance orbitale
        if exoplanet.temperature and exoplanet.temperature.value is not None and exoplanet.semi_major_axis and exoplanet.semi_major_axis.value is not None:
            temp = exoplanet.temperature.value
            orbit = exoplanet.semi_major_axis.value
            
            # Ne classer comme Jupiter chaud que si la planète est proche de son étoile
            if orbit < 0.1:  # Moins de 0.1 UA
                if temp > 2000:
                    categories.append("Jupiter ultra-chaud")
                elif temp > 1000:
                    categories.append("Jupiter chaud")
            elif orbit < 1:  # Entre 0.1 et 1 UA
                if temp > 1000:
                    categories.append("Jupiter tiède")
            else:  # Plus de 1 UA
                if temp > 500:
                    categories.append("Jupiter froid")
                
        return categories 