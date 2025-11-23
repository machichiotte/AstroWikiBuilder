# src/generators/articles/exoplanet/sections/formation_mechanism_section.py

from collections.abc import Callable

from src.models.entities.exoplanet_entity import Exoplanet
from src.utils.formatters.article_formatter import ArticleFormatter


class FormationMechanismSection:
    def __init__(self, article_util: ArticleFormatter):
        self.article_util = article_util
        self.rules: dict[str, Callable[[Exoplanet], bool]] = {
            "hot_jupiter": self._is_hot_jupiter,
            "red_dwarf": self._is_red_dwarf_system,
            "super_earth": self._is_super_earth_or_mini_neptune,
            "eccentric": self._has_eccentric_orbit,
        }

        self.templates: dict[str, str] = {
            "hot_jupiter": (
                "Les modèles de formation planétaire suggèrent que cette exoplanète, "
                "de par sa nature gazeuse et sa proximité extrême avec son étoile, ne "
                "s'est probablement pas formée à sa position actuelle. Les théories de "
                "[[migration planétaire]] proposent qu'elle se soit formée dans les "
                "régions externes du système, avant de migrer vers l'intérieur par interaction "
                "gravitationnelle avec le [[Disque protoplanétaire|disque protoplanétaire]].\n"
            ),
            "red_dwarf": (
                "L'évolution de cette planète autour de [[{star}]], une [[naine rouge]], "
                "présente des défis particuliers. L'[[activité stellaire]] intense, notamment "
                "les [[éruption stellaire|éruptions]] fréquentes, peut éroder l'atmosphère "
                "primitive. La [[zone habitable]] très proche induit un fort "
                "[[verrouillage gravitationnel]].\n"
            ),
            "eccentric": (
                "L'excentricité orbitale élevée de cette planète suggère des perturbations "
                "gravitationnelles importantes. Ces orbites peuvent résulter d'interactions "
                "dynamiques avec d'autres planètes, d'une migration induite par le disque, "
                "ou de rencontres stellaires dans l'environnement de formation.\n"
            ),
            "super_earth": (
                "Cette planète, classée parmi les [[super-Terre]]s ou [[mini-Neptune]]s, "
                "soulève des questions sur les processus de formation. Elle pourrait être "
                "un noyau rocheux massif avec une atmosphère épaisse, ou une planète riche "
                "en volatils.\n"
            ),
        }

    def _safe_float(self, value: object) -> float:
        try:
            return float(value)
        except (ValueError, TypeError):
            return 0.0

    def _is_hot_jupiter(self, exoplanet: Exoplanet) -> bool:
        mass = self._safe_float(getattr(getattr(exoplanet, "pl_mass", None), "value", None)) * 318
        radius = self._safe_float(getattr(getattr(exoplanet, "pl_radius", None), "value", None))
        period = self._safe_float(
            getattr(getattr(exoplanet, "pl_orbital_period", None), "value", None)
        )

        return ((mass > 30) or (radius > 0.8)) and period < 10

    def _is_red_dwarf_system(self, exoplanet: Exoplanet) -> bool:
        if exoplanet.st_spectral_type and exoplanet.st_spectral_type.startswith("M"):
            return True

        mass = self._safe_float(getattr(getattr(exoplanet, "st_mass", None), "value", None))
        return mass < 0.5

    def _is_super_earth_or_mini_neptune(self, exoplanet: Exoplanet) -> bool:
        radius = self._safe_float(getattr(getattr(exoplanet, "pl_radius", None), "value", None))
        return 1.5 < radius < 4.0

    def _has_eccentric_orbit(self, exoplanet: Exoplanet) -> bool:
        eccentricity = self._safe_float(
            getattr(getattr(exoplanet, "pl_eccentricity", None), "value", None)
        )
        return eccentricity > 0.3

    def generate(self, exoplanet: Exoplanet) -> str:
        matched_key = next((key for key, rule in self.rules.items() if rule(exoplanet)), None)
        if not matched_key:
            return ""

        template = self.templates[matched_key]

        return "== Mécanismes de formation ==\n" + template.format(
            star=exoplanet.st_name or "l'étoile hôte"
        )
