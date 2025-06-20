# src/generators/star/star_category_generator.py
from typing import List, Optional, Callable
from src.models.entities.star import Star
from src.generators.base_category_generator import BaseCategoryGenerator
from src.utils.astro.classification.star_type_utils import StarTypeUtils
from src.utils.astro.classification.star_type_utils import SpectralComponents


# ============================================================================
# UTILITAIRES
# ============================================================================
def convert_integer_to_roman(num):
    # Limité à 0-9 pour les sous-types spectraux
    roman_numerals: List[str] = [
        "0",
        "I",
        "II",
        "III",
        "IV",
        "V",
        "VI",
        "VII",
        "VIII",
        "IX",
    ]
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

    # ============================================================================
    # INITIALISATION
    # ============================================================================
    def __init__(self, rules_filepath: str = "src/constants/categories_rules.yaml"):
        super().__init__(rules_filepath)
        self.star_type_utils = StarTypeUtils()

    # ============================================================================
    # MÉTHODES DE BASE
    # ============================================================================
    def get_object_type(self) -> str:
        return "star"

    def list_category_rules(self) -> List[Callable]:
        return [
            self.add_custom_category,
            self.resolve_catalog_category,
            self.map_spectral_type_to_category,
            self.convert_spectral_subtype_to_roman_category,
            self.map_luminosity_class_to_category,
            self.resolve_star_type_category,
            self.resolve_variable_star_category,
        ]

    # ============================================================================
    # MAPPINGS ET CATÉGORIES
    # ============================================================================
    def resolve_catalog_category(self, star: Star) -> Optional[str]:
        """
        Génère les catégories de catalogue basées sur les préfixes des noms,
        au format [[Catégorie:XYZ|clef]].
        """
        catalog_mappings = (
            self.generator.rules.get("star", {})
            .get("mapped", {})
            .get("prefix_catalog", {})
        )

        categories = set()

        def extract_key(name: str, prefix: str) -> str:
            return name[len(prefix) :].strip()

        def process_name(raw_name: str):
            if not raw_name:
                return

            name = raw_name.strip().upper()
            for prefix, category in catalog_mappings.items():
                if name.startswith(prefix):
                    key = extract_key(name, prefix)
                    formatted = (
                        f"{category}|{key}]]"  # Catégorie déjà incluse dans YAML
                    )
                    formatted = formatted.replace(
                        "]]", ""
                    )  # nettoyer pour éviter ]] de trop
                    categories.add(f"{formatted}]]")

        # Nom principal
        if star.st_name:
            process_name(star.st_name)

        # Noms alternatifs
        if star.st_altname:
            for alt_name in star.st_altname:
                process_name(alt_name)

        return "\n".join(sorted(categories)) if categories else None

    def map_spectral_type_to_category(self, star: Star) -> Optional[str]:
        """
        Catégorie basée sur la lettre principale du type spectral.
        """
        spectral_class: str | None = (
            self.star_type_utils.extract_spectral_class_from_star(star)
        )
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

    def convert_spectral_subtype_to_roman_category(self, star: Star) -> Optional[str]:
        """
        Catégorie basée sur le sous-type spectral, converti en chiffre romain.
        """
        if not star.st_spectral_type:
            return None

        spectral_type: str = star.st_spectral_type
        if not spectral_type:
            return None

        spectral_component: SpectralComponents = (
            self.star_type_utils.extract_spectral_components_from_string(spectral_type)
        )

        if spectral_component.spectral_class and spectral_component.subtype:
            roman: str | None = convert_integer_to_roman(spectral_component.subtype)
            if roman:
                #  Ajouter si besoin de categorie combinée (return f"[[Catégorie:Étoile de type spectral {letter}{roman}]]")
                return None
        return None

    def map_luminosity_class_to_category(self, star: Star) -> Optional[str]:
        """
        Catégorie basée sur la classe de luminosité (V, IV, III, etc.)
        """
        luminosity: str | None = (
            self.star_type_utils.extract_luminosity_class_from_star(star)
        )
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

    # ============================================================================
    # RÈGLES PERSONNALISÉES
    # ============================================================================
    def resolve_star_type_category(self, star: Star) -> Optional[str]:
        """
        Règle personnalisée pour déterminer la catégorie de type d'étoile.
        """
        star_types: List[str] = (
            self.star_type_utils.determine_star_types_from_properties(star)
        )
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

    def resolve_variable_star_category(self, star: Star) -> Optional[str]:
        """
        Règle personnalisée pour déterminer la catégorie de type d'étoile variable.
        """
        return None

    def add_custom_category(self, star: Star) -> Optional[str]:
        """
        Ajoute une catégorie personnalisée pour le système planétaire.
        """
        return "\n[[Catégorie:Système planétaire]]"

    def add_catalogs_category(self, star: Star) -> Optional[str]:
        """
        #ici dans star.st_name on a le prefix qui nous donne le catalogue mais il faut le numero
        car


        idem dans star.alt_names qui contient plusieurs string
        """
        return "\n[[Catégorie:Système planétaire]]"
