from src.models.exoplanet import Exoplanet
from .reference_utils import ReferenceUtils
from .planet_type_utils import PlanetTypeUtils
from .format_utils import FormatUtils

class InfoboxGenerator:
    """
    Classe pour générer l'infobox des articles d'exoplanètes
    """
    FIELD_DEFAULT_UNITS = {
        "masse": "M_J", "rayon": "R_J", "température": "K", "distance": "pc",
        "demi-grand axe": "ua", "période": "j", "inclinaison": "°", "périastre": "ua",
        "apoastre": "ua", "masse minimale": "M_J", "masse volumique": "kg/m³",
        "gravité": "m/s²", "période de rotation": "h", "arg_péri": "°",
    }

    WIKILINK_FIELDS_DIRECT = {
        "étoile", "constellation", "programme", "lieu"
        # Ex: "programme": "Programme Kepler" -> [[Programme Kepler]]
        # Ex: "lieu": "Observatoire de La Silla" -> [[Observatoire de La Silla]]
    }

    # Dictionnaire pour traduire les méthodes de découverte et lier vers l'article FR
    # Les clés sont les valeurs attendues de la source de données (en anglais, normalisées en minuscules)
    METHOD_NAME_MAPPING = {
        "transit": {
            "display": "Transits",
            "article": "Méthode des transits"
        },
        "radial velocity": {
            "display": "Vitesses radiales",
            "article": "Méthode des vitesses radiales"
        },
        "imaging": {
            "display": "Imagerie directe",
            "article": "Imagerie directe des exoplanètes" # ou "Imagerie directe" si plus générique
        },
        "microlensing": {
            "display": "Microlentille gravitationnelle",
            "article": "Microlentille gravitationnelle"
        },
        "gravitational microlensing": { # Au cas où la source utiliserait ce terme plus long
            "display": "Microlentille gravitationnelle",
            "article": "Microlentille gravitationnelle"
        },
        "timing": { # Terme générique, peut nécessiter plus de spécificité
            "display": "Variations de chronométrage",
            "article": "Chronométrage (astronomie)" # Exemple, à vérifier pour la pertinence
        },
        "pulsar timing": {
            "display": "Chronométrage de pulsar",
            "article": "Détection des exoplanètes par chronométrage de pulsar" # Titre d'article possible
        },
        "transit timing variations": {
            "display": "Variations du moment de transit",
            "article": "Mesure des variations de temps de transit" # TTV
        },
        "ttv": { # Acronyme commun pour Transit Timing Variations
            "display": "Variations du moment de transit (TTV)",
            "article": "Mesure des variations de temps de transit"
        },
        "astrometry": {
            "display": "Astrométrie",
            "article": "Astrométrie"
        },
        # Ajoutez d'autres méthodes ici au besoin
        # "primary transit": { # Si vos données ont des variantes
        # "display": "Transits (primaire)",
        # "article": "Méthode des transits"
        # }
    }


    def __init__(self, reference_utils: ReferenceUtils):
        self.reference_utils = reference_utils
        self.format_utils =  FormatUtils()
        self.planet_type_utils = PlanetTypeUtils()

    def generate_infobox(self, exoplanet: Exoplanet) -> str:
        def val(attr_name):
            attribute_obj = getattr(exoplanet, attr_name, None)
            if attribute_obj is not None:
                if hasattr(attribute_obj, 'value'):
                    return attribute_obj.value
                return attribute_obj
            return None
        
        def unit(attr_name):
            datapoint = getattr(exoplanet, attr_name, None)
            return datapoint.unit if datapoint and hasattr(datapoint, 'unit') and datapoint.unit else None
        
        def notes(attr_name):
            if attr_name == "host_star":
                return None
            datapoint = getattr(exoplanet, attr_name, None)
            if not datapoint or not hasattr(datapoint, 'reference') or not datapoint.reference:
                return None
            ref = datapoint.reference
            if not ref or not hasattr(ref, 'source') or not ref.source or not hasattr(ref, 'to_wiki_ref'):
                return None
            ref_name = str(ref.source.value) if hasattr(ref.source, 'value') else str(ref.source)
            ref_content_full = ref.to_wiki_ref(self.reference_utils.template_refs, exoplanet.name)
            if ref_content_full:
                return self.reference_utils.add_reference(ref_name, ref_content_full)
            return None

        def add_field(label, attr_name):
            v = val(attr_name)
            s = ""
            if v is not None and str(v).strip() != "":
                processed_v = str(v)

                if label == "distance":
                    try:
                        processed_v = f"{{{{Parsec|{str(v)}|pc}}}}"
                    except (ValueError, TypeError):
                        # fallback si le formatage échoue
                        processed_v = str(v)
                elif label == "méthode":
                    # Normaliser la valeur brute (ex: minuscules) pour la recherche dans le mapping
                    # Supposons que v est la chaîne de caractères de la méthode, ex: "Transit"
                    normalized_method_value = str(v).lower().strip()
                    if normalized_method_value in self.METHOD_NAME_MAPPING:
                        map_entry = self.METHOD_NAME_MAPPING[normalized_method_value]
                        processed_v = f"[[{map_entry['article']}|{map_entry['display']}]]"
                    else:
                        # Fallback: si non trouvé, afficher la valeur brute (ou la franciser si possible)
                        # Pour l'instant, on affiche la valeur brute sans lien pour éviter les erreurs.
                        # On pourrait aussi tenter un lien simple: [[{str(v).capitalize()}]] si on pense que v est déjà en français.
                        processed_v = str(v) 
                elif label in self.WIKILINK_FIELDS_DIRECT and str(v).strip(): # Assurer que la valeur n'est pas vide
                    processed_v = f"[[{str(v)}]]"
                
                s += f" | {label} = {processed_v}\n"
                
                actual_unit = unit(attr_name)
                n = notes(attr_name)
                expected_default_unit = self.FIELD_DEFAULT_UNITS.get(label)

                if actual_unit:
                    if not (expected_default_unit and actual_unit == expected_default_unit):
                        s += f" | {label} unité = {actual_unit}\n"
                if n:
                    s += f" | {label} notes = {n}\n"
            return s

        infobox = f"{{{{Infobox Exoplanète\n"
        infobox += f" | nom = {exoplanet.name}\n"
        infobox += " | image = \n | légende = \n"
        
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
        
        planet_type_value = self.planet_type_utils.get_planet_type(exoplanet)
        if planet_type_value:
            infobox += f" | type = [[{planet_type_value}]]\n" 
        
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
        
        infobox += add_field("masse", "mass")
        infobox += add_field("masse minimale", "minimum_mass")
        infobox += add_field("rayon", "radius")
        infobox += add_field("masse volumique", "density")
        infobox += add_field("gravité", "gravity")
        infobox += add_field("période de rotation", "rotation_period")
        infobox += add_field("température", "temperature")
        infobox += add_field("albedo_bond", "bond_albedo")
        
        infobox += add_field("pression", "pressure")
        infobox += add_field("composition", "composition")
        infobox += add_field("vitesse des vents", "wind_speed")
        
        infobox += add_field("découvreurs", "discoverers")
        infobox += add_field("programme", "discovery_program") # Sera lié si dans WIKILINK_FIELDS_DIRECT
        infobox += add_field("méthode", "discovery_method")   # Logique spéciale via METHOD_NAME_MAPPING
        infobox += add_field("date", "discovery_date")
        infobox += add_field("lieu", "discovery_location")     # Sera lié si dans WIKILINK_FIELDS_DIRECT
        infobox += add_field("prédécouverte", "pre_discovery")
        infobox += add_field("détection", "detection_method") # Peut-être redondant avec "méthode" ou nécessiter un mapping similaire
        infobox += add_field("statut", "status")
        
        other_names_list = val("other_names") 
        if other_names_list:
            other_names_str = ", ".join(other_names_list)
            infobox += f" | autres noms = {other_names_str}\n"
            
        infobox += "}}"
        return infobox