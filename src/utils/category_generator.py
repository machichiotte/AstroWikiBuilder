# src/utils/category_generator.py
from typing import List
from src.models.exoplanet import Exoplanet
from src.utils.planet_type_utils import PlanetTypeUtils


class CategoryGenerator:
    """
    Classe pour générer les catégories des articles d'exoplanètes.
    """

    def __init__(self):
        self.base_categories = ["Exoplanète"]
        self.planet_type_utils = PlanetTypeUtils()

    def generate_categories(self, exoplanet: Exoplanet) -> List[str]:
        categories = self.base_categories.copy()

        # Catégorie par constellation
        if exoplanet.constellation and exoplanet.constellation.value:
            categories.append(
                f"Exoplanète de la constellation du {exoplanet.constellation.value}"
            )

        # Catégorie par type spectral
        if exoplanet.spectral_type and exoplanet.spectral_type.value:
            spectral_class = exoplanet.spectral_type.value[0]
            categories.append(
                f"Exoplanète orbitant une étoile de type {spectral_class}"
            )

        # Catégorie par méthode de découverte
        if exoplanet.discovery_method and exoplanet.discovery_method.value:
            method = exoplanet.discovery_method.value
            if method == "Transit":
                categories.append("Exoplanète découverte par la méthode des transits")
            elif method == "Radial Velocity":
                categories.append(
                    "Exoplanète découverte par la méthode des vitesses radiales"
                )
            elif method == "Imaging":
                categories.append("Exoplanète découverte par imagerie directe")
            else:
                categories.append(f"Exoplanète découverte par {method.lower()}")

        # Catégorie par année de découverte
        if exoplanet.discovery_date and exoplanet.discovery_date.value:
            if hasattr(exoplanet.discovery_date.value, "year"):
                year = exoplanet.discovery_date.value.year
            else:
                year = str(exoplanet.discovery_date.value)
            categories.append(f"Exoplanète découverte en {year}")

        # Catégorie par type de planète (classification physique)
        try:
            planet_type = self.planet_type_utils.get_planet_type(exoplanet)
            categories.append(f"Exoplanète de type {planet_type}")
        except Exception:
            pass  # Fallback en cas de données corrompues

        return categories
