# src/generators/exoplanet_infobox_generator.py
from src.constants.field_mappings import (
    FIELD_DEFAULT_UNITS,
    WIKILINK_FIELDS_DIRECT,
    METHOD_NAME_MAPPING,
)
from src.models.data_source_exoplanet import DataSourceExoplanet
from src.services.reference_manager import ReferenceManager
from src.utils.constellation_utils import ConstellationUtils
from src.utils.exoplanet_type_utils import ExoplanetTypeUtils


class ExoplanetInfoboxGenerator:
    """
    Classe pour générer l'infobox des articles d'exoplanètes
    """

    def __init__(self, reference_manager: ReferenceManager):
        self.reference_manager = reference_manager
        self.planet_type_utils = ExoplanetTypeUtils()
        self.constellation_utils = ConstellationUtils()

    def generate_exoplanet_infobox(self, exoplanet: DataSourceExoplanet) -> str:
        def val(attr_name):
            attribute_obj = getattr(exoplanet, attr_name, None)
            if attribute_obj is not None:
                if hasattr(attribute_obj, "value"):
                    return attribute_obj.value
                return attribute_obj
            return None

        def unit(attr_name):
            datapoint = getattr(exoplanet, attr_name, None)
            return (
                datapoint.unit
                if datapoint and hasattr(datapoint, "unit") and datapoint.unit
                else None
            )

        def notes(attr_name):
            if attr_name == "host_star":
                return None
            datapoint = getattr(exoplanet, attr_name, None)
            if (
                not datapoint
                or not hasattr(datapoint, "reference")
                or not datapoint.reference
            ):
                return None
            ref = datapoint.reference
            if (
                not ref
                or not hasattr(ref, "source")
                or not ref.source
                or not hasattr(ref, "to_wiki_ref")
            ):
                return None
            ref_name = (
                str(ref.source.value)
                if hasattr(ref.source, "value")
                else str(ref.source)
            )
            ref_content_full = ref.to_wiki_ref(exoplanet.name)
            if ref_content_full:
                return self.reference_manager.add_reference(ref_name, ref_content_full)
            return None

        def add_field(label, attribute_name):
            v = val(attribute_name)
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
                    if normalized_method_value in METHOD_NAME_MAPPING:
                        map_entry = METHOD_NAME_MAPPING[normalized_method_value]
                        processed_v = (
                            f"[[{map_entry['article']}|{map_entry['display']}]]"
                        )
                    else:
                        # Fallback: si non trouvé, afficher la valeur brute (ou la franciser si possible)
                        # Pour l'instant, on affiche la valeur brute sans lien pour éviter les erreurs.
                        # On pourrait aussi tenter un lien simple: [[{str(v).capitalize()}]] si on pense que v est déjà en français.
                        processed_v = str(v)
                elif (
                    label in WIKILINK_FIELDS_DIRECT and str(v).strip()
                ):  # Assurer que la valeur n'est pas vide
                    processed_v = f"[[{str(v)}]]"

                s += f" | {label} = {processed_v}\n"

                actual_unit = unit(attribute_name)
                n = notes(attribute_name)
                expected_default_unit = FIELD_DEFAULT_UNITS.get(label)

                if actual_unit:
                    if not (
                        expected_default_unit and actual_unit == expected_default_unit
                    ):
                        s += f" | {label} unité = {actual_unit}\n"
                if n:
                    s += f" | {label} notes = {n}\n"
            return s

        infobox = "{{Infobox Exoplanète\n"
        infobox += f" | nom = {exoplanet.name}\n"
        infobox += " | image = \n | légende = \n"

        infobox += add_field("étoile", "host_star")
        infobox += add_field("époque étoile", "star_epoch")
        infobox += add_field("ascension droite", "right_ascension")
        infobox += add_field("déclinaison", "declination")
        infobox += add_field("distance", "distance")
        infobox += add_field("type spectral", "spectral_type")
        infobox += add_field("magnitude apparente", "apparent_magnitude")
        infobox += f" | carte UAI = {self.constellation_utils.get_constellation_name(exoplanet.right_ascension.value, exoplanet.declination.value)}\n"
        infobox += f" | constellation = {self.constellation_utils.get_constellation_UAI(exoplanet.right_ascension.value, exoplanet.declination.value)}\n"

        planet_type_value = self.planet_type_utils.get_exoplanet_planet_type(exoplanet)
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
        infobox += add_field("programme", "discovery_program")
        infobox += add_field("méthode", "discovery_method")
        infobox += add_field("date", "discovery_date")
        infobox += add_field("lieu", "discovery_location")
        infobox += add_field("prédécouverte", "pre_discovery")
        infobox += add_field("détection", "detection_method")
        infobox += add_field("statut", "status")

        other_names_list = val("other_names")
        if other_names_list:
            other_names_str = ", ".join(other_names_list)
            infobox += f" | autres noms = {other_names_str}\n"

        infobox += "}}"
        return infobox
