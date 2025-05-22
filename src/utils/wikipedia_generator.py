# src/utils/wikipedia_generator.py
from typing import Dict, List, Optional, Set
from src.models.exoplanet import Exoplanet
from src.models.reference import SourceType, DataPoint
import datetime
import locale
import re
from typing import Optional
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
        self.comparison_utils = ComparisonUtils(self.format_utils)
        self.star_utils = StarUtils(self.format_utils)
        self.reference_utils = ReferenceUtils()
        self.infobox_generator = InfoboxGenerator(self.reference_utils)

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
    
    def _get_used_references(self, exoplanet: Exoplanet) -> List[str]:
        """
        Retourne la liste des références utilisées pour l'exoplanète
        """
        refs = set()
        
        # Parcourir tous les attributs de l'exoplanète
        for field_name in exoplanet.__dataclass_fields__:
            if field_name == 'name' or field_name == 'other_names':
                continue
                
            value = getattr(exoplanet, field_name)
            if value and hasattr(value, 'reference') and value.reference:
                if isinstance(value.reference.source, SourceType):
                    refs.add(value.reference.source.value)
        
        # Si aucune référence n'a été trouvée, ajouter au moins EPE par défaut
        # Ne rien ajouter si pas de référence
            
        return list(refs)

    def generate_article_content(self, exoplanet: Exoplanet) -> str:
        """Génère le contenu complet d'un article Wikipedia pour une exoplanète."""
        content = f"""
{self.infobox_generator.generate_infobox(exoplanet)}
{self._generate_introduction_sentence(exoplanet)}
{self._generate_physical_section(exoplanet)}
{self._generate_orbit_section(exoplanet)}
{self._generate_discovery_section(exoplanet)}
{self._generate_star_section(exoplanet)}
{self._generate_habitability_section(exoplanet)}
{self._generate_references_section(exoplanet)}
"""
        return content.strip()
    
    def _generate_introduction_sentence(self, exoplanet: Exoplanet) -> str:
        """Génère la phrase d'introduction pour l'article."""
        
        star_name_formatted = ""
        if exoplanet.host_star and exoplanet.host_star.value:
            if isinstance(exoplanet.host_star, DataPoint):
                 star_name = exoplanet.host_star.value
                 star_name_formatted = f"[[{star_name}]]"
            else: 
                star_name = str(exoplanet.host_star.value) 
                star_name_formatted = f"[[{star_name}]]"
        else:
            star_name_formatted = "son étoile hôte"

        # Use star_utils.get_star_description for additional details about the star
        star_details = self.star_utils.get_star_description(exoplanet) 

        # Construct constellation part if available
        constellation_part = ""
        if exoplanet.constellation and exoplanet.constellation.value:
            constellation_name = exoplanet.constellation.value
            constellation_part = f" dans la [[constellation]] de [[{constellation_name}]]"

        intro = f"'''{{{{nobr|{exoplanet.name}}}}}''' est une [[exoplanète]] en [[orbite]] autour de {{{{nobr|{star_name_formatted}}}}}, {star_details}{constellation_part}."
        return intro

    def _generate_categories(self, exoplanet: Exoplanet) -> str:
        """Génère les catégories pour l'article."""
        categories = []
        planet_type = self._get_planet_type(exoplanet)
        mass_comparison = self.comparison_utils.get_mass_comparison(exoplanet)
        radius_comparison = self.comparison_utils.get_radius_comparison(exoplanet)
        
        section = "== Caractéristiques ==\n"
        section += f"Cette [[exoplanète]] est un [[{planet_type}]]"
        
        description_parts = []
        if mass_comparison:
            description_parts.append(mass_comparison)
        if radius_comparison:
            description_parts.append(radius_comparison)
            
        if description_parts:
            section += ", " + ", ".join(description_parts)
            
        section += "."
        
        return section

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

    def _get_size_comparison(self, exoplanet: Exoplanet) -> str:
        """
        Génère une comparaison de taille avec Jupiter ou la Terre
        """
        mass_value = exoplanet.mass.value if exoplanet.mass and exoplanet.mass.value else None
        if mass_value:
            if mass_value > 10:
                return f"environ {self.format_utils.format_numeric_value(mass_value/317.8, 1)} fois plus massif que [[Jupiter (planète)|Jupiter]]"
            else:
                return f"environ {self.format_utils.format_numeric_value(mass_value, 1)} fois plus massif que la [[Terre]]"
        return ""
    
    def _get_orbital_comparison(self, exoplanet: Exoplanet) -> str:
        """
        Génère la section de l'habitabilité de l'exoplanète
        """
        # Pour l'instant, cette section est vide car nous n'avons pas encore implémenté
        # la logique d'habitabilité
        return ""

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
    
    def _get_planet_description(self, exoplanet: Exoplanet) -> str:
        """
        Génère une description de la planète
        """
        desc = []
        if exoplanet.mass and exoplanet.mass.value:
            desc.append(self._get_size_comparison(exoplanet)) # _get_size_comparison uses format_utils.format_numeric_value, not _format_datapoint
        if exoplanet.radius and exoplanet.radius.value:
            # Pass exoplanet.name for context to _format_datapoint
            desc.append(f"d'un rayon de {self.format_utils.format_datapoint(exoplanet.radius, exoplanet.name, self.template_refs, self.reference_utils.add_reference)} [[rayon jovien|R_J]]")
        if exoplanet.temperature and exoplanet.temperature.value:
            # Pass exoplanet.name for context to _format_datapoint
            desc.append(f"avec une température de {self.format_utils.format_datapoint(exoplanet.temperature, exoplanet.name, self.template_refs, self.reference_utils.add_reference)} [[kelvin|K]]")
        
        return ", ".join(desc) if desc else ""
    
    def _format_references(self, exoplanet: Exoplanet) -> str:
        """Formate les références pour l'article."""
        references = []
        if exoplanet.source == "exoplanet_eu":
            references.append(
                f'<ref>{{{{Lien web |langue=en |nom1=EPE |titre={exoplanet.name} |url=https://exoplanet.eu/catalog/{exoplanet.name.lower().replace(" ", "_")}/ |site=exoplanet.eu |date=2024-8-1 |consulté le=2025-1-3 }}}}</ref>'
            )
        if exoplanet.source == "nasa":
            references.append(
                f'<ref>{{{{Lien web |langue=en |nom1=NasaGov |titre={exoplanet.name} |url=https://science.nasa.gov/exoplanet-catalog/{exoplanet.name.lower().replace(" ", "-")}/ |site=science.nasa.gov |date=2024-11-1 |consulté le=2025-1-3 }}}}</ref>'
            )
        return " ".join(references) 

    def _generate_physical_section(self, exoplanet: Exoplanet) -> str:
        """
        Génère la section des caractéristiques physiques de l'exoplanète
        """
        section = "== Caractéristiques physiques ==\n"
        
        # Description de la planète
        planet_desc = self._get_planet_description(exoplanet)
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