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
        self._has_grouped_notes = False # Initialize the new flag
        locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
        self.format_utils = FormatUtils()
        self.comparison_utils = ComparisonUtils(self.format_utils)
        self.reference_utils = ReferenceUtils()
        self.infobox_generator = InfoboxGenerator(self.reference_utils)
        self.introduction_generator = IntroductionGenerator(self.comparison_utils, self.format_utils)
        self.category_generator = CategoryGenerator()
        self.star_utils = StarUtils(self.format_utils)

    def _parsecs_to_lightyears(self, parsecs: float) -> float:
        """Convertit les parsecs en années-lumière."""
        return parsecs * 3.26156
    
    def _format_numeric_value(self, value: Optional[float], precision: int = 2) -> str:
        """
        Formate une valeur numérique avec le format français
        """
        if value is None:
            return ""
        return locale.format_string(f"%.{precision}f", value, grouping=True)
    
    def _format_value_with_unit(self, value: Optional[float], unit: str, precision: int = 2) -> str:
        """
        Formate une valeur avec son unité, gère les valeurs None
        """
        if value is None:
            return ""
        return f"{self._format_numeric_value(value, precision)} {unit}"
    
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
            value_str = self._format_numeric_value(value)
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
            v = val(attr)
            s = ""
            if v is not None and v != "":
                s += f" | {label} = {v}\n"
                
                actual_unit = unit(attr)
                n = notes(attr)
                expected_default_unit = self.FIELD_DEFAULT_UNITS.get(label)

                if actual_unit:
                    if expected_default_unit and actual_unit == expected_default_unit:
                        pass  # Omit unit line: actual unit is same as predefined default
                    else:
                        # Add unit line: actual unit is different, or no predefined default for this field
                        s += f" | {label} unité = {actual_unit}\n"
                # If actual_unit is None, no unit line is printed.
                
                if n:
                    s += f" | {label} notes = {n}\n"
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
Cette [[exoplanète]] est un [[{planet_type}]] {self._get_planet_description(exoplanet)}. Elle orbite à {{{{unité|{self._format_datapoint(exoplanet.semi_major_axis, exoplanet.name)}|[[unité astronomique|unités astronomiques]]}}}} de son étoile{self._get_orbital_comparison(exoplanet)}.

== Découverte ==
Cette planète a été découverte en {self._format_year_field(exoplanet.discovery_date, exoplanet.name)} par la méthode de {self._format_datapoint(exoplanet.discovery_method, exoplanet.name)}.

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

    def _generate_categories(self, exoplanet: Exoplanet) -> str:
        """Génère les catégories pour l'article."""
        categories = []
        planet_type = self._get_planet_type(exoplanet)
        if planet_type:
            categories.append(f"[[Catégorie:{planet_type}]]")

        if exoplanet.discovery_date and exoplanet.discovery_date.value:
            try:
                # Assuming discovery_date.value is a string like "YYYY-MM-DD" or "YYYY"
                year = str(exoplanet.discovery_date.value).split('-')[0]
                if year.isdigit() and len(year) == 4:
                    categories.append(f"[[Catégorie:Exoplanète découverte en {year}]]")
            except: #pylint: disable=bare-except
                pass # Ignore if year parsing fails

        if exoplanet.discovery_method and exoplanet.discovery_method.value:
            method = str(exoplanet.discovery_method.value)
            # Simple mapping, can be expanded
            method_map = {
                "Transit": "par transit",
                "Vitesse radiale": "par vitesse radiale",
                # Add other common methods
            }
            if method in method_map:
                 categories.append(f"[[Catégorie:Exoplanète découverte {method_map[method]}]]")
            else:
                 categories.append(f"[[Catégorie:Exoplanète découverte par {method}]]")


        if exoplanet.spectral_type and exoplanet.spectral_type.value:
            spectral_type_full = str(exoplanet.spectral_type.value)
            # Extract the main star type (e.g., G from G5V)
            if len(spectral_type_full) > 0:
                spectral_class = spectral_type_full[0].upper()
                if spectral_class in "OBAFGKM":
                    categories.append(f"[[Catégorie:Exoplanète en orbite autour d'une étoile de type {spectral_class}]]")
        
        return "\n".join(categories)

    def _format_year_field(self, datapoint: Optional[DataPoint], exoplanet_name: str) -> str:
        """
        Formats a DataPoint assumed to represent a year or a full date.
        Years are formatted as plain integers. Full dates are returned as strings.
        Includes reference if available.
        """
        if not datapoint or datapoint.value is None: # Allow datapoint.value to be 0
            return ""

        value_str = ""
        # Ensure we are working with a string version of the value first
        raw_value_str = str(datapoint.value)

        # Attempt to clean known problematic formatting for years
        # Remove common thousands separators (French non-breaking space, regular space)
        # Replace comma decimal with period for robust float conversion
        cleaned_value_str = raw_value_str.replace("\u202F", "").replace(" ", "")
        if ',' in cleaned_value_str and '.' not in cleaned_value_str: # Handle "2011,00" -> "2011.00"
            cleaned_value_str = cleaned_value_str.replace(",", ".")

        try:
            numeric_value = float(cleaned_value_str)
            if numeric_value.is_integer():
                # Check for plausible year range
                year_int = int(numeric_value)
                if 1000 <= year_int <= (datetime.datetime.now().year + 10): # Allow some future years
                    value_str = str(year_int) # "2011"
                else:
                    value_str = raw_value_str # Not a plausible year, use original
            else:
                # It's a float but not an integer (e.g. 2011.5), use original raw string
                value_str = raw_value_str
        except (ValueError, TypeError):
            # Not a number (e.g. "2011-2012", "Unknown", "vers 2011"), use original raw string
            value_str = raw_value_str

        if datapoint.reference:
            ref_name = str(datapoint.reference.source.value) if hasattr(datapoint.reference.source, 'value') else str(datapoint.reference.source)
            # Pass templates and exoplanet name to to_wiki_ref
            ref_content_full = datapoint.reference.to_wiki_ref(self.template_refs, exoplanet_name)
            if ref_content_full:
                 return f"{value_str} {self._add_reference(ref_name, ref_content_full)}"
        
        return value_str
    R_JUPITER_IN_EARTH_RADII = 11.209  # Rayon de Jupiter en rayons terrestres
    M_JUPITER_IN_EARTH_MASSES = 317.8  # Masse de Jupiter en masses terrestres
    
    def _get_radius_comparison(self, exoplanet: Exoplanet) -> str:
        """
        Génère une comparaison de rayon avec Jupiter ou la Terre.
        Le rayon de l'exoplanète (exoplanet.radius.value) est supposé être en rayons joviens (R_J).
        """
        if not exoplanet.radius or exoplanet.radius.value is None:
            return ""

        radius_rj = exoplanet.radius.value  # Rayon en rayons de Jupiter (R_J)

        # Seuils de similarité (par exemple, +/- 20% du rayon du corps de référence)
        SIMILARITY_MARGIN = 0.2  # Marge de 20%

        # Seuils pour Jupiter (le rayon de référence est 1 R_J)
        JUPITER_SIMILARITY_LOWER_RJ = 1.0 - SIMILARITY_MARGIN  # 0.8 R_J
        JUPITER_SIMILARITY_UPPER_RJ = 1.0 + SIMILARITY_MARGIN  # 1.2 R_J

        # Cas 1 : Comparaison prioritaire avec Jupiter
        if radius_rj >= JUPITER_SIMILARITY_LOWER_RJ:
            if radius_rj <= JUPITER_SIMILARITY_UPPER_RJ:  # Proche du rayon de Jupiter
                return "d'un rayon environ similaire à celui de [[Jupiter (planète)|Jupiter]]"
            else:  # Nettement plus grand que Jupiter
                return f"d'un rayon environ {self._format_numeric_value(radius_rj, 1)} fois celui de [[Jupiter (planète)|Jupiter]]"
        # Cas 2 : Comparaison avec la Terre (si radius_rj < JUPITER_SIMILARITY_LOWER_RJ)
        else:
            radius_re = radius_rj * self.R_JUPITER_IN_EARTH_RADII  # Conversion en rayons terrestres (R_E)

            # Seuils pour la Terre (le rayon de référence est 1 R_E)
            EARTH_SIMILARITY_LOWER_RE = 1.0 - SIMILARITY_MARGIN  # 0.8 R_E
            EARTH_SIMILARITY_UPPER_RE = 1.0 + SIMILARITY_MARGIN  # 1.2 R_E

            if radius_re >= EARTH_SIMILARITY_LOWER_RE and radius_re <= EARTH_SIMILARITY_UPPER_RE: # Proche du rayon de la Terre
                return "d'un rayon environ similaire à celui de la [[Terre]]"
            elif radius_re > EARTH_SIMILARITY_UPPER_RE:  # Nettement plus grand que la Terre
                return f"d'un rayon environ {self._format_numeric_value(radius_re, 1)} fois celui de la [[Terre]]"
            elif radius_re > 0:  # Plus petit que la Terre (et rayon positif)
                                 # ex: 0.5 R_E -> 1/0.5 = 2 fois plus petit
                return f"d'un rayon environ {self._format_numeric_value(1 / radius_re, 1)} fois plus petit que celui de la [[Terre]]"
            else:
                # Cas où le rayon est nul ou négatif
                return ""
            
    def _get_size_comparison(self, exoplanet) -> str: # exoplanet: Exoplanet (type hint)
        """
        Génère une comparaison de masse avec Jupiter ou la Terre.
        La masse de l'exoplanète (exoplanet.mass.value) est supposée être en masses joviennes.
        """
        if not exoplanet.mass or exoplanet.mass.value is None:
            return ""

        mass_mj = exoplanet.mass.value  # Masse en masses de Jupiter (MJ)

        # Seuils de similarité (par exemple, +/- 20% de la masse du corps de référence)
        # Une planète est "similaire" si sa masse est dans [MASSE_REF * (1-MARGE), MASSE_REF * (1+MARGE)]
        SIMILARITY_MARGIN = 0.2  # Marge de 20%

        # Seuils pour Jupiter (la masse de référence est 1 MJ)
        JUPITER_SIMILARITY_LOWER_MJ = 1.0 - SIMILARITY_MARGIN  # 0.8 MJ
        JUPITER_SIMILARITY_UPPER_MJ = 1.0 + SIMILARITY_MARGIN  # 1.2 MJ

        # Cas 1 : Comparaison prioritaire avec Jupiter
        # Si la masse de l'exoplanète est supérieure ou égale à JUPITER_SIMILARITY_LOWER_MJ
        if mass_mj >= JUPITER_SIMILARITY_LOWER_MJ:
            if mass_mj <= JUPITER_SIMILARITY_UPPER_MJ:  # Proche de la masse de Jupiter (ex: 0.8 MJ à 1.2 MJ)
                return "environ la même masse que [[Jupiter (planète)|Jupiter]]"
            else:  # Nettement plus massive que Jupiter (ex: > 1.2 MJ)
                return f"environ {self._format_numeric_value(mass_mj, 1)} fois plus massif que [[Jupiter (planète)|Jupiter]]"
        # Cas 2 : Comparaison avec la Terre (si mass_mj < JUPITER_SIMILARITY_LOWER_MJ, ex: < 0.8 MJ)
        else:
            mass_me = mass_mj * self.M_JUPITER_IN_EARTH_MASSES  # Conversion en masses terrestres (ME)

            # Seuils pour la Terre (la masse de référence est 1 ME)
            EARTH_SIMILARITY_LOWER_ME = 1.0 - SIMILARITY_MARGIN  # 0.8 ME
            EARTH_SIMILARITY_UPPER_ME = 1.0 + SIMILARITY_MARGIN  # 1.2 ME

            if mass_me >= EARTH_SIMILARITY_LOWER_ME and mass_me <= EARTH_SIMILARITY_UPPER_ME: # Proche de la masse de la Terre
                return "environ la même masse que la [[Terre]]"
            elif mass_me > EARTH_SIMILARITY_UPPER_ME:  # Nettement plus massive que la Terre
                return f"environ {self._format_numeric_value(mass_me, 1)} fois plus massif que la [[Terre]]"
            elif mass_me > 0:  # Moins massive que la Terre (et masse positive)
                               # ex: 0.5 ME -> 1/0.5 = 2 fois moins massif
                # Gérer les cas où 1/mass_me devient très grand, c'est mathématiquement correct.
                return f"environ {self._format_numeric_value(1 / mass_me, 1)} fois moins massif que la [[Terre]]"
            else:
                # Cas où la masse est nulle ou négative (ne devrait pas arriver si mass_mj > 0)
                return "" # Ou un message approprié comme "Masse non positive"
            
    def _get_orbital_comparison(self, exoplanet: Exoplanet) -> str:
        """
        Génère une comparaison orbitale avec le système solaire
        """
        sma = exoplanet.semi_major_axis.value if exoplanet.semi_major_axis and exoplanet.semi_major_axis.value else None
        if sma:
            if sma < 0.1:
                return ", une distance comparable à celle de [[Mercure (planète)|Mercure]] dans le [[système solaire]]"
            elif sma < 1:
                return ", une distance comparable à celle de [[Vénus (planète)|Vénus]] dans le [[système solaire]]"
            elif sma < 2:
                return ", une distance comparable à celle de [[Mars (planète)|Mars]] dans le [[système solaire]]"
            else:
                return ", une distance comparable à la [[ceinture d'astéroïdes]] (entre [[Mars (planète)|Mars]] et Jupiter) dans le [[système solaire]]"
        return ""
    
    def _get_star_description(self, exoplanet: Exoplanet) -> str:
        """
        Génère une description de l'étoile hôte avec un lien spécifique selon le type spectral.
        """
        desc = []

        if exoplanet.spectral_type and exoplanet.spectral_type.value:
            spectral = exoplanet.spectral_type.value
            link = self._get_spectral_type_link(spectral)
            if link:
                desc.append(f"une [[{link}|étoile de type spectral {spectral}]]")
            else:
                desc.append(f"une [[étoile]] de type spectral [[{spectral}]]")

        if exoplanet.distance and exoplanet.distance.value is not None:
            try:
                pc_value = float(exoplanet.distance.value)
                ly_value = self._parsecs_to_lightyears(pc_value)
                formatted_ly_value = self._format_numeric_value(ly_value, precision=0)
                formatted_pc_value_with_ref = self._format_datapoint(exoplanet.distance, exoplanet.name)
                distance_str = f"située à {formatted_ly_value} [[année-lumière|années-lumière]] ({formatted_pc_value_with_ref} [[parsec|pc]]) de la [[Terre]]"
                desc.append(distance_str)
            except (ValueError, TypeError):
                original_distance_str = self._format_datapoint(exoplanet.distance, exoplanet.name)
                if original_distance_str:
                    desc.append(f"située à {original_distance_str} [[parsec|pc]] de la [[Terre]]")

        if exoplanet.apparent_magnitude and exoplanet.apparent_magnitude.value:
            desc.append(f"d'une [[magnitude apparente]] de {self._format_datapoint(exoplanet.apparent_magnitude, exoplanet.name)}")

        return " ".join(desc) if desc else "une étoile"

    def _parse_spectral_type(self, spectral_type: str) -> tuple[str, Optional[str]]:
        """
        Extrait la classe spectrale et la classe de luminosité d'un type spectral complet.
        Exemple : 'G2V' => ('G', 'V')
        """
        match = re.match(r'^([OBAFGKMLTYDCSP])\d?\.?\d*([IV]{1,3})?', spectral_type.upper())
        if not match:
            return spectral_type[0].upper(), None  # fallback
        return match.group(1), match.group(2)

    def _get_spectral_type_link(self, spectral_type: str) -> Optional[str]:
        """
        Associe un type spectral (classe + luminosité) à un lien Wikipédia pertinent.
        """
        main_class, luminosity_class = self._parse_spectral_type(spectral_type)

        # Mapping composite : (classe spectrale, classe de luminosité) => article Wikipédia
        mapping = {
            ("O", "V"): "Étoile_bleue_de_la_séquence_principale",
            ("B", "V"): "Étoile_bleue-blanche_de_la_séquence_principale",
            ("A", "V"): "Étoile_blanche_de_la_séquence_principale",
            ("F", "V"): "Étoile_blanc-jaune_de_la_séquence_principale",
            ("G", "V"): "Naine_jaune",
            ("K", "V"): "Naine_orangée",
            ("M", "V"): "Naine_rouge",
            ("L", "V"): "Naine_brune",
            ("T", "V"): "Naine_brune",
            ("Y", "V"): "Naine_brune",
            ("D", None): "Naine_blanche",
            ("C", None): "Étoile_carbone",
            ("S", None): "Étoile_de_type_S",
            ("G", "III"): "Géante_jaune",
            ("M", "III"): "Géante_rouge",
            ("K", "III"): "Géante_orangée",
            ("F", "III"): "Géante_blanc-jaune"
        }

        return mapping.get((main_class, luminosity_class)) or mapping.get((main_class, None))

    def _get_planet_description(self, exoplanet: Exoplanet) -> str:
        """
        Génère une description de la planète
        """
        desc = []
        
        # Comparaison de masse
        if exoplanet.mass and exoplanet.mass.value is not None: # Vérifier explicitement None
            mass_comparison = self._get_size_comparison(exoplanet)
            if mass_comparison: # Ajouter seulement si la comparaison retourne quelque chose
                desc.append(mass_comparison)
        
        # Comparaison de rayon (NOUVEAU)
        if exoplanet.radius and exoplanet.radius.value is not None: # Vérifier explicitement None
            radius_comparison = self._get_radius_comparison(exoplanet)
            if radius_comparison: # Ajouter seulement si la comparaison retourne quelque chose
                desc.append(radius_comparison)
            
        if exoplanet.temperature and exoplanet.temperature.value is not None: # Vérifier explicitement None
            temp_str = self._format_datapoint(exoplanet.temperature, exoplanet.name)
            if temp_str: # S'assurer que format_datapoint retourne quelque chose avant d'ajouter
                 desc.append(f"avec une température de surface estimée à {temp_str} [[kelvin|K]]")
        
        # Joindre les descriptions avec des virgules, mais gérer le cas d'une seule description.
        if not desc:
            return ""
        
        # Construction de la phrase finale
        # "Elle est {desc[0]}, {desc[1]} et {desc[2]}."
        # ou "Elle est {desc[0]} et {desc[1]}."
        # ou "Elle est {desc[0]}."

        if len(desc) == 1:
            return f"Elle est {desc[0]}."
        elif len(desc) > 1:
            # Joindre tous sauf le dernier avec ", " et ajouter " et " avant le dernier.
            return f"Elle est {', '.join(desc[:-1])} et {desc[-1]}."
        
        return "" # Ne devrait pas être atteint si desc n'est pas vide
    
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

    def generate_article(self, exoplanet: Exoplanet) -> str:
        """
        Génère l'article Wikipedia complet pour une exoplanète
        """
        # Réinitialiser les références pour le nouvel article
        self.reference_utils.reset_references()

        # Générer les différentes sections
        infobox = self.infobox_generator.generate_infobox(exoplanet)
        introduction = self.introduction_generator.generate_introduction(exoplanet)
        star_description = self.star_utils.get_star_description(exoplanet)
        categories = self.category_generator.generate_categories(exoplanet)
        references = self.reference_utils.format_references_section()

        # Assembler l'article
        article = f"{infobox}\n\n"
        article += f"{introduction}\n\n"
        
        if star_description:
            article += f"== Étoile hôte ==\n{star_description}\n\n"
            
        article += f"== Notes et références ==\n{references}\n\n"
        
        # Ajouter les catégories
        for category in categories:
            article += f"[[Catégorie:{category}]]\n"

        return article 