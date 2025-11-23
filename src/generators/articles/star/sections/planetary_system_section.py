from src.models.entities.exoplanet_entity import Exoplanet
from src.models.entities.star_entity import Star
from src.utils.formatters.article_formatter import ArticleFormatter


class PlanetarySystemSection:
    """
    Génère la section sur le système planétaire de l'étoile.
    """

    def __init__(self, article_util: ArticleFormatter):
        self.article_util = article_util

    def generate(self, star: Star, exoplanets: list[Exoplanet]) -> str:
        """
        Génère une section listant les exoplanètes de l'étoile avec le template Wikipedia.
        """
        if not exoplanets:
            return ""

        star_name = star.st_name if star.st_name else "Cette étoile"
        section = "== Système planétaire ==\n"

        # Template de début
        section += "{{Système planétaire début\n"
        section += f"| nom = {star_name}\n"
        section += "}}\n"

        # Templates pour chaque exoplanète
        # Trier les exoplanètes par nom alphabétique avant de les ajouter à la section
        exoplanets.sort(key=lambda exoplanet: exoplanet.pl_name)

        for exoplanet in exoplanets:
            section += self._generate_planet_template(exoplanet)

        # Template de fin
        section += "{{Système planétaire fin}}\n"

        return section

    def _generate_planet_template(self, exoplanet: Exoplanet) -> str:
        """Génère le template Wiki pour une exoplanète donnée."""
        pl_name: str = exoplanet.pl_name
        template = "{{Système planétaire\n"
        template += f"| exoplanète = [[{pl_name}]]\n"

        # Masse
        mass_str = self._format_field_with_uncertainty(exoplanet.pl_mass)
        template += f"| masse = {mass_str}\n"

        # Rayon
        radius_str = self._format_field_with_uncertainty(exoplanet.pl_radius)
        template += f"| rayon = {radius_str}\n"

        # Demi-grand axe
        axis_str = self._format_field_with_uncertainty(exoplanet.pl_semi_major_axis)
        template += f"| demi grand axe = {axis_str}\n"

        # Période
        period_str = ""
        if (
            exoplanet.pl_orbital_period
            and exoplanet.pl_orbital_period.value is not None
        ):
            try:
                period = float(exoplanet.pl_orbital_period.value)
                if period.is_integer():
                    period_str = f"{int(period)}"
                else:
                    period_str = f"{period:.2f}"
            except (ValueError, TypeError):
                pass
        template += f"| période = {period_str}\n"

        # Excentricité
        ecc_str = ""
        if exoplanet.pl_eccentricity and exoplanet.pl_eccentricity.value is not None:
            try:
                ecc = float(exoplanet.pl_eccentricity.value)
                ecc_str = f"{ecc:.3f}"
            except (ValueError, TypeError):
                pass
        template += f"| excentricité = {ecc_str}\n"

        # Inclinaison
        incl_str = self._format_field_with_uncertainty(exoplanet.pl_inclination)
        template += f"| inclinaison = {incl_str}\n"

        template += "}}\n"
        return template

    def _format_field_with_uncertainty(self, value_obj) -> str:
        """Helper to format a value with its uncertainty."""
        if value_obj and value_obj.value is not None:
            try:
                val = float(value_obj.value)
                return self._format_uncertainty(
                    val,
                    value_obj.error_positive,
                    value_obj.error_negative,
                )
            except (ValueError, TypeError):
                pass
        return ""

    def _format_uncertainty(
        self,
        value: float,
        error_positive: float | None,
        error_negative: float | None,
    ) -> str:
        """
        Formate une valeur avec ses incertitudes selon les cas possibles.
        """
        if error_positive is not None and error_negative is not None:
            if error_positive == error_negative:
                return f"{value:.2f} ± {error_positive:.2f}"
            else:
                return f"{value:.2f} +{error_positive:.2f} -{error_negative:.2f}"
        elif error_positive is not None:
            return f"{value:.2f} +{error_positive:.2f}"
        elif error_negative is not None:
            return f"{value:.2f} -{error_negative:.2f}"
        else:
            return f"{value:.2f}"
