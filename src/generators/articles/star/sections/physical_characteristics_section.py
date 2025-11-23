from src.models.entities.star_entity import Star
from src.utils.formatters.article_formatter import ArticleFormatter


class PhysicalCharacteristicsSection:
    """
    Génère la section des caractéristiques physiques de l'étoile.
    """

    def __init__(self, article_util: ArticleFormatter):
        self.article_util = article_util

    def generate(self, star: Star) -> str:
        """
        Génère le contenu de la section.
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

        self._add_spectral_type(star, content)
        self._add_temperature(star, content)
        self._add_mass(star, content)
        self._add_radius(star, content)
        self._add_luminosity(star, content)

        return "\n".join(content)

    def _add_spectral_type(self, star: Star, content: list[str]) -> None:
        if star.st_spectral_type:
            content.append(
                f"Cette étoile est de type spectral {star.st_spectral_type}."
            )

    def _add_temperature(self, star: Star, content: list[str]) -> None:
        if star.st_temperature and star.st_temperature.value:
            temp: str = self.article_util.format_number_as_french_string(
                star.st_temperature.value
            )
            content.append(
                f"Sa température effective est d'environ {temp} [[kelvin|K]]."
            )

    def _add_mass(self, star: Star, content: list[str]) -> None:
        if star.st_mass and star.st_mass.value:
            mass: str = self.article_util.format_number_as_french_string(
                star.st_mass.value
            )
            content.append(f"Sa masse est estimée à {mass} fois celle du [[Soleil]].")

    def _add_radius(self, star: Star, content: list[str]) -> None:
        if star.st_radius and star.st_radius.value:
            radius: str = self.article_util.format_number_as_french_string(
                star.st_radius.value
            )
            content.append(f"Son rayon est d'environ {radius} fois celui du Soleil.")

    def _add_luminosity(self, star: Star, content: list[str]) -> None:
        if star.st_luminosity and star.st_luminosity.value:
            lum: str = self.article_util.format_number_as_french_string(
                star.st_luminosity.value
            )
            content.append(f"Sa luminosité est d'environ {lum} fois celle du Soleil.")
