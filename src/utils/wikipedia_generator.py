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
        references = self.reference_manager.format_references_section()
        categories = self.category_utils.generate_categories(exoplanet)
        
        # Assembler l'article
        article = f"""{{{{Ébauche|exoplanète|}}}}

{infobox}

{introduction}

{physical_characteristics}

{orbit}

{discovery}

{habitability}

{references}

{categories}"""
        
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
        """
        Génère la section de la découverte de l'exoplanète
        """
        discovery_date = self.format_utils.format_year_field_with_ref(exoplanet.discovery_date, exoplanet.name, self.reference_manager.template_refs, self.reference_manager.add_reference)
        discovery_method = self.format_utils.format_datapoint(exoplanet.discovery_method, exoplanet.name, self.reference_manager.template_refs, self.reference_manager.add_reference)
        
        section = "== Découverte ==\n"
        section += f"Cette planète a été découverte en {discovery_date} par la méthode de {discovery_method}."
        
        return section

    def _generate_references_section(self, exoplanet: Exoplanet) -> str:
        """
        Génère une description de l'étoile hôte
        """
        desc = []
        if exoplanet.spectral_type and exoplanet.spectral_type.value:
            desc.append(f"une [[étoile]] de type spectral [[{exoplanet.spectral_type.value}]]")

        if exoplanet.distance and exoplanet.distance.value is not None:
            try:
                pc_value = float(exoplanet.distance.value)
                ly_value = self.format_utils.parsecs_to_lightyears(pc_value)
                formatted_ly_value = self.format_utils.format_numeric_value(ly_value, precision=0)
                # Pass exoplanet.name for context to _format_datapoint
                formatted_pc_value_with_ref = self.format_utils.format_datapoint(exoplanet.distance, exoplanet.name, self.reference_manager.template_refs, self.reference_manager.add_reference)
                distance_str = f"située à {formatted_ly_value} [[année-lumière|années-lumière]] ({formatted_pc_value_with_ref} [[parsec|pc]]) de la [[Terre]]"
                desc.append(distance_str)
            except (ValueError, TypeError):
                original_distance_str = self.format_utils.format_datapoint(exoplanet.distance, exoplanet.name, self.reference_manager.template_refs, self.reference_manager.add_reference)
                if original_distance_str:
                    desc.append(f"située à {original_distance_str} [[parsec|pc]] de la [[Terre]]")

        if exoplanet.apparent_magnitude and exoplanet.apparent_magnitude.value:
            # Pass exoplanet.name for context to _format_datapoint
            desc.append(f"d'une [[magnitude apparente]] de {self.format_utils.format_datapoint(exoplanet.apparent_magnitude, exoplanet.name, self.reference_manager.template_refs, self.reference_manager.add_reference)}")

        return " ".join(desc) if desc else "une étoile"

    def _generate_physical_section(self, exoplanet: Exoplanet) -> str:
        """
        Génère la section des caractéristiques physiques de l'exoplanète
        """
        section = "== Caractéristiques physiques ==\n"
        
        # Description de la planète
        planet_desc = self._generate_planet_description(exoplanet)
        if planet_desc:
            section += f"{planet_desc}.\n"
            
        # Comparaisons de taille
        mass_comparison = self.comparison_utils.get_mass_comparison(exoplanet)
        radius_comparison = self.comparison_utils.get_radius_comparison(exoplanet)
        
        comparisons = []
        if mass_comparison:
            comparisons.append(mass_comparison)
        if radius_comparison:
            comparisons.append(radius_comparison)
            
        if comparisons:
            section += " ".join(comparisons) + ".\n"
            
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
            desc.append(self.comparison_utils.get_mass_comparison(exoplanet)) # get_mass_comparison uses format_utils.format_numeric_value, not _format_datapoint
        if exoplanet.radius and exoplanet.radius.value:
            # Pass exoplanet.name for context to _format_datapoint
            desc.append(f"d'un rayon de {self.format_utils.format_datapoint(exoplanet.radius, exoplanet.name, self.reference_manager.template_refs, self.reference_manager.add_reference)} [[rayon jovien|R_J]]")
        if exoplanet.temperature and exoplanet.temperature.value:
            # Pass exoplanet.name for context to _format_datapoint
            desc.append(f"avec une température de {self.format_utils.format_datapoint(exoplanet.temperature, exoplanet.name, self.reference_manager.template_refs, self.reference_manager.add_reference)} [[kelvin|K]]")
        
        return ", ".join(desc) if desc else ""
    
    def _generate_introduction(self, exoplanet: Exoplanet) -> str:
        """
        Génère l'introduction de l'article Wikipedia
        """
        # Obtenir le type de planète
        planet_type = self.planet_type_utils.get_planet_type(exoplanet)
        
        # Générer la description de l'étoile hôte
        star_desc = self._generate_references_section(exoplanet)
        
        # Assembler l'introduction
        intro = f"{exoplanet.name} est {planet_type} orbitant autour de {star_desc}.\n"
        
        return intro
    