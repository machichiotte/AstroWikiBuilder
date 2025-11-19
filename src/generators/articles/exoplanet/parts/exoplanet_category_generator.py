# src/generators/articles/exoplanet/parts/exoplanet_category_generator.py
from typing import List, Optional, Callable
from src.models.entities.exoplanet import Exoplanet
from src.utils.astro.classification.exoplanet_type_utils import ExoplanetTypeUtils
from src.generators.base.base_category_generator import BaseCategoryGenerator
import logging


class ExoplanetCategoryGenerator(BaseCategoryGenerator):
    """
    Classe pour générer les catégories des articles d'exoplanètes.
    Utilise un générateur de règles centralisé.
    """

    def __init__(self, rules_filepath: str = "src/constants/categories_rules.yaml"):
        super().__init__(rules_filepath)
        self.planet_type_utils = ExoplanetTypeUtils()

    # --- Implémentation des méthodes abstraites ---

    def retrieve_object_type(self) -> str:
        return "exoplanet"

    def define_category_rules(self) -> List[Callable]:
        return [
            self.map_planet_type_to_category,
            self.map_discovery_program_to_category,
            self.map_constellation_to_category,  # Cette méthode doit exister !
        ]

    # --- Règles de catégorisation spécifiques aux exoplanètes ---

    def map_planet_type_to_category(self, exoplanet: Exoplanet) -> Optional[str]:
        """
        Règle personnalisée pour déterminer la catégorie de type de planète.
        """
        try:
            planet_type: str = (
                self.planet_type_utils.determine_exoplanet_classification(exoplanet)
            )
            if planet_type:
                mapping = (
                    self._category_rules_manager.rules.get("exoplanet", {})
                    .get("mapped", {})
                    .get("planet_type", {})
                )
                if planet_type in mapping:
                    return mapping[planet_type]
        except (KeyError, AttributeError) as e:
            logging.warning(
                f"Clé de mapping non trouvée pour l'exoplanète {exoplanet.pl_name}: {e}"
            )
            pass
        except Exception as e:
            logging.error(
                f"Erreur inattendue dans _get_planet_type_category pour {exoplanet.pl_name}: {e}"
            )
            pass
        return None

    def map_discovery_program_to_category(self, exoplanet: Exoplanet) -> Optional[str]:
        """
        Règle personnalisée pour déterminer la catégorie 'découverte grâce à'
        en utilisant le champ 'discovery_program' de l'exoplanète et le mapping.
        """
        discovered_by_program: str | None = (
            exoplanet.disc_program.value if exoplanet.disc_program else None
        )

        disc_facility_list = (
            self._category_rules_manager.rules.get("exoplanet", {})
            .get("mapped", {})
            .get("disc_facility", {})
        )

        if discovered_by_program:
            # Check for exact matches first
            if discovered_by_program in disc_facility_list:
                return disc_facility_list[discovered_by_program]
            # If no exact match, check for partial matches (case-insensitive for robustness)
            for key, cat in disc_facility_list.items():
                if key.lower() in discovered_by_program.lower():
                    return cat
        return None

    def map_constellation_to_category(self, exoplanet: Exoplanet) -> Optional[str]:
        """
        Règle personnalisée pour déterminer la catégorie liée à la constellation.
        Génère une catégorie sous la forme "Exoplanète de la constellation de [Nom]".
        """
        if not exoplanet.sy_constellation:
            return None
            
        # On nettoie le nom de la constellation si nécessaire
        constellation = exoplanet.sy_constellation.strip()
        
        # Construction de la catégorie
        # Note: Ceci suppose que 'sy_constellation' est le nom français (ex: "Cygne")
        return f"Exoplanète de la constellation de {constellation}"