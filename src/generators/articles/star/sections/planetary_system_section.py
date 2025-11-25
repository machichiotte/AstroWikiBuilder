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

        # Ajouter des informations contextuelles sur le système
        section += self._generate_system_context(exoplanets[0])

        # Template de début
        section += "{{Système planétaire début\n"
        section += f"| nom = {star_name}\n"
        section += "}}\n"

        # Trier et ajouter les exoplanètes
        sorted_exoplanets = self._sort_exoplanets(exoplanets)

        for exoplanet in sorted_exoplanets:
            section += self._generate_planet_template(exoplanet)

        # Template de fin
        section += "{{Système planétaire fin}}\n"

        return section

    def _generate_system_context(self, first_exo: Exoplanet) -> str:
        """Génère les informations contextuelles sur le système."""
        context_parts = []

        if first_exo.sy_snum and first_exo.sy_snum > 1:
            plural = "s" if first_exo.sy_snum > 1 else ""
            context_parts.append(f"Le système est composé de {first_exo.sy_snum} étoile{plural}.")

        if first_exo.cb_flag and first_exo.cb_flag == 1:
            context_parts.append(
                "Les planètes orbitent autour d'un système binaire (planètes circumbinaires)."
            )

        if first_exo.sy_mnum and first_exo.sy_mnum > 0:
            plural = "s" if first_exo.sy_mnum > 1 else ""
            context_parts.append(
                f"Le système compte également {first_exo.sy_mnum} lune{plural} connue{plural}."
            )

        if context_parts:
            return "\n".join(context_parts) + "\n\n"
        return ""

    def _sort_exoplanets(self, exoplanets: list[Exoplanet]) -> list[Exoplanet]:
        """Trie les exoplanètes par demi-grand axe."""

        def sort_key(exo):
            if exo.pl_semi_major_axis and exo.pl_semi_major_axis.value:
                try:
                    return (0, float(exo.pl_semi_major_axis.value))
                except (ValueError, TypeError):
                    pass
            return (1, exo.pl_name)

        return sorted(exoplanets, key=sort_key)

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
        period_str = self._format_field_with_uncertainty(exoplanet.pl_orbital_period)
        template += f"| période = {period_str}\n"

        # Excentricité
        ecc_str = self._format_field_with_uncertainty(exoplanet.pl_eccentricity, precision=3)
        template += f"| excentricité = {ecc_str}\n"

        # Inclinaison
        incl_str = self._format_field_with_uncertainty(exoplanet.pl_inclination)
        template += f"| inclinaison = {incl_str}\n"

        template += "}}\n"
        return template

    def _format_field_with_uncertainty(self, value_obj, precision: int = 4) -> str:
        """Helper to format a value with its uncertainty using French format."""
        if value_obj and value_obj.value is not None:
            try:
                val = float(value_obj.value)
                return self._format_uncertainty(
                    val,
                    value_obj.error_positive,
                    value_obj.error_negative,
                    precision,
                )
            except (ValueError, TypeError):
                pass
        return ""

    def _format_uncertainty(
        self,
        value: float,
        error_positive: float | None,
        error_negative: float | None,
        precision: int = 4,
    ) -> str:
        """
        Formate une valeur avec ses incertitudes selon les standards Wikipedia français.
        Utilise le template {{±}} et la virgule comme séparateur décimal.
        """
        # Formater la valeur principale avec virgule française
        value_str = self._to_french_decimal(value, precision)

        if error_positive is not None and error_negative is not None:
            err_pos_str = self._to_french_decimal(error_positive, precision)
            err_neg_str = self._to_french_decimal(error_negative, precision)

            if error_positive == error_negative:
                # Utiliser le template {{±|erreur}}
                return f"{value_str} {{{{±|{err_pos_str}}}}}"
            # Utiliser le template {{±|erreur_positive|erreur_négative}}
            return f"{value_str} {{{{±|{err_pos_str}|{err_neg_str}}}}}"
        if error_positive is not None:
            err_pos_str = self._to_french_decimal(error_positive, precision)
            return f"{value_str} +{err_pos_str}"
        if error_negative is not None:
            err_neg_str = self._to_french_decimal(error_negative, precision)
            return f"{value_str} -{err_neg_str}"
        return value_str

    def _to_french_decimal(self, value: float, precision: int = 4) -> str:
        """
        Convertit un nombre en format français (virgule comme séparateur décimal).
        Supprime les zéros inutiles à droite.
        """
        # Formater avec la précision demandée
        formatted = f"{value:.{precision}f}"

        # Supprimer les zéros inutiles à droite
        formatted = formatted.rstrip("0").rstrip(".")

        # Remplacer le point par une virgule
        formatted = formatted.replace(".", ",")

        return formatted
