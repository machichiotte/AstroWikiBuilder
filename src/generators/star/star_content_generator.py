# ============================================================================
# IMPORTS
# ============================================================================
from src.models.entities.star import Star
from src.utils.formatters.article_formatters import ArticleUtils


# ============================================================================
# DÉCLARATION DE LA CLASSE StarContentGenerator
# ============================================================================
class StarContentGenerator:
    """
    Générateur de contenu pour les articles d'étoiles.
    Responsable de la génération des différentes sections de l'article.
    """

    # ============================================================================
    # INITIALISATION
    # ============================================================================
    def __init__(self):
        self.article_utils = ArticleUtils()

    # ============================================================================
    # MÉTHODE PRINCIPALE
    # ============================================================================
    def compose_full_article(self, star: Star) -> str:
        """
        Génère l'ensemble du contenu de l'article pour une étoile.
        """
        sections: list[str] = [
            self.build_physical_section(star),
            self.build_observation_section(star),
            self.build_environment_section(star),
            self.write_history_paragraph(star),
        ]

        # Filtrer les sections vides et les combiner
        return "\n\n".join(filter(None, sections))

    # ============================================================================
    # GÉNÉRATION DES SECTIONS DE CONTENU
    # ============================================================================

    # --- CARACTÉRISTIQUES PHYSIQUES ---
    def build_physical_section(self, star: Star) -> str:
        """
        Génère la section des caractéristiques physiques de l'étoile.
        """
        if not any(
            [
                star.st_spectral_type,
                star.st_temperature,
                star.st_mass,
                star.st_radius,
                star.st_luminosity,
            ]
        ):
            return ""

        content: list[str] = ["== Caractéristiques physiques ==\n"]

        if star.st_spectral_type and star.st_spectral_type:
            content.append(
                f"Cette étoile est de type spectral {star.st_spectral_type}."
            )

        if star.st_temperature and star.st_temperature.value:
            temp: str = self.article_utils.format_number_as_french_string(
                star.st_temperature.value
            )
            content.append(
                f"Sa température effective est d'environ {temp} [[kelvin|K]]."
            )

        if star.st_mass and star.st_mass.value:
            mass: str = self.article_utils.format_number_as_french_string(
                star.st_mass.value
            )
            content.append(f"Sa masse est estimée à {mass} fois celle du [[Soleil]].")

        if star.st_radius and star.st_radius.value:
            radius: str = self.article_utils.format_number_as_french_string(
                star.st_radius.value
            )
            content.append(f"Son rayon est d'environ {radius} fois celui du Soleil.")

        if star.st_luminosity and star.st_luminosity.value:
            lum: str = self.article_utils.format_number_as_french_string(
                star.st_luminosity.value
            )
            content.append(f"Sa luminosité est d'environ {lum} fois celle du Soleil.")

        return "\n".join(content)

    # --- OBSERVATION ---
    def build_observation_section(self, star: Star) -> str:
        """
        Génère la section sur l'observation de l'étoile.
        """
        if not any(
            [star.st_apparent_magnitude, star.st_right_ascension, star.st_declination]
        ):
            return ""

        content: list[str] = ["== Observation ==\n"]

        if star.st_apparent_magnitude and star.st_apparent_magnitude.value:
            mag: str = self.article_utils.format_number_as_french_string(
                star.st_magnitude.value
            )
            content.append(f"Sa magnitude apparente est de {mag}.")

        if star.st_right_ascension and star.st_declination:
            ra: str = star.st_right_ascension
            dec: str = star.st_declination
            content.append(
                f"Ses coordonnées célestes sont : ascension droite {ra}, déclinaison {dec}."
            )

        return "\n".join(content)

    # --- ENVIRONNEMENT STELLAIRE ---
    def build_environment_section(self, star: Star) -> str:
        """
        Génère la section sur l'environnement stellaire.
        """
        if not any([star.st_constellation, star.st_distance]):
            return ""

        content: list[str] = ["== Environnement stellaire ==\n"]

        if star.st_constellation:
            content.append(
                f"L'étoile se trouve dans la constellation [[{star.st_constellation}]]."
            )

        if star.st_distance:
            dist_val = float(star.st_distance.value)
            formatted = f"{dist_val:.2f}"
            content.append(
                f"Elle est située à environ {formatted} [[parsec|parsecs]] de la [[Terre]]."
            )

        return "\n".join(content)

    # --- HISTOIRE ---
    def write_history_paragraph(self, star: Star) -> str:
        """
        Génère la section historique de l'étoile.
        """
        if not star.st_name:
            return ""

        content = ["== Histoire ==\n"]
        content.append(
            f"L'étoile {star.st_name} a été découverte et cataloguée dans le cadre des observations astronomiques modernes."
        )

        return "\n".join(content)
