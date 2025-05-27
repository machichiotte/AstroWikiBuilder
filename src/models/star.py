from dataclasses import dataclass, field
from typing import Optional, List, Dict

# Basic DataPoint class (can be refined later or imported)
@dataclass
class DataPoint:
    value: any
    unit: Optional[str] = None
    reference: Optional[str] = None # Simplified for now

@dataclass
class Star:
    # English Name: French Name (Template Key)
    name: Optional[DataPoint] = None  # nom
    image: Optional[DataPoint] = None  # image
    caption: Optional[DataPoint] = None  # légende
    epoch: Optional[DataPoint] = None  # époque
    right_ascension: Optional[DataPoint] = None  # ascension_droite
    declination: Optional[DataPoint] = None  # déclinaison
    constellation: Optional[DataPoint] = None  # constellation
    apparent_magnitude: Optional[DataPoint] = None  # magnitude_apparente (V)
    spectral_type: Optional[DataPoint] = None  # type_spectral
    distance: Optional[DataPoint] = None  # distance_pc (parsecs), distance_al (light-years)
    mass: Optional[DataPoint] = None  # masse
    radius: Optional[DataPoint] = None  # rayon
    temperature: Optional[DataPoint] = None  # température (surface)
    age: Optional[DataPoint] = None  # âge
    
    # Designations / Identifiers
    designations: Optional[DataPoint] = None # autres_désignations (can be a list or comma-separated string)

    # TODO: Add other attributes from "Infobox Étoile" as needed
    # For example:
    # luminosity: Optional[DataPoint] = None # luminosité
    # metallicity: Optional[DataPoint] = None # métallicité
    # rotation_velocity: Optional[DataPoint] = None # vitesse_rotation
    # proper_motion_ra: Optional[DataPoint] = None # mouvement_propre_ad
    # proper_motion_dec: Optional[DataPoint] = None # mouvement_propre_dec
    # radial_velocity: Optional[DataPoint] = None # vitesse_radiale
    # parallax: Optional[DataPoint] = None # parallaxe
    
    # Companion system details (if applicable)
    # companion_system: Optional[DataPoint] = None # système_planétaire (e.g., "[[Système planétaire de Proxima Centauri]]")
    # binary_star: Optional[DataPoint] = None # étoile_binaire (e.g. "Alpha Centauri A")
    # primary_star: Optional[DataPoint] = None # primaire (e.g. "Alpha Centauri B")
    # secondary_star: Optional[DataPoint] = None # secondaire (e.g. "Proxima Centauri")

    # Database identifiers
    # simbad_id: Optional[DataPoint] = None # identifiant_Simbad

    def __post_init__(self):
        # Ensure that 'designations' is a list if it's a string
        if self.designations and isinstance(self.designations.value, str):
            self.designations.value = [d.strip() for d in self.designations.value.split(',')]
        elif self.designations and not isinstance(self.designations.value, list):
            # If it's not a string and not a list, wrap it in a list
            # or handle as an error/log it, depending on expected input.
            # For now, wrapping in a list if it's a single DataPoint value.
            self.designations.value = [self.designations.value]
        
        # Example of how to handle multiple names if 'nom' could be a list
        # if self.name and isinstance(self.name.value, str):
        #     self.name.value = [n.strip() for n in self.name.value.split('/')] # Assuming names split by '/'

# Example usage:
if __name__ == '__main__':
    # This is just for demonstration and testing within this file.
    # Actual instantiation will happen based on data extraction.

    star_data_example = {
        "name": DataPoint("Sirius"),
        "image": DataPoint("Sirius_A_and_B_artwork.jpg"),
        "caption": DataPoint("Artistic impression of Sirius A and B"),
        "epoch": DataPoint("J2000.0"),
        "right_ascension": DataPoint("06h 45m 08.9173s"),
        "declination": DataPoint("-16° 42′ 58.017″"),
        "constellation": DataPoint("Grand Chien"),
        "apparent_magnitude": DataPoint("-1.46"),
        "spectral_type": DataPoint("A1V + DA2"),
        "distance": DataPoint(value=2.64, unit="pc"), # 8.6 light years
        "mass": DataPoint(value=2.063, unit="M☉"),
        "radius": DataPoint(value=1.711, unit="R☉"),
        "temperature": DataPoint(value=9940, unit="K (A) / 25000 K (B)"), # Surface temperature
        "age": DataPoint(value="237–247", unit="Myr"),
        "designations": DataPoint("Alpha Canis Majoris, α CMa, HD 48915, HR 2491, BD -16°1591, Gl 244 A/B, SAO 151881, HIP 32349")
    }

    sirius = Star(**star_data_example)

    print(f"Star Name: {sirius.name.value if sirius.name else 'N/A'}")
    print(f"Constellation: {sirius.constellation.value if sirius.constellation else 'N/A'}")
    print(f"Designations: {sirius.designations.value if sirius.designations else 'N/A'}")

    if sirius.designations:
        print(f"Type of designations: {type(sirius.designations.value)}")

    # Example with a single designation initially not as a list
    proxima_data = {
        "name": DataPoint("Proxima Centauri"),
        "designations": DataPoint("V645 Cen") # Single string value
    }
    proxima = Star(**proxima_data)
    print(f"Proxima Designations: {proxima.designations.value if proxima.designations else 'N/A'}")
    if proxima.designations:
        print(f"Type of Proxima designations: {type(proxima.designations.value)}")

    # Example with designations already as a list
    sun_data = {
        "name": DataPoint("Sun"),
        "designations": DataPoint(["Sol", "Hélios"]) # Already a list
    }
    sun = Star(**sun_data)
    print(f"Sun Designations: {sun.designations.value if sun.designations else 'N/A'}")
    if sun.designations:
        print(f"Type of Sun designations: {type(sun.designations.value)}")
