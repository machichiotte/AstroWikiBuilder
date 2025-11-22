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
            self.build_nomenclature_section(exoplanet),
            self.build_host_star_section(exoplanet),
            self.build_physical_characteristics_section(exoplanet),
            self.build_orbit_section(exoplanet),
            self.build_discovery_section(exoplanet),
            self.build_habitability_section(exoplanet),
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
        Génère la section sur l'habitabilité de l'exoplanète en se basant sur la température d'équilibre.
        """
        section = "== Habitabilité ==\n"

        temp = self._get_value_or_none_if_nan(exoplanet.pl_temperature)

        if temp is None:
            section += "Les conditions d'habitabilité de cette exoplanète ne sont pas déterminées ou ne sont pas connues.\n"
            return section

        try:
            temp_val = float(temp)
        except (ValueError, TypeError):
            section += "Les conditions d'habitabilité de cette exoplanète ne sont pas déterminées ou ne sont pas connues.\n"
            return section

        # Estimation basique basée sur la température d'équilibre
        # Zone habitable approximative (très simplifiée) : 180K - 395K
        # Note: C'est une estimation purement thermique sans tenir compte de l'atmosphère

        temp_str = self.article_util.format_uncertain_value_for_article(exoplanet.pl_temperature)

        if temp_val > 395:
            section += (
                f"Avec une température d'équilibre estimée à {temp_str} [[Kelvin|K]], "
                "cette exoplanète est considérée comme trop chaude pour abriter de l'eau liquide en surface.\n"
            )
        elif temp_val < 180:
            section += (
                f"Avec une température d'équilibre estimée à {temp_str} [[Kelvin|K]], "
                "cette exoplanète est considérée comme trop froide pour abriter de l'eau liquide en surface.\n"
            )
        else:
            section += (
                f"Avec une température d'équilibre estimée à {temp_str} [[Kelvin|K]], "
                "cette exoplanète se situe théoriquement dans la zone habitable de son étoile, "
                "permettant potentiellement la présence d'eau liquide en surface sous réserve d'une atmosphère adéquate.\n"
            )

        return section

    def build_nomenclature_section(self, exoplanet: Exoplanet) -> str:
        """
        Génère un paragraphe standard expliquant la convention de nommage.
        """
        if not exoplanet.pl_name:
            return ""

        content = "== Nomenclature ==\n"
        content += (
            "La convention de l'[[Union astronomique internationale]] (UAI) pour la désignation des exoplanètes "
            "consiste à ajouter une lettre minuscule à la suite du nom de l'étoile hôte, en commençant par la lettre « b » "
            "pour la première planète découverte dans le système (la lettre « a » désignant l'étoile elle-même). "
            "Les planètes suivantes reçoivent les lettres « c », « d », etc., dans l'ordre de leur découverte.\n"
        )

        return content

    def build_host_star_section(self, exoplanet: Exoplanet) -> str:
        """
        Génère la section résumant les caractéristiques de l'étoile hôte.
        """
        if not exoplanet.st_name:
            return ""

        content = "== Étoile hôte ==\n"

        # Introduction avec le nom de l'étoile
        content += f"L'exoplanète orbite autour de [[{exoplanet.st_name}]], "

        characteristics = []

        # Type spectral
        if exoplanet.st_spectral_type:
            characteristics.append(f"une étoile de type spectral {exoplanet.st_spectral_type}")

        # Masse
        if exoplanet.st_mass and exoplanet.st_mass.value:
            mass_str = self.article_util.format_uncertain_value_for_article(exoplanet.st_mass)
            if mass_str:
                characteristics.append(
                    f"d'une masse de {mass_str} [[Masse solaire|''M''{{{{ind|☉}}}}]]"
                )

        # Métallicité
        if exoplanet.st_metallicity and exoplanet.st_metallicity.value:
            met_str = self.article_util.format_uncertain_value_for_article(exoplanet.st_metallicity)
            if met_str:
                characteristics.append(f"d'une métallicité de {met_str} [Fe/H]")

        # Âge
        if exoplanet.st_age and exoplanet.st_age.value:
            age_str = self.article_util.format_uncertain_value_for_article(exoplanet.st_age)
            if age_str:
                characteristics.append(f"âgée de {age_str} [[milliard]]s d'années")

        if not characteristics:
            # Si on a juste le nom mais aucune info, on fait une phrase simple
            content = f"== Étoile hôte ==\nL'exoplanète orbite autour de l'étoile [[{exoplanet.st_name}]].\n"
            return content

        # Assemblage de la phrase
        if len(characteristics) == 1:
            content += f"{characteristics[0]}.\n"
        else:
            content += f"{', '.join(characteristics[:-1])} et {characteristics[-1]}.\n"

        return content
