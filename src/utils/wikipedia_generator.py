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
            spectral_type = exoplanet.spectral_type.value
            spectral_class = spectral_type[0] if spectral_type else None
            description = self.star_utils.spectral_type_descriptions.get(spectral_class, "étoile")
            desc.append(f"d'une [[{spectral_type}|{description}]]")

        if exoplanet.distance and exoplanet.distance.value is not None:
            try:
                pc_value = float(exoplanet.distance.value)
                ly_value = self.format_utils.parsecs_to_lightyears(pc_value)
                formatted_ly_value = self.format_utils.format_numeric_value(ly_value, precision=0)
                # Pass exoplanet.name for context to _format_datapoint
                formatted_pc_value_with_ref = self.format_utils.format_datapoint(exoplanet.distance, exoplanet.name, self.reference_manager.template_refs, self.reference_manager.add_reference)
                distance_str = f"située à environ {formatted_ly_value} [[année-lumière|années-lumière]] ({formatted_pc_value_with_ref} [[parsec|pc]]) de la [[Terre]]"
                desc.append(distance_str)
            except (ValueError, TypeError):
                original_distance_str = self.format_utils.format_datapoint(exoplanet.distance, exoplanet.name, self.reference_manager.template_refs, self.reference_manager.add_reference)
                if original_distance_str:
                    desc.append(f"située à {original_distance_str} [[parsec|pc]] de la [[Terre]]")

        if exoplanet.apparent_magnitude and exoplanet.apparent_magnitude.value:
            # Pass exoplanet.name for context to _format_datapoint
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
            mass_value = self.format_utils.format_numeric_value(mass)
            if mass < 0.1:
                desc_parts.append(f"sa masse, relativement faible, est de {mass_value} M_J")
            elif mass < 1:
                desc_parts.append(f"sa masse modérée de {mass_value} M_J")
            else:
                desc_parts.append(f"sa masse imposante de {mass_value} M_J")
                
        if radius is not None:
            radius_value = self.format_utils.format_numeric_value(radius)
            if radius < 0.5:
                desc_parts.append(f"son rayon compact de {radius_value} R_J")
            elif radius < 1.5:
                desc_parts.append(f"son rayon de {radius_value} R_J")
            else:
                desc_parts.append(f"son rayon étendu de {radius_value} R_J")
                
        if temp is not None:
            temp_value = self.format_utils.format_numeric_value(temp)
            if temp < 500:
                desc_parts.append(f"sa température de surface de {temp_value} K")
            elif temp < 1000:
                desc_parts.append(f"sa température élevée de {temp_value} K")
            else:
                desc_parts.append(f"sa température extrême de {temp_value} K")
        
        if desc_parts:
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
        """
        Génère l'introduction de l'article Wikipedia
        """
        # Obtenir le type de planète
        planet_type = self.planet_type_utils.get_planet_type(exoplanet)
        
        # Déterminer l'article approprié
        article = "une"
        if planet_type.startswith(("Jupiter", "Neptune")):
            article = "un" if planet_type.startswith("Jupiter") else "une"
        
        # Générer la description de l'étoile hôte
        star_desc = self._generate_references_section(exoplanet)
        
        # Rendre le type d'astre cliquable
        planet_type_link = f"[[{planet_type}|{planet_type}]]"
        
        # Assembler l'introduction
        intro = f"{exoplanet.name} est {article} {planet_type_link}, orbitant autour {star_desc}.\n"
        
        return intro
    
    def generate_infobox(self, exoplanet: Exoplanet) -> str:
        """
        Génère l'infobox pour l'exoplanète
        """
        infobox = """{{Infobox Exoplanète
 | nom = {name}
 | image = 
 | légende = 
 | étoile = {star}
 | distance = {distance}
 | distance notes = {distance_ref}
 | type spectral = {spectral_type}
 | type spectral notes = {spectral_type_ref}
 | magnitude apparente = {apparent_magnitude}
 | magnitude apparente notes = {apparent_magnitude_ref}
 | type = {type}
 | demi-grand axe = {semi_major_axis}
 | demi-grand axe notes = {semi_major_axis_ref}
 | excentricité = {eccentricity}
 | excentricité notes = {eccentricity_ref}
 | période = {period}
 | période notes = {period_ref}
 | inclinaison = {inclination}
 | inclinaison notes = {inclination_ref}
 | masse = {mass}
 | masse notes = {mass_ref}
 | rayon = {radius}
 | rayon notes = {radius_ref}
 | température = {temperature}
 | température notes = {temperature_ref}
 | méthode = {method}
 | méthode notes = {method_ref}
 | date = {discovery_date}
 | date notes = {discovery_date_ref}
}}""".format(
            name=exoplanet.name,
            star=exoplanet.star_name,
            distance=exoplanet.distance.value if exoplanet.distance else "",
            distance_ref=self.reference_manager.format_datapoint(exoplanet.distance, exoplanet.name) if exoplanet.distance else "",
            spectral_type=exoplanet.spectral_type.value if exoplanet.spectral_type else "",
            spectral_type_ref=self.reference_manager.format_datapoint(exoplanet.spectral_type, exoplanet.name) if exoplanet.spectral_type else "",
            apparent_magnitude=exoplanet.apparent_magnitude.value if exoplanet.apparent_magnitude else "",
            apparent_magnitude_ref=self.reference_manager.format_datapoint(exoplanet.apparent_magnitude, exoplanet.name) if exoplanet.apparent_magnitude else "",
            type=exoplanet.type.value if exoplanet.type else "",
            semi_major_axis=exoplanet.semi_major_axis.value if exoplanet.semi_major_axis else "",
            semi_major_axis_ref=self.reference_manager.format_datapoint(exoplanet.semi_major_axis, exoplanet.name) if exoplanet.semi_major_axis else "",
            eccentricity=exoplanet.eccentricity.value if exoplanet.eccentricity else "",
            eccentricity_ref=self.reference_manager.format_datapoint(exoplanet.eccentricity, exoplanet.name) if exoplanet.eccentricity else "",
            period=exoplanet.period.value if exoplanet.period else "",
            period_ref=self.reference_manager.format_datapoint(exoplanet.period, exoplanet.name) if exoplanet.period else "",
            inclination=exoplanet.inclination.value if exoplanet.inclination else "",
            inclination_ref=self.reference_manager.format_datapoint(exoplanet.inclination, exoplanet.name) if exoplanet.inclination else "",
            mass=exoplanet.mass.value if exoplanet.mass else "",
            mass_ref=self.reference_manager.format_datapoint(exoplanet.mass, exoplanet.name) if exoplanet.mass else "",
            radius=exoplanet.radius.value if exoplanet.radius else "",
            radius_ref=self.reference_manager.format_datapoint(exoplanet.radius, exoplanet.name) if exoplanet.radius else "",
            temperature=exoplanet.temperature.value if exoplanet.temperature else "",
            temperature_ref=self.reference_manager.format_datapoint(exoplanet.temperature, exoplanet.name) if exoplanet.temperature else "",
            method=exoplanet.discovery_method.value if exoplanet.discovery_method else "",
            method_ref=self.reference_manager.format_datapoint(exoplanet.discovery_method, exoplanet.name) if exoplanet.discovery_method else "",
            discovery_date=exoplanet.discovery_date.value if exoplanet.discovery_date else "",
            discovery_date_ref=self.reference_manager.format_datapoint(exoplanet.discovery_date, exoplanet.name) if exoplanet.discovery_date else ""
        )
        return infobox
    