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

    def _get_reference(self, source: str, title: str, id: str) -> str:
        """
        Retourne la référence formatée pour une source donnée
        """
        template = self.template_refs.get(source, "")
        return template.format(title=title, id=id)
    
    def _add_reference(self, ref_name: str, ref_content: str) -> str:
        """
        Ajoute une référence et retourne la balise de référence appropriée.
        ref_content is expected to be the full reference tag for the first use,
        including the <ref name="..."> wrapper.
        e.g. <ref name="NasaGov">{{Lien web...}}</ref>
        """
        if ref_name not in self._used_refs:
            self._used_refs.add(ref_name)
            # Check if the content being added defines a grouped note
            if isinstance(ref_content, str) and 'group="note"' in ref_content.lower():
                self._has_grouped_notes = True
            return ref_content 
        return f'<ref name="{ref_name}" />'
    
    def _format_datapoint(self, datapoint: DataPoint, exoplanet_name: str) -> str:
        """Formate un DataPoint pour l'affichage dans l'article"""
        if not datapoint or not datapoint.value:
            return ""
            
        # Essayer de convertir la valeur en nombre si possible
        try:
            value = float(datapoint.value)
            value_str = self.format_utils.format_numeric_value(value)
        except (ValueError, TypeError):
            # Si la conversion échoue, utiliser la valeur telle quelle
            value_str = str(datapoint.value)
        
        if datapoint.reference:
            # Standardized ref_name derivation
            ref_name = str(datapoint.reference.source.value) if hasattr(datapoint.reference.source, 'value') else str(datapoint.reference.source)
            # Pass templates and exoplanet name to to_wiki_ref
            ref_content_full = datapoint.reference.to_wiki_ref(self.template_refs, exoplanet_name) 
            return f"{value_str} {self._add_reference(ref_name, ref_content_full)}"
            
        return value_str
    
    def generate_infobox_exoplanet(self, exoplanet: Exoplanet) -> str:
        """
        Génère l'infobox pour une exoplanète, conforme au modèle Wikipédia fourni, sans afficher les unités/notes si la valeur principale est absente
        """
        def val(attr):
            return getattr(exoplanet, attr).value if getattr(exoplanet, attr) and hasattr(getattr(exoplanet, attr), 'value') else None
        def unit(attr):
            return getattr(exoplanet, attr).unit if getattr(exoplanet, attr) and hasattr(getattr(exoplanet, attr), 'unit') and getattr(exoplanet, attr).unit else None
        def notes(attr):
            datapoint = getattr(exoplanet, attr, None)
            if not datapoint or not hasattr(datapoint, 'reference') or not datapoint.reference:
                return None
            
            ref = datapoint.reference
            # Ensure ref.source and ref.to_wiki_ref are available
            if not hasattr(ref, 'source') or not ref.source or not hasattr(ref, 'to_wiki_ref'):
                return None

            # ref_name should be like "NasaGov", "EPE", from ref.source.value
            # It's crucial that ref.source has a 'value' attribute if it's an Enum or similar.
            # Assuming ref.source.value gives the string name for the ref.
            ref_name = str(ref.source.value) if hasattr(ref.source, 'value') else str(ref.source)
            
            # Pass templates and exoplanet name to to_wiki_ref
            ref_content_full = ref.to_wiki_ref(self.template_refs, exoplanet.name)

            if ref_content_full:
                # self._add_reference will handle the logic of first vs. subsequent use
                return self._add_reference(ref_name, ref_content_full)
            return None

        def add_field(label, attr): # Removed predefined_default_unit_for_field from signature
            datapoint = getattr(exoplanet, attr, None)
            if not datapoint or not datapoint.value:
                return ""
                
            s = ""
            value_str = self.format_utils.format_datapoint(datapoint, exoplanet.name, self.template_refs, self._add_reference)
            if value_str:
                s += f" | {label} = {value_str}\n"
                
                actual_unit = unit(attr)
                expected_default_unit = self.FIELD_DEFAULT_UNITS.get(label)

                if actual_unit:
                    if expected_default_unit and actual_unit == expected_default_unit:
                        pass  # Omit unit line: actual unit is same as predefined default
                    else:
                        # Add unit line: actual unit is different, or no predefined default for this field
                        s += f" | {label} unité = {actual_unit}\n"
                # If actual_unit is None, no unit line is printed.
            return s

        # REMOVED: self._used_refs = set() # This was resetting global tracking

        infobox = f"{{{{Infobox Exoplanète\n"
        infobox += f" | nom = {exoplanet.name}\n"
        infobox += " | image = \n | légende = \n"
        # Étoile
        infobox += add_field("étoile", "host_star") # No default unit typically
        infobox += add_field("époque étoile", "star_epoch") # No default unit
        infobox += add_field("ascension droite", "right_ascension") # No default unit
        infobox += add_field("déclinaison", "declination") # No default unit
        infobox += add_field("distance", "distance") # Default is 'pc' from map
        infobox += add_field("constellation", "constellation") # No default unit
        # Add "carte UAI" here, assuming exoplanet.iau_constellation_map holds the image filename
        if hasattr(exoplanet, 'iau_constellation_map') and exoplanet.iau_constellation_map:
            infobox += f" | carte = {exoplanet.iau_constellation_map}\n"
        infobox += add_field("type spectral", "spectral_type") # No default unit
        infobox += add_field("magnitude apparente", "apparent_magnitude") # No default unit
        # Planète
        infobox += f" | type = {self._get_planet_type(exoplanet)}\n"
        # Caractéristiques orbitales
        infobox += add_field("demi-grand axe", "semi_major_axis") # Default 'ua'
        infobox += add_field("périastre", "periastron") # Default 'ua'
        infobox += add_field("apoastre", "apoastron") # Default 'ua'
        infobox += add_field("excentricité", "eccentricity") # No default unit
        infobox += add_field("période", "orbital_period") # Default 'j'
        infobox += add_field("distance angulaire", "angular_distance") # No default unit (mas, etc.)
        infobox += add_field("t_peri", "periastron_time") # No default unit
        infobox += add_field("inclinaison", "inclination") # Default '°'
        infobox += add_field("arg_péri", "argument_of_periastron") # Default '°'
        infobox += add_field("époque", "epoch") # No default unit
        # Caractéristiques physiques
        infobox += add_field("masse", "mass") # Default 'M_J'
        infobox += add_field("masse minimale", "minimum_mass") # Default 'M_J'
        infobox += add_field("rayon", "radius") # Default 'R_J'
        infobox += add_field("masse volumique", "density") # Default 'kg/m³'
        infobox += add_field("gravité", "gravity") # Default 'm/s²'
        infobox += add_field("période de rotation", "rotation_period") # Default 'h'
        infobox += add_field("température", "temperature") # Default 'K'
        infobox += add_field("albedo_bond", "bond_albedo") # No default unit
        # Atmosphère
        infobox += add_field("pression", "pressure") # No default unit (bar, atm, etc.)
        infobox += add_field("composition", "composition") # No default unit
        infobox += add_field("vitesse des vents", "wind_speed") # No default unit (m/s, km/h)
        # Découverte
        infobox += add_field("découvreurs", "discoverers") # No default unit
        infobox += add_field("programme", "discovery_program") # No default unit
        infobox += add_field("méthode", "discovery_method") # No default unit
        infobox += add_field("date", "discovery_date") # No default unit
        infobox += add_field("lieu", "discovery_location") # No default unit
        infobox += add_field("prédécouverte", "pre_discovery") # No default unit
        infobox += add_field("détection", "detection_method") # No default unit
        infobox += add_field("statut", "status") # No default unit
        # Autres noms
        other_names_str = ", ".join(exoplanet.other_names) if exoplanet.other_names else None
        if other_names_str:
            infobox += f" | autres noms = {other_names_str}\n"
        infobox += "}}"
        return infobox
    
    def _get_planet_type(self, exoplanet: Exoplanet) -> str:
        """
        Détermine le type de planète en fonction de ses caractéristiques physiques
        """
        mass_value = exoplanet.mass.value if exoplanet.mass and exoplanet.mass.value else None
        radius_value = exoplanet.radius.value if exoplanet.radius and exoplanet.radius.value else None
        temp_value = exoplanet.temperature.value if exoplanet.temperature and exoplanet.temperature.value else None

        # Classification des planètes gazeuses
        if mass_value and mass_value >= 1:  # Masse >= 1 M_J
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
        elif radius_value and radius_value >= 0.8:  # Rayon >= 0.8 R_J
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
        elif mass_value and mass_value < 1:  # Masse < 1 M_J
            if radius_value:
                if radius_value >= 1.5:
                    return "Super-Terre"
                elif radius_value >= 0.8:
                    return "Planète de dimensions terrestres"
                else:
                    return "Sous-Terre"
            else:
                return "Planète tellurique"

        # Cas par défaut
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

    # Chemin du fichier : astro/wiki/ref_utils.py

    def _format_references_section(self) -> str:
        """
        Génère la section "Notes et références" avec les sous-sections
        "Notes" et "Références". The "Notes" subsection is conditional.
        """
        notes_section = ""
        if self._has_grouped_notes:
            notes_section = """=== Notes ===
{{références|groupe="note"}}
"""
        
        return f"""
== Notes et références ==
{notes_section}
=== Références ===
{{Références}}
"""

    def generate_article_content(self, exoplanet: Exoplanet) -> str:
        """Génère le contenu de l'article Wikipedia"""
        # Réinitialiser les références pour chaque nouvel article
        self._used_refs = set()
        self._has_grouped_notes = False # Reset for the current article
        
        planet_type = self._get_planet_type(exoplanet)
        # Generate introduction sentence
        introduction = self.introduction_generator.generate_introduction(exoplanet)
        # Generate categories
        categories = self.category_generator.generate_categories(exoplanet)

        content = f"""{{{{Ébauche|exoplanète|}}}}

{self.generate_infobox_exoplanet(exoplanet)}

{introduction}

== Caractéristiques ==
Cette [[exoplanète]] est un [[{planet_type}]] {self._get_planet_description(exoplanet)}. Elle orbite à {{{{unité|{self.format_utils.format_datapoint(exoplanet.semi_major_axis, exoplanet.name, self.template_refs, self._add_reference)}|[[unité astronomique|unités astronomiques]]}}}} de son étoile{self.comparison_utils.get_orbital_comparison(exoplanet)}.

== Découverte ==
Cette planète a été découverte en {self.format_utils.format_year_field_with_ref(exoplanet.discovery_date, exoplanet.name, self.template_refs, self._add_reference)} par la méthode de {self.format_utils.format_datapoint(exoplanet.discovery_method, exoplanet.name, self.template_refs, self._add_reference)}.

{self._format_references_section()}

{{{{portail|astronomie|exoplanètes}}}}

{categories}
"""
        return content
    
    def _generate_introduction_sentence(self, exoplanet: Exoplanet) -> str:
        """Génère la phrase d'introduction pour l'article."""
        
        star_name_formatted = ""
        if exoplanet.host_star and exoplanet.host_star.value:
            # If host_star is a DataPoint, format it. Otherwise, use its value directly.
            # This assumes host_star could be a simple string or a DataPoint.
            # For the intro, we might not want references on the star name itself.
            if isinstance(exoplanet.host_star, DataPoint):
                 # If we want to use _format_datapoint, it now needs exoplanet_name
                 # star_name_formatted = self._format_datapoint(exoplanet.host_star, exoplanet.name)
                 # However, for linking a star name, simpler formatting is usually better.
                 star_name = exoplanet.host_star.value
                 star_name_formatted = f"[[{star_name}]]"
            else: # Assuming it's a direct value like string
                star_name = str(exoplanet.host_star.value) # Ensure it's a string
                star_name_formatted = f"[[{star_name}]]"
        else:
            star_name_formatted = "son étoile hôte"

        # Use _get_star_description for additional details about the star
        star_details = self.star_utils.get_star_description(exoplanet) 

        # Construct constellation part if available
        constellation_part = ""
        if exoplanet.constellation and exoplanet.constellation.value:
            constellation_name = exoplanet.constellation.value
            constellation_part = f" dans la [[constellation]] de [[{constellation_name}]]"
            # If constellation itself has a reference via _format_datapoint(exoplanet.constellation), 
            # it would be complex. Usually, constellation is just a name.

        intro = f"'''{{{{nobr|{exoplanet.name}}}}}''' est une [[exoplanète]] en [[orbite]] autour de {{{{nobr|{star_name_formatted}}}}}, {star_details}{constellation_part}."
        return intro

    def _get_planet_description(self, exoplanet: Exoplanet) -> str:
        """
        Génère une description de la planète basée sur ses caractéristiques physiques
        """
        mass_comparison = self.comparison_utils.get_mass_comparison(exoplanet)
        radius_comparison = self.comparison_utils.get_radius_comparison(exoplanet)
        
        description_parts = []
        if mass_comparison:
            description_parts.append(mass_comparison)
        if radius_comparison:
            description_parts.append(radius_comparison)
            
        if description_parts:
            return ", ".join(description_parts)
        return ""

    def _format_references(self, exoplanet: Exoplanet) -> str:
        """
        Génère la section des références
        """
        refs = self._get_used_references(exoplanet)
        if not refs:
            return ""
            
        ref_section = "== Notes et références ==\n{{Références}}\n"
        return ref_section

    def generate_article(self, exoplanet: Exoplanet) -> str:
        """
        Génère l'article complet pour une exoplanète
        """
        return self.generate_article_content(exoplanet) 