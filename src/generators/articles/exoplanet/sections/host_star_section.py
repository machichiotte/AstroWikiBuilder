# src/generators/articles/exoplanet/sections/host_star_section.py

from src.models.entities.exoplanet_entity import Exoplanet
from src.utils.formatters.article_formatter import ArticleFormatter


class HostStarSection:
    """Génère la section étoile hôte pour les articles d'exoplanètes."""

    def __init__(self, article_util: ArticleFormatter):
        self.article_util = article_util

    def generate(self, exoplanet: Exoplanet) -> str:
        """
        Génère la section résumant les caractéristiques de l'étoile hôte.

        Returns:
            str: Contenu de la section ou chaîne vide si pas d'étoile
        """
        if not exoplanet.st_name:
            return ""

        content = "== Étoile hôte ==\n"
        content += f"L'exoplanète orbite autour de [[{exoplanet.st_name}]], "

        characteristics = []

        if exoplanet.st_spectral_type:
            characteristics.append(f"une étoile de type spectral {exoplanet.st_spectral_type}")

        if exoplanet.st_mass and exoplanet.st_mass.value:
            mass_str = self.article_util.format_uncertain_value_for_article(exoplanet.st_mass)
            if mass_str:
                characteristics.append(
                    f"d'une masse de {mass_str} [[Masse solaire|''M''{{{{ind|☉}}}}]]"
                )

        if exoplanet.st_metallicity and exoplanet.st_metallicity.value:
            met_str = self.article_util.format_uncertain_value_for_article(exoplanet.st_metallicity)
            if met_str:
                characteristics.append(f"d'une métallicité de {met_str} [Fe/H]")

        if exoplanet.st_age and exoplanet.st_age.value:
            age_str = self.article_util.format_uncertain_value_for_article(exoplanet.st_age)
            if age_str:
                characteristics.append(f"âgée de {age_str} [[milliard]]s d'années")

        if not characteristics:
            content = f"== Étoile hôte ==\nL'exoplanète orbite autour de l'étoile [[{exoplanet.st_name}]].\n"
            return content

        if len(characteristics) == 1:
            content += f"{characteristics[0]}.\n"
        else:
            content += f"{', '.join(characteristics[:-1])} et {characteristics[-1]}.\n"

        return content
