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
            'nasa': "{{Lien web |langue=en |nom1=NASA |titre={title} |url=https://science.nasa.gov/exoplanet-catalog/{id}/ |site=science.nasa.gov |date=2024-11-1 |consulté le=2025-1-3 }}",
            'exoplanet_eu': "{{Lien web |langue=en |nom1=EPE |titre={title} |url=https://exoplanet.eu/catalog/{id}/ |site=exoplanet.eu |date=2024-8-1 |consulté le=2025-1-3 }}",
            'open_exoplanet': "{{Lien web |langue=en |nom1=OEC |titre={title} |url=https://github.com/OpenExoplanetCatalogue/open_exoplanet_catalogue |site=Open Exoplanet Catalogue |date=2024-1-1 |consulté le=2025-1-3 }}"
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
        Ajoute une référence et retourne la balise de référence appropriée
        """
        if ref_name not in self._used_refs:
            self._used_refs.add(ref_name)
            return f'<ref name="{ref_name}">{ref_content}</ref>'
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
            ref = getattr(exoplanet, attr).reference if getattr(exoplanet, attr) and hasattr(getattr(exoplanet, attr), 'reference') else None
            if not ref or not hasattr(ref, 'to_wiki_ref'):
                return None
            
            # Vérifier si c'est la première occurrence de cette référence
            ref_name = ref.source.value
            
            if not hasattr(self, '_used_refs'):
                self._used_refs = set()
            
            if ref_name not in self._used_refs:
                self._used_refs.add(ref_name)
                return ref.to_wiki_ref()
            else:
                return f"<ref name=\"{ref_name}\" />"

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
        if not refs:
            refs.add("EPE")
            
        return list(refs)

    # Chemin du fichier : astro/wiki/ref_utils.py

    def _format_references_section(self, exoplanet: Exoplanet) -> str:
        """Génère la section Références"""

        reference_templates = {
            "NasaGov": (
                '<ref name="NasaGov">{{{{Lien web |langue=en |nom1=NasaGov |titre={name} |url=https://science.nasa.gov/exoplanet-catalog/{slug}/ '
                '|site=science.nasa.gov |date=2024-11-1 |consulté le=2025-1-3 }}}}</ref>'
            ),
            "EPE": (
                '<ref name="EPE">{{{{Lien web |langue=en |nom1=EPE |titre={name} |url=https://exoplanet.eu/catalog/{underscored}/ '
                '|site=exoplanet.eu |date=2024-8-1 |consulté le=2025-1-3 }}}}</ref>'
            ),
            "OEC": (
                '<ref name="OEC">{{{{Lien web |langue=en |nom1=OEC |titre={name} |url=https://www.openexoplanetcatalogue.com/planet/{name}/ '
                '|site=Open Exoplanet Catalogue |date=2024-8-1 |consulté le=2025-1-3 }}}}</ref>'
            ),
        }

        name = exoplanet.name
        slug = name.lower().replace(" ", "-")
        underscored = name.lower().replace(" ", "_")

        refs = []
        for ref_name in self._get_used_references(exoplanet):
            template = reference_templates.get(ref_name)
            if template:
                refs.append(template.format(name=name, slug=slug, underscored=underscored))

        return '\n'.join(refs) + '\n\n{{références}}'


    def generate_article_content(self, exoplanet: Exoplanet) -> str:
        """Génère le contenu de l'article Wikipedia"""
        # Réinitialiser les références pour chaque nouvel article
        self._used_refs = set()
        
        planet_type = self._get_planet_type(exoplanet)
        content = f"""{{{{Ébauche|exoplanète|}}}}

{self.generate_infobox_exoplanet(exoplanet)}

'''{{{{nobr|{exoplanet.name}}}}}''' est une [[planète]] en [[orbite]] autour de {{{{nobr|[[{self._format_datapoint(exoplanet.host_star)}]]}}}}, {self._get_star_description(exoplanet)}.

== Caractéristiques ==
Cette [[exoplanète]] est un [[{planet_type}]] {self._get_planet_description(exoplanet)}. Elle orbite à {{{{unité|{self._format_datapoint(exoplanet.semi_major_axis)}|[[unité astronomique|unités astronomiques]]}}}} de son étoile{self._get_orbital_comparison(exoplanet)}.

== Découverte ==
Cette planète a été découverte en {self._format_datapoint(exoplanet.discovery_date)} par la méthode de {self._format_datapoint(exoplanet.discovery_method)}.

== Références ==
{self._format_references_section(exoplanet)}

{{{{portail|astronomie|exoplanètes}}}}

[[Catégorie:{planet_type}]]
"""
        return content
    
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