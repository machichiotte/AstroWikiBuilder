from src.models.exoplanet import Exoplanet
from .reference_utils import ReferenceUtils
from .planet_type_utils import PlanetTypeUtils

class InfoboxGenerator:
    """
    Classe pour générer l'infobox des articles d'exoplanètes
    """
    FIELD_DEFAULT_UNITS = {
        "masse": "M_J",
        "rayon": "R_J",
        "température": "K",
        "distance": "pc",
        "demi-grand axe": "ua",
        "période": "j",
        "inclinaison": "°",
        "périastre": "ua",
        "apoastre": "ua",
        "masse minimale": "M_J",
        "masse volumique": "kg/m³",
        "gravité": "m/s²",
        "période de rotation": "h",
        "arg_péri": "°",
    }

    def __init__(self, reference_utils: ReferenceUtils):
        self.reference_utils = reference_utils
        self.planet_type_utils = PlanetTypeUtils()

    def generate_infobox(self, exoplanet: Exoplanet) -> str:
        """
        Génère l'infobox pour une exoplanète
        """
        def val(attr):
            return getattr(exoplanet, attr).value if getattr(exoplanet, attr) and hasattr(getattr(exoplanet, attr), 'value') else None
        
        def unit(attr):
            return getattr(exoplanet, attr).unit if getattr(exoplanet, attr) and hasattr(getattr(exoplanet, attr), 'unit') and getattr(exoplanet, attr).unit else None
        
        def notes(attr):
            # Ne pas ajouter de notes pour le champ étoile
            if attr == "host_star":
                return None
                
            datapoint = getattr(exoplanet, attr, None)
            if not datapoint or not hasattr(datapoint, 'reference') or not datapoint.reference:
                return None
            
            ref = datapoint.reference
            if not hasattr(ref, 'source') or not ref.source or not hasattr(ref, 'to_wiki_ref'):
                return None

            ref_name = str(ref.source.value) if hasattr(ref.source, 'value') else str(ref.source)
            ref_content_full = ref.to_wiki_ref(self.reference_utils.template_refs, exoplanet.name)

            if ref_content_full:
                return self.reference_utils.add_reference(ref_name, ref_content_full)
            return None

        def add_field(label, attr):
            
            v = val(attr)
                        
            s = ""
            if v is not None and v != "":
                s += f" | {label} = {v}\n"
                
                actual_unit = unit(attr)
                n = notes(attr)
                expected_default_unit = self.FIELD_DEFAULT_UNITS.get(label)

                if actual_unit:
                    if expected_default_unit and actual_unit == expected_default_unit:
                        pass
                    else:
                        s += f" | {label} unité = {actual_unit}\n"
                
                if n:
                    # Vérifier si la référence est déjà encapsulée dans une balise ref
                    if n.startswith('<ref') and n.endswith('</ref>'):
                        s += f" | {label} notes = {n}\n"
                    else:
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
        infobox += add_field("distance", "distance")
        infobox += add_field("constellation", "constellation")
        
        if hasattr(exoplanet, 'iau_constellation_map') and exoplanet.iau_constellation_map:
            infobox += f" | carte = {exoplanet.iau_constellation_map}\n"
            
        infobox += add_field("type spectral", "spectral_type")
        infobox += add_field("magnitude apparente", "apparent_magnitude")
        
        # Planète
        infobox += f" | type = {self.planet_type_utils.get_planet_type(exoplanet)}\n"
        
        # Caractéristiques orbitales
        infobox += add_field("demi-grand axe", "semi_major_axis")
        infobox += add_field("périastre", "periastron")
        infobox += add_field("apoastre", "apoastron")
        infobox += add_field("excentricité", "eccentricity")
        infobox += add_field("période", "orbital_period")
        infobox += add_field("distance angulaire", "angular_distance")
        infobox += add_field("t_peri", "periastron_time")
        infobox += add_field("inclinaison", "inclination")
        infobox += add_field("arg_péri", "argument_of_periastron")
        infobox += add_field("époque", "epoch")
        
        # Caractéristiques physiques
        infobox += add_field("masse", "mass")
        infobox += add_field("masse minimale", "minimum_mass")
        infobox += add_field("rayon", "radius")
        infobox += add_field("masse volumique", "density")
        infobox += add_field("gravité", "gravity")
        infobox += add_field("période de rotation", "rotation_period")
        infobox += add_field("température", "temperature")
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