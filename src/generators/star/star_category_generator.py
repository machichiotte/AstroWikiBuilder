# src/generators/star/star_category_generator.py
from typing import List, Optional
from src.models.data_source_star import DataSourceStar
from src.generators.category_generator import CategoryGenerator
import re


def int_to_roman(num):
    # Limité à 0-9 pour les sous-types spectraux
    roman_numerals = ['0', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX']
    try:
        n = int(float(num))
        return roman_numerals[n]
    except Exception:
        return None


class StarCategoryGenerator:
    """
    Classe pour générer les catégories des articles d'étoiles.
    Utilise un générateur de règles centralisé.
    """

    def __init__(self, rules_filepath: str = "src/constants/categories_rules.yaml"):
        """
        Initialise le générateur de catégories.
        """
        self.generator = CategoryGenerator(rules_filepath)

    def _parse_spectral_type(self, spectral_type: str):
        """
        Parse un type spectral complexe (ex: 'K1 V', 'G2V', 'M4.5+/-0.5', 'F8/G0 V', etc.)
        Retourne (lettre, sous-type, classe de luminosité) ou None si non reconnu.
        """
        # Exemples : 'K1 V', 'G2V', 'M4.5+/-0.5', 'F8/G0 V', 'K0III', 'G5 IV/V'
        match = re.match(r"([OBAFGKMLTY])\s*([0-9.]*)\s*([IV]+)?", spectral_type)
        if match:
            letter = match.group(1)
            subtype = match.group(2) if match.group(2) else None
            luminosity = match.group(3) if match.group(3) else None
            return letter, subtype, luminosity
        return None, None, None

    def _get_spectral_type_category(self, star: DataSourceStar) -> Optional[str]:
        """
        Catégorie basée sur la lettre principale du type spectral.
        """
        spectral_type_str = star.st_spectral_type.value if star.st_spectral_type else ""
        letter, subtype, _ = self._parse_spectral_type(spectral_type_str)
        mapping = self.generator.rules.get("star", {}).get("mapped", {}).get("st_spectral_type", {})
        if letter:
            if letter in mapping:
                return mapping[letter]
            else:
                return f"[[Catégorie:Étoile de type spectral {letter}]]"
        return None

    def _get_spectral_subtype_roman_category(self, star: DataSourceStar) -> Optional[str]:
        """
        Catégorie basée sur le sous-type spectral, converti en chiffre romain.
        """
        spectral_type_str = star.st_spectral_type.value if star.st_spectral_type else ""
        letter, subtype, _ = self._parse_spectral_type(spectral_type_str)
        if letter and subtype:
            roman = int_to_roman(subtype)
            if roman:
                return f"[[Catégorie:Étoile de type spectral {letter}{roman}]]"
        return None

    def _get_luminosity_class_category(self, star: DataSourceStar) -> Optional[str]:
        """
        Catégorie basée sur la classe de luminosité (V, IV, III, etc.)
        """
        spectral_type_str = star.st_spectral_type.value if star.st_spectral_type else ""
        _, _, luminosity = self._parse_spectral_type(spectral_type_str)
        if luminosity:
            mapping = self.generator.rules.get("star", {}).get("mapped", {}).get("luminosity_class", {})
            if luminosity in mapping:
                return mapping[luminosity]
            else:
                return f"[[Catégorie:Classe de luminosité {luminosity}]]"
        return None

    def _get_star_type_category(self, star: DataSourceStar) -> Optional[str]:
        """
        Règle personnalisée pour déterminer la catégorie de type d'étoile (naine blanche,
        naine brune, étoile à neutrons, etc.).
        Cette logique dépendra des attributs disponibles dans DataSourceStar pour classifier l'étoile.
        Exemple rudimentaire basé sur le type spectral ou d'autres attributs comme la masse/rayon si disponibles.
        """
        spectral_type_str = star.st_spectral_type.value if star.st_spectral_type else ""
        mass_value = star.st_mass.value if star.st_mass else None
        radius_value = star.st_radius.value if star.st_radius else None

        if 'D' in spectral_type_str: # Souvent pour les naines blanches
            return '[[Catégorie:Naine blanche]]'
        if 'L' in spectral_type_str or 'T' in spectral_type_str or 'Y' in spectral_type_str:
            # Assumant que ces types spectraux indiquent une naine brune
            return '[[Catégorie:Naine brune]]'
        # D'autres classifications nécessiteraient des règles plus sophistiquées
        # basées sur les données disponibles (ex: masse très faible pour naine brune,
        # masse très élevée/rayon très petit pour étoile à neutrons, etc.)
        # Pour les étoiles chimiquement particulières, un attribut spécifique pourrait être nécessaire.
        return None

    def _get_variable_star_type_category(self, star: DataSourceStar) -> Optional[str]:
        """
        Règle personnalisée pour déterminer la catégorie de type d'étoile variable.
        DataSourceStar ne semble pas avoir un attribut direct 'variable_type'.
        Cette logique devrait dériver le type variable à partir d'autres propriétés
        ou d'une liste de types variables associés au nom de l'étoile si disponible.
        C'est un exemple générique; l'implémentation exacte dépend des données sources.
        """
        # Si un champ 'is_variable' ou 'variable_type_classification' existe dans DataSourceStar, l'utiliser.
        # Par exemple, si star.variable_type est une chaîne comme "Delta Scuti"
        # var_type_data = star.variable_type.value if hasattr(star, 'variable_type') and star.variable_type else None
        # Si DataSourceStar a un champ pour cela:
        # if var_type_data == 'Delta Scuti':
        #     return '[[Catégorie:Étoile variable de type Delta Scuti]]'
        # else:
        #     return None # Ou plus de logique de mapping
        return None # Retourne None car il n'y a pas de champ direct dans DataSourceStar pour le moment

    def generate_categories(self, star: DataSourceStar) -> List[str]:
        """
        Génère les catégories pour une étoile en déléguant au générateur de règles
        et en ajoutant des règles personnalisées pour les types complexes.
        """
        custom_rules = [
            self._get_spectral_type_category,
            self._get_spectral_subtype_roman_category,
            self._get_luminosity_class_category,
            self._get_star_type_category,
            self._get_variable_star_type_category,
            # Ajoutez d'autres règles personnalisées ici si nécessaire
        ]
        return self.generator.generate(star, "star", custom_rules=custom_rules)