# src/utils/wikipedia_generator.py
from typing import Dict, List, Optional, Set
from src.models.exoplanet import Exoplanet
from src.models.reference import SourceType, DataPoint
import datetime
import locale

class WikipediaGenerator:
    """
    Classe pour générer le contenu wikitexte des articles d'exoplanètes
    """
    
    def __init__(self):
        self.template_refs = {
            'nasa': "{{Lien web |langue=en |nom1=NasaGov |titre={title} |url=https://science.nasa.gov/exoplanet-catalog/{id}/ |site=science.nasa.gov |date=2024-11-1 |consulté le=2025-1-3 }}",
            'exoplanet_eu': "{{Lien web |langue=en |nom1=EPE |titre={title} |url=https://exoplanet.eu/catalog/{id}/ |site=exoplanet.eu |date=2024-8-1 |consulté le=2025-1-3 }}",
            'open_exoplanet': "{{Lien web |langue=en |nom1=OEC |titre={title} |url=https://github.com/OpenExoplanetCatalogue/open_exoplanet_catalogue |site=Open Exoplanet Catalogue |date=2024-1-1 |consulté le=2025-1-3 }}",
            'article': "{{Article |langue= |auteur= |titre= |périodique= |année= |volume= |numéro= |pages= |lire en ligne= |consulté le= }}",
            'ouvrage': "{{Ouvrage |langue= |auteur= |titre= |éditeur= |année= |pages totales= |passage= |isbn= |lire en ligne= |consulté le= }}"
        }
        self._used_refs = set()
        locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
    
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
            return ref_content # ref_content is already the full <ref name="NasaGov">{{...}}</ref>
        return f'<ref name="{ref_name}" />'
    
    def _format_datapoint(self, datapoint: DataPoint) -> str:
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
            ref_name = "EPE" if datapoint.reference.source == SourceType.EPE else "NasaGov" if datapoint.reference.source == SourceType.NASA else "OEC"
            ref_content = datapoint.reference.to_wiki_ref()
            return f"{value_str} {self._add_reference(ref_name, ref_content)}"
            
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
            
            # ref.to_wiki_ref() is expected to return the full reference string for the first use,
            # e.g., <ref name="NasaGov">{{Lien web...}}</ref>
            ref_content_full = ref.to_wiki_ref()

            if ref_content_full:
                # self._add_reference will handle the logic of first vs. subsequent use
                return self._add_reference(ref_name, ref_content_full)
            return None

        def add_field(label, attr, default_unit=None):
            v = val(attr)
            s = ""
            if v is not None and v != "":
                s += f" | {label} = {v}\n"
                u = unit(attr)
                n = notes(attr)
                if u:
                    s += f" | {label} unité = {u}\n"
                elif default_unit:
                    s += f" | {label} unité = {default_unit}\n"
                if n:
                    s += f" | {label} notes = {n}\n"
            return s

        # Réinitialiser les références utilisées pour chaque nouvelle exoplanète
        self._used_refs = set()

        infobox = f"{{{{Infobox Exoplanète\n"
        infobox += f" | nom = {exoplanet.name}\n"
        infobox += " | image = \n | légende = \n"
        # Étoile
        infobox += add_field("étoile", "host_star")
        infobox += add_field("époque étoile", "star_epoch")
        infobox += add_field("ascension droite", "right_ascension")
        infobox += add_field("déclinaison", "declination")
        infobox += add_field("distance", "distance", "pc")
        infobox += add_field("constellation", "constellation")
        # Add "carte UAI" here, assuming exoplanet.iau_constellation_map holds the image filename
        if hasattr(exoplanet, 'iau_constellation_map') and exoplanet.iau_constellation_map:
            infobox += f" | carte = {exoplanet.iau_constellation_map}\n"
        infobox += add_field("type spectral", "spectral_type")
        infobox += add_field("magnitude apparente", "apparent_magnitude")
        # Planète
        infobox += f" | type = {self._get_planet_type(exoplanet)}\n"
        # Caractéristiques orbitales
        infobox += add_field("demi-grand axe", "semi_major_axis", "ua")
        infobox += add_field("périastre", "periastron", "ua")
        infobox += add_field("apoastre", "apoastron", "ua")
        infobox += add_field("excentricité", "eccentricity")
        infobox += add_field("période", "orbital_period", "j")
        infobox += add_field("distance angulaire", "angular_distance")
        infobox += add_field("t_peri", "periastron_time")
        infobox += add_field("inclinaison", "inclination", "°")
        infobox += add_field("arg_péri", "argument_of_periastron", "°")
        infobox += add_field("époque", "epoch")
        # Caractéristiques physiques
        infobox += add_field("masse", "mass", "M_J")
        infobox += add_field("masse minimale", "minimum_mass", "M_J")
        infobox += add_field("rayon", "radius", "R_J")
        infobox += add_field("masse volumique", "density", "kg/m³")
        infobox += add_field("gravité", "gravity", "m/s²")
        infobox += add_field("période de rotation", "rotation_period", "h")
        infobox += add_field("température", "temperature", "K")
        infobox += add_field("albedo_bond", "bond_albedo")
        # Atmosphère
        infobox += add_field("pression", "pressure")
        infobox += add_field("composition", "composition")
        infobox += add_field("vitesse des vents", "wind_speed")
        # Découverte
        infobox += add_field("découvreurs", "discoverers")
        infobox += add_field("programme", "discovery_program")
        infobox += add_field("méthode", "discovery_method")
        infobox += add_field("date", "discovery_date")
        infobox += add_field("lieu", "discovery_location")
        infobox += add_field("prédécouverte", "pre_discovery")
        infobox += add_field("détection", "detection_method")
        infobox += add_field("statut", "status")
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
        "Notes" et "Références".
        """
        return """
== Notes et références ==
=== Notes ===
{{références|groupe="note"}}

=== Références ===
{{Références}}
"""

    def generate_article_content(self, exoplanet: Exoplanet) -> str:
        """Génère le contenu de l'article Wikipedia"""
        # Réinitialiser les références pour chaque nouvel article
        self._used_refs = set()
        
        planet_type = self._get_planet_type(exoplanet)
        # Generate introduction sentence
        introduction = self._generate_introduction_sentence(exoplanet)
        # Generate categories
        categories = self._generate_categories(exoplanet)

        content = f"""{{{{Ébauche|exoplanète|}}}}

{self.generate_infobox_exoplanet(exoplanet)}

{introduction}

== Caractéristiques ==
Cette [[exoplanète]] est un [[{planet_type}]] {self._get_planet_description(exoplanet)}. Elle orbite à {{{{unité|{self._format_datapoint(exoplanet.semi_major_axis)}|[[unité astronomique|unités astronomiques]]}}}} de son étoile{self._get_orbital_comparison(exoplanet)}.

== Découverte ==
Cette planète a été découverte en {self._format_datapoint(exoplanet.discovery_date)} par la méthode de {self._format_datapoint(exoplanet.discovery_method)}.

{self._format_references_section()}

{{{{portail|astronomie|exoplanètes}}}}

{categories}
"""
        return content
    
    def _generate_introduction_sentence(self, exoplanet: Exoplanet) -> str:
        """Génère la phrase d'introduction pour l'article."""
        
        star_name_formatted = ""
        if exoplanet.host_star and exoplanet.host_star.value:
            # Assuming host_star.value is the name, and we want to link it.
            # _format_datapoint might add references, which is unusual for a direct star link in intro.
            # For now, let's just use the value. If it's a DataPoint, we need just the value.
            star_name = exoplanet.host_star.value
            star_name_formatted = f"[[{star_name}]]" # Simple link to the star name
            # If host_star is a DataPoint itself and has a reference for its name,
            # _format_datapoint(exoplanet.host_star) would include that.
            # For an intro, usually, we don't ref the star name itself, but its properties.
            # Using exoplanet.host_star.value directly is safer if it's just a name.
        else:
            star_name_formatted = "son étoile hôte"

        # Use _get_star_description for additional details about the star
        star_details = self._get_star_description(exoplanet) # This already fetches spectral type, distance, etc.

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

    def _get_size_comparison(self, exoplanet: Exoplanet) -> str:
        """
        Génère une comparaison de taille avec Jupiter ou la Terre
        """
        mass_value = exoplanet.mass.value if exoplanet.mass and exoplanet.mass.value else None
        if mass_value:
            if mass_value > 10:
                return f"environ {self._format_numeric_value(mass_value/317.8, 1)} fois plus massif que [[Jupiter (planète)|Jupiter]]"
            else:
                return f"environ {self._format_numeric_value(mass_value, 1)} fois plus massif que la [[Terre]]"
        return ""
    
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
        Génère une description de l'étoile hôte
        """
        desc = []
        if exoplanet.spectral_type and exoplanet.spectral_type.value:
            desc.append(f"une [[étoile]] de type spectral [[{exoplanet.spectral_type.value}]]")
        if exoplanet.distance and exoplanet.distance.value:
            desc.append(f"située à {self._format_datapoint(exoplanet.distance)} [[parsec|pc]] de la [[Terre]]")
        if exoplanet.apparent_magnitude and exoplanet.apparent_magnitude.value:
            desc.append(f"d'une [[magnitude apparente]] de {self._format_datapoint(exoplanet.apparent_magnitude)}")
        
        return " ".join(desc) if desc else "une étoile"
    
    def _get_planet_description(self, exoplanet: Exoplanet) -> str:
        """
        Génère une description de la planète
        """
        desc = []
        if exoplanet.mass and exoplanet.mass.value:
            desc.append(self._get_size_comparison(exoplanet))
        if exoplanet.radius and exoplanet.radius.value:
            desc.append(f"d'un rayon de {self._format_datapoint(exoplanet.radius)} [[rayon jovien|R_J]]")
        if exoplanet.temperature and exoplanet.temperature.value:
            desc.append(f"avec une température de {self._format_datapoint(exoplanet.temperature)} [[kelvin|K]]")
        
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