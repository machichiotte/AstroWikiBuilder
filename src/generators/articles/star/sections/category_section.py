# src/generators/articles/star/sections/category_section.py

from collections.abc import Callable

from src.generators.base.category_rules_manager import CategoryRulesManager
from src.models.entities.star_entity import Star
from src.utils.astro.classification.star_type_util import StarTypeUtil


class CategorySection:
    """
    Classe pour générer les catégories des articles d'étoiles.
    """

    def __init__(self, rules_filepath: str = "src/constants/categories_rules.yaml"):
        self._category_rules_manager = CategoryRulesManager(rules_filepath)
        self.star_type_util = StarTypeUtil()

    def generate(self, star: Star) -> str:
        """Génère la section des catégories."""
        categories = self.build_categories(star)
        if not categories:
            return ""

        # Séparer les catégories multiples (certaines fonctions retournent plusieurs catégories séparées par \n)
        all_categories = []
        for cat in categories:
            # Séparer les catégories multiples
            if "\n" in cat:
                all_categories.extend(cat.split("\n"))
            else:
                all_categories.append(cat)

        # Formater chaque catégorie avec le préfixe Wikipedia
        formatted_categories = []
        for cat in all_categories:
            cat = cat.strip()  # Enlever les espaces en début/fin
            if not cat:  # Ignorer les chaînes vides
                continue
            # Si la catégorie commence déjà par [[Catégorie:
            if cat.startswith("[[Catégorie:"):
                formatted_categories.append(cat)
            else:
                formatted_categories.append(f"[[Catégorie:{cat}]]")

        return "\n".join(formatted_categories)

    def build_categories(self, star: Star) -> list[str]:
        """
        Génère les catégories pour une étoile en utilisant les règles standard
        et les règles personnalisées.
        """
        custom_rules: list[Callable] = [
            self.append_static_planetary_system_category,
            self.map_catalog_prefix_to_category,
            self.map_spectral_type_to_category,
            self.map_luminosity_class_to_category,
            self.map_star_type_to_category,
            self.map_constellation_to_category,
        ]
        return self._category_rules_manager.generate_categories_for(
            star, "star", custom_rules=custom_rules
        )

    # --- Règles de catégorisation spécifiques aux "étoiles" ---

    def map_catalog_prefix_to_category(self, star: Star) -> str | None:
        """
        Génère les catégories de catalogue basées sur les préfixes des noms,
        au format [[Catégorie:XYZ|clef]].
        """
        catalog_mappings = (
            self._category_rules_manager.rules.get("star", {})
            .get("mapped", {})
            .get("prefix_catalog", {})
        )

        categories = set()

        def extract_key(name: str, prefix: str) -> str:
            key = name[len(prefix) :].strip()

            # Formatage spécial pour les objets Kepler : toujours 4 chiffres
            if prefix == "KEPLER-":
                try:
                    # Extraire le numéro après "KEPLER-"
                    number_part = key
                    # Essayer de convertir en entier pour vérifier que c'est un nombre
                    number = int(number_part)
                    # Formater avec 4 chiffres avec des zéros en tête
                    return f"{number:04d}"
                except (ValueError, TypeError):
                    # Si ce n'est pas un nombre, retourner tel quel
                    return key

            return key

        def process_name(raw_name: str):
            if not raw_name:
                return

            name = raw_name.strip().upper()
            for prefix, category in catalog_mappings.items():
                if name.startswith(prefix):
                    key = extract_key(name, prefix)
                    formatted = f"{category}|{key}"
                    categories.add(formatted)

        # Nom principal
        if star.st_name:
            process_name(star.st_name)

        # Noms alternatifs
        if star.st_altname:
            for alt_name in star.st_altname:
                process_name(alt_name)

        return "\n".join(sorted(categories)) if categories else None

    def map_spectral_type_to_category(self, star: Star) -> str | None:
        """
        Catégorie basée sur la lettre principale du type spectral.
        """
        spectral_class: str | None = self.star_type_util.extract_spectral_class_from_star(star)
        if spectral_class:
            mapping = (
                self._category_rules_manager.rules.get("star", {})
                .get("mapped", {})
                .get("st_spectral_type", {})
            )

            if spectral_class in mapping:
                return mapping[spectral_class]
            else:
                return f"Étoile de type spectral {spectral_class}"
        return None

    def map_luminosity_class_to_category(self, star: Star) -> str | None:
        """
        Catégorie basée sur la classe de luminosité (V, IV, III, etc.)
        """
        luminosity: str | None = self.star_type_util.extract_luminosity_class_from_star(star)
        if luminosity:
            mapping = (
                self._category_rules_manager.rules.get("star", {})
                .get("mapped", {})
                .get("luminosity_class", {})
            )
            if luminosity in mapping:
                return mapping[luminosity]
            else:
                return f"Classe de luminosité {luminosity}"
        return None

    def map_star_type_to_category(self, star: Star) -> str | None:
        """
        Règle personnalisée pour déterminer la catégorie de type d'étoile.
        """
        star_types: list[str] = self.star_type_util.determine_star_types_from_properties(star)
        if not star_types:
            return None

        categories = []
        for star_type in star_types:
            # Pour les types spéciaux (naine blanche, naine brune, etc.)
            if star_type in [
                "Naine blanche",
                "Naine brune",
                "Étoile Wolf-Rayet",
                "Étoile à neutrons",
                "Naine rouge",
                "Naine jaune",
                "Naine bleue",
                "Géante rouge",
                "Géante bleue",
                "Géante jaune",
                "Supergéante rouge",
                "Supergéante bleue",
                "Étoile pauvre en métaux",
                "Étoile riche en métaux",
            ]:
                categories.append(star_type)
            # Pour les types spectraux standards
            elif star_type.startswith("Étoile de type spectral"):
                categories.append(star_type)
            # Pour les étoiles variables
            elif star_type.startswith("Étoile variable"):
                categories.append(star_type)

        return "\n".join(categories) if categories else None

    def append_static_planetary_system_category(self, star: Star) -> str | None:
        """
        Ajoute une catégorie personnalisée pour le système planétaire.
        """
        return "Système planétaire"

    def map_constellation_to_category(self, star: Star) -> str | None:
        """
        Règle commune pour déterminer la catégorie de constellation.
        Fonctionne pour tout objet ayant un attribut 'sy_constellation'.
        """
        if hasattr(star, "sy_constellation") and star.sy_constellation:
            constellation: str = star.sy_constellation

            mapping = (
                self._category_rules_manager.rules.get("common", {})
                .get("mapped", {})
                .get("sy_constellation", {})
            )

            if constellation in mapping:
                return mapping[constellation]
        return None
