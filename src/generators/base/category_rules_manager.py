# src/generators/base/category_rules_manager.py
import yaml
from typing import Any, List, Dict, Optional, Set, Callable


class CategoryRulesManager:
    """
    Génère des catégories Wikipedia basées sur un ensemble de règles
    et les données d'un objet (exoplanète, étoile).
    """

    def __init__(self, rules_filepath: str = "src/constants/categories_rules.yaml"):
        with open(rules_filepath, "r", encoding="utf-8") as f:
            self.rules: Dict = yaml.safe_load(f)

    def _retrieve_attribute_value(
        self, data_object: Any, attribute: str
    ) -> Optional[Any]:
        """Récupère la valeur d'un attribut, même s'il est dans un objet .value"""
        if hasattr(data_object, attribute):
            attr = getattr(data_object, attribute)
            if hasattr(attr, "value"):
                return attr.value
            return attr
        return None

    def generate_categories_for(
        self,
        data_object: Any,
        rule_key: str,
        custom_rules: Optional[List[Callable[[Any], Optional[str]]]] = None,
    ) -> List[str]:
        """
        Génère une liste de catégories pour l'objet de données fourni.
        """
        categories: Set[str] = set()
        config = self.rules.get(rule_key, {})
        common_config = self.rules.get("common", {})

        # 1. Catégorie de base
        if "base" in config:
            categories.add(config["base"])

        # 2. Règles de mapping (spécifiques et communes)
        all_mappings = {**common_config.get("mapped", {}), **config.get("mapped", {})}
        for attribute, mapping in all_mappings.items():
            value = self._retrieve_attribute_value(data_object, attribute)
            if value is None:
                continue

            value_str = str(value)
            # Essayer une correspondance exacte
            if value_str in mapping:
                categories.add(mapping[value_str])
                continue

            # Essayer une correspondance partielle (pour les types spectraux ou instruments)
            for key, cat in mapping.items():
                if key in value_str:
                    categories.add(cat)
                    break

        # 3. Règles de génération
        if "generated" in config:
            for attribute, rule in config["generated"].items():
                value = self._retrieve_attribute_value(data_object, attribute)
                if value:
                    if rule.get("value_extractor") == "year" and hasattr(value, "year"):
                        value = value.year

                    template = rule["template"]
                    categories.add(template.format(value=int(value)))

        # 4. Règles personnalisées (pour la logique complexe)
        if custom_rules:
            for rule_func in custom_rules:
                category = rule_func(data_object)
                if category:
                    categories.add(category)

        return sorted(list(categories))
