# src/utils/wikipedia_generator.py
import locale
from src.models.exoplanet import Exoplanet
from .infobox_generator import InfoboxGenerator
from .introduction_generator import IntroductionGenerator
from .category_generator import CategoryGenerator
from .reference_utils import ReferenceUtils
from .star_utils import StarUtils
from .format_utils import FormatUtils
from .comparison_utils import ComparisonUtils

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
    
    def __init__(self):
        self.template_refs = {
            'nasa': "{{Lien web |langue=en |nom1=NasaGov |titre={title} |url=https://science.nasa.gov/exoplanet-catalog/{id}/ |site=science.nasa.gov |date=2024-11-1 |consulté le=2025-1-3 }}",
            'exoplanet_eu': "{{Lien web |langue=en |nom1=EPE |titre={title} |url=https://exoplanet.eu/catalog/{id}/ |site=exoplanet.eu |date=2024-8-1 |consulté le=2025-1-3 }}",
            'open_exoplanet': "{{Lien web |langue=en |nom1=OEC |titre={title} |url=https://github.com/OpenExoplanetCatalogue/open_exoplanet_catalogue |site=Open Exoplanet Catalogue |date=2024-1-1 |consulté le=2025-1-3 }}",
            'article': "{{Article |langue= |auteur= |titre= |périodique= |année= |volume= |numéro= |pages= |lire en ligne= |consulté le= }}",
            'ouvrage': "{{Ouvrage |langue= |auteur= |titre= |éditeur= |année= |pages totales= |passage= |isbn= |lire en ligne= |consulté le= }}"
        }
        self._used_refs = set()
        self._has_grouped_notes = False
        locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
        self.format_utils = FormatUtils()
        self.category_utils = CategoryGenerator()
        self.comparison_utils = ComparisonUtils(self.format_utils)
        self.star_utils = StarUtils(self.format_utils)
        self.reference_utils = ReferenceUtils()
        self.infobox_generator = InfoboxGenerator(self.reference_utils)
        self.introduction_generator = IntroductionGenerator(self.comparison_utils, self.format_utils)
    
    def _get_planet_type(self, exoplanet: Exoplanet) -> str:
        """
        Détermine le type de planète en fonction de ses caractéristiques physiques
        """
        mass_value = exoplanet.mass.value if exoplanet.mass and exoplanet.mass.value else None
        radius_value = exoplanet.radius.value if exoplanet.radius and exoplanet.radius.value else None
        temp_value = exoplanet.temperature.value if exoplanet.temperature and exoplanet.temperature.value else None

        # Classification des planètes gazeuses
        if mass_value and mass_value >= 1:
            if temp_value:
                if temp_value >= 2200:
                    return "Jupiter ultra-chaud"
                elif temp_value >= 1000:
                    return "Jupiter chaud"
                elif temp_value >= 500:
                    return "Jupiter tiède"
                else:
                    return "Jupiter froid"
            else:
                return "Géante gazeuse"

        # Classification des planètes de glace
        elif radius_value and radius_value >= 0.8:
            if temp_value:
                if temp_value >= 1000:
                    return "Neptune chaud"
                elif temp_value >= 500:
                    return "Neptune tiède"
                else:
                    return "Neptune froid"
            else:
                return "Géante de glaces"

        # Classification des planètes telluriques
        elif mass_value and mass_value < 1:
            if radius_value:
                if radius_value >= 1.5:
                    return "Super-Terre"
                elif radius_value >= 0.8:
                    return "Planète de dimensions terrestres"
                else:
                    return "Sous-Terre"
            else:
                return "Planète tellurique"

        return "Planète tellurique"
    
    def generate_article_content(self, exoplanet: Exoplanet) -> str:
        """Génère le contenu complet d'un article Wikipedia pour une exoplanète."""
        content = f"""
{self.infobox_generator.generate_infobox(exoplanet)}
{self.introduction_generator.generate_introduction(exoplanet)}
{self._generate_physical_section(exoplanet)}
{self._generate_orbit_section(exoplanet)}
{self._generate_discovery_section(exoplanet)}
{self._generate_star_section(exoplanet)}
{self._generate_habitability_section(exoplanet)}
{self._generate_references_section(exoplanet)}
"""
        return content.strip()

    def _generate_orbit_section(self, exoplanet: Exoplanet) -> str:
        """
        Génère la section de l'orbite de l'exoplanète
        """
        orbital_comparison = self.comparison_utils.get_orbital_comparison(exoplanet)
        semi_major_axis = self.format_utils.format_datapoint(exoplanet.semi_major_axis, exoplanet.name, self.template_refs, self.reference_utils.add_reference)
        
        section = "== Orbite ==\n"
        section += f"Elle orbite à {{{{unité|{semi_major_axis}|[[unité astronomique|unités astronomiques]]}}}} de son étoile{orbital_comparison}."
        
        return section

    def _generate_discovery_section(self, exoplanet: Exoplanet) -> str:
        """
        Génère la section de la découverte de l'exoplanète
        """
        discovery_date = self.format_utils.format_year_field_with_ref(exoplanet.discovery_date, exoplanet.name, self.template_refs, self.reference_utils.add_reference)
        discovery_method = self.format_utils.format_datapoint(exoplanet.discovery_method, exoplanet.name, self.template_refs, self.reference_utils.add_reference)
        
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
                formatted_pc_value_with_ref = self.format_utils.format_datapoint(exoplanet.distance, exoplanet.name, self.template_refs, self.reference_utils.add_reference)
                distance_str = f"située à {formatted_ly_value} [[année-lumière|années-lumière]] ({formatted_pc_value_with_ref} [[parsec|pc]]) de la [[Terre]]"
                desc.append(distance_str)
            except (ValueError, TypeError):
                original_distance_str = self.format_utils.format_datapoint(exoplanet.distance, exoplanet.name, self.template_refs, self.reference_utils.add_reference)
                if original_distance_str:
                     desc.append(f"située à {original_distance_str} [[parsec|pc]] de la [[Terre]]")

        if exoplanet.apparent_magnitude and exoplanet.apparent_magnitude.value:
            # Pass exoplanet.name for context to _format_datapoint
            desc.append(f"d'une [[magnitude apparente]] de {self.format_utils.format_datapoint(exoplanet.apparent_magnitude, exoplanet.name, self.template_refs, self.reference_utils.add_reference)}")
        
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
            desc.append(f"d'un rayon de {self.format_utils.format_datapoint(exoplanet.radius, exoplanet.name, self.template_refs, self.reference_utils.add_reference)} [[rayon jovien|R_J]]")
        if exoplanet.temperature and exoplanet.temperature.value:
            # Pass exoplanet.name for context to _format_datapoint
            desc.append(f"avec une température de {self.format_utils.format_datapoint(exoplanet.temperature, exoplanet.name, self.template_refs, self.reference_utils.add_reference)} [[kelvin|K]]")
        
        return ", ".join(desc) if desc else ""
    