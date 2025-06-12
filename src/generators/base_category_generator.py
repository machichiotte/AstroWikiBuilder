from abc import ABC, abstractmethod
from typing import List, Callable
from src.generators.category_generator import CategoryGenerator


class BaseCategoryGenerator(ABC):
    """
    Classe de base abstraite pour les générateurs de catégories.
    Fournit une structure commune pour la génération de catégories.
    """

    def __init__(self, rules_filepath: str = "src/constants/categories_rules.yaml"):
        """
        Initialise le générateur de catégories.

        Args:
            rules_filepath: Chemin vers le fichier de règles YAML
        """
        self.generator = CategoryGenerator(rules_filepath)

    @abstractmethod
    def get_custom_rules(self) -> List[Callable]:
        """
        Retourne la liste des règles personnalisées pour le type d'objet.
        À implémenter par les classes filles.
        """
        pass

    def generate_categories(self, obj) -> List[str]:
        """
        Génère les catégories pour un objet en utilisant les règles standard
        et les règles personnalisées.

        Args:
            obj: L'objet pour lequel générer les catégories

        Returns:
            Liste des catégories générées
        """
        custom_rules = self.get_custom_rules()
        return self.generator.generate(
            obj, self.get_object_type(), custom_rules=custom_rules
        )

    @abstractmethod
    def get_object_type(self) -> str:
        """
        Retourne le type d'objet pour la génération de catégories.
        À implémenter par les classes filles.
        """
        pass
