# src/utils/wikipedia_generator.py
import locale
from src.models.exoplanet import Exoplanet
from .infobox_generator import InfoboxGenerator
from .introduction_generator import IntroductionGenerator
from .category_generator import CategoryGenerator
from .reference_manager import ReferenceManager
from .star_utils import StarUtils
from .format_utils import FormatUtils
from .comparison_utils import ComparisonUtils
from .planet_type_utils import PlanetTypeUtils


class WikipediaGenerator:
    """
    Classe pour générer les articles Wikipedia des exoplanètes
    """

    FIELD_DEFAULT_UNITS = {
        "masse": "M_J",
        "rayon": "R_J",
        "température": "K",
        "distance": "pc",
        "demi-grand axe": "ua",
        "période": "j",  # jours
        "inclinaison": "°",  # degrés
        # Add other fields if they have common default units displayed in infoboxes
        "périastre": "ua",
        "apoastre": "ua",
        "masse minimale": "M_J",
        "masse volumique": "kg/m³",  # Though often g/cm³ is also used
        "gravité": "m/s²",
        "période de rotation": "h",  # heures
        "arg_péri": "°",  # argument of periastron
    }

    # Constantes de classification des planètes
    MASS_THRESHOLDS = {
        "GAS_GIANT": 1.0,  # Masse en M_J
        "TERRESTRIAL": 1.0,  # Masse en M_J
    }

    RADIUS_THRESHOLDS = {
        "ICE_GIANT": 0.8,  # Rayon en R_J
        "SUPER_EARTH": 1.5,  # Rayon en R_J
        "EARTH_LIKE": 0.8,  # Rayon en R_J
    }

    TEMPERATURE_THRESHOLDS = {
        "ULTRA_HOT": 2200,  # Température en K
        "HOT": 1000,  # Température en K
        "WARM": 500,  # Température en K
    }

    def __init__(self):
        locale.setlocale(locale.LC_ALL, "fr_FR.UTF-8")

        self.reference_manager = ReferenceManager()
        self.category_utils = CategoryGenerator()
        self.infobox_generator = InfoboxGenerator(self.reference_manager)
        self.format_utils = FormatUtils()
        self.star_utils = StarUtils(self.format_utils)
        self.comparison_utils = ComparisonUtils(self.format_utils)
        self.planet_type_utils = PlanetTypeUtils()
        self.introduction_generator = IntroductionGenerator(
            self.comparison_utils, self.format_utils
        )

    def generate_article_content(self, exoplanet: Exoplanet) -> str:
        """
        Génère le contenu complet de l'article Wikipedia
        """
        # Réinitialiser les références pour le nouvel article
        self.reference_manager.reset_references()

        # Générer les différentes sections
        infobox = self.infobox_generator.generate_infobox(exoplanet)
        introduction = self.introduction_generator.generate_introduction(exoplanet)
        physical_characteristics = self._generate_physical_characteristics(exoplanet)
        orbit = self._generate_orbit_section(exoplanet)
        discovery = self._generate_discovery_section(exoplanet)
        habitability = self._generate_habitability_section(exoplanet)

        # Assembler l'article
        article = f"""{{{{Ébauche|exoplanète|}}}}

{infobox}

{introduction}

{physical_characteristics}

{orbit}

{discovery}

{habitability}

== Références ==
{{{{références}}}}

{{{{Portail|astronomie|exoplanètes}}}}

"""
        # Ajouter les catégories
        categories = self.category_utils.generate_categories(exoplanet)
        for category in categories:
            article += f"[[Catégorie:{category}]]\n"

        return article

    def _generate_orbit_section(self, exoplanet: Exoplanet) -> str:
        """
        Génère la section de l'orbite de l'exoplanète
        """
        orbital_comparison = self.comparison_utils.get_orbital_comparison(exoplanet)
        semi_major_axis = self.format_utils.format_datapoint(
            exoplanet.semi_major_axis,
            exoplanet.name,
            self.reference_manager.template_refs,
            self.reference_manager.add_reference,
        )

        section = "== Orbite ==\n"
        section += f"Elle orbite à {{{{unité|{semi_major_axis}|[[unité astronomique|unités astronomiques]]}}}} de son étoile{orbital_comparison}."

        return section

    def _generate_discovery_section(self, exoplanet: Exoplanet) -> str:
        """Génère la section de découverte."""
        if not exoplanet.discovery_date:
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

        discovery_method = (
            exoplanet.discovery_method.value if exoplanet.discovery_method else ""
        )
        discovery_method = method_translations.get(
            discovery_method, f"de {discovery_method.lower()}"
        )

        # Gestion robuste de la date
        date_value = (
            exoplanet.discovery_date.value
            if hasattr(exoplanet.discovery_date, "value")
            else exoplanet.discovery_date
        )
        if hasattr(date_value, "year"):
            date_str = f"en {date_value.year}"
        else:
            date_str = f"en {str(date_value)}"

        section += f"L'exoplanète a été découverte par la méthode {discovery_method} {date_str}.\n"

        return section

    def _generate_physical_characteristics(self, exoplanet: Exoplanet) -> str:
        """Génère la section des caractéristiques physiques."""
        mass = (
            exoplanet.mass.value
            if exoplanet.mass and exoplanet.mass.value is not None
            else None
        )
        radius = (
            exoplanet.radius.value
            if exoplanet.radius and exoplanet.radius.value is not None
            else None
        )
        temp = (
            exoplanet.temperature.value
            if exoplanet.temperature and exoplanet.temperature.value is not None
            else None
        )

        if not any([mass, radius, temp]):
            return ""

        section = "== Caractéristiques physiques ==\n"

        # Construction d'une description plus naturelle
        desc_parts = []

        if mass is not None:
            mass_value = self.format_utils.format_numeric_value(
                mass, precision=3 if mass < 0.1 else (2 if mass < 1 else 1)
            )
            if mass < 0.1:
                desc_parts.append(
                    f"sa masse faible de {mass_value} [[Masse_jovienne|''M''{{{{ind|J}}}}]]"
                )
            elif mass < 1:
                desc_parts.append(
                    f"sa masse modérée de {mass_value} [[Masse_jovienne|''M''{{{{ind|J}}}}]]"
                )
            else:
                desc_parts.append(
                    f"sa masse imposante de {mass_value} [[Masse_jovienne|''M''{{{{ind|J}}}}]]"
                )

        if radius is not None:
            radius_value = self.format_utils.format_numeric_value(
                radius, precision=3 if radius < 0.1 else (2 if radius < 1 else 1)
            )
            if radius < 0.5:
                desc_parts.append(
                    f"son rayon compact de {radius_value} [[Rayon_jovien|''R''{{{{ind|J}}}}]]"
                )
            elif radius < 1.5:
                desc_parts.append(
                    f"son rayon de {radius_value} [[Rayon_jovien|''R''{{{{ind|J}}}}]]"
                )
            else:
                desc_parts.append(
                    f"son rayon étendu de {radius_value} [[Rayon_jovien|''R''{{{{ind|J}}}}]]"
                )

        if temp is not None:
            temp_value = self.format_utils.format_numeric_value(
                temp, precision=1 if temp < 100 else 0
            )
            if temp < 500:
                desc_parts.append(f"sa température de {temp_value} [[Kelvin|K]]")
            elif temp < 1000:
                desc_parts.append(f"sa température élevée de {temp_value} [[Kelvin|K]]")
            else:
                desc_parts.append(
                    f"sa température extrême de {temp_value} [[Kelvin|K]]"
                )

        if desc_parts:
            if len(desc_parts) == 1:
                section += f"L'exoplanète se distingue par {desc_parts[0]}.\n"
            else:
                section += f"L'exoplanète se distingue par {', '.join(desc_parts[:-1])} et {desc_parts[-1]}.\n"

        return section

    def _generate_habitability_section(self, exoplanet: Exoplanet) -> str:
        """
        Génère la section sur l'habitabilité de l'exoplanète
        """
        section = "== Habitabilité ==\n"
        section += "Les conditions d'habitabilité de cette exoplanète ne sont pas déterminées ou ne sont pas connues.\n"
        return section
