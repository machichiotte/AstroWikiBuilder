# src/generators/articles/exoplanet/sections/system_architecture_section.py

from src.models.entities.exoplanet_entity import Exoplanet
from src.utils.formatters.article_formatter import ArticleFormatter


class SystemArchitectureSection:
    """Génère la section système planétaire pour les articles d'exoplanètes."""

    def __init__(self, article_util: ArticleFormatter):
        self.article_util = article_util

    def generate(self, exoplanet: Exoplanet, system_planets: list[Exoplanet] = None) -> str:
        """Génère la section sur le système planétaire."""
        # Si on a la liste des planètes du système, on l'utilise pour enrichir le contenu
        if system_planets and len(system_planets) > 1:
            return self._generate_with_siblings(exoplanet, system_planets)

        # Fallback sur l'ancienne logique basée sur le compteur (sans tableau car pas de données)
        if not exoplanet.sy_planet_count:
            return ""
        try:
            if hasattr(exoplanet.sy_planet_count, "value"):
                planet_count = int(exoplanet.sy_planet_count.value)
            else:
                planet_count = int(exoplanet.sy_planet_count)
        except (ValueError, TypeError, AttributeError):
            return ""

        if planet_count <= 1:
            return ""

        section = "== Système planétaire ==\n"
        if planet_count == 2:
            section += f"Cette planète fait partie d'un système binaire planétaire orbitant autour de [[{exoplanet.st_name}]]. L'existence de multiples planètes dans un même système permet d'étudier la formation et l'évolution planétaire de manière comparative.\n"
        elif planet_count >= 3 and planet_count <= 5:
            section += f"Cette planète fait partie d'un système de {planet_count} planètes connues orbitant autour de [[{exoplanet.st_name}]]. L'étude de systèmes multi-planétaires fournit des informations précieuses sur les mécanismes de formation et de migration planétaire.\n"
        else:
            section += f"Cette planète fait partie d'un système planétaire remarquable contenant {planet_count} planètes connues autour de [[{exoplanet.st_name}]]. Un tel système dense offre une opportunité unique d'étudier les interactions gravitationnelles entre planètes et la stabilité dynamique à long terme.\n"
        return section

    def _generate_with_siblings(
        self, current_planet: Exoplanet, system_planets: list[Exoplanet]
    ) -> str:
        """Génère le contenu en utilisant la liste complète des planètes du système."""

        # Trier les planètes par demi-grand axe (si dispo) ou par nom
        def sort_key(p):
            if p.pl_semi_major_axis and p.pl_semi_major_axis.value is not None:
                try:
                    return (0, float(p.pl_semi_major_axis.value))
                except (ValueError, TypeError):
                    pass
            return (1, p.pl_name)

        sorted_planets = sorted(system_planets, key=sort_key)
        planet_count = len(sorted_planets)

        section = "== Système planétaire ==\n"
        section += f"Le système planétaire de [[{current_planet.st_name}]] compte au moins {planet_count} planètes confirmées. "

        # Trouver la position de la planète actuelle
        try:
            current_index = [p.pl_name for p in sorted_planets].index(current_planet.pl_name)
            position_str = ""
            if current_index == 0:
                position_str = "la plus interne"
            elif current_index == planet_count - 1:
                position_str = "la plus externe"
            else:
                position_str = f"la {current_index + 1}e planète en partant de l'étoile"

            section += f"[[{current_planet.pl_name}]] est {position_str} du système.\n\n"
        except ValueError:
            section += "\n\n"

        # Générer le tableau des planètes
        star_name = current_planet.st_name if current_planet.st_name else "l'étoile"
        section += "{{Système planétaire début\n"
        section += f"| nom = {star_name}\n"
        section += "}}\n"

        for planet in sorted_planets:
            section += self._generate_planet_template(planet)

        section += "{{Système planétaire fin}}\n"

        return section

    def _generate_planet_template(self, exoplanet: Exoplanet) -> str:
        """Génère le template Wiki pour une exoplanète donnée."""
        pl_name: str = exoplanet.pl_name
        template = "{{Système planétaire\n"
        template += f"| exoplanète = [[{pl_name}]]\n"

        # Masse : privilégier la masse terrestre pour les petits objets (< 0.1 M_J)
        use_earth_mass = False
        if exoplanet.pl_mass_earth and exoplanet.pl_mass_earth.value is not None:
            if exoplanet.pl_mass and exoplanet.pl_mass.value is not None:
                try:
                    if float(exoplanet.pl_mass.value) < 0.1:
                        use_earth_mass = True
                except (ValueError, TypeError):
                    pass
            else:
                use_earth_mass = True

        if use_earth_mass:
            mass_str = self._format_field_with_uncertainty(exoplanet.pl_mass_earth)
            template += f"| masse_terrestre = {mass_str}\n"
        else:
            mass_str = self._format_field_with_uncertainty(exoplanet.pl_mass)
            template += f"| masse = {mass_str}\n"

        # Rayon : privilégier le rayon terrestre pour les petits objets (< 0.5 R_J)
        use_earth_radius = False
        if exoplanet.pl_radius_earth and exoplanet.pl_radius_earth.value is not None:
            if exoplanet.pl_radius and exoplanet.pl_radius.value is not None:
                try:
                    if float(exoplanet.pl_radius.value) < 0.5:
                        use_earth_radius = True
                except (ValueError, TypeError):
                    pass
            else:
                use_earth_radius = True

        if use_earth_radius:
            radius_str = self._format_field_with_uncertainty(exoplanet.pl_radius_earth)
            template += f"| rayon_terrestre = {radius_str}\n"
        else:
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
