# src/generators/exoplanet/exoplanet_category_generator.py
from typing import List, Optional
from src.models.data_source_exoplanet import DataSourceExoplanet
from src.utils.exoplanet_type_utils import ExoplanetTypeUtils # Assuming this utility is correctly implemented and available
from src.generators.category_generator import CategoryGenerator


class ExoplanetCategoryGenerator:
    """
    Classe pour générer les catégories des articles d'exoplanètes.
    Utilise un générateur de règles centralisé.
    """

    def __init__(self, rules_filepath: str = "src/constants/categories_rules.yaml"):
        """
        Initialise le générateur de catégories.
        """
        self.generator = CategoryGenerator(rules_filepath)
        self.planet_type_utils = ExoplanetTypeUtils()

    def _get_planet_type_category(self, exoplanet: DataSourceExoplanet) -> Optional[str]:
        """
        Règle personnalisée pour déterminer la catégorie de type de planète.
        Cette logique est trop complexe pour le YAML et est gérée en Python,
        assumant que ExoplanetTypeUtils renvoie déjà la catégorie formatée.
        """
        try:
            # Assumons que get_exoplanet_planet_type retourne déjà la catégorie formatée
            planet_type = self.planet_type_utils.get_exoplanet_planet_type(exoplanet)
            if isinstance(planet_type, str) and planet_type.startswith("[[Catégorie:"):
                return planet_type
        except Exception:
            # En cas de données manquantes ou d'erreur pour la classification
            pass
        return None

    def _get_discovered_by_category(self, exoplanet: DataSourceExoplanet) -> Optional[str]:
        """
        Règle personnalisée pour déterminer la catégorie 'découverte grâce à'
        en utilisant le champ 'discovery_program' de l'exoplanète.
        """
        discovered_by_program = exoplanet.discovery_program.value if exoplanet.discovery_program else None
        if discovered_by_program:
            # Mapping direct basé sur les exemples de categories_notes.md
            mapping = {
                'Kepler': '[[Catégorie:Exoplanète découverte grâce à Kepler]]',
                'Transiting Exoplanet Survey Satellite': '[[Catégorie:Exoplanète découverte grâce au Transiting Exoplanet Survey Satellite]]',
                'TESS': '[[Catégorie:Exoplanète découverte grâce au Transiting Exoplanet Survey Satellite]]',
                'CoRoT': '[[Catégorie:Exoplanète découverte grâce au télescope spatial CoRoT]]',
                'Very Large Telescope': '[[Catégorie:Exoplanète découverte grâce au Very Large Telescope (VLT)]]',
                'Paranal Observatory': '[[Catégorie:Exoplanète découverte grâce au Very Large Telescope (VLT)]]',
                'VLT': '[[Catégorie:Exoplanète découverte grâce au Very Large Telescope (VLT)]]',
                'Hubble Space Telescope': '[[Catégorie:Exoplanète découverte grâce au télescope spatial Hubble]]',
                'HST': '[[Catégorie:Exoplanète découverte grâce au télescope spatial Hubble]]',
                'HARPS': '[[Catégorie:Exoplanète découverte grâce à HARPS]]',
                'La Silla Observatory': '[[Catégorie:Exoplanète découverte grâce à HARPS]]',
                'James Webb Space Telescope': '[[Catégorie:Exoplanète découverte grâce au télescope spatial James Webb]]',
                'JWST': '[[Catégorie:Exoplanète découverte grâce au télescope spatial James Webb]]',
                'Spitzer Space Telescope': '[[Catégorie:Exoplanète découverte grâce au télescope spatial Spitzer]]',
                'Spitzer': '[[Catégorie:Exoplanète découverte grâce au télescope spatial Spitzer]]',
                'Gaia': '[[Catégorie:Exoplanète découverte grâce au télescope spatial Gaia]]',
                'W. M. Keck Observatory': '[[Catégorie:Exoplanète découverte grâce au W. M. Keck Observatory]]',
                'Keck': '[[Catégorie:Exoplanète découverte grâce au W. M. Keck Observatory]]',
                'Gemini Observatory': '[[Catégorie:Exoplanète découverte grâce au Gemini Observatory]]',
                'CHEOPS': '[[Catégorie:Exoplanète découverte grâce au télescope spatial CHEOPS]]'
            }
            # Cherche une correspondance exacte ou partielle
            if discovered_by_program in mapping:
                return mapping[discovered_by_program]
            for key, cat in mapping.items():
                if key in discovered_by_program:
                    return cat
        return None

    def generate_categories(self, exoplanet: DataSourceExoplanet) -> List[str]:
        """
        Génère les catégories pour une exoplanète en déléguant au générateur de règles
        et en ajoutant des règles personnalisées.
        """
        custom_rules = [
            self._get_planet_type_category,
            self._get_discovered_by_category,
            # Ajoutez d'autres règles personnalisées ici si nécessaire,
            # par exemple pour la date de découverte si elle n'est pas directement gérée par YAML.
        ]
        
        return self.generator.generate(exoplanet, "exoplanet", custom_rules=custom_rules)