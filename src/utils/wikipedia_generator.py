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
        self.reference_utils = ReferenceUtils()
        self.infobox_generator = InfoboxGenerator(self.reference_utils)
        self.introduction_generator = IntroductionGenerator(self.comparison_utils, self.format_utils)
        self.category_generator = CategoryGenerator()
        self.star_utils = StarUtils(self.format_utils)

    def _get_reference(self, source: str, title: str) -> str:
        """
        Génère une référence au format Wikipedia
        """
        return f"<ref name=\"{source}\">{title}</ref>"

    def _add_reference(self, ref_name: str, ref_content: str) -> str:
        """
        Ajoute une référence à la liste des références utilisées
        """
        if ref_name not in self._used_refs:
            self._used_refs.add(ref_name)
            self.template_refs[ref_name] = ref_content
        return self._get_reference(ref_name, "")

    def _format_year_field(self, field: DataPoint, exoplanet_name: str) -> str:
        """
        Formate un champ de type année avec sa référence
        """
        if not field or not field.value:
            return ""
            
        year = str(field.value)
        if not year.isdigit() or len(year) != 4:
            return year
            
        ref = self._add_reference(str(field.reference.source.value), field.reference.to_wiki_ref(self.template_refs, exoplanet_name))
        return f"{year}{ref}"

    def _format_year_field_with_ref(self, field: DataPoint, exoplanet_name: str) -> str:
        """
        Formate un champ de type année avec sa référence
        """
        if not field or not field.value:
            return ""
            
        year = str(field.value)
        if not year.isdigit() or len(year) != 4:
            return year
            
        ref = self._add_reference(str(field.reference.source.value), field.reference.to_wiki_ref(self.template_refs, exoplanet_name))
        return f"{year}{ref}"

    def generate_article(self, exoplanet: Exoplanet) -> str:
        """
        Génère l'article complet pour une exoplanète
        """
        return self.generate_article_content(exoplanet)

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
        """
        Génère le contenu complet de l'article pour une exoplanète
        """
        # Générer l'introduction
        introduction = self.introduction_generator.generate_introduction(exoplanet)
        
        # Générer l'infobox
        infobox = self.infobox_generator.generate_infobox(exoplanet)
        
        # Générer les sections
        sections = []
        
        # Section Caractéristiques physiques
        physical_section = self._generate_physical_section(exoplanet)
        if physical_section:
            sections.append(physical_section)
            
        # Section Orbite
        orbit_section = self._generate_orbit_section(exoplanet)
        if orbit_section:
            sections.append(orbit_section)
            
        # Section Découverte
        discovery_section = self._generate_discovery_section(exoplanet)
        if discovery_section:
            sections.append(discovery_section)
            
        # Section Étoile hôte
        star_section = self._generate_star_section(exoplanet)
        if star_section:
            sections.append(star_section)
            
        # Section Habitabilité
        habitability_section = self._generate_habitability_section(exoplanet)
        if habitability_section:
            sections.append(habitability_section)
            
        # Section Références
        references_section = self._generate_references_section()
        if references_section:
            sections.append(references_section)
            
        # Assembler le contenu
        content = f"{infobox}\n\n{introduction}\n\n"
        content += "\n\n".join(sections)
        
        return content

    def _generate_physical_section(self, exoplanet: Exoplanet) -> str:
        """
        Génère la section des caractéristiques physiques de l'exoplanète
        """
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
        semi_major_axis = self.format_utils.format_datapoint(exoplanet.semi_major_axis, exoplanet.name, self.template_refs, self._add_reference)
        
        section = "== Orbite ==\n"
        section += f"Elle orbite à {{{{unité|{semi_major_axis}|[[unité astronomique|unités astronomiques]]}}}} de son étoile{orbital_comparison}."
        
        return section

    def _generate_discovery_section(self, exoplanet: Exoplanet) -> str:
        """
        Génère la section de la découverte de l'exoplanète
        """
        discovery_date = self.format_utils.format_year_field_with_ref(exoplanet.discovery_date, exoplanet.name, self.template_refs, self._add_reference)
        discovery_method = self.format_utils.format_datapoint(exoplanet.discovery_method, exoplanet.name, self.template_refs, self._add_reference)
        
        section = "== Découverte ==\n"
        section += f"Cette planète a été découverte en {discovery_date} par la méthode de {discovery_method}."
        
        return section

    def _generate_star_section(self, exoplanet: Exoplanet) -> str:
        """
        Génère la section de l'étoile hôte de l'exoplanète
        """
        star_description = self.star_utils.get_star_description(exoplanet)
        
        section = "== Étoile hôte ==\n"
        section += star_description
        
        return section

    def _generate_habitability_section(self, exoplanet: Exoplanet) -> str:
        """
        Génère la section de l'habitabilité de l'exoplanète
        """
        # Pour l'instant, cette section est vide car nous n'avons pas encore implémenté
        # la logique d'habitabilité
        return ""

    def _generate_references_section(self) -> str:
        """
        Génère la section des références
        """
        if not self._used_refs:
            return ""
            
        section = "== Références ==\n"
        section += "{{Références}}\n"
        
        return section

    def generate_article_content(self, exoplanet: Exoplanet) -> str:
        """
        Génère le contenu complet de l'article pour une exoplanète
        """
        # Générer l'introduction
        introduction = self.introduction_generator.generate_introduction(exoplanet)
        
        # Générer l'infobox
        infobox = self.infobox_generator.generate_infobox(exoplanet)
        
        # Générer les sections
        sections = []
        
        # Section Caractéristiques physiques
        physical_section = self._generate_physical_section(exoplanet)
        if physical_section:
            sections.append(physical_section)
            
        # Section Orbite
        orbit_section = self._generate_orbit_section(exoplanet)
        if orbit_section:
            sections.append(orbit_section)
            
        # Section Découverte
        discovery_section = self._generate_discovery_section(exoplanet)
        if discovery_section:
            sections.append(discovery_section)
            
        # Section Étoile hôte
        star_section = self._generate_star_section(exoplanet)
        if star_section:
            sections.append(star_section)
            
        # Section Habitabilité
        habitability_section = self._generate_habitability_section(exoplanet)
        if habitability_section:
            sections.append(habitability_section)
            
        # Section Références
        references_section = self._generate_references_section()
        if references_section:
            sections.append(references_section)
            
        # Assembler le contenu
        content = f"{infobox}\n\n{introduction}\n\n"
        content += "\n\n".join(sections)
        
        return content 