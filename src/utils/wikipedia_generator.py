from typing import Dict, List, Optional
from src.models.exoplanet import Exoplanet
import datetime
from src.models.reference import SourceType

class WikipediaGenerator:
    """
    Classe pour générer le contenu wikitexte des articles d'exoplanètes
    """
    
    def __init__(self):
        self.template_refs = {
            'nasa': "{{Lien web |langue=en |nom1=NasaGov |titre={title} |url=https://science.nasa.gov/exoplanet-catalog/{id}/ |site=science.nasa.gov |date=2024-11-1 |consulté le=2025-1-3 }}",
            'exoplanet_eu': "{{Lien web |langue=en |nom1=EPE |titre={title} |url=https://exoplanet.eu/catalog/{id}/ |site=exoplanet.eu |date=2024-8-1 |consulté le=2025-1-3 }}",
            'open_exoplanet': "{{Lien web |langue=en |nom1=OEC |titre={title} |url=https://github.com/OpenExoplanetCatalogue/open_exoplanet_catalogue |site=Open Exoplanet Catalogue |date=2024-1-1 |consulté le=2025-1-3 }}"
        }
    
    def _format_value_with_unit(self, value: Optional[float], unit: str) -> str:
        """
        Formate une valeur avec son unité, gère les valeurs None
        """
        if value is None:
            return ""
        return f"{value} {unit}"
    
    def _get_reference(self, source: str, title: str, id: str) -> str:
        """
        Retourne la référence formatée pour une source donnée
        """
        template = self.template_refs.get(source, "")
        return template.format(title=title, id=id)
    
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
            return ref.to_wiki_ref() if ref and hasattr(ref, 'to_wiki_ref') else None

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
        if exoplanet.other_names:
            other_names_str = ", ".join([f"{k}: {v.value}" for k, v in exoplanet.other_names.items() if v.value])
            if other_names_str:
                infobox += f" | autres noms = {other_names_str}\n"
        infobox += "}}"
        return infobox
    
    def _get_planet_type(self, exoplanet: Exoplanet) -> str:
        """
        Détermine le type de planète en fonction de ses caractéristiques
        """
        mass_value = exoplanet.mass.value if exoplanet.mass and exoplanet.mass.value else None
        radius_value = exoplanet.radius.value if exoplanet.radius and exoplanet.radius.value else None

        if mass_value and mass_value > 10:
            return "Géante gazeuse"
        elif radius_value and radius_value > 2:
            return "Géante gazeuse"
        else:
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
                if value.reference.source == SourceType.NASA:
                    refs.add("NasaGov")
                elif value.reference.source == SourceType.EPE:
                    refs.add("EPE")
                elif value.reference.source == SourceType.OEP:
                    refs.add("OEC")
        
        # Si aucune référence n'a été trouvée, ajouter au moins EPE par défaut
        if not refs:
            refs.add("EPE")
            
        return list(refs)

    def _format_references_section(self, exoplanet: Exoplanet) -> str:
        """
        Génère la section Références avec les définitions des références utilisées
        """
        refs = self._get_used_references(exoplanet)
        refs_text = []
        if "EPE" in refs:
            refs_text.append(f'<ref name="EPE">{self._get_reference("exoplanet_eu", exoplanet.name, exoplanet.name.lower().replace(" ", "_"))}</ref>')
        if "NasaGov" in refs:
            refs_text.append(f'<ref name="NasaGov">{self._get_reference("nasa", exoplanet.name, exoplanet.name.lower().replace(" ", "-") )}</ref>')
        refs_text.append("{{références}}")
        return "\n".join(refs_text)

    def generate_article_content(self, exoplanet: Exoplanet) -> str:
        """
        Génère le contenu complet de l'article
        """
        content = f"""{{{{Ébauche|exoplanète|}}}}

{self.generate_infobox_exoplanet(exoplanet)}

'''{{{{nobr|{exoplanet.name}}}}}''' est une [[planète]] en [[orbite]] autour de {{{{nobr|[[{exoplanet.host_star}]]}}}}, une [[étoile]] [[{exoplanet.spectral_type or "?"}]] qui est l'objet primaire du système {{{{nobr|[[{exoplanet.host_star}]]}}}}.

Cette [[exoplanète]] est un [[{self._get_planet_type(exoplanet)}]] {self._get_size_comparison(exoplanet)}. Elle orbite à {{{{unité|{exoplanet.semi_major_axis}|[[unité astronomique|unités astronomiques]]}}}} de son étoile{self._get_orbital_comparison(exoplanet)}.

== Références ==
{self._format_references_section(exoplanet)}

{{{{portail|astronomie|exoplanètes}}}}

[[Catégorie:{self._get_planet_type(exoplanet)}]]
"""
        return content
    
    def _get_size_comparison(self, exoplanet: Exoplanet) -> str:
        """ 
        Génère une comparaison de taille avec Jupiter ou la Terre
        """
        mass_value = exoplanet.mass.value if exoplanet.mass and exoplanet.mass.value else None
        if mass_value:
            if mass_value > 10:
                return f"environ {mass_value/317.8:.1f} fois plus massif que [[Jupiter (planète)|Jupiter]]"
            else:
                return f"environ {mass_value:.1f} fois plus massif que la [[Terre]]"
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