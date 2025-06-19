# src/generators/article_exoplanet_generator.py
import locale
import math

from src.models.entities.exoplanet import Exoplanet

from src.utils.formatters.article_formatters import ArticleUtils
from src.utils.astro.constellation_utils import ConstellationUtils

from src.utils.astro.classification.exoplanet_comparison_utils import (
    ExoplanetComparisonUtils,
)
from src.utils.astro.classification.exoplanet_type_utils import ExoplanetTypeUtils
from src.generators.exoplanet.exoplanet_infobox_generator import (
    ExoplanetInfoboxGenerator,
)
from src.generators.exoplanet.exoplanet_introduction_generator import (
    ExoplanetIntroductionGenerator,
)
from src.generators.exoplanet.exoplanet_category_generator import (
    ExoplanetCategoryGenerator,
)
from src.services.processors.reference_manager import ReferenceManager
from src.generators.base_article_generator import BaseArticleGenerator


class ArticleExoplanetGenerator(BaseArticleGenerator):
    """
    Classe pour générer les articles Wikipedia des exoplanètes
    """

    def __init__(self):
        locale.setlocale(locale.LC_ALL, "fr_FR.UTF-8")

        reference_manager = ReferenceManager()
        category_generator = ExoplanetCategoryGenerator()
        stub_type = "exoplanète"
        portals = ["astronomie", "exoplanètes"]

        super().__init__(reference_manager, category_generator, stub_type, portals)

        self.infobox_generator = ExoplanetInfoboxGenerator(self.reference_manager)
        self.article_utils = ArticleUtils()
        self.constellation_utils = ConstellationUtils()
        self.comparison_utils = ExoplanetComparisonUtils()
        self.planet_type_utils = ExoplanetTypeUtils()
        self.introduction_generator = ExoplanetIntroductionGenerator(
            self.comparison_utils, self.article_utils
        )

    def compose_exoplanet_article(self, exoplanet: Exoplanet) -> str:
        """
        Génère l'ensemble du contenu de l'article Wikipédia pour une exoplanète.
        Appelle des sous-fonctions dédiées pour chaque partie.
        """
        parts = []

        # 1. Templates de base (stub + source)
        parts.append(self.compose_stub_and_source())

        # 2. Infobox
        parts.append(self.infobox_generator.generate(exoplanet))

        # 3. Introduction
        parts.append(
            self.introduction_generator.compose_exoplanet_introduction(exoplanet)
        )

        # 4. Caractéristiques physiques
        parts.append(self.build_physical_characteristics_section(exoplanet))

        # 5. Orbite
        parts.append(self.build_orbit_section(exoplanet))

        # 6. Découverte
        parts.append(self.build_discovery_section(exoplanet))

        # 7. Habitabilité
        parts.append(self.build_habitability_section(exoplanet))

        # 8. Références et portails
        parts.append(self.build_references_section())

        # 9. Catégories
        parts.append(self.build_category_section(exoplanet))

        # On assemble le tout en filtrant les chaînes vides
        return "\n\n".join(filter(None, parts))

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
            semi_major_axis_str = self.article_utils.format_uncertain_value_for_article(
                exoplanet.pl_semi_major_axis
            )
            if semi_major_axis_str:
                content.append(
                    f"L'exoplanète orbite à une distance de {semi_major_axis_str} [[unité astronomique|UA]] de son étoile."
                )

        if exoplanet.pl_eccentricity:
            print("ici pl_name", exoplanet.pl_name)
            print("ici pl_eccentricity", exoplanet.pl_eccentricity)
            eccentricity_str: str = (
                self.article_utils.format_uncertain_value_for_article(
                    exoplanet.pl_eccentricity
                )
            )
            if eccentricity_str:
                content.append(f"L'orbite a une excentricité de {eccentricity_str}.")

        if exoplanet.pl_orbital_period:
            period_str: str = self.article_utils.format_uncertain_value_for_article(
                exoplanet.pl_orbital_period
            )
            if period_str:
                content.append(
                    f"La période orbitale est de {period_str} [[jour|jours]]."
                )

        if exoplanet.pl_inclination:
            inclination_str: str = (
                self.article_utils.format_uncertain_value_for_article(
                    exoplanet.pl_inclination
                )
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
            date_str: str = (
                f"en {self.article_utils.format_year_without_decimals(date_value.year)}"
            )
        else:
            date_str: str = (
                f"en {str(self.article_utils.format_year_without_decimals(date_value))}"
            )

        if disc_method:
            section += f"L'exoplanète a été découverte par la méthode {disc_method} {date_str}.\n"
        else:
            section += f"L'exoplanète a été découverte {date_str}.\n"

        return section

    def build_physical_characteristics_section(self, exoplanet: Exoplanet) -> str:
        """Génère la section des caractéristiques physiques."""

        def get_value_or_none_if_nan(data_point):
            if (
                data_point
                and hasattr(data_point, "value")
                and data_point.value is not None
            ):
                value = data_point.value
                if isinstance(value, str) and value.lower() == "nan":
                    return None
                return value
            return None

        mass: float | int | None = get_value_or_none_if_nan(exoplanet.pl_mass)
        radius: float | int | None = get_value_or_none_if_nan(exoplanet.pl_radius)
        temp: float | int | None = get_value_or_none_if_nan(exoplanet.pl_temperature)

        if not any([mass is not None, radius is not None, temp is not None]):
            return ""

        section = "== Caractéristiques physiques ==\n"

        # Construction d'une description plus naturelle
        desc_parts = []

        if mass is not None:
            try:
                mass_f = float(mass)
            except Exception:
                mass_f = None
            mass_value = self.article_utils.format_number_as_french_string(
                mass,
                precision=3
                if mass_f is not None and mass_f < 0.1
                else (2 if mass_f is not None and mass_f < 1 else 1),
            )

            if mass_f is not None:
                if mass_f < 0.1:
                    label = "faible"
                elif mass_f < 1:
                    label = "modérée"
                else:
                    label = "imposante"
                desc_parts.append(
                    f"sa masse {label} de {mass_value} [[Masse_jovienne|''M''{{{{ind|J}}}}]]"
                )

        if radius is not None:
            try:
                radius_f = float(radius)
            except Exception:
                radius_f = None
            radius_value: str = self.article_utils.format_number_as_french_string(
                radius,
                precision=3
                if radius_f is not None and radius_f < 0.1
                else (2 if radius_f is not None and radius_f < 1 else 1),
            )
            if radius_f is not None:
                if radius_f < 0.5:
                    label = "compact"
                elif radius_f < 1.5:
                    label: str = None
                else:
                    label = "étendu"
                desc: str = f"son rayon{' ' + label if label else ''} de {radius_value} [[Rayon_jovien|''R''{{{{ind|J}}}}]]"
                desc_parts.append(desc)

        if (
            temp is not None
            and not (isinstance(temp, str) and temp.lower() == "nan")
            and not (isinstance(temp, float) and math.isnan(temp))
        ):
            # Affiche sans décimale inutile, mais garde les décimales significatives
            try:
                temp_f = float(temp)
            except Exception:
                temp_f = None
            if isinstance(temp, (int, float)):
                temp_value: str = f"{float(temp):.5f}".rstrip("0").rstrip(".")
            else:
                temp_value = str(temp)

            if temp_f is not None:
                if temp_f < 500:
                    label = ""
                elif temp_f < 1000:
                    label = "élevée "
                else:
                    label = "extrême "
                desc_parts.append(f"sa température {label}de {temp_value} [[Kelvin|K]]")

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
