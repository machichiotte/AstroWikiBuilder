from typing import Dict, List, Optional
from src.models.exoplanet import Exoplanet
import datetime

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
        Génère l'infobox pour une exoplanète
        """
        # Utiliser uniquement les balises <ref name="EPE"/> et <ref name="NasaGov"/>
        infobox = f"""{{{{Infobox Exoplanète
 | nom                       = {exoplanet.name}
 | image                     = 
 | légende                   = 
<!-- ÉTOILE -->
 | étoile                    = [[{exoplanet.host_star}]]
 | époque étoile             = 
 | époque étoile notes       = 
 | ascension droite          = 
 | ascension droite notes    = <ref name=\"EPE\"/>
 | déclinaison               = 
 | déclinaison notes         = <ref name=\"EPE\"/>
 | distance                  = {self._format_value_with_unit(exoplanet.distance, "pc")}
 | distance notes            = <ref name=\"EPE\"/>
 | constellation             = 
 | carte UAI                 = 
 | type spectral             = [[{exoplanet.star_type or "?"}]]
 | type spectral notes       = <ref name=\"EPE\"/>
 | magnitude apparente       = 
 | magnitude apparente notes = <ref name=\"EPE\"/>
<!-- PLANÈTE -->
<!-- Type -->
 | type                      = [[{self._get_planet_type(exoplanet)}]]
 | type notes                = <ref name=\"EPE\"/>
<!-- Caractéristiques orbitales -->
 | demi-grand axe            = {self._format_value_with_unit(exoplanet.semi_major_axis, "")}
 | demi-grand axe notes      = <ref name=\"EPE\"/>
 | périastre                 = 
 | périastre unité           = 
 | périastre notes           = 
 | apoastre                  = 
 | apoastre unité            = 
 | apoastre notes            = 
 | excentricité              = {self._format_value_with_unit(exoplanet.eccentricity, "")}
 | excentricité notes        = <ref name=\"EPE\"/>
 | période                   = {self._format_value_with_unit(exoplanet.orbital_period, "")}
 | période année             = 
 | période heure             = 
 | période notes             = <ref name=\"EPE\"/>
 | distance angulaire        = 
 | distance angulaire notes  = 
 | t_peri                    = 
 | t_peri notes              = 
 | inclinaison               = {self._format_value_with_unit(exoplanet.inclination, "")}
 | inclinaison unité         = 
 | inclinaison notes         = 
 | arg_péri                  = 
 | arg_péri notes            = 
 | époque                    = 
 | époque notes              = 
<!-- Caractéristiques physiques -->
 | masse                     = {self._format_value_with_unit(exoplanet.mass, "")}
 | masse notes               = <ref name=\"EPE\"/>
 | masse minimale            = 
 | masse minimale unité      = 
 | masse minimale notes      = 
 | rayon                     = {self._format_value_with_unit(exoplanet.radius, "")}
 | rayon notes               = (estimation) <ref name=\"NasaGov\"/>
 | masse volumique           = {self._format_value_with_unit(exoplanet.density, "")}
 | masse volumique unité     = 
 | masse volumique notes     = 
 | gravité                   = {self._format_value_with_unit(exoplanet.gravity, "")}
 | gravité unité             = 
 | gravité notes             = 
 | période de rotation       = 
 | période de rotation unité = 
 | période de rotation notes = 
 | température               = {self._format_value_with_unit(exoplanet.equilibrium_temperature, "")}
 | température unité         = 
 | température notes         = 
<!-- Atmosphère -->
 | pression                  = 
 | pression notes            = 
 | composition               = 
 | composition notes         = 
 | vitesse des vents         = 
 | vitesse des vents notes   = 
<!-- Découverte -->
 | découvreurs               = 
 | découvreurs notes         = 
 | programme                 = 
 | programme notes           = 
 | méthode                   = {exoplanet.discovery_method or "?"}
 | méthode notes             = <ref name=\"NasaGov\"/>
 | date                      = {exoplanet.discovery_year or "?"}
 | date notes                = <ref name=\"NasaGov\"/>
 | lieu                      = 
 | lieu notes                = 
 | prédécouverte             = 
 | prédécouverte notes       = 
 | détection                 = 
 | détection notes           = 
 | statut                    = Confirmée
 | statut notes              = <ref name=\"EPE\"/>
<!-- Informations supplémentaires -->
 | autres noms               = {exoplanet.name}}}}}"""
        return infobox
    
    def _get_planet_type(self, exoplanet: Exoplanet) -> str:
        """
        Détermine le type de planète en fonction de ses caractéristiques
        """
        if exoplanet.mass and exoplanet.mass > 10:
            return "Géante gazeuse"
        elif exoplanet.radius and exoplanet.radius > 2:
            return "Géante gazeuse"
        else:
            return "Planète tellurique"
    
    def _get_used_references(self, exoplanet: Exoplanet) -> List[str]:
        """
        Retourne la liste des références utilisées pour l'exoplanète
        """
        refs = []
        # EPE est toujours utilisée dans l'infobox
        refs.append("EPE")
        # NasaGov est utilisée si la source est 'nasa' ou pour le rayon
        if exoplanet.source == "nasa" or exoplanet.radius:
            refs.append("NasaGov")
        return list(set(refs))

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

'''{{{{nobr|{exoplanet.name}}}}}''' est une [[planète]] en [[orbite]] autour de {{{{nobr|[[{exoplanet.host_star}]]}}}}, une [[étoile]] [[{exoplanet.star_type or "?"}]] qui est l'objet primaire du système {{{{nobr|[[{exoplanet.host_star}]]}}}}.

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
        if exoplanet.mass:
            if exoplanet.mass > 10:
                return f"environ {exoplanet.mass/317.8:.1f} fois plus massif que [[Jupiter (planète)|Jupiter]]"
            else:
                return f"environ {exoplanet.mass:.1f} fois plus massif que la [[Terre]]"
        return ""
    
    def _get_orbital_comparison(self, exoplanet: Exoplanet) -> str:
        """
        Génère une comparaison orbitale avec le système solaire
        """
        if exoplanet.semi_major_axis:
            if exoplanet.semi_major_axis < 0.1:
                return ", une distance comparable à celle de [[Mercure (planète)|Mercure]] dans le [[système solaire]]"
            elif exoplanet.semi_major_axis < 1:
                return ", une distance comparable à celle de [[Vénus (planète)|Vénus]] dans le [[système solaire]]"
            elif exoplanet.semi_major_axis < 2:
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