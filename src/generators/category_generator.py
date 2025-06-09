# src/generators/category_generator.py
import yaml
from typing import Any, List, Dict


class CategoryGenerator:
    """
    Génère des catégories Wikipedia basées sur un ensemble de règles
    et les données d'un objet (exoplanète, étoile).
    """

    def __init__(self, rules_filepath="src/constants/categories_rules.yaml"):
        """Charge les règles depuis un fichier YAML."""
        with open(rules_filepath, "r", encoding="utf-8") as f:
            self.rules = yaml.safe_load(f)

    def get_categories(self, data_object: Any) -> List[str]:
        """
        Génère une liste de catégories pour l'objet de données fourni.

        Args:
            data_object: Une instance de classe (ex: Exoplanet) ayant des attributs
                         correspondant aux clés dans le fichier de règles.

        Returns:
            Une liste de chaînes de catégories Wikipedia uniques.
        """
        categories = set()  # Utiliser un set pour éviter les doublons

        # --- Règle 1: Mapped Categories ---
        if 'mapped' in self.rules:
            for attribute, mapping in self.rules['mapped'].items():
                if hasattr(data_object, attribute):
                    value = getattr(data_object, attribute)
                    if value:
                        # Gère les cas comme le type spectral (ex: 'G2V' -> 'G')
                        # On cherche la correspondance la plus spécifique d'abord
                        key_to_check = str(value)
                        if key_to_check in mapping:
                            categories.add(mapping[key_to_check])
                        # Sinon, on vérifie avec la première lettre (pour le type spectral)
                        elif len(key_to_check) > 1 and key_to_check[0] in mapping:
                            categories.add(mapping[key_to_check[0]])

        # --- Règle 2: Generated Categories ---
        if 'generated' in self.rules:
            for attribute, generator_rule in self.rules['generated'].items():
                if hasattr(data_object, attribute):
                    value = getattr(data_object, attribute)
                    if value:
                        template = generator_rule['template']
                        categories.add(template.format(value=value))

        # On pourrait ajouter d'autres types de règles ici (ranged, etc.)

        return sorted(list(categories))
