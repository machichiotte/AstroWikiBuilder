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

        # Catégorie selon le type spectral de l'étoile
        if exoplanet.spectral_type and exoplanet.spectral_type.value:
            spectral_type = exoplanet.spectral_type.value
            spectral_class = spectral_type[0] if spectral_type else None
            if spectral_class:
                categories.append(f"Exoplanète orbitant une étoile de type {spectral_class}")

        # Catégorie selon la méthode de découverte
        if exoplanet.discovery_method and exoplanet.discovery_method.value:
            method = exoplanet.discovery_method.value.lower()
            if "transit" in method:
                categories.append("Exoplanète découverte par la méthode du transit")
            elif "radial" in method:
                categories.append("Exoplanète découverte par la méthode des vitesses radiales")
            elif "imaging" in method:
                categories.append("Exoplanète découverte par imagerie directe")

        # Catégorie selon l'année de découverte
        if exoplanet.discovery_date and exoplanet.discovery_date.value:
            year = exoplanet.discovery_date.value
            if isinstance(year, str) and year.isdigit():
                categories.append(f"Exoplanète découverte en {year}")

        # Catégorie selon la température (une seule, priorisation)
        temp_category = None
        if exoplanet.temperature and exoplanet.temperature.value is not None:
            temp = exoplanet.temperature.value
            if temp >= 1000:
                temp_category = "Jupiter ultra-chaud"
            elif temp >= 500:
                temp_category = "Jupiter chaud"
            elif temp >= 300:
                temp_category = "Jupiter tiède"
            else:
                temp_category = "Jupiter froid"
        
        # Catégorie selon le type de planète (une seule, priorisation, sans doublon avec la température)
        planet_type = None
        if exoplanet.mass and exoplanet.mass.value is not None and exoplanet.radius and exoplanet.radius.value is not None:
            mass = exoplanet.mass.value
            radius = exoplanet.radius.value
            if mass >= 10:
                candidate = "Jupiter chaud"
                if candidate != temp_category:
                    planet_type = candidate
            elif mass >= 0.1 and mass < 10 and radius > 2:
                candidate = "Mini-Neptune"
                if candidate != temp_category:
                    planet_type = candidate
            elif mass >= 0.1 and mass < 10 and radius <= 2:
                candidate = "Super-Terre"
                if candidate != temp_category:
                    planet_type = candidate
            elif mass < 0.1:
                candidate = "Sous-Terre"
                if candidate != temp_category:
                    planet_type = candidate
        if planet_type:
            categories.append(planet_type)
        if temp_category:
            categories.append(temp_category)

        return categories 