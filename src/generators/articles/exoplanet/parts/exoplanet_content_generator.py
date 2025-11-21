# src/generators/articles/exoplanet/parts/exoplanet_content_generator.py

# ============================================================================
# IMPORTS
# ============================================================================
import math

from src.models.entities.exoplanet_entity import Exoplanet
from src.utils.formatters.article_formatter import ArticleFormatter


# ============================================================================
# DÉCLARATION DE LA CLASSE ExoplanetContentGenerator
# ============================================================================
class ExoplanetContentGenerator:
    """
    Générateur de contenu pour les articles d'exoplanetes.
    Responsable de la génération des différentes sections de l'article.
    """

    # ============================================================================
    # INITIALISATION
    # ============================================================================
    def __init__(self):
        self.article_util = ArticleFormatter()

    # ============================================================================
    # MÉTHODE PRINCIPALE
    # ============================================================================
    def compose_exoplanet_content(self, exoplanet: Exoplanet) -> str:
        """
        Génère l'ensemble du contenu de l'article pour une étoile.
        """
        sections: list[str] = [
            self.build_physical_characteristics_section(exoplanet),
            self.build_orbit_section(exoplanet),
            self.build_discovery_section(exoplanet),
            # self.build_habitability_section(exoplanet)
        ]

        # Filtrer les sections vides et les combiner
        return "\n\n".join(filter(None, sections))

    # ============================================================================
    # GÉNÉRATION DES SECTIONS DE CONTENU
    # ============================================================================

    # --- CARACTÉRISTIQUES PHYSIQUES ---
    def build_orbit_section(self, exoplanet: Exoplanet) -> str:
        """Génère la section sur l'orbite de l'exoplanète."""
        if not any(
            [
                exoplanet.pl_semi_major_axis,
                exoplanet.pl_eccentricity,
                exoplanet.pl_orbital_period,
                exoplanet.pl_inclination,
            ]
        ):
            return ""

        content: list[str] = ["== Orbite ==\n"]

        if exoplanet.pl_semi_major_axis:
            semi_major_axis_str = self.article_util.format_uncertain_value_for_article(
                exoplanet.pl_semi_major_axis
            )
            if semi_major_axis_str:
                content.append(
                    f"L'exoplanète orbite à une distance de {semi_major_axis_str} [[unité astronomique|UA]] de son étoile."
                )

        if exoplanet.pl_eccentricity:
            eccentricity_str: str = self.article_util.format_uncertain_value_for_article(
                exoplanet.pl_eccentricity
            )
            if eccentricity_str:
                content.append(f"L'orbite a une excentricité de {eccentricity_str}.")

        if exoplanet.pl_orbital_period:
            period_str: str = self.article_util.format_uncertain_value_for_article(
                exoplanet.pl_orbital_period
            )
            if period_str:
                content.append(f"La période orbitale est de {period_str} [[jour|jours]].")

        if exoplanet.pl_inclination:
            inclination_str: str = self.article_util.format_uncertain_value_for_article(
                exoplanet.pl_inclination
            )
            if inclination_str:
                content.append(
                    f"L'inclinaison de l'orbite est de {inclination_str} [[degré (angle)|degrés]]."
                )

        return "\n".join(content)

    def build_discovery_section(self, exoplanet: Exoplanet) -> str:
        """Génère la section de découverte."""
        if not exoplanet.disc_year:
            return ""

        section = "== Découverte ==\n"

        # Traduction des méthodes de découverte
        method_translations: dict[str, str] = {
            "Transit": "des transits",
            "Radial Velocity": "des vitesses radiales",
            "Imaging": "de l'imagerie directe",
            "Microlensing": "de la microlentille gravitationnelle",
            "Timing": "du chronométrage",
            "Astrometry": "de l'astrométrie",
            "Orbital Brightness Modulation": "de la modulation de luminosité orbitale",
            "Eclipse Timing Variations": "des variations temporelles d'éclipses",
            "Pulsar Timing": "du chronométrage de pulsar",
            "Pulsation Timing Variations": "des variations temporelles de pulsation",
            "Disk Kinematics": "de la cinématique du disque",
            "Transit Timing Variations": "des variations temporelles de transit",
        }

        method_raw = (
            exoplanet.disc_method.value
            if exoplanet.disc_method and hasattr(exoplanet.disc_method, "value")
            else ""
        )
        disc_method: str | None = method_translations.get(method_raw, None)

        # Gestion robuste de la date
        date_value = exoplanet.disc_year
        if hasattr(date_value, "value"):
            date_value = date_value.value

        if hasattr(date_value, "year"):
            date_str: str = f"en {self.article_util.format_year_without_decimals(date_value.year)}"
        else:
            date_str: str = f"en {str(self.article_util.format_year_without_decimals(date_value))}"

        if disc_method:
            section += f"L'exoplanète a été découverte par la méthode {disc_method} {date_str}.\n"
        else:
            section += f"L'exoplanète a été découverte {date_str}.\n"

        return section

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

        if isinstance(temp, (int, float)):
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

    def build_physical_characteristics_section(self, exoplanet: Exoplanet) -> str:
        """Génère la section des caractéristiques physiques."""
        mass = self._get_value_or_none_if_nan(exoplanet.pl_mass)
        radius = self._get_value_or_none_if_nan(exoplanet.pl_radius)
        temp = self._get_value_or_none_if_nan(exoplanet.pl_temperature)

        if not any([mass is not None, radius is not None, temp is not None]):
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

    def build_habitability_section(self, exoplanet: Exoplanet) -> str:
        """
        Génère la section sur l'habitabilité de l'exoplanète
        """
        section = "== Habitabilité ==\n"
        section += "Les conditions d'habitabilité de cette exoplanète ne sont pas déterminées ou ne sont pas connues.\n"
        return section
