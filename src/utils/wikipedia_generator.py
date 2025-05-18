from typing import Dict, List, Optional
from src.models.exoplanet import Exoplanet
import datetime

class WikipediaGenerator:
    """
    Classe pour générer le contenu wikitexte des articles d'exoplanètes
    """
    
    def __init__(self):
        self.template_refs = {
            'nasa': "{{cite web |url=https://exoplanetarchive.ipac.caltech.edu/ |title=NASA Exoplanet Archive |accessdate=" + datetime.datetime.now().strftime("%Y-%m-%d") + "}}",
            'exoplanet_eu': "{{cite web |url=http://exoplanet.eu/ |title=The Extrasolar Planets Encyclopaedia |accessdate=" + datetime.datetime.now().strftime("%Y-%m-%d") + "}}",
            'open_exoplanet': "{{cite web |url=https://github.com/OpenExoplanetCatalogue/open_exoplanet_catalogue |title=Open Exoplanet Catalogue |accessdate=" + datetime.datetime.now().strftime("%Y-%m-%d") + "}}"
        }
    
    def _format_value_with_unit(self, value: Optional[float], unit: str) -> str:
        """
        Formate une valeur avec son unité, gère les valeurs None
        """
        if value is None:
            return "?"
        return f"{value} {unit}"
    
    def _get_reference(self, source: str) -> str:
        """
        Retourne la référence formatée pour une source donnée
        """
        return self.template_refs.get(source, "")
    
    def generate_infobox_exoplanet(self, exoplanet: Exoplanet) -> str:
        """
        Génère l'infobox pour une exoplanète
        """
        infobox = """{{Infobox Exoplanète
| nom = """ + exoplanet.name + """
| image = 
| légende = 
| étoile = """ + exoplanet.host_star + """
| constellation = 
| ascension_droite = 
| déclinaison = 
| distance = """ + self._format_value_with_unit(exoplanet.distance, "al") + """
| type_spectral = """ + (exoplanet.star_type or "?") + """
| masse = """ + self._format_value_with_unit(exoplanet.mass, "M⊕") + """<ref>""" + self._get_reference(exoplanet.source) + """</ref>
| rayon = """ + self._format_value_with_unit(exoplanet.radius, "R⊕") + """<ref>""" + self._get_reference(exoplanet.source) + """</ref>
| densité = """ + self._format_value_with_unit(exoplanet.density, "g/cm³") + """<ref>""" + self._get_reference(exoplanet.source) + """</ref>
| gravité = """ + self._format_value_with_unit(exoplanet.gravity, "g") + """<ref>""" + self._get_reference(exoplanet.source) + """</ref>
| température = """ + self._format_value_with_unit(exoplanet.equilibrium_temperature, "K") + """<ref>""" + self._get_reference(exoplanet.source) + """</ref>
| période = """ + self._format_value_with_unit(exoplanet.orbital_period, "j") + """<ref>""" + self._get_reference(exoplanet.source) + """</ref>
| demi_grand_axe = """ + self._format_value_with_unit(exoplanet.semi_major_axis, "ua") + """<ref>""" + self._get_reference(exoplanet.source) + """</ref>
| excentricité = """ + self._format_value_with_unit(exoplanet.eccentricity, "") + """<ref>""" + self._get_reference(exoplanet.source) + """</ref>
| inclinaison = """ + self._format_value_with_unit(exoplanet.inclination, "°") + """<ref>""" + self._get_reference(exoplanet.source) + """</ref>
| méthode_découverte = """ + (exoplanet.discovery_method or "?") + """
| date_découverte = """ + (str(exoplanet.discovery_year) if exoplanet.discovery_year else "?") + """
| statut = Confirmée
}}"""
        return infobox
    
    def generate_infobox_star(self, exoplanet: Exoplanet) -> str:
        """
        Génère l'infobox pour l'étoile hôte
        """
        infobox = """{{Infobox Étoile
| nom = """ + exoplanet.host_star + """
| image = 
| légende = 
| constellation = 
| ascension_droite = 
| déclinaison = 
| distance = """ + self._format_value_with_unit(exoplanet.distance, "al") + """
| type_spectral = """ + (exoplanet.star_type or "?") + """
| magnitude_absolue = 
| magnitude_apparente = 
| masse = """ + self._format_value_with_unit(exoplanet.star_mass, "M☉") + """<ref>""" + self._get_reference(exoplanet.source) + """</ref>
| rayon = """ + self._format_value_with_unit(exoplanet.star_radius, "R☉") + """<ref>""" + self._get_reference(exoplanet.source) + """</ref>
| température = """ + self._format_value_with_unit(exoplanet.star_temperature, "K") + """<ref>""" + self._get_reference(exoplanet.source) + """</ref>
| métallicité = """ + self._format_value_with_unit(exoplanet.star_metallicity, "") + """<ref>""" + self._get_reference(exoplanet.source) + """</ref>
| âge = """ + self._format_value_with_unit(exoplanet.star_age, "Ga") + """<ref>""" + self._get_reference(exoplanet.source) + """</ref>
}}"""
        return infobox
    
    def generate_article_content(self, exoplanet: Exoplanet) -> str:
        """
        Génère le contenu complet de l'article
        """
        content = f"""== {exoplanet.name} ==

{self.generate_infobox_exoplanet(exoplanet)}

{exoplanet.name} est une exoplanète découverte en {exoplanet.discovery_year} par la méthode de {exoplanet.discovery_method}. Elle orbite autour de l'étoile {exoplanet.host_star}.

== Caractéristiques ==

=== Caractéristiques orbitales ===
* Période orbitale : {self._format_value_with_unit(exoplanet.orbital_period, "jours")}<ref>{self._get_reference(exoplanet.source)}</ref>
* Demi-grand axe : {self._format_value_with_unit(exoplanet.semi_major_axis, "ua")}<ref>{self._get_reference(exoplanet.source)}</ref>
* Excentricité : {self._format_value_with_unit(exoplanet.eccentricity, "")}<ref>{self._get_reference(exoplanet.source)}</ref>
* Inclinaison : {self._format_value_with_unit(exoplanet.inclination, "°")}<ref>{self._get_reference(exoplanet.source)}</ref>

=== Caractéristiques physiques ===
* Masse : {self._format_value_with_unit(exoplanet.mass, "M⊕")}<ref>{self._get_reference(exoplanet.source)}</ref>
* Rayon : {self._format_value_with_unit(exoplanet.radius, "R⊕")}<ref>{self._get_reference(exoplanet.source)}</ref>
* Densité : {self._format_value_with_unit(exoplanet.density, "g/cm³")}<ref>{self._get_reference(exoplanet.source)}</ref>
* Température d'équilibre : {self._format_value_with_unit(exoplanet.equilibrium_temperature, "K")}<ref>{self._get_reference(exoplanet.source)}</ref>

== Étoile hôte ==

{self.generate_infobox_star(exoplanet)}

L'étoile hôte {exoplanet.host_star} est une étoile de type spectral {exoplanet.star_type or "inconnu"}.

== Découverte ==

{exoplanet.name} a été découverte en {exoplanet.discovery_year} par la méthode de {exoplanet.discovery_method}.

== Références ==
<references />

[[Catégorie:Exoplanète]]
[[Catégorie:Exoplanète découverte en {exoplanet.discovery_year}]]
"""
        return content 