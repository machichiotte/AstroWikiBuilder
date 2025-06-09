# src/generators/star/star_category_generator.py
from typing import List, Optional
from src.models.data_source_star import DataSourceStar
from src.generators.category_generator import CategoryGenerator


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

    def _get_luminosity_class_category(self, star: DataSourceStar) -> Optional[str]:
        """
        Règle personnalisée pour déterminer la catégorie de classe de luminosité.
        Nécessite une logique pour déduire la classe de luminosité des attributs de l'étoile
        (ex: du type spectral complet si disponible, ou de la luminosité absolue).
        Puisque DataSourceStar n'a pas de champ direct 'luminosity_class', cette logique
        doit être implémentée ici. Pour l'instant, c'est un exemple et nécessiterait
        une implémentation basée sur les données réelles disponibles pour la détermination
        de la classe de luminosité (e.g., parsing du spectral_type complet, ou calcul).
        """
        # Exemple: Si spectral_type contient une classe de luminosité (ex: "G2V", "B0Ia")
        spectral_type_str = star.spectral_type.value if star.spectral_type else ""
        if 'Iab' in spectral_type_str or 'Ia' in spectral_type_str:
            return '[[Catégorie:Classe de luminosité Ia]]'
        elif 'Ib' in spectral_type_str:
            return '[[Catégorie:Classe de luminosité Ib]]'
        elif 'II' in spectral_type_str:
            return '[[Catégorie:Classe de luminosité II]]'
        elif 'III' in spectral_type_str:
            return '[[Catégorie:Classe de luminosité III]]'
        elif 'IV' in spectral_type_str:
            return '[[Catégorie:Classe de luminosité IV]]'
        elif 'V' in spectral_type_str: # Séquence principale
            return '[[Catégorie:Classe de luminosité V]]'
        elif 'VI' in spectral_type_str: # Sous-naine
            return '[[Catégorie:Classe de luminosité VI]]'
        elif 'D' in spectral_type_str: # Naine blanche
            return '[[Catégorie:Classe de luminosité D]]' # Non dans le YAML précédent, mais commun pour naines blanches
        return None

    def _get_star_type_category(self, star: DataSourceStar) -> Optional[str]:
        """
        Règle personnalisée pour déterminer la catégorie de type d'étoile (naine blanche,
        naine brune, étoile à neutrons, etc.).
        Cette logique dépendra des attributs disponibles dans DataSourceStar pour classifier l'étoile.
        Exemple rudimentaire basé sur le type spectral ou d'autres attributs comme la masse/rayon si disponibles.
        """
        spectral_type_str = star.spectral_type.value if star.spectral_type else ""
        mass_value = star.mass.value if star.mass else None
        radius_value = star.radius.value if star.radius else None

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
            self._get_luminosity_class_category,
            self._get_star_type_category,
            self._get_variable_star_type_category,
            # Ajoutez d'autres règles personnalisées ici si nécessaire
        ]
        return self.generator.generate(star, "star", custom_rules=custom_rules)