from typing import List
from src.models.exoplanet import Exoplanet

class CategoryGenerator:
    """
    Classe pour générer les catégories des articles d'exoplanètes
    """
    def __init__(self):
        self.base_categories = [
            "Exoplanète",
            "Article de qualité",
            "Article de qualité en astronomie"
        ]

    def generate_categories(self, exoplanet: Exoplanet) -> List[str]:
        """
        Génère la liste des catégories pour une exoplanète
        """
        categories = self.base_categories.copy()

        # Catégorie par constellation
        if exoplanet.constellation and exoplanet.constellation.value:
            categories.append(f"Exoplanète de la constellation de {exoplanet.constellation.value}")

        # Catégorie par type spectral de l'étoile
        if exoplanet.spectral_type and exoplanet.spectral_type.value:
            spectral_type = exoplanet.spectral_type.value[0]  # Prend la première lettre du type spectral
            categories.append(f"Exoplanète orbitant une étoile de type {spectral_type}")

        # Catégorie par méthode de découverte
        if exoplanet.discovery_method and exoplanet.discovery_method.value:
            method = exoplanet.discovery_method.value.lower()
            if "transit" in method:
                categories.append("Exoplanète découverte par la méthode du transit")
            elif "radial" in method:
                categories.append("Exoplanète découverte par la méthode des vitesses radiales")
            elif "imagerie" in method:
                categories.append("Exoplanète découverte par imagerie directe")
            elif "microlentille" in method:
                categories.append("Exoplanète découverte par microlentille gravitationnelle")

        # Catégorie par type de planète
        if exoplanet.mass and exoplanet.mass.value:
            if exoplanet.mass.value >= 1:
                categories.append("Géante gazeuse")
            else:
                categories.append("Planète tellurique")

        # Catégorie par année de découverte
        if exoplanet.discovery_date and exoplanet.discovery_date.value:
            year = exoplanet.discovery_date.value.split("-")[0]  # Prend l'année de la date
            categories.append(f"Exoplanète découverte en {year}")

        return categories 