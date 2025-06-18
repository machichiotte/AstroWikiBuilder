from src.models.entities.star import Star
from src.utils.formatters.article_formatters import ArticleUtils


class StarContentGenerator:
    """
    Générateur de contenu pour les articles d'étoiles.
    Responsable de la génération des différentes sections de l'article.
    """

    def __init__(self):
        self.article_utils = ArticleUtils()

    def generate_all_content(self, star: Star) -> str:
        """
        Génère l'ensemble du contenu de l'article pour une étoile.
        """
        sections = [
            self.generate_physical_characteristics(star),
            self.generate_observation_section(star),
            self.generate_stellar_environment(star),
            self.generate_history_section(star),
        ]

        # Filtrer les sections vides et les combiner
        return "\n\n".join(filter(None, sections))

    def generate_physical_characteristics(self, star: Star) -> str:
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

        content = ["== Caractéristiques physiques ==\n"]

        if star.st_spectral_type and star.st_spectral_type:
            content.append(
                f"Cette étoile est de type spectral {star.st_spectral_type}."
            )

        if star.st_temperature and star.st_temperature.value:
            temp = self.article_utils.format_numeric_value(star.st_temperature.value)
            content.append(
                f"Sa température effective est d'environ {temp} [[kelvin|K]]."
            )

        if star.st_mass and star.st_mass.value:
            mass = self.article_utils.format_numeric_value(star.st_mass.value)
            content.append(f"Sa masse est estimée à {mass} fois celle du [[Soleil]].")

        if star.st_radius and star.st_radius.value:
            radius = self.article_utils.format_numeric_value(star.st_radius.value)
            content.append(f"Son rayon est d'environ {radius} fois celui du Soleil.")

        if star.st_luminosity and star.st_luminosity.value:
            lum = self.article_utils.format_numeric_value(star.st_luminosity.value)
            content.append(f"Sa luminosité est d'environ {lum} fois celle du Soleil.")

        return "\n".join(content)

    def generate_observation_section(self, star: Star) -> str:
        """
        Génère la section sur l'observation de l'étoile.
        """
        if not any(
            [star.st_apparent_magnitude, star.st_right_ascension, star.st_declination]
        ):
            return ""

        content = ["== Observation ==\n"]

        if star.st_apparent_magnitude and star.st_apparent_magnitude.value:
            mag = self.article_utils.format_numeric_value(star.st_magnitude.value)
            content.append(f"Sa magnitude apparente est de {mag}.")

        if star.st_right_ascension and star.st_declination:
            ra = star.st_right_ascension
            dec = star.st_declination
            content.append(
                f"Ses coordonnées célestes sont : ascension droite {ra}, déclinaison {dec}."
            )

        return "\n".join(content)

    def generate_stellar_environment(self, star: Star) -> str:
        """
        Génère la section sur l'environnement stellaire.
        """
        if not any([star.st_constellation, star.st_distance]):
            return ""

        content = ["== Environnement stellaire ==\n"]

        if star.st_constellation:
            content.append(
                f"L'étoile se trouve dans la constellation [[{star.st_constellation}]]."
            )

        if star.st_distance:
            dist = self.article_utils.format_numeric_value(star.st_distance)
            content.append(
                f"Elle est située à environ {dist} [[parsec|parsecs]] de la [[Terre]]."
            )

        return "\n".join(content)

    def generate_history_section(self, star: Star) -> str:
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
