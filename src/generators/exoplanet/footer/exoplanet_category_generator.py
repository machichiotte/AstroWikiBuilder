# src/generators/exoplanet/exoplanet_category_generator.py
from typing import List, Optional, Callable
from src.models.entities.exoplanet import Exoplanet
from src.utils.astro.classification.exoplanet_type_utils import ExoplanetTypeUtils
from src.generators.base_category_generator import BaseCategoryGenerator


class ExoplanetCategoryGenerator(BaseCategoryGenerator):
    """
    Classe pour générer les catégories des articles d'exoplanètes.
    Utilise un générateur de règles centralisé.
    """

    def resolve_discovery_facility(self) -> Optional[str]:
        """
        Génère les catégories de catalogue basées sur les préfixes des noms,
        au format [[Catégorie:XYZ|clef]].
        """
        catalog_mappings = (
            self.generator.rules.get("exoplanet", {})
            .get("mapped", {})
            .get("disc_facility", {})
        )

        return catalog_mappings

    def __init__(self, rules_filepath: str = "src/constants/categories_rules.yaml"):
        super().__init__(rules_filepath)
        self.planet_type_utils = ExoplanetTypeUtils()

    def get_object_type(self) -> str:
        return "exoplanet"

    def list_category_rules(self) -> List[Callable]:
        return [
            self._get_planet_type_category,
            self.resolve_constellation_category,
        ]

    def _get_planet_type_category(self, exoplanet: Exoplanet) -> Optional[str]:
        """
        Règle personnalisée pour déterminer la catégorie de type de planète.
        """
        try:
            planet_type: str = (
                self.planet_type_utils.determine_exoplanet_classification(exoplanet)
            )
            if planet_type:
                mapping = (
                    self.generator.rules.get("exoplanet", {})
                    .get("mapped", {})
                    .get("planet_type", {})
                )
                if planet_type in mapping:
                    return mapping[planet_type]
        except Exception:
            pass
        return None

    def resolve_constellation_category(self, exoplanet: Exoplanet) -> Optional[str]:
        """
        Règle personnalisée pour déterminer la catégorie de constellation.
        """
        if exoplanet.sy_constellation:
            constellation: str = exoplanet.sy_constellation

            mapping = (
                self.generator.rules.get("common", {})
                .get("mapped", {})
                .get("sy_constellation", {})
            )

            if constellation in mapping.keys():
                return mapping[constellation]
        return None

    def _get_discovered_by_category(self, exoplanet: Exoplanet) -> Optional[str]:
        """
        Règle personnalisée pour déterminer la catégorie 'découverte grâce à'
        en utilisant le champ 'discovery_program' de l'exoplanète et le mapping.
        """
        discovered_by_program: str | None = (
            exoplanet.disc_program.value if exoplanet.disc_program else None
        )

        disc_facility_list = self.resolve_discovery_facility()

        if discovered_by_program:
            # Check for exact matches first
            if discovered_by_program in disc_facility_list:
                return disc_facility_list[discovered_by_program]
            # If no exact match, check for partial matches (case-insensitive for robustness)
            for key, cat in disc_facility_list.items():
                if key.lower() in discovered_by_program.lower():
                    return cat
        return None  # Returns None if no match is found, or if disc_program is None.

    def generate_categories(self, exoplanet: Exoplanet) -> List[str]:
        """
        Génère les catégories pour une exoplanète en déléguant au générateur de règles
        et en ajoutant des règles personnalisées.
        """
        custom_rules = [
            self._get_planet_type_category,
            self._get_discovered_by_category,
            self.resolve_constellation_category,
        ]

        # The CategoryGenerator.generate method should be responsible for filtering out
        # empty strings or None values returned by custom rules.
        return self.generator.generate(
            exoplanet, "exoplanet", custom_rules=custom_rules
        )
