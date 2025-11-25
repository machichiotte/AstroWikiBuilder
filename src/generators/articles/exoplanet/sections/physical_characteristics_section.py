# src/generators/articles/exoplanet/sections/physical_characteristics_section.py

import math

from src.models.entities.exoplanet_entity import Exoplanet
from src.utils.formatters.article_formatter import ArticleFormatter


class PhysicalCharacteristicsSection:
    """Génère la section caractéristiques physiques pour les articles d'exoplanètes."""

    def __init__(self, article_util: ArticleFormatter):
        self.article_util = article_util

    def _get_value_or_none_if_nan(self, data_point) -> float | int | None:
        """Extrait la valeur d'un data point ou retourne None si NaN."""
        if data_point and hasattr(data_point, "value") and data_point.value is not None:
            value = data_point.value
            if isinstance(value, str) and value.lower() == "nan":
                return None
            return value
        return None

    def _format_mass_description(self, mass: float | int) -> str | None:
        """Formate la description de la masse."""
        try:
            mass_f = float(mass)
        except Exception:
            return None

        precision = 3 if mass_f < 0.1 else (2 if mass_f < 1 else 1)
        mass_value = self.article_util.format_number_as_french_string(mass, precision=precision)

        if mass_f < 0.1:
            label = "faible"
        elif mass_f < 1:
            label = "modérée"
        else:
            label = "imposante"

        return f"sa masse {label} de {mass_value} [[Masse_jovienne|''M''{{{{ind|J}}}}]]"

    def _format_radius_description(self, radius: float | int) -> str | None:
        """Formate la description du rayon."""
        try:
            radius_f = float(radius)
        except Exception:
            return None

        precision = 3 if radius_f < 0.1 else (2 if radius_f < 1 else 1)
        radius_value = self.article_util.format_number_as_french_string(radius, precision=precision)

        if radius_f < 0.5:
            label = "compact"
        elif radius_f < 1.5:
            label = None
        else:
            label = "étendu"

        return f"son rayon{' ' + label if label else ''} de {radius_value} [[Rayon_jovien|''R''{{{{ind|J}}}}]]"

    def _format_temperature_description(self, temp: float | int) -> str | None:
        """Formate la description de la température."""
        if isinstance(temp, str) and temp.lower() == "nan":
            return None
        if isinstance(temp, float) and math.isnan(temp):
            return None

        try:
            temp_f = float(temp)
        except Exception:
            return None

        if isinstance(temp, int | float):
            temp_value = f"{float(temp):.5f}".rstrip("0").rstrip(".")
        else:
            temp_value = str(temp)

        if temp_f < 500:
            label = ""
        elif temp_f < 1000:
            label = "élevée "
        else:
            label = "extrême "

        return f"sa température {label}de {temp_value} [[Kelvin|K]]"

    def _compare_to_solar_system(self, density: float) -> str:
        """Compare la densité à celle des planètes du système solaire.

        Args:
            density: Densité en g/cm³

        Returns:
            Phrase de comparaison avec les planètes du système solaire
        """
        if density < 0.7:
            return "moins dense que Saturne"
        elif density < 1.0:
            return "comparable à Saturne"
        elif density < 1.5:
            return "proche de Jupiter"
        elif density < 2.0:
            return "entre Jupiter et Neptune"
        elif density < 3.5:
            return "plus dense que les géantes gazeuses"
        elif density < 5.0:
            return "de densité intermédiaire"
        else:
            return "comparable aux planètes telluriques comme la Terre"

    def _format_density_description(self, density: float | int) -> str | None:
        """Formate la description de la densité.

        Args:
            density: Densité en g/cm³

        Returns:
            Description formatée de la densité ou None si erreur
        """
        try:
            density_f = float(density)
        except Exception:
            return None

        precision = 2
        density_value = self.article_util.format_number_as_french_string(
            density, precision=precision
        )
        comparison = self._compare_to_solar_system(density_f)

        return f"sa densité de {density_value} g/cm³ ({comparison})"

    def generate(self, exoplanet: Exoplanet) -> str:
        """
        Génère la section des caractéristiques physiques.

        Returns:
            str: Contenu de la section ou chaîne vide si pas de données
        """
        mass = self._get_value_or_none_if_nan(exoplanet.pl_mass)
        radius = self._get_value_or_none_if_nan(exoplanet.pl_radius)
        density = self._get_value_or_none_if_nan(exoplanet.pl_density)
        temp = self._get_value_or_none_if_nan(exoplanet.pl_temperature)

        if not any([mass is not None, radius is not None, density is not None, temp is not None]):
            return ""

        section = "== Caractéristiques physiques ==\n"
        desc_parts = []

        if mass is not None:
            mass_desc = self._format_mass_description(mass)
            if mass_desc:
                desc_parts.append(mass_desc)

        if radius is not None:
            radius_desc = self._format_radius_description(radius)
            if radius_desc:
                desc_parts.append(radius_desc)

        if density is not None:
            density_desc = self._format_density_description(density)
            if density_desc:
                desc_parts.append(density_desc)

        if temp is not None:
            temp_desc = self._format_temperature_description(temp)
            if temp_desc:
                desc_parts.append(temp_desc)

        if desc_parts:
            if len(desc_parts) == 1:
                section += f"L'exoplanète se distingue par {desc_parts[0]}.\n"
            else:
                section += f"L'exoplanète se distingue par {', '.join(desc_parts[:-1])} et {desc_parts[-1]}.\n"

        return section
