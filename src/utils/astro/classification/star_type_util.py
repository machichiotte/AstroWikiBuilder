# src/utils/astro/classification/star_type_util.py
# ============================================================================
# IMPORTS
# ============================================================================
import re
from dataclasses import dataclass

from src.constants.wikipedia_field_config import STELLAR_EVOLUTION_MAP
from src.models.entities.exoplanet_entity import Exoplanet
from src.models.entities.star_entity import Star


# ============================================================================
# DATACLASS POUR LES COMPOSANTS SPECTRAUX
# ============================================================================
@dataclass
class SpectralComponents:
    spectral_class: str | None
    subtype: str | None
    luminosity_class: str | None


# ============================================================================
# CLASSE PRINCIPALE StarTypeUtil
# ============================================================================
class StarTypeUtil:
    """
    Classe utilitaire pour déterminer les types d'étoiles.
    """

    # ============================================================================
    # 1. PARSING ET EXTRACTION DE COMPOSANTS
    # ============================================================================
    @staticmethod
    def extract_spectral_components_from_string(
        spectral_type: str,
    ) -> SpectralComponents:
        """
        Extrait les composants spectroscopiques d'une chaîne brute, en tolérant les formats hybrides.
        """

        cleaned = spectral_type.strip()
        for noise in ["var", "Ve", "e", "P", "(+ G)", "+ G", "CH+0.4", "CN+1", "Fe-1"]:
            cleaned = cleaned.replace(noise, "")
        cleaned = cleaned.replace(":", "")

        # Nouvelle regex plus simple et robuste
        regex = re.compile(
            r"""
            ^\s*
            (?P<class>[OBAFGKMLTYWDsdDCQ]{1,3})   # classe spectrale obligatoire
            \s*
            (?P<subtype>\d+(\.\d+)?(?:\+/-\d+(\.\d+)?)?)?  # sous-type avec tolérance
            \s*
            (?P<luminosity>I{1,3}[ab]?|IV-?V?|VI|V)?       # classe de luminosité
            """,
            re.IGNORECASE | re.VERBOSE,
        )

        match = regex.match(cleaned)
        if match:
            return SpectralComponents(
                spectral_class=match.group("class"),
                subtype=match.group("subtype") or None,
                luminosity_class=match.group("luminosity") or None,
            )

        return SpectralComponents(None, None, None)

    # ============================================================================
    # 2. MÉTHODES D'ACCÈS RAPIDE
    # ============================================================================
    @staticmethod
    def extract_luminosity_class_from_star(star: Star) -> str | None:
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
            StarTypeUtil.extract_spectral_components_from_string(spectral_type)
        )
        return spectral_components.luminosity_class

    @staticmethod
    def extract_spectral_class_from_star(star: Star) -> str | None:
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
            StarTypeUtil.extract_spectral_components_from_string(spectral_type)
        )
        return spectral_component.spectral_class

    # ============================================================================
    # 3. UTILITAIRES
    # ============================================================================
    @staticmethod
    def get_temperature_range_for_spectral_class(letter: str) -> tuple[float, float]:
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

    # ============================================================================
    # 4. DÉTERMINATION DE TYPE (MÉTHODE PRINCIPALE ET HELPERS)
    # ============================================================================
    @staticmethod
    def determine_star_types_from_properties(obj: Star | Exoplanet) -> list[str]:
        """
        Détermine le type d'étoile basé sur ses caractéristiques.
        Retourne une liste de types d'étoiles (ex: ["Étoile de type spectral KIII", "Géante rouge"]).
        """
        types = []
        if not obj.st_spectral_type:
            return types
        spectral_components = StarTypeUtil.extract_spectral_components_from_string(
            obj.st_spectral_type
        )
        spectral_class = spectral_components.spectral_class
        subtype = spectral_components.subtype
        luminosity = spectral_components.luminosity_class

        if not spectral_class:
            return types
        types += StarTypeUtil._get_neutron_star_type(obj)
        types += StarTypeUtil._get_evolutionary_stages(spectral_class, luminosity)
        types += StarTypeUtil._get_variability_type(obj)
        types += StarTypeUtil._get_metallicity_type(obj)
        types += StarTypeUtil._get_raw_spectral_type(
            spectral_class, subtype, luminosity
        )
        return types

    @staticmethod
    def _get_neutron_star_type(obj: Star | Exoplanet) -> list[str]:
        if obj.st_mass and obj.st_radius:
            try:
                mass = float(obj.st_mass.value)
                radius = float(obj.st_radius.value)
                if mass > 1.4 and radius < 0.01:
                    return ["Étoile à neutrons"]
            except (ValueError, TypeError):
                pass
        return []

    @staticmethod
    def _get_evolutionary_stages(
        spectral_class: str, luminosity: str | None
    ) -> list[str]:
        stages = []
        stage1 = StarTypeUtil.infer_evolutionary_stage_from_spectral_data(
            spectral_class, luminosity
        )
        if stage1:
            stages.append(stage1)
        stage2 = StarTypeUtil.infer_evolutionary_stage_from_spectral_class(
            spectral_class
        )
        if stage2:
            stages.append(stage2)
        return stages

    @staticmethod
    def _get_variability_type(obj: Star | Exoplanet) -> list[str]:
        if obj.st_variability and obj.st_variability.value:
            return [f"Étoile variable de type {obj.st_variability.value}"]
        return []

    @staticmethod
    def _get_metallicity_type(obj: Star | Exoplanet) -> list[str]:
        if obj.st_metallicity:
            try:
                metallicity = float(obj.st_metallicity.value)
                if metallicity < -1.0:
                    return ["Étoile pauvre en métaux"]
                elif metallicity > 0.5:
                    return ["Étoile riche en métaux"]
            except (ValueError, TypeError):
                pass
        return []

    @staticmethod
    def _get_raw_spectral_type(
        spectral_class: str, subtype: str | None, luminosity: str | None
    ) -> list[str]:
        parts = [f"Étoile de type spectral {spectral_class}"]
        if subtype:
            parts.append(subtype)
        if luminosity:
            parts.append(luminosity)
        return ["".join(parts)]

    # ============================================================================
    # 5. STADE ÉVOLUTIF
    # ============================================================================
    @staticmethod
    def infer_evolutionary_stage_from_spectral_data(
        spectral_class: str | None, luminosity: str | None
    ) -> str | None:
        """
        Déduit le stade évolutif d'une étoile à partir de sa classe spectrale et de luminosité.
        """
        if not spectral_class or not luminosity:
            return None
        class_letter = spectral_class.strip().upper()
        lum_key = (
            luminosity.strip()
            .upper()
            .replace("IAB", "I")
            .replace("IB", "I")
            .replace("IAB-IB", "I")
            .replace("IIIb", "III")
            .replace("IV-V", "V")
            .replace("IV/V", "V")
            .replace("III-IV", "III")
            .replace("IV", "IV")
        )
        # Cas des naines blanches
        if class_letter in ["DC", "DQ", "DA", "DB", "WD", "DO", "DZ"]:
            return STELLAR_EVOLUTION_MAP.get("VII", {}).get(
                class_letter, "Naine blanche"
            )
        # Recherche progressive
        for lum_class, class_map in STELLAR_EVOLUTION_MAP.items():
            if lum_key.startswith(lum_class):
                match = class_map.get(class_letter)
                if match:
                    return match
        # Pas trouvé
        return None

    @staticmethod
    def infer_evolutionary_stage_from_spectral_class(
        spectral_class: str | None,
    ) -> str | None:
        """
        Déduit le stade évolutif d'une étoile à partir de sa classe spectrale et de luminosité.
        """
        # Types spéciaux
        if "D" in spectral_class:
            return "Naine blanche"
        if any(t in spectral_class for t in ["L", "T", "Y"]):
            return "Naine brune"
        if "W" in spectral_class:
            return "Étoile Wolf-Rayet"
        if "S" in spectral_class:
            return "Étoile de type spectral S"
        if "C" in spectral_class:
            return "Étoile de type spectral C"
        # Pas trouvé
        return None
