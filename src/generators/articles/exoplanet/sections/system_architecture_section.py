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

        # Fallback sur l'ancienne logique basée sur le compteur
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

        # Lister les autres planètes
        other_planets = [p.pl_name for p in sorted_planets if p.pl_name != current_planet.pl_name]
        if other_planets:
            others_links = [f"[[{name}]]" for name in other_planets]
            if len(others_links) == 1:
                section += f"L'autre planète connue du système est {others_links[0]}.\n"
            else:
                last = others_links.pop()
                section += (
                    f"Les autres planètes du système sont {', '.join(others_links)} et {last}.\n"
                )

        return section
