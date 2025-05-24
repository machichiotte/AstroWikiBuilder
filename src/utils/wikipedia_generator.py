# src/utils/wikipedia_generator.py
import locale
from typing import Literal
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
        "période": "j", # jours
        "inclinaison": "°", # degrés
        # Add other fields if they have common default units displayed in infoboxes
        "périastre": "ua",
        "apoastre": "ua",
        "masse minimale": "M_J",
        "masse volumique": "kg/m³", # Though often g/cm³ is also used
        "gravité": "m/s²",
        "période de rotation": "h", # heures
        "arg_péri": "°", # argument of periastron
    }
    
    # Constantes de classification des planètes
    MASS_THRESHOLDS = {
        'GAS_GIANT': 1.0,  # Masse en M_J
        'TERRESTRIAL': 1.0  # Masse en M_J
    }
    
    RADIUS_THRESHOLDS = {
        'ICE_GIANT': 0.8,   # Rayon en R_J
        'SUPER_EARTH': 1.5, # Rayon en R_J
        'EARTH_LIKE': 0.8   # Rayon en R_J
    }
    
    TEMPERATURE_THRESHOLDS = {
        'ULTRA_HOT': 2200,  # Température en K
        'HOT': 1000,        # Température en K
        'WARM': 500         # Température en K
    }
    
    def __init__(self):
        locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')

        self.reference_manager = ReferenceManager()
        self.category_utils = CategoryGenerator()
        self.infobox_generator = InfoboxGenerator(self.reference_manager)
        self.format_utils = FormatUtils()
        self.star_utils = StarUtils(self.format_utils)
        self.comparison_utils = ComparisonUtils(self.format_utils)
        self.planet_type_utils = PlanetTypeUtils()

    def generate_article_content(self, exoplanet: Exoplanet) -> str:
        """
        Génère le contenu complet de l'article Wikipedia
        """
        # Réinitialiser les références pour le nouvel article
        self.reference_manager.reset_references()
        
        # Générer les différentes sections
        infobox = self.infobox_generator.generate_infobox(exoplanet)
        introduction = self._generate_introduction(exoplanet)
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
        semi_major_axis = self.format_utils.format_datapoint(exoplanet.semi_major_axis, exoplanet.name, self.reference_manager.template_refs, self.reference_manager.add_reference)
        
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
            "Transit": "du transit",
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
            "Transit Timing Variations": "des variations temporelles de transit"
        }
        
        discovery_method = exoplanet.discovery_method.value if exoplanet.discovery_method else ""
        discovery_method = method_translations.get(discovery_method, f"de {discovery_method.lower()}")
        
        # Gestion robuste de la date
        date_value = exoplanet.discovery_date.value if hasattr(exoplanet.discovery_date, 'value') else exoplanet.discovery_date
        if hasattr(date_value, 'year'):
            date_str = f"en {date_value.year}"
        else:
            date_str = f"en {str(date_value)}"
        
        section += f"L'exoplanète a été découverte par la méthode {discovery_method} {date_str}.\n"
        
        return section

    def _generate_references_section(self, exoplanet: Exoplanet) -> str:
        """
        Génère une description de l'étoile hôte
        """
        desc = []
        if exoplanet.spectral_type and exoplanet.spectral_type.value:
            spectral_type = exoplanet.spectral_type.value
            spectral_class = spectral_type[0] if spectral_type else None
            description = self.star_utils.SPECTRAL_TYPE_DESCRIPTIONS.get(spectral_class, "étoile")
            desc.append(f"d'une [[{description}|{description}]]")

        if exoplanet.distance and exoplanet.distance.value is not None:
            try:
                pc_value = float(exoplanet.distance.value)
                ly_value = self.format_utils.parsecs_to_lightyears(pc_value)
                formatted_ly_value = self.format_utils.format_numeric_value(ly_value, precision=0)
                formatted_pc_value_with_ref = self.format_utils.format_datapoint(exoplanet.distance, exoplanet.name, self.reference_manager.template_refs, self.reference_manager.add_reference)
                distance_str = f"située à environ {formatted_ly_value} [[année-lumière|années-lumière]] ({formatted_pc_value_with_ref} [[parsec|pc]]) de la [[Terre]]"
                desc.append(distance_str)
            except (ValueError, TypeError):
                original_distance_str = self.format_utils.format_datapoint(exoplanet.distance, exoplanet.name, self.reference_manager.template_refs, self.reference_manager.add_reference)
                if original_distance_str:
                    desc.append(f"située à {original_distance_str} [[parsec|pc]] de la [[Terre]]")

        if exoplanet.apparent_magnitude and exoplanet.apparent_magnitude.value:
            desc.append(f"avec une [[magnitude apparente]] de {self.format_utils.format_datapoint(exoplanet.apparent_magnitude, exoplanet.name, self.reference_manager.template_refs, self.reference_manager.add_reference)}")

        return " ".join(desc) if desc else "une étoile"

    def _generate_physical_characteristics(self, exoplanet: Exoplanet) -> str:
        """Génère la section des caractéristiques physiques."""
        mass = exoplanet.mass.value if exoplanet.mass and exoplanet.mass.value is not None else None
        radius = exoplanet.radius.value if exoplanet.radius and exoplanet.radius.value is not None else None
        temp = exoplanet.temperature.value if exoplanet.temperature and exoplanet.temperature.value is not None else None
        
        if not any([mass, radius, temp]):
            return ""
            
        section = "== Caractéristiques physiques ==\n"
        
        # Construction d'une description plus naturelle
        desc_parts = []
        
        if mass is not None:
            mass_value = self.format_utils.format_numeric_value(mass, precision=3 if mass < 0.1 else (2 if mass < 1 else 1))
            if mass < 0.1:
                desc_parts.append(f"sa masse faible de {mass_value} [[Masse_jovienne|''M''{{{{ind|J}}}}]]")
            elif mass < 1:
                desc_parts.append(f"sa masse modérée de {mass_value} [[Masse_jovienne|''M''{{{{ind|J}}}}]]")
            else:
                desc_parts.append(f"sa masse imposante de {mass_value} [[Masse_jovienne|''M''{{{{ind|J}}}}]]")
                
        if radius is not None:
            radius_value = self.format_utils.format_numeric_value(radius, precision=3 if radius < 0.1 else (2 if radius < 1 else 1))
            if radius < 0.5:
                desc_parts.append(f"son rayon compact de {radius_value} [[Rayon_jovien|''R''{{{{ind|J}}}}]]")
            elif radius < 1.5:
                desc_parts.append(f"son rayon de {radius_value} [[Rayon_jovien|''R''{{{{ind|J}}}}]]")
            else:
                desc_parts.append(f"son rayon étendu de {radius_value} [[Rayon_jovien|''R''{{{{ind|J}}}}]]")
                
        if temp is not None:
            temp_value = self.format_utils.format_numeric_value(temp, precision=1 if temp < 100 else 0)
            if temp < 500:
                desc_parts.append(f"sa température de {temp_value} [[Kelvin|K]]")
            elif temp < 1000:
                desc_parts.append(f"sa température élevée de {temp_value} [[Kelvin|K]]")
            else:
                desc_parts.append(f"sa température extrême de {temp_value} [[Kelvin|K]]")
        
        if desc_parts:
            if len(desc_parts) == 1:
                section += f"L'exoplanète se distingue par {desc_parts[0]}.\n"
            else:
                section += f"L'exoplanète se distingue par {', '.join(desc_parts[:-1])} et {desc_parts[-1]}.\n"
        
        return section

    def _generate_star_section(self, exoplanet: Exoplanet) -> str:
        """
        Génère la section sur l'étoile hôte de l'exoplanète
        """
        section = "== Étoile hôte ==\n"
        star_desc = self.star_utils.get_star_description(exoplanet)
        if star_desc:
            section += f"{star_desc}.\n"
        else:
            section += "Informations sur l'étoile hôte indisponibles.\n"
        return section 

    def _generate_habitability_section(self, exoplanet: Exoplanet) -> str:
        """
        Génère la section sur l'habitabilité de l'exoplanète
        """
        section = "== Habitabilité ==\n"
        section += "Les conditions d'habitabilité de cette exoplanète ne sont pas déterminées ou ne sont pas connues.\n"
        return section  
    
    def _generate_planet_description(self, exoplanet: Exoplanet) -> str:
        """
        Génère une description de la planète
        """
        desc = []
        if exoplanet.mass and exoplanet.mass.value:
            mass_str = self.format_utils.format_datapoint(exoplanet.mass, exoplanet.name, self.reference_manager.template_refs, self.reference_manager.add_reference)
            desc.append(f"d'une masse de {mass_str}")
        if exoplanet.radius and exoplanet.radius.value:
            radius_str = self.format_utils.format_datapoint(exoplanet.radius, exoplanet.name, self.reference_manager.template_refs, self.reference_manager.add_reference)
            desc.append(f"d'un rayon de {radius_str}")
        if exoplanet.temperature and exoplanet.temperature.value:
            temp_str = self.format_utils.format_datapoint(exoplanet.temperature, exoplanet.name, self.reference_manager.template_refs, self.reference_manager.add_reference)
            desc.append(f"avec une température de {temp_str}")
        
        return ", ".join(desc) if desc else ""
    
    def _generate_introduction(self, exoplanet: Exoplanet) -> str:
        """Génère l'introduction de l'article Wikipedia."""
        # Obtenir le type de planète
        planet_type = self.planet_type_utils.get_planet_type(exoplanet)
        
        # Obtenir la description de l'étoile
        star_desc = self.star_utils.get_star_description(exoplanet.spectral_type.value if exoplanet.spectral_type else None)
        
        # Construire l'introduction
        introduction = f"{exoplanet.name} est un [[{planet_type}|{planet_type}]], orbitant autour de {star_desc}"
        
        # Ajouter la distance si disponible
        if exoplanet.distance and exoplanet.distance.value is not None:
            try:
                pc_value = float(exoplanet.distance.value)
                ly_value = self.format_utils.parsecs_to_lightyears(pc_value)
                formatted_ly_value = self.format_utils.format_numeric_value(ly_value, precision=0)
                formatted_pc_value = self.format_utils.format_numeric_value(pc_value, precision=2)
                introduction += f" située à environ {formatted_ly_value} [[année-lumière|années-lumière]] ({formatted_pc_value} [[parsec|pc]]) de la [[Terre]]"
            except (ValueError, TypeError):
                pass
                
        # Ajouter la magnitude apparente si disponible
        if exoplanet.apparent_magnitude and exoplanet.apparent_magnitude.value is not None:
            mag_value = self.format_utils.format_numeric_value(exoplanet.apparent_magnitude.value, precision=2)
            introduction += f" avec une [[magnitude apparente]] de {mag_value}"
            
        introduction += "."
        return introduction
    
    def generate_infobox(self, exoplanet: Exoplanet) -> str:
        """
        Génère l'infobox pour l'exoplanète
        """
        fields = {
            "nom": exoplanet.name,
            "image": "",
            "légende": "",
            "étoile": exoplanet.star_name,
            "distance": self.format_utils.format_value(exoplanet.distance.value if exoplanet.distance else None, "distance"),
            "distance notes": self.reference_manager.format_datapoint(exoplanet.distance, exoplanet.name) if exoplanet.distance else None,
            "type spectral": exoplanet.spectral_type.value if exoplanet.spectral_type else None,
            "type spectral notes": self.reference_manager.format_datapoint(exoplanet.spectral_type, exoplanet.name) if exoplanet.spectral_type else None,
            "magnitude apparente": self.format_utils.format_value(exoplanet.apparent_magnitude.value if exoplanet.apparent_magnitude else None, "apparent_magnitude"),
            "magnitude apparente notes": self.reference_manager.format_datapoint(exoplanet.apparent_magnitude, exoplanet.name) if exoplanet.apparent_magnitude else None,
            "type": exoplanet.type.value if exoplanet.type else None,
            "demi-grand axe": self.format_utils.format_value(exoplanet.semi_major_axis.value if exoplanet.semi_major_axis else None, "semi_major_axis"),
            "demi-grand axe notes": self.reference_manager.format_datapoint(exoplanet.semi_major_axis, exoplanet.name) if exoplanet.semi_major_axis else None,
            "excentricité": self.format_utils.format_value(exoplanet.eccentricity.value if exoplanet.eccentricity else None, "eccentricity"),
            "excentricité notes": self.reference_manager.format_datapoint(exoplanet.eccentricity, exoplanet.name) if exoplanet.eccentricity else None,
            "période": self.format_utils.format_value(exoplanet.period.value if exoplanet.period else None, "period"),
            "période notes": self.reference_manager.format_datapoint(exoplanet.period, exoplanet.name) if exoplanet.period else None,
            "inclinaison": self.format_utils.format_value(exoplanet.inclination.value if exoplanet.inclination else None, "inclination"),
            "inclinaison notes": self.reference_manager.format_datapoint(exoplanet.inclination, exoplanet.name) if exoplanet.inclination else None,
            "masse": self.format_utils.format_value(exoplanet.mass.value if exoplanet.mass else None, "mass"),
            "masse notes": self.reference_manager.format_datapoint(exoplanet.mass, exoplanet.name) if exoplanet.mass else None,
            "rayon": self.format_utils.format_value(exoplanet.radius.value if exoplanet.radius else None, "radius"),
            "rayon notes": self.reference_manager.format_datapoint(exoplanet.radius, exoplanet.name) if exoplanet.radius else None,
            "température": self.format_utils.format_value(exoplanet.temperature.value if exoplanet.temperature else None, "temperature"),
            "température notes": self.reference_manager.format_datapoint(exoplanet.temperature, exoplanet.name) if exoplanet.temperature else None,
            "méthode": exoplanet.discovery_method.value if exoplanet.discovery_method else None,
            "méthode notes": self.reference_manager.format_datapoint(exoplanet.discovery_method, exoplanet.name) if exoplanet.discovery_method else None,
            "date": self.format_utils.format_value(exoplanet.discovery_date.value if exoplanet.discovery_date else None, "date"),
            "date notes": self.reference_manager.format_datapoint(exoplanet.discovery_date, exoplanet.name) if exoplanet.discovery_date else None
        }

        infobox_lines = ["{{Infobox Exoplanète"]
        for key, value in fields.items():
            if value is not None:
                infobox_lines.append(f" | {key} = {value}")
        infobox_lines.append("}}")

        return "\n".join(infobox_lines)
    