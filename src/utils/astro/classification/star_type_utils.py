# src/utils/astro/classification/star_type_utils.py
# ============================================================================
# IMPORTS
# ============================================================================
from dataclasses import dataclass
from re import Match, search
from typing import Optional, Tuple, List

from src.models.entities.star import Star
from src.models.entities.exoplanet import Exoplanet


@dataclass
class SpectralComponents:
    spectral_class: Optional[str]
    subtype: Optional[str]
    luminosity_class: Optional[str]


# ============================================================================
# DÉCLARATION DE LA CLASSE StarTypeUtils
# ============================================================================
class StarTypeUtils:
    """
    Classe utilitaire pour déterminer les types d'étoiles.
    """

    # ============================================================================
    # MÉTHODES DE PARSING ET UTILITAIRES DE BASE
    # ============================================================================
    @staticmethod
    def extract_spectral_components_from_string(
        spectral_type: str,
    ) -> SpectralComponents:
        """
        Extrait les composants spectroscopiques d'une chaîne brute, en tolérant les formats hybrides.
        """

        # Nettoyage rapide : virer les annotations connues parasites
        cleaned = spectral_type.strip().replace(":", "")
        cleaned = cleaned.replace("var", "").replace("Ve", "")
        cleaned = cleaned.replace("e", "").replace("P", "")
        cleaned = cleaned.replace("(+ G)", "").replace("+ G", "")
        cleaned = cleaned.split()[
            0
        ]  # Se concentrer sur le premier bloc (éviter les `/`, etc.)

        # Exemple : "G2 IV/V" -> "G2", "IV/V"
        regex = r"""(?ix)  # ignore case, verbose
            (?P<class>[OBAFGKMLTYWDsdDCQ]+)      # Spectral class
            [\s\-:/]*
            (?P<subtype>[0-9.\-+/]+)?           # Subtype (optionnel)
            [\s\-:/]*                           # séparateur
            (?P<luminosity>I{1,3}[ab]?(?:/?[IV]+)?)?  # Classe de luminosité : III, IIIb, IV, V, IV-V etc.
        """

        match: Optional[Match] = search(regex, cleaned)

        if match:
            spectral_class = match.group("class")
            subtype = match.group("subtype") or None
            luminosity = match.group("luminosity") or None

            return SpectralComponents(spectral_class, subtype, luminosity)

        # Fallback
        return SpectralComponents(None, None, None)

    @staticmethod
    def get_temperature_range_for_spectral_class(letter: str) -> Tuple[float, float]:
        """
        Retourne la plage de température pour un type spectral donné.
        """
        ranges = {
            "O": (30000, float("inf")),
            "B": (10000, 30000),
            "A": (7500, 10000),
            "F": (6000, 7500),
            "G": (5200, 6000),
            "K": (3700, 5200),
            "M": (0, 3700),
        }
        return ranges.get(letter, (0, 0))

    @staticmethod
    def infer_evolutionary_stage_from_spectral_data(
        spectral_class: str, luminosity: Optional[str]
    ) -> Optional[str]:
        """
        Détermine le stade évolutif de l'étoile basé sur ses caractéristiques.
        """
        if not luminosity:
            return None

        # Naines
        if luminosity == "V":
            if spectral_class in ["K", "M"]:
                return "Naine rouge"
            elif spectral_class == "G":
                return "Naine jaune"
            elif spectral_class in ["O", "B"]:
                return "Naine bleue"
            return "Naine"

        # Géantes
        if luminosity == "III":
            if spectral_class in ["K", "M"]:
                return "Géante rouge"
            elif spectral_class in ["O", "B"]:
                return "Géante bleue"
            elif spectral_class in ["F", "G"]:
                return "Géante jaune"
            return "Géante"

        # Supergéantes
        if luminosity == "I":
            if spectral_class in ["K", "M"]:
                return "Supergéante rouge"
            elif spectral_class in ["O", "B"]:
                return "Supergéante bleue"
            return "Supergéante"

        return None

    # ============================================================================
    # MÉTHODE PRINCIPALE DE DÉTERMINATION DE TYPE
    # ============================================================================
    @staticmethod
    def determine_star_types_from_properties(obj: Star | Exoplanet) -> List[str]:
        """
        Détermine le type d'étoile basé sur ses caractéristiques.
        Retourne une liste de types d'étoiles (ex: ["Étoile de type spectral KIII", "Géante rouge"])
        """
        types = []

        if not obj.st_spectral_type:
            return types

        spectral_type: str = obj.st_spectral_type
        if not spectral_type:
            return types

        spectral_components: SpectralComponents = (
            StarTypeUtils.extract_spectral_components_from_string(spectral_type)
        )

        spectral_class = spectral_components.spectral_class
        subtype = spectral_components.subtype
        luminosity = spectral_components.luminosity_class
        if not spectral_class:
            return types

        # Types spéciaux
        if "D" in spectral_type:
            types.append("Naine blanche")
            return types
        if any(t in spectral_type for t in ["L", "T", "Y"]):
            types.append("Naine brune")
            return types
        if "W" in spectral_type:
            types.append("Étoile Wolf-Rayet")
            return types
        if "S" in spectral_type:
            types.append("Étoile de type spectral S")
            return types
        if "C" in spectral_type:
            types.append("Étoile de type spectral C")
            return types

        # Étoile à neutrons (basé sur des caractéristiques physiques)
        if obj.st_mass and obj.st_radius:
            try:
                mass = float(obj.st_mass.value)
                radius = float(obj.st_radius.value)
                # Une étoile à neutrons typique a une masse > 1.4 M☉ et un rayon très petit
                if mass > 1.4 and radius < 0.01:
                    types.append("Étoile à neutrons")
                    return types
            except (ValueError, TypeError):
                pass

        # Étoile variable (nécessiterait un attribut spécifique)
        # if hasattr(star, 'is_variable') and star.is_variable:
        #     return "Étoile variable"

        # Étoile chimiquement particulière (nécessiterait des attributs spécifiques)
        # if hasattr(star, 'peculiar_type'):
        #     return f"Étoile {star.peculiar_type}"

        # Stade évolutif
        evolutionary_stage: str | None = (
            StarTypeUtils.infer_evolutionary_stage_from_spectral_data(
                spectral_class, luminosity
            )
        )
        if evolutionary_stage:
            types.append(evolutionary_stage)

        # Étoile variable
        if obj.st_variability and obj.st_variability.value:
            types.append(f"Étoile variable de type {obj.st_variability.value}")

        # Étoile chimiquement particulière
        if obj.st_metallicity:
            try:
                metallicity = float(obj.st_metallicity.value)
                if metallicity < -1.0:
                    types.append("Étoile pauvre en métaux")
                elif metallicity > 0.5:
                    types.append("Étoile riche en métaux")
            except (ValueError, TypeError):
                pass

        # Type spectral standard
        type_parts: List[str] = [f"Étoile de type spectral {spectral_class}"]

        # Ajouter le sous-type si présent
        if subtype:
            type_parts.append(subtype)

        # Ajouter la classe de luminosité si présente
        if luminosity:
            type_parts.append(luminosity)

        types.append("".join(type_parts))
        return types

    # ============================================================================
    # MÉTHODES D'ACCÈS RAPIDE
    # ============================================================================
    @staticmethod
    def extract_luminosity_class_from_star(star: Star) -> Optional[str]:
        """
        Détermine la classe de luminosité de l'étoile.
        Retourne la classe de luminosité (ex: "V", "III", etc.)
        """
        if not star.st_spectral_type:
            return None

        spectral_type: str = star.st_spectral_type
        if not spectral_type:
            return None

        spectral_components: SpectralComponents = (
            StarTypeUtils.extract_spectral_components_from_string(spectral_type)
        )
        return spectral_components.luminosity_class

    @staticmethod
    def extract_spectral_class_from_star(star: Star) -> Optional[str]:
        """
        Détermine la classe spectrale de l'étoile.
        Retourne la classe spectrale (ex: "K", "G", etc.)
        """
        if not star.st_spectral_type:
            return None

        spectral_type: str = star.st_spectral_type
        if not spectral_type:
            return None

        spectral_component: SpectralComponents = (
            StarTypeUtils.extract_spectral_components_from_string(spectral_type)
        )
        return spectral_component.spectral_class
