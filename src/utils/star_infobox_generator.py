from typing import Any, Optional
from src.models.star import (
    Star,
    DataPoint,
)  # Assuming DataPoint is in star.py as per previous task
# If DataPoint was moved to models.reference, this would be:
# from src.models.star import Star
# from src.models.reference import DataPoint
# from src.utils.format_utils import FormatUtils # Will add if complex formatting is needed


class StarInfoboxGenerator:
    """
    Classe pour générer l'infobox des articles d'étoiles.
    """

    def __init__(self):
        # self.format_utils = FormatUtils() # Not strictly needed for this simplified version
        pass

    def _add_field(
        self, star: Star, attribute_name: str, infobox_field_name: str
    ) -> str:
        """
        Helper function to add a field to the infobox string.
        Handles DataPoint access, None checks, and common formatting.
        """
        attr_dp = getattr(star, attribute_name, None)

        if attr_dp is None:
            return ""

        value: Any = None
        unit: Optional[str] = None

        if isinstance(attr_dp, DataPoint):
            if attr_dp.value is not None:
                value = attr_dp.value
            if attr_dp.unit is not None:
                unit = attr_dp.unit
        else:  # Fallback if not a DataPoint instance (should ideally be)
            value = attr_dp

        if value is None or (isinstance(value, str) and not value.strip()):
            return ""

        # Ensure string representation for non-list values before further processing
        if not isinstance(value, list):
            str_value = str(value).strip()
            if not str_value:
                return ""
            value = str_value

        # 1. Designations (special list handling)
        if infobox_field_name == "désignations":
            if isinstance(value, list):
                # Filter out empty strings or None from the list before joining
                processed_list = [str(v) for v in value if str(v).strip()]
                if not processed_list:
                    return ""
                return f" | {infobox_field_name} = {', '.join(processed_list)}\n"
            # If it's a single string value for designations
            return f" | {infobox_field_name} = {value}\n"

        if infobox_field_name == "âge":
            return f" | {infobox_field_name} = {value}×10<sup>9</sup>"

        # 3. Fields requiring unit on a separate line (e.g., "masse", "rayon")
        # These infobox_field_names should be the exact names used in the template for the value.
        # The " unité" suffix will be appended for the unit line.
        fields_with_separate_unit_line = [
            "masse",
            "rayon",
            "température",
            "luminosité",
            "vitesse radiale",
            "mouvement propre ad",
            "mouvement propre déc",
            "parallaxe",
            "gravité",
            "rotation",
            "masse volumique",
            "demi-grand axe",
            "période",
            "inclinaison",
            "nœud",
            "argument",
            # Note: température might sometimes be "valeur K" instead of separate unit.
            # The French template usually lists "température" and expects K, or "température unité".
        ]
        if infobox_field_name in fields_with_separate_unit_line:
            line = f" | {infobox_field_name} = {value}\n"
            if unit:
                # Specific unit parameter names if they differ from "{infobox_field_name} unité"
                unit_param_name_overrides = {
                    "longitude du nœud ascendant (Ω)": "longitude nœud ascendant unité",  # Example if different
                    "argument du périastre (ω)": "argument périastre unité",  # Example if different
                }
                unit_param_name = unit_param_name_overrides.get(
                    infobox_field_name, f"{infobox_field_name} unité"
                )
                line += f" | {unit_param_name} = {unit}\n"
            return line

        # 4. Default formatting: " | field = value unit" or " | field = value"
        # This handles fields like spectral type, epoch, magnitudes (which usually don't list units explicitly in infobox)
        # or fields where unit is conventionally appended if present.
        output_str = f" | {infobox_field_name} = {value}"
        if unit:
            # Avoid appending unit if it's implied (e.g. metallicity [Fe/H] unit is 'dex' but often not written)
            # or if the value itself already contains it (less ideal for DataPoint)
            if (
                infobox_field_name
                not in [
                    "métallicité ([Fe/H])",
                    "type spectral",
                    "époque",
                    "constellation",
                ]
                and not infobox_field_name.startswith("magnitude apparente")
                and not infobox_field_name.startswith("magnitude absolue")
                and not infobox_field_name.startswith("indice ")
            ):
                output_str += f" {unit}"
        output_str += "\n"
        return output_str

    def generate_star_infobox(self, star: Star) -> str:
        """
        Génère le contenu de l'infobox Wikipédia pour une étoile.
        """
        if not isinstance(star, Star):
            raise TypeError("Input must be a Star object.")

        infobox = "{{Infobox Étoile\n"

        # Section: Identifiers
        infobox += self._add_field(star, "name", "nom")
        infobox += self._add_field(star, "image", "image")
        infobox += self._add_field(star, "upright", "upright")  # Image scaling
        infobox += self._add_field(star, "caption", "légende")
        infobox += self._add_field(star, "coord_title", "coord titre")  # oui/non
        infobox += self._add_field(star, "iau_map", "carte UAI")
        infobox += self._add_field(star, "designations", "désignations")

        # Section: Données d'observation
        infobox += self._add_field(star, "epoch", "époque")  # Epoch for coordinates
        infobox += self._add_field(star, "constellation", "constellation")

        infobox += self._add_field(star, "right_ascension", "ascension droite")
        infobox += self._add_field(star, "right_ascension_2", "ascension droite 2")
        infobox += self._add_field(star, "declination", "déclinaison")
        infobox += self._add_field(star, "declination_2", "déclinaison 2")

        infobox += self._add_field(star, "radial_velocity", "vitesse radiale")
        infobox += self._add_field(star, "radial_velocity_2", "vitesse radiale 2")
        infobox += self._add_field(star, "proper_motion_ra", "mouvement propre ad")
        infobox += self._add_field(star, "proper_motion_ra_2", "mouvement propre ad 2")
        infobox += self._add_field(star, "proper_motion_dec", "mouvement propre déc")
        infobox += self._add_field(
            star, "proper_motion_dec_2", "mouvement propre déc 2"
        )

        infobox += self._add_field(star, "parallax", "parallaxe")
        infobox += self._add_field(star, "parallax_2", "parallaxe 2")

        # Distance:
        infobox += self._add_field(star, "distance", "distance")
        infobox += self._add_field(star, "distance_2", "distance 2")

        # Section: Caractéristiques (Photometry & Spectral Type)
        infobox += self._add_field(star, "spectral_type", "type spectral")
        infobox += self._add_field(star, "spectral_type_2", "type spectral 2")

        infobox += self._add_field(
            star, "apparent_magnitude_u_band", "magnitude apparente bande U"
        )
        infobox += self._add_field(
            star, "apparent_magnitude_u_band_2", "magnitude apparente bande U 2"
        )
        infobox += self._add_field(
            star, "apparent_magnitude_b_band", "magnitude apparente bande B"
        )
        infobox += self._add_field(
            star, "apparent_magnitude_b_band_2", "magnitude apparente bande B 2"
        )
        infobox += self._add_field(
            star, "apparent_magnitude_v_band", "magnitude apparente bande V"
        )  # Explicit V
        infobox += self._add_field(
            star, "apparent_magnitude_v_band_2", "magnitude apparente bande V 2"
        )
        infobox += self._add_field(
            star, "apparent_magnitude_g_band", "magnitude apparente bande G"
        )
        infobox += self._add_field(
            star, "apparent_magnitude_g_band_2", "magnitude apparente bande G 2"
        )
        infobox += self._add_field(
            star, "apparent_magnitude_r_band", "magnitude apparente bande R"
        )
        infobox += self._add_field(
            star, "apparent_magnitude_r_band_2", "magnitude apparente bande R 2"
        )
        infobox += self._add_field(
            star, "apparent_magnitude_i_band", "magnitude apparente bande I"
        )
        infobox += self._add_field(
            star, "apparent_magnitude_i_band_2", "magnitude apparente bande I 2"
        )
        infobox += self._add_field(
            star, "apparent_magnitude_j_band", "magnitude apparente bande J"
        )
        infobox += self._add_field(
            star, "apparent_magnitude_j_band_2", "magnitude apparente bande J 2"
        )
        infobox += self._add_field(
            star, "apparent_magnitude_h_band", "magnitude apparente bande H"
        )
        infobox += self._add_field(
            star, "apparent_magnitude_h_band_2", "magnitude apparente bande H 2"
        )
        infobox += self._add_field(
            star, "apparent_magnitude_k_band", "magnitude apparente bande K"
        )
        infobox += self._add_field(
            star, "apparent_magnitude_k_band_2", "magnitude apparente bande K 2"
        )

        infobox += self._add_field(star, "u_b_color", "u-b")
        infobox += self._add_field(star, "u_b_color_2", "u-b 2")
        infobox += self._add_field(star, "b_v_color", "b-v")
        infobox += self._add_field(star, "b_v_color_2", "b-v 2")
        infobox += self._add_field(star, "v_r_color", "v-r")
        infobox += self._add_field(star, "v_r_color_2", "v-r 2")
        infobox += self._add_field(star, "r_i_color", "r-i")
        infobox += self._add_field(star, "r_i_color_2", "r-i 2")
        infobox += self._add_field(star, "j_k_color", "j-k")
        infobox += self._add_field(star, "j_k_color_2", "j-k 2")
        infobox += self._add_field(star, "j_h_color", "j-h")
        infobox += self._add_field(star, "j_h_color_2", "j-h 2")

        infobox += self._add_field(star, "absolute_magnitude", "magnitude absolue")
        infobox += self._add_field(star, "absolute_magnitude_2", "magnitude absolue 2")
        infobox += self._add_field(star, "variability", "variabilité")
        infobox += self._add_field(star, "variability_2", "variabilité 2")

        # Section: Caractéristiques physiques
        infobox += self._add_field(star, "mass", "masse")
        infobox += self._add_field(star, "mass_2", "masse 2")
        infobox += self._add_field(star, "radius", "rayon")
        infobox += self._add_field(star, "radius_2", "rayon 2")
        infobox += self._add_field(star, "density", "masse volumique")
        infobox += self._add_field(star, "density_2", "masse volumique 2")
        infobox += self._add_field(star, "luminosity", "luminosité")
        infobox += self._add_field(star, "luminosity_2", "luminosité 2")
        infobox += self._add_field(star, "surface_gravity", "gravité")
        infobox += self._add_field(star, "surface_gravity_2", "gravité 2")
        infobox += self._add_field(star, "temperature", "température")
        infobox += self._add_field(star, "temperature_2", "température 2")
        infobox += self._add_field(star, "metallicity", "métallicité")
        infobox += self._add_field(star, "metallicity_2", "métallicité 2")
        infobox += self._add_field(star, "rotation", "rotation")
        infobox += self._add_field(star, "rotation_2", "rotation 2")
        infobox += self._add_field(star, "age", "âge")
        infobox += self._add_field(star, "age_2", "âge 2")
        infobox += self._add_field(star, "evolutionary_stage", "stade évolutif")
        infobox += self._add_field(star, "evolutionary_stage_2", "stade évolutif 2")

        # Section: Système stellaire / planétaire
        # The template might have "Système stellaire" and "Système planétaire" as distinct sections
        # or combine them. For now, adding fields related to system components.
        infobox += self._add_field(star, "stellar_components", "composantes stellaires")
        infobox += self._add_field(star, "companion", "compagnon")
        infobox += self._add_field(star, "planets", "planètes")  # Number or list

        # Section: Éléments orbitaux (si binaire)
        # Check if it's a binary; perhaps a flag in Star model or check if orbital params exist
        # For now, assume if any binary param is present, the section is relevant.
        # The template uses "orbite binaire" or similar for the section header.
        # For simplicity, just adding fields. A check could be added to only print if populated.
        # Example of how one might conditionally add this section title:
        # binary_params_present = any(getattr(star, attr, None) for attr in ["semi_major_axis", "period", ...])
        # if binary_params_present:
        #     infobox += "| section éléments orbitaux = oui\n" # Or specific title for binary section

        infobox += self._add_field(star, "semi_major_axis", "demi-grand axe")
        infobox += self._add_field(
            star, "eccentricity", "excentricité (e)"
        )  # Unitless typically
        infobox += self._add_field(star, "period", "période")
        infobox += self._add_field(star, "inclination", "inclinaison")
        infobox += self._add_field(star, "argument_of_periapsis", "argument")
        infobox += self._add_field(star, "argument_of_periapsis_2", "argument 2")
        infobox += self._add_field(star, "longitude_of_ascending_node", "nœud")
        infobox += self._add_field(star, "epoch_binary", "époque binaire")

        # Other binary characteristics (e.g. semi-amplitude, might fit under "Données spectroscopiques" or similar)
        infobox += self._add_field(
            star, "semi_amplitude_1", "demi-amplitude"
        )  # Example infobox field name
        infobox += self._add_field(
            star, "semi_amplitude_2", "demi-amplitude 2"
        )  # Example infobox field name

        infobox += "}}\n"

        return infobox
