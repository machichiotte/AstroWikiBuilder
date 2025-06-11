# src/generators/star/star_category_generator.py
from typing import List, Optional, Callable
from src.models.data_source_star import DataSourceStar
from src.generators.base_category_generator import BaseCategoryGenerator
from src.utils.star_type_utils import StarTypeUtils


def int_to_roman(num):
    # Limité à 0-9 pour les sous-types spectraux
    roman_numerals = ["0", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"]
    try:
        n = int(float(num))
        return roman_numerals[n]
    except Exception:
        return None


class StarCategoryGenerator(BaseCategoryGenerator):
    """
    Classe pour générer les catégories des articles d'étoiles.
    Utilise un générateur de règles centralisé.
    """

    def __init__(self, rules_filepath: str = "src/constants/categories_rules.yaml"):
        super().__init__(rules_filepath)
        self.star_type_utils = StarTypeUtils()

    def get_object_type(self) -> str:
        return "star"

    def get_custom_rules(self) -> List[Callable]:
        return [
            self._get_spectral_type_category,
            self._get_spectral_subtype_roman_category,
            self._get_luminosity_class_category,
            self._get_star_type_category,
            self._get_variable_star_type_category,
        ]

    def _get_spectral_type_category(self, star: DataSourceStar) -> Optional[str]:
        """
        Catégorie basée sur la lettre principale du type spectral.
        """
        spectral_class = self.star_type_utils.get_spectral_class(star)
        if spectral_class:
            mapping = (
                self.generator.rules.get("star", {})
                .get("mapped", {})
                .get("st_spectral_type", {})
            )
            if spectral_class in mapping:
                return mapping[spectral_class]
            else:
                return f"[[Catégorie:Étoile de type spectral {spectral_class}]]"
        return None

    def _get_spectral_subtype_roman_category(
        self, star: DataSourceStar
    ) -> Optional[str]:
        """
        Catégorie basée sur le sous-type spectral, converti en chiffre romain.
        """
        if not star.st_spectral_type:
            return None

        spectral_type = star.st_spectral_type.value
        if not spectral_type:
            return None

        letter, subtype, _ = self.star_type_utils.parse_spectral_type(spectral_type)
        if letter and subtype:
            roman = int_to_roman(subtype)
            if roman:
                # Ajouter si besoin de categorie combinée (return f"[[Catégorie:Étoile de type spectral {letter}{roman}]]")
                return None
        return None

    def _get_luminosity_class_category(self, star: DataSourceStar) -> Optional[str]:
        """
        Catégorie basée sur la classe de luminosité (V, IV, III, etc.)
        """
        luminosity = self.star_type_utils.get_luminosity_class(star)
        if luminosity:
            mapping = (
                self.generator.rules.get("star", {})
                .get("mapped", {})
                .get("luminosity_class", {})
            )
            if luminosity in mapping:
                return mapping[luminosity]
            else:
                return f"[[Catégorie:Classe de luminosité {luminosity}]]"
        return None

    def _get_star_type_category(self, star: DataSourceStar) -> Optional[str]:
        """
        Règle personnalisée pour déterminer la catégorie de type d'étoile.
        """
        star_types = self.star_type_utils.get_star_type(star)
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
                categories.append(f"[[Catégorie:{star_type}]]")
            # Pour les types spectraux standards
            elif star_type.startswith("Étoile de type spectral"):
                categories.append(f"[[Catégorie:{star_type}]]")
            # Pour les étoiles variables
            elif star_type.startswith("Étoile variable"):
                categories.append(f"[[Catégorie:{star_type}]]")

        return "\n".join(categories) if categories else None

    def _get_variable_star_type_category(self, star: DataSourceStar) -> Optional[str]:
        """
        Règle personnalisée pour déterminer la catégorie de type d'étoile variable.
        """
        return None
