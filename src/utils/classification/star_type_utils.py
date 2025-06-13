# src/utils/classification/star_type_utils.py
from typing import Optional, Tuple, List
from src.models.data_source_star import DataSourceStar


class StarTypeUtils:
    """
    Classe utilitaire pour déterminer les types d'étoiles.
    """

    @staticmethod
    def parse_spectral_type(
        spectral_type: str,
    ) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        """
        Parse un type spectral complexe (ex: 'K1 V', 'G2V', 'M4.5+/-0.5', 'F8/G0 V', etc.)
        Retourne (lettre, sous-type, classe de luminosité) ou None si non reconnu.
        """
        import re

        # Exemples : 'K1 V', 'G2V', 'M4.5+/-0.5', 'F8/G0 V', 'K0III', 'G5 IV/V'
        match = re.match(r"([OBAFGKMLTY])\s*([0-9.]*)\s*([IV]+)?", spectral_type)
        if match:
            letter = match.group(1)
            subtype = match.group(2) if match.group(2) else None
            luminosity = match.group(3) if match.group(3) else None
            return letter, subtype, luminosity
        return None, None, None

    @staticmethod
    def _get_temperature_range(letter: str) -> Tuple[float, float]:
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
    def _get_evolutionary_stage(
        star: DataSourceStar, letter: str, luminosity: Optional[str]
    ) -> Optional[str]:
        """
        Détermine le stade évolutif de l'étoile basé sur ses caractéristiques.
        """
        if not luminosity:
            return None

        # Naines
        if luminosity == "V":
            if letter in ["K", "M"]:
                return "Naine rouge"
            elif letter == "G":
                return "Naine jaune"
            elif letter in ["O", "B"]:
                return "Naine bleue"
            return "Naine"

        # Géantes
        if luminosity == "III":
            if letter in ["K", "M"]:
                return "Géante rouge"
            elif letter in ["O", "B"]:
                return "Géante bleue"
            elif letter in ["F", "G"]:
                return "Géante jaune"
            return "Géante"

        # Supergéantes
        if luminosity == "I":
            if letter in ["K", "M"]:
                return "Supergéante rouge"
            elif letter in ["O", "B"]:
                return "Supergéante bleue"
            return "Supergéante"

        return None

    @staticmethod
    def get_star_type(star: DataSourceStar) -> List[str]:
        """
        Détermine le type d'étoile basé sur ses caractéristiques.
        Retourne une liste de types d'étoiles (ex: ["Étoile de type spectral KIII", "Géante rouge"])
        """
        types = []

        if not star.st_spectral_type:
            return types

        spectral_type = star.st_spectral_type.value
        if not spectral_type:
            return types

        letter, subtype, luminosity = StarTypeUtils.parse_spectral_type(spectral_type)
        if not letter:
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
        if star.st_mass and star.st_radius:
            try:
                mass = float(star.st_mass.value)
                radius = float(star.st_radius.value)
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

        # Type spectral standard
        type_parts = [f"Étoile de type spectral {letter}"]

        # Ajouter le sous-type si présent
        if subtype:
            type_parts.append(subtype)

        # Ajouter la classe de luminosité si présente
        if luminosity:
            type_parts.append(luminosity)

        types.append("".join(type_parts))

        # Stade évolutif
        evolutionary_stage = StarTypeUtils._get_evolutionary_stage(
            star, letter, luminosity
        )
        if evolutionary_stage:
            types.append(evolutionary_stage)

        # Étoile variable
        if star.st_variability and star.st_variability.value:
            types.append(f"Étoile variable de type {star.st_variability.value}")

        # Étoile chimiquement particulière
        if star.st_metallicity:
            try:
                metallicity = float(star.st_metallicity.value)
                if metallicity < -1.0:
                    types.append("Étoile pauvre en métaux")
                elif metallicity > 0.5:
                    types.append("Étoile riche en métaux")
            except (ValueError, TypeError):
                pass

        return types

    @staticmethod
    def get_luminosity_class(star: DataSourceStar) -> Optional[str]:
        """
        Détermine la classe de luminosité de l'étoile.
        Retourne la classe de luminosité (ex: "V", "III", etc.)
        """
        if not star.st_spectral_type:
            return None

        spectral_type = star.st_spectral_type.value
        if not spectral_type:
            return None

        _, _, luminosity = StarTypeUtils.parse_spectral_type(spectral_type)
        return luminosity

    @staticmethod
    def get_spectral_class(star: DataSourceStar) -> Optional[str]:
        """
        Détermine la classe spectrale de l'étoile.
        Retourne la classe spectrale (ex: "K", "G", etc.)
        """
        if not star.st_spectral_type:
            return None

        spectral_type = star.st_spectral_type.value
        if not spectral_type:
            return None

        letter, _, _ = StarTypeUtils.parse_spectral_type(spectral_type)
        return letter
