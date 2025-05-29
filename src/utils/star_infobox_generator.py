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
        Handles DataPoint access and None checks.
        """
        attr = getattr(star, attribute_name, None)
        if attr is None:
            return ""

        value = None
        unit = None

        if isinstance(attr, DataPoint):
            if attr.value is not None:
                value = attr.value
            if attr.unit is not None:
                unit = attr.unit
        else:  # Should not happen if Star model uses DataPoints for all relevant fields
            value = attr

        if value is None or str(value).strip() == "":
            return ""

        # Special handling for specific fields
        if infobox_field_name == "distance" and unit:
            if unit.lower() == "pc":
                return f" | {infobox_field_name} = {{{{Parsec|{value}|pc}}}}\n"
            elif unit.lower() == "al":  # distance_al is also a field in the template
                return f" | distance al = {value}\n"  # Or use a template if available for al
            # Fallback for other distance units or if only value is present
            return f" | {infobox_field_name} = {value}{f' {unit}' if unit else ''}\n"
        elif infobox_field_name in ["masse", "rayon", "température", "âge"] and unit:
            return f" | {infobox_field_name} = {value}\n | {infobox_field_name} unité = {unit}\n"
        elif infobox_field_name == "désignations":
            if isinstance(value, list):
                return f" | {infobox_field_name} = {', '.join(value)}\n"
            return f" | {infobox_field_name} = {value}\n"

        return f" | {infobox_field_name} = {value}\n"

    def generate_star_infobox(self, star: Star) -> str:
        """
        Génère le contenu de l'infobox Wikipédia pour une étoile.
        """
        if not isinstance(star, Star):
            raise TypeError("Input must be a Star object.")

        infobox = "{{Infobox Étoile\n"

        # Directly add fields that don't need special unit handling or are simple DataPoints
        infobox += self._add_field(star, "name", "nom")
        infobox += self._add_field(star, "image", "image")
        infobox += self._add_field(star, "caption", "légende")
        infobox += self._add_field(star, "epoch", "époque")
        infobox += self._add_field(star, "right_ascension", "ascension droite")
        infobox += self._add_field(star, "declination", "déclinaison")
        infobox += self._add_field(star, "constellation", "constellation")
        infobox += self._add_field(
            star, "apparent_magnitude", "magnitude apparente"
        )  # Assumes V-band if not specified
        infobox += self._add_field(star, "spectral_type", "type spectral")

        # Fields with potential units or special formatting
        infobox += self._add_field(
            star, "distance", "distance"
        )  # Handles pc/al and other units
        infobox += self._add_field(star, "mass", "masse")
        infobox += self._add_field(star, "radius", "rayon")
        infobox += self._add_field(star, "temperature", "température")
        infobox += self._add_field(star, "age", "âge")

        # Designations
        infobox += self._add_field(star, "designations", "désignations")

        infobox += "}}\n"

        return infobox
