# src/generators/article_exoplanet_generator.py
import locale
import math

from src.models.data_source_exoplanet import DataSourceExoplanet

from src.utils.formatters.article_formatters import ArticleUtils
from src.utils.constellation_utils import ConstellationUtils

from src.utils.exoplanet_comparison_utils import ExoplanetComparisonUtils
from src.utils.exoplanet_type_utils import ExoplanetTypeUtils
from src.generators.exoplanet.exoplanet_infobox_generator_v2 import (
    ExoplanetInfoboxGenerator,
)
from src.generators.exoplanet.exoplanet_introduction_generator import (
    ExoplanetIntroductionGenerator,
)
from src.generators.exoplanet.exoplanet_category_generator import (
    ExoplanetCategoryGenerator,
)
from src.services.reference_manager import ReferenceManager
from src.generators.base_article_generator import BaseArticleGenerator



class ArticleExoplanetGenerator(BaseArticleGenerator):
    """
    Classe pour générer les articles Wikipedia des exoplanètes
    """

    # Constantes de classification des planètes
    EXOPLANET_MASS_THRESHOLDS = {
        "GAS_GIANT": 1.0,  # Masse en M_J
        "TERRESTRIAL": 1.0,  # Masse en M_J
    }

    EXOPLANET_RADIUS_THRESHOLDS = {
        "ICE_GIANT": 0.8,  # Rayon en R_J
        "SUPER_EARTH": 1.5,  # Rayon en R_J
        "EARTH_LIKE": 0.8,  # Rayon en R_J
    }

    EXOPLANET_TEMPERATURE_THRESHOLDS = {
        "ULTRA_HOT": 2200,  # Température en K
        "HOT": 1000,  # Température en K
        "WARM": 500,  # Température en K
    }

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

    def generate_article_content(self, exoplanet: DataSourceExoplanet) -> str:
        """
        Génère l'ensemble du contenu de l'article Wikipédia pour une exoplanète.
        Appelle des sous-fonctions dédiées pour chaque partie.
        """
        self.reference_manager.reset_references()
        parts = []

        # 1. Templates de base (stub + source)
        parts.append(self.generate_stub_and_source())

        # 2. Infobox
        parts.append(self.infobox_generator.generate(exoplanet))

        # 3. Introduction
        parts.append(self.introduction_generator.generate_exoplanet_introduction(exoplanet))

        # 4. Caractéristiques physiques
        parts.append(self._generate_physical_characteristics_section(exoplanet))

        # 5. Orbite
        parts.append(self._generate_orbit_section(exoplanet))

        # 6. Découverte
        parts.append(self._generate_discovery_section(exoplanet))

        # 7. Habitabilité
        parts.append(self._generate_habitability_section(exoplanet))

        # 8. Références et portails
        parts.append(self.generate_references_section())

        # 9. Catégories
        parts.append(self.generate_category_section(exoplanet))

        # On assemble le tout en filtrant les chaînes vides
        return "\n\n".join(filter(None, parts))

    def _generate_orbit_section(self, exoplanet: DataSourceExoplanet) -> str:
        """
        Génère la section de l'orbite de l'exoplanète
        """
        orbital_comparison = self.comparison_utils.get_orbital_comparison(exoplanet)
        semi_major_axis_str = self.article_utils.format_datapoint(
            exoplanet.pl_semi_major_axis,
            exoplanet.pl_name,
            self.reference_manager.template_refs,
            self.reference_manager.add_reference,
        )

        section = "== Orbite ==\n"

        cleaned_semi_major_axis_str = (
            semi_major_axis_str.replace(",", ".").split("<ref")[0].strip()
        )

        try:
            semi_major_axis_val = float(cleaned_semi_major_axis_str)
        except ValueError:
            # Handle cases where conversion might still fail (e.g., if semi_major_axis is None or non-numeric)
            # You might want to log this or set a default value, or skip the comparison.
            # For now, let's assume a default that will likely result in plural if the value is unparseable.
            semi_major_axis_val = 0.0

        # Determine whether to use singular or plural for "unité astronomique"
        if exoplanet.pl_semi_major_axis is not None and semi_major_axis_val <= 2:
            unit_text = "[[unité astronomique|unité astronomique]]"
        else:
            unit_text = "[[unité astronomique|unités astronomiques]]"

        section += f"Elle orbite à {{{{unité|{semi_major_axis_str}|{unit_text}}}}} de son étoile."
        section += " "
        section += f"{orbital_comparison}."

        return section

    def _generate_discovery_section(self, exoplanet: DataSourceExoplanet) -> str:
        """Génère la section de découverte."""
        if not exoplanet.disc_year:
            return ""

        section = "== Découverte ==\n"

        # Traduction des méthodes de découverte
        method_translations = {
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

        method_raw = exoplanet.disc_method.value if exoplanet.disc_method else ""
        disc_method = method_translations.get(method_raw, None)

        # Gestion robuste de la date
        date_value = (
            exoplanet.disc_year.value
            if hasattr(exoplanet.disc_year, "value")
            else exoplanet.disc_year
        )
        if hasattr(date_value, "year"):
            date_str = f"en {self.article_utils.format_year_value(date_value.year)}"
        else:
            date_str = f"en {str(self.article_utils.format_year_value(date_value))}"

        if disc_method:
            section += f"L'exoplanète a été découverte par la méthode {disc_method} {date_str}.\n"
        else:
            section += f"L'exoplanète a été découverte {date_str}.\n"

        return section

    def _generate_physical_characteristics_section(self, exoplanet: DataSourceExoplanet) -> str:
        """Génère la section des caractéristiques physiques."""
        def get_value_or_none_if_nan(data_point):
            if data_point and hasattr(data_point, "value") and data_point.value is not None:
                value = data_point.value
                if isinstance(value, str) and value.lower() == "nan":
                    return None
                return value
            return None

        mass = get_value_or_none_if_nan(exoplanet.pl_mass)
        radius = get_value_or_none_if_nan(exoplanet.pl_radius)
        temp = get_value_or_none_if_nan(exoplanet.pl_temperature)

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
            mass_value = self.article_utils.format_numeric_value(
                mass, precision=3 if mass_f is not None and mass_f < 0.1 else (2 if mass_f is not None and mass_f < 1 else 1)
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
            radius_value = self.article_utils.format_numeric_value(
                radius, precision=3 if radius_f is not None and radius_f < 0.1 else (2 if radius_f is not None and radius_f < 1 else 1)
            )
            if radius_f is not None:
                if radius_f < 0.5:
                    label = "compact"
                elif radius_f < 1.5:
                    label = ""
                else:
                    label = "étendu"
                desc = f"son rayon{' ' + label if label else ''} de {radius_value} [[Rayon_jovien|''R''{{{{ind|J}}}}]]"
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
                temp_value = f"{float(temp):.5f}".rstrip("0").rstrip(".")
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

    def _generate_habitability_section(self, exoplanet: DataSourceExoplanet) -> str:
        """
        Génère la section sur l'habitabilité de l'exoplanète
        """
        section = "== Habitabilité ==\n"
        section += "Les conditions d'habitabilité de cette exoplanète ne sont pas déterminées ou ne sont pas connues.\n"
        return section
