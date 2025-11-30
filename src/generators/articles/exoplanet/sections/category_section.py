# src/generators/articles/exoplanet/sections/category_section.py

import logging
from collections.abc import Callable

from src.generators.base.category_rules_manager import CategoryRulesManager
from src.models.entities.exoplanet_entity import Exoplanet
from src.utils.astro.classification.exoplanet_type_util import ExoplanetTypeUtil


class CategorySection:
    """
    Génère les catégories pour les articles d'exoplanètes.
    """

    def __init__(self, rules_filepath: str = "src/constants/categories_rules.yaml"):
        self._category_rules_manager = CategoryRulesManager(rules_filepath)
        self.planet_type_util = ExoplanetTypeUtil()

    def generate(self, exoplanet: Exoplanet) -> str:
        """Génère la section des catégories."""
        categories = self.build_categories(exoplanet)
        if not categories:
            return ""
        # Formater chaque catégorie avec le préfixe Wikipedia
        formatted_categories = [f"[[Catégorie:{cat}]]" for cat in categories]
        return "\n".join(formatted_categories)

    def build_categories(self, exoplanet: Exoplanet) -> list[str]:
        """Génère la liste des catégories."""
        custom_rules: list[Callable] = [
            self.map_planet_type_to_category,
            self.map_discovery_program_to_category,
            self.map_constellation_to_category,
        ]
        return self._category_rules_manager.generate_categories_for(
            exoplanet, "exoplanet", custom_rules=custom_rules
        )

    def map_planet_type_to_category(self, exoplanet: Exoplanet) -> str | None:
        """Règle personnalisée pour déterminer la catégorie de type de planète."""
        try:
            planet_type: str = self.planet_type_util.determine_exoplanet_classification(exoplanet)
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
        except Exception as e:
            logging.error(
                f"Erreur inattendue dans map_planet_type_to_category pour {exoplanet.pl_name}: {e}"
            )
        return None

    def map_discovery_program_to_category(self, exoplanet: Exoplanet) -> str | None:
        """Règle personnalisée pour déterminer la catégorie 'découverte grâce à'."""
        discovered_by_program: str | None = (
            exoplanet.disc_program.value if exoplanet.disc_program else None
        )

        disc_facility_list = (
            self._category_rules_manager.rules.get("exoplanet", {})
            .get("mapped", {})
            .get("disc_facility", {})
        )

        if discovered_by_program:
            if discovered_by_program in disc_facility_list:
                return disc_facility_list[discovered_by_program]
            for key, cat in disc_facility_list.items():
                if key.lower() in discovered_by_program.lower():
                    return cat
        return None

    def map_constellation_to_category(self, exoplanet: Exoplanet) -> str | None:
        """Règle personnalisée pour déterminer la catégorie liée à la constellation."""
        if not exoplanet.sy_constellation:
            return None

        constellation = exoplanet.sy_constellation.strip()
        return f"Exoplanète de la constellation de {constellation}"
