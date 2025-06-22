# src/generators/base/base_category_generator.py
from abc import ABC, abstractmethod
from typing import List, Callable, Optional, Any
from src.generators.base.category_rules_manager import CategoryRulesManager


class BaseCategoryGenerator(ABC):
    """
    Classe de base abstraite pour les générateurs de catégories.
    Fournit une structure commune et des méthodes utilitaires pour la génération de catégories.
    """

    def __init__(self, rules_filepath: str = "src/constants/categories_rules.yaml"):
        self._category_rules_manager = CategoryRulesManager(rules_filepath)

    # --- Méthodes à implémenter par les classes filles ---

    @abstractmethod
    def retrieve_object_type(self) -> str:
        """
        Retourne le type d'objet pour la génération de catégories.
        À implémenter par les classes filles.
        """
        pass

    @abstractmethod
    def define_category_rules(self) -> List[Callable]:
        """
        Retourne la liste des règles personnalisées pour le type d'objet.
        À implémenter par les classes filles.
        """
        pass

    # --- Moteur de génération principal ---

    def build_categories(self, obj) -> List[str]:
        """
        Génère les catégories pour un objet en utilisant les règles standard
        et les règles personnalisées.

        Args:
            obj: L'objet pour lequel générer les catégories

        Returns:
            Liste des catégories générées
        """
        custom_rules: List[Callable] = self.define_category_rules()
        return self._category_rules_manager.generate_categories_for(
            obj, self.retrieve_object_type(), custom_rules=custom_rules
        )

    def map_constellation_to_category(self, obj: Any) -> Optional[str]:
        """
        Règle commune pour déterminer la catégorie de constellation.
        Fonctionne pour tout objet ayant un attribut 'sy_constellation'.
        """
        if hasattr(obj, "sy_constellation") and obj.sy_constellation:
            constellation: str = obj.sy_constellation

            mapping = (
                self._category_rules_manager.rules.get("common", {})
                .get("mapped", {})
                .get("sy_constellation", {})
            )

            if constellation in mapping:
                return mapping[constellation]
        return None
