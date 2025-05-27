from src.models.star import Star, DataPoint # Assuming DataPoint is in star.py as per previous task
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

    def _add_field(self, star: Star, attribute_name: str, infobox_field_name: str) -> str:
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
        else: # Should not happen if Star model uses DataPoints for all relevant fields
            value = attr 

        if value is None or str(value).strip() == "":
            return ""

        # Special handling for specific fields
        if infobox_field_name == "distance" and unit:
            if unit.lower() == "pc":
                return f" | {infobox_field_name} = {{{{Parsec|{value}|pc}}}}\n"
            elif unit.lower() == "al": # distance_al is also a field in the template
                 return f" | distance al = {value}\n" # Or use a template if available for al
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
        infobox += self._add_field(star, "apparent_magnitude", "magnitude apparente") # Assumes V-band if not specified
        infobox += self._add_field(star, "spectral_type", "type spectral")
        
        # Fields with potential units or special formatting
        infobox += self._add_field(star, "distance", "distance") # Handles pc/al and other units
        infobox += self._add_field(star, "mass", "masse")
        infobox += self._add_field(star, "radius", "rayon")
        infobox += self._add_field(star, "temperature", "température")
        infobox += self._add_field(star, "age", "âge")
        
        # Designations
        infobox += self._add_field(star, "designations", "désignations")

        infobox += "}}\n"
        return infobox

# Example Usage:
if __name__ == '__main__':
    # Ensure DataPoint is accessible, either from star.py or a common reference.py
    # For this example, assuming DataPoint is defined in src.models.star
    
    # Sample Star Data (mimicking the structure from star.py)
    sirius_data = {
        "name": DataPoint("Sirius"),
        "image": DataPoint("Sirius_A_and_B_artwork.jpg"),
        "caption": DataPoint("Artistic impression of Sirius A and B"),
        "epoch": DataPoint("J2000.0"),
        "right_ascension": DataPoint("06h 45m 08.9173s"),
        "declination": DataPoint("-16° 42′ 58.017″"),
        "constellation": DataPoint("Grand Chien"),
        "apparent_magnitude": DataPoint("-1.46"), # Magnitude Apparente (V)
        "spectral_type": DataPoint("A1V + DA2"),
        "distance": DataPoint(value=2.64, unit="pc"),
        "mass": DataPoint(value=2.063, unit="M☉"),
        "radius": DataPoint(value=1.711, unit="R☉"),
        "temperature": DataPoint(value=9940, unit="K"), # Surface temperature of component A
        "age": DataPoint(value="237–247", unit="Myr"),
        "designations": DataPoint(["Alpha Canis Majoris", "α CMa", "HD 48915", "HR 2491"]) # Already a list
    }
    sirius_star = Star(**sirius_data)

    proxima_data = {
        "name": DataPoint("Proxima Centauri"),
        "epoch": DataPoint("J2000.0"),
        "constellation": DataPoint("Centaure"),
        "distance": DataPoint(value=1.30197, unit="pc"), # Approx 4.2465 al
        "spectral_type": DataPoint("M5.5Ve"),
        "apparent_magnitude": DataPoint("11.13"),
        "mass": DataPoint(value=0.1221, unit="M☉"),
        "radius": DataPoint(value=0.1542, unit="R☉"),
        "temperature": DataPoint(value=3042, unit="K"),
        "age": DataPoint(value="4.85", unit="Gyr"), # Gyr for Gigayears
        "designations": DataPoint("V645 Cen, Alpha Centauri C, GCTP 3309.02, HIP 70890") # String to be split by Star class
    }
    proxima_star = Star(**proxima_data) # __post_init__ in Star should handle splitting designations

    generator = StarInfoboxGenerator()

    print("--- Sirius Infobox ---")
    sirius_infobox = generator.generate_star_infobox(sirius_star)
    print(sirius_infobox)

    print("\n--- Proxima Centauri Infobox ---")
    proxima_infobox = generator.generate_star_infobox(proxima_star)
    print(proxima_infobox)

    # Example of a star with fewer fields
    barnard_data = {
         "name": DataPoint("Barnard's Star"),
         "constellation": DataPoint("Ophiuchus"),
         "distance": DataPoint(value=1.827, unit="pc"),
         "designations": DataPoint(["BD+04°3561a", "HIP 87937"])
    }
    barnard_star = Star(**barnard_data)
    print("\n--- Barnard's Star Infobox (minimal) ---")
    barnard_infobox = generator.generate_star_infobox(barnard_star)
    print(barnard_infobox)

    # Example with distance in light years (al)
    trappist_1_data = {
        "name": DataPoint("TRAPPIST-1"),
        "distance": DataPoint(value=40.66, unit="al"), # Light years
        "spectral_type": DataPoint("M8V"),
        "mass": DataPoint(value=0.0898, unit="M☉"),
        "radius": DataPoint(value=0.1192, unit="R☉"),
        "temperature": DataPoint(value=2511, unit="K"),
        "designations": DataPoint("2MASS J23062928-0502285")
    }
    trappist_1_star = Star(**trappist_1_data)
    print("\n--- TRAPPIST-1 Infobox (distance in al) ---")
    trappist_1_infobox = generator.generate_star_infobox(trappist_1_star)
    print(trappist_1_infobox)
