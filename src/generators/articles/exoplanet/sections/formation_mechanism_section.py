# src/generators/articles/exoplanet/sections/formation_mechanism_section.py

from src.models.entities.exoplanet_entity import Exoplanet
from src.utils.formatters.article_formatter import ArticleFormatter


class FormationMechanismSection:
    """Génère la section mécanismes de formation pour les articles d'exoplanètes."""

    def __init__(self, article_util: ArticleFormatter):
        self.article_util = article_util

    def _is_hot_jupiter(self, exoplanet: Exoplanet) -> bool:
        """Détermine si c'est un Hot Jupiter."""
        is_massive = False
        if exoplanet.pl_mass and exoplanet.pl_mass.value:
            try:
                mass_earth = float(exoplanet.pl_mass.value) * 318
                is_massive = mass_earth > 30
            except (ValueError, TypeError):
                pass
        is_large = False
        if exoplanet.pl_radius and exoplanet.pl_radius.value:
            try:
                is_large = float(exoplanet.pl_radius.value) > 0.8
            except (ValueError, TypeError):
                pass
        is_close = False
        if exoplanet.pl_orbital_period and exoplanet.pl_orbital_period.value:
            try:
                is_close = float(exoplanet.pl_orbital_period.value) < 10
            except (ValueError, TypeError):
                pass
        return (is_massive or is_large) and is_close

    def _is_red_dwarf_system(self, exoplanet: Exoplanet) -> bool:
        """Détermine si l'étoile est une naine rouge."""
        if exoplanet.st_spectral_type and exoplanet.st_spectral_type.startswith("M"):
            return True
        if exoplanet.st_mass and hasattr(exoplanet.st_mass, "value"):
            try:
                return float(exoplanet.st_mass.value) < 0.5
            except (ValueError, TypeError):
                pass
        return False

    def _is_super_earth_or_mini_neptune(self, exoplanet: Exoplanet) -> bool:
        """Détermine si c'est une super-Terre ou mini-Neptune."""
        if not exoplanet.pl_radius or not exoplanet.pl_radius.value:
            return False
        try:
            radius_earth = float(exoplanet.pl_radius.value)
            return 1.5 < radius_earth < 4.0
        except (ValueError, TypeError):
            return False

    def _has_eccentric_orbit(self, exoplanet: Exoplanet) -> bool:
        """Détermine si l'orbite est fortement excentrique."""
        if not exoplanet.pl_eccentricity or not exoplanet.pl_eccentricity.value:
            return False
        try:
            return float(exoplanet.pl_eccentricity.value) > 0.3
        except (ValueError, TypeError):
            return False

    def generate(self, exoplanet: Exoplanet) -> str:
        """Génère une section sur les mécanismes de formation (spéculatif)."""
        is_hot_jupiter = self._is_hot_jupiter(exoplanet)
        is_red_dwarf = self._is_red_dwarf_system(exoplanet)
        is_super_earth = self._is_super_earth_or_mini_neptune(exoplanet)
        is_eccentric = self._has_eccentric_orbit(exoplanet)
        if not any([is_hot_jupiter, is_red_dwarf, is_super_earth, is_eccentric]):
            return ""
        section = "== Mécanismes de formation ==\n"
        if is_hot_jupiter:
            section += "Les modèles de formation planétaire suggèrent que cette exoplanète, de par sa nature gazeuse et sa proximité extrême avec son étoile, ne s'est probablement pas formée à sa position actuelle. Les théories de [[migration planétaire]] proposent qu'elle se soit formée dans les régions externes du système, où les températures permettent l'accumulation de gaz, avant de migrer vers l'intérieur par interaction gravitationnelle avec le [[Disque protoplanétaire|disque protoplanétaire]].\n"
        elif is_red_dwarf:
            section += f"L'évolution de cette planète autour de [[{exoplanet.st_name}]], une [[naine rouge]], présente des défis particuliers. L'[[activité stellaire]] intense des naines rouges, notamment les [[éruption stellaire|éruptions]] fréquentes, peut éroder l'atmosphère planétaire primitive. De plus, la [[zone habitable]] très proche de ces étoiles implique un fort [[verrouillage gravitationnel]], avec des conséquences importantes sur la circulation atmosphérique et le climat.\n"
        elif is_eccentric:
            section += "L'excentricité orbitale élevée de cette planète suggère qu'elle a subi des perturbations gravitationnelles importantes. De telles orbites excentriques peuvent résulter d'interactions dynamiques avec d'autres planètes du système, d'une migration induite par le disque, ou de rencontres stellaires dans l'environnement de formation.\n"
        elif is_super_earth:
            section += "La nature exacte de cette planète, située dans la catégorie des [[super-Terre]]s ou [[mini-Neptune]]s, reste débattue. Cette classe d'exoplanètes, rare dans notre Système solaire, soulève des questions sur les processus de formation. Il pourrait s'agir soit d'un noyau rocheux massif avec une atmosphère épaisse, soit d'une planète majoritairement composée de volatils.\n"
        return section
