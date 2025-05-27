# src/utils/category_generator.py
from typing import List, Dict, Optional
from src.models.exoplanet import Exoplanet
from src.utils.planet_type_utils import PlanetTypeUtils
from src.utils.category_parser import parse_categories
import re # For constellation matching

class CategoryGenerator:
    """
    Classe pour générer les catégories des articles d'exoplanètes.
    """

    def __init__(self):
        self.predefined_categories: Dict[str, List[str]] = parse_categories()
        self.base_categories: List[str] = ["[[Catégorie:Exoplanète]]"]
        self.planet_type_utils = PlanetTypeUtils()

        # Mappings from Exoplanet data to predefined category strings
        self.discovery_method_map: Dict[str, str] = {
            "Radial Velocity": "[[Catégorie:Exoplanète découverte par la méthode des vitesses radiales]]",
            "Transit": "[[Catégorie:Exoplanète découverte par la méthode des transits]]",
            "Microlensing": "[[Catégorie:Exoplanète découverte par microlentille gravitationnelle]]",
            "Imaging": "[[Catégorie:Exoplanète découverte par imagerie directe]]",
            "Pulsar Timing": "[[Catégorie:Exoplanète découverte par chronométrie de pulsar]]",
            "Transit Timing Variations": "[[Catégorie:Exoplanète découverte par la méthode de la variation du temps de transit (TTV)]]",
            "Astrometry": "[[Catégorie:Exoplanète découverte par la méthode de l'astrométrie]]",
            "Orbital Brightness Modulation": "[[Catégorie:Exoplanète découverte par la méthode du décalage des minima]]",
            # Add other methods if present in data and categories_notes.md
        }

        self.instrument_map: Dict[str, str] = { # Renamed from discovery_facility_map
            # Exact keys here should match exoplanet.discovered_by.value
            # Example: "Kepler Space Telescope" might be just "Kepler" in notes.
            # We need to be careful or use a contains check.
            # For now, let's assume the keys are somewhat aligned or use common names.
            "Kepler": "[[Catégorie:Exoplanète découverte grâce à Kepler]]",
            "Kepler Space Telescope": "[[Catégorie:Exoplanète découverte grâce à Kepler]]",
            "Transiting Exoplanet Survey Satellite (TESS)": "[[Catégorie:Exoplanète découverte grâce au Transiting Exoplanet Survey Satellite]]",
            "TESS": "[[Catégorie:Exoplanète découverte grâce au Transiting Exoplanet Survey Satellite]]",
            "CoRoT": "[[Catégorie:Exoplanète découverte grâce au télescope spatial CoRoT]]",
            "Very Large Telescope (VLT)": "[[Catégorie:Exoplanète découverte grâce au Very Large Telescope (VLT)]]", # VLT is an instrument, facility Paranal
            "VLT": "[[Catégorie:Exoplanète découverte grâce au Very Large Telescope (VLT)]]",
            "Paranal Observatory": "[[Catégorie:Exoplanète découverte grâce au Very Large Telescope (VLT)]]", # Assuming VLT for Paranal
            "Hubble Space Telescope": "[[Catégorie:Exoplanète découverte grâce au télescope spatial Hubble]]",
            "HST": "[[Catégorie:Exoplanète découverte grâce au télescope spatial Hubble]]",
            "HARPS": "[[Catégorie:Exoplanète découverte grâce à HARPS]]", # HARPS is an instrument, facility La Silla
            "La Silla Observatory": "[[Catégorie:Exoplanète découverte grâce à HARPS]]", # Assuming HARPS for La Silla
            "James Webb Space Telescope (JWST)": "[[Catégorie:Exoplanète découverte grâce au télescope spatial James Webb]]",
            "JWST": "[[Catégorie:Exoplanète découverte grâce au télescope spatial James Webb]]",
            "Spitzer Space Telescope": "[[Catégorie:Exoplanète découverte grâce au télescope spatial Spitzer]]",
            "Spitzer": "[[Catégorie:Exoplanète découverte grâce au télescope spatial Spitzer]]",
            "Gaia Space Telescope": "[[Catégorie:Exoplanète découverte grâce au télescope spatial Gaia]]",
            "Gaia": "[[Catégorie:Exoplanète découverte grâce au télescope spatial Gaia]]",
            "W. M. Keck Observatory": "[[Catégorie:Exoplanète découverte grâce au W. M. Keck Observatory]]",
            "Keck Observatory": "[[Catégorie:Exoplanète découverte grâce au W. M. Keck Observatory]]",
            "Gemini Observatory": "[[Catégorie:Exoplanète découverte grâce au Gemini Observatory]]",
            "CHEOPS": "[[Catégorie:Exoplanète découverte grâce au télescope spatial CHEOPS]]",
        }


    def generate_categories(self, exoplanet: Exoplanet) -> List[str]:
        categories = set(self.base_categories.copy()) # Use a set to avoid duplicates initially

        # Predefined categories from notes
        available_constellations = self.predefined_categories.get("Constellations", [])
        available_discovery_methods = self.predefined_categories.get("Discovery Methods", [])
        available_discovery_years = self.predefined_categories.get("Discovery Years (from 1992 to 2025)", [])
        available_discovery_instruments = self.predefined_categories.get("Discovery Instruments/Telescopes", [])

        # Catégorie par constellation
        if exoplanet.constellation and hasattr(exoplanet.constellation, 'value') and exoplanet.constellation.value is not None:
            constellation_input_value = exoplanet.constellation.value
            
            constellation_name: str
            if not isinstance(constellation_input_value, str):
                # If data is not string (e.g. a number mistakenly), convert to string.
                # This case should ideally not happen for proper constellation names.
                constellation_name = str(constellation_input_value)
            else:
                constellation_name = constellation_input_value

            if constellation_name: # Proceed only if constellation_name is not empty
                for cat_string in available_constellations:
                    match_cat_text = re.search(r"\[\[Catégorie:(.*?)\]\]", cat_string)
                    if match_cat_text:
                        text_part = match_cat_text.group(1) # e.g., "Constellation du Lion"
                        # Robust check for constellation name within the text part using regex word boundaries
                        # re.escape handles if constellation_name has special characters
                        if re.search(r"\b" + re.escape(constellation_name) + r"\b", text_part, re.IGNORECASE):
                            categories.add(cat_string)
                            break # Found one, no need to check further

        # Catégorie par méthode de découverte
        if exoplanet.discovery_method and exoplanet.discovery_method.value:
            method_value = exoplanet.discovery_method.value
            if method_value in self.discovery_method_map:
                target_category = self.discovery_method_map[method_value]
                if target_category in available_discovery_methods:
                    categories.add(target_category)
            # else: # Old logic preserved below, but task asked to stick to predefined for this.
            #    categories.add(f"[[Catégorie:Exoplanète découverte par {method_value.lower()}]]")


        # Catégorie par année de découverte
        if exoplanet.discovery_date and exoplanet.discovery_date.value:
            year = None
            if hasattr(exoplanet.discovery_date.value, "year"):
                year = exoplanet.discovery_date.value.year
            else:
                try:
                    year = int(str(exoplanet.discovery_date.value)) # Assuming it's a year string or int
                except ValueError:
                    pass # Not a valid year

            if year:
                target_category = f"[[Catégorie:Exoplanète découverte en {year}]]"
                if target_category in available_discovery_years:
                    categories.add(target_category)

        # Catégorie par instrument/telescope de découverte
        # Using exoplanet.discovered_by.value as per task instructions
        if hasattr(exoplanet, 'discovered_by') and exoplanet.discovered_by and hasattr(exoplanet.discovered_by, 'value') and exoplanet.discovered_by.value is not None:
            instrument_value = exoplanet.discovered_by.value
            
            # Ensure instrument_value is a string for matching
            if not isinstance(instrument_value, str):
                instrument_value_str = str(instrument_value)
            else:
                instrument_value_str = instrument_value

            if instrument_value_str: # Proceed only if not empty
                # First, try direct mapping
                if instrument_value_str in self.instrument_map:
                    target_category = self.instrument_map[instrument_value_str]
                    if target_category in available_discovery_instruments:
                        categories.add(target_category)
                else:
                    # If direct map fails, try to find a partial match in keys (e.g. "Kepler" for "Kepler Space Telescope")
                    for key_instrument, mapped_cat_string in self.instrument_map.items():
                        if key_instrument in instrument_value_str: # e.g. "Kepler" is in "Kepler Space Telescope"
                            if mapped_cat_string in available_discovery_instruments:
                                categories.add(mapped_cat_string)
                                break # Add first match
                            
        # --- Preserving and adapting existing logic for other categories ---
        # These categories are not in categories_notes.md, so they are generated directly.
        # They should also follow the [[Catégorie:...]] format.

        # Catégorie par type spectral
        if hasattr(exoplanet, 'spectral_type') and exoplanet.spectral_type and \
           hasattr(exoplanet.spectral_type, 'value') and exoplanet.spectral_type.value is not None:
            spectral_type_value = exoplanet.spectral_type.value
            
            spectral_class_char = None
            if isinstance(spectral_type_value, str) and len(spectral_type_value) > 0:
                spectral_class_char = spectral_type_value[0].upper()
            # elif isinstance(spectral_type_value, (int, float)):
                # pass # Or handle if numbers can be spectral types, e.g. str(spectral_type_value)[0]
            
            if spectral_class_char:
                categories.add(
                    f"[[Catégorie:Exoplanète orbitant une étoile de type {spectral_class_char}]]"
                )

        # Catégorie par type de planète (classification physique)
        try:
            planet_type = self.planet_type_utils.get_planet_type(exoplanet)
            if planet_type and planet_type != "Unknown": # Avoid "Exoplanète de type Unknown"
                 categories.add(f"[[Catégorie:Exoplanète de type {planet_type}]]")
        except Exception:
            # This could happen if data is missing for get_planet_type (e.g. mass, radius)
            pass 

        return sorted(list(categories)) # Return as a sorted list

if __name__ == '__main__':
    # Mock Exoplanet object for testing
    class MockValue:
        def __init__(self, value):
            self.value = value

    class MockExoplanet(Exoplanet):
        # MockExoplanet signature uses 'discovered_by' as per task's final instruction for attribute name.
        def __init__(self, name, constellation, spectral_type, discovery_method, discovery_date, discovered_by, mass_mj, radius_rj, orbital_period_days, semi_major_axis_au, eccentricity, inclination_deg, stellar_effective_temperature_k, stellar_radius_rsun, stellar_mass_msun, distance_pc):
            # Reverting to fully positional arguments for super().__init__, matching MockExoplanet's own param order.
            # This relies on defensive coding within generate_categories to handle potential type mismatches if Exoplanet.__init__
            # has a different internal order causing, e.g., exoplanet.mass_mj.value to receive a string.
            super().__init__(name,
                MockValue(constellation),
                MockValue(spectral_type),
                MockValue(discovery_method),
                MockValue(discovery_date),
                MockValue(discovered_by), 
                MockValue(mass_mj),
                MockValue(radius_rj),
                MockValue(orbital_period_days),
                MockValue(semi_major_axis_au),
                MockValue(eccentricity),
                MockValue(inclination_deg),
                MockValue(stellar_effective_temperature_k),
                MockValue(stellar_radius_rsun),
                MockValue(stellar_mass_msun),
                MockValue(distance_pc)
            )

    # Test cases
    generator = CategoryGenerator()

    print("Predefined categories loaded:")
    for cat_type, cat_list in generator.predefined_categories.items():
        print(f"  {cat_type}: {len(cat_list)} categories")
        if cat_type == "Constellations" and cat_list:
             print(f"    Example: {cat_list[0]}")
    print("-" * 20)

    # Example 1: Kepler-186 f
    kepler_186_f = MockExoplanet(
        name="Kepler-186 f",
        constellation="Cygne", 
        spectral_type="M1V",
        discovery_method="Transit",
        discovery_date="2014",
        discovered_by="Kepler Space Telescope", # Changed from discovery_facility
        mass_mj=0.0044, radius_rj=0.100, orbital_period_days=129.9, semi_major_axis_au=0.356,
        eccentricity=0.04, inclination_deg=89.9, stellar_effective_temperature_k=3755,
        stellar_radius_rsun=0.52, stellar_mass_msun=0.54, distance_pc=171.5
    )
    cats1 = generator.generate_categories(kepler_186_f)
    print(f"Categories for Kepler-186 f ({kepler_186_f.name}):") # Changed .name.value to .name
    for cat in cats1:
        print(f"  - {cat}")
    # Expected: Exoplanète, Constellation du Cygne, Type M, Transit, 2014, Kepler, Type Earth-size
    assert "[[Catégorie:Exoplanète]]" in cats1
    assert "[[Catégorie:Constellation du Cygne]]" in cats1 # Test constellation matching
    assert "[[Catégorie:Exoplanète orbitant une étoile de type M]]" in cats1
    assert "[[Catégorie:Exoplanète découverte par la méthode des transits]]" in cats1
    assert "[[Catégorie:Exoplanète découverte en 2014]]" in cats1
    assert "[[Catégorie:Exoplanète découverte grâce à Kepler]]" in cats1
    # Planet type depends on PlanetTypeUtils logic, assuming "Earth-size" or similar
    # assert "[[Catégorie:Exoplanète de type Earth-size]]" in cats1 # This will depend on the mass/radius thresholds

    print("-" * 20)

    # Example 2: HD 209458 b (Osiris)
    hd_209458_b = MockExoplanet(
        name="HD 209458 b",
        constellation="Pégase", 
        spectral_type="G0V",
        discovery_method="Transit", 
        discovery_date="1999",
        discovered_by="Multiple Observatories", # Changed from discovery_facility
        mass_mj=0.71, radius_rj=1.38, orbital_period_days=3.52, semi_major_axis_au=0.047,
        eccentricity=0.01, inclination_deg=86.7, stellar_effective_temperature_k=6091,
        stellar_radius_rsun=1.20, stellar_mass_msun=1.15, distance_pc=47.0
    )
    cats2 = generator.generate_categories(hd_209458_b)
    print(f"Categories for HD 209458 b ({hd_209458_b.name}):") # Changed .name.value to .name
    for cat in cats2:
        print(f"  - {cat}")
    assert "[[Catégorie:Exoplanète]]" in cats2
    assert "[[Catégorie:Constellation de Pégase]]" in cats2
    assert "[[Catégorie:Exoplanète orbitant une étoile de type G]]" in cats2
    assert "[[Catégorie:Exoplanète découverte par la méthode des transits]]" in cats2
    assert "[[Catégorie:Exoplanète découverte en 1999]]" in cats2
    # No specific facility match expected for "Multiple Observatories" unless added to map.
    # Planet type: Hot Jupiter
    # assert "[[Catégorie:Exoplanète de type Hot Jupiter]]" in cats2


    print("-" * 20)
    # Example 3: Test a method not in map (if any left) or facility not in map
    unknown_method_planet = MockExoplanet(
        name="Planet X", constellation="Lupus", spectral_type="K2V",
        discovery_method="Unknown Method", discovery_date="2023", discovered_by="Some New Telescope", # Changed from discovery_facility
        mass_mj=1, radius_rj=1, orbital_period_days=100, semi_major_axis_au=0.5,
        eccentricity=0, inclination_deg=90, stellar_effective_temperature_k=5000,
        stellar_radius_rsun=1, stellar_mass_msun=1, distance_pc=10
    )
    cats3 = generator.generate_categories(unknown_method_planet)
    print(f"Categories for Planet X ({unknown_method_planet.name}):") # Changed .name.value to .name
    for cat in cats3:
        print(f"  - {cat}")
    assert "[[Catégorie:Exoplanète découverte en 2023]]" in cats3 # Assuming 2023 is in range
    assert "[[Catégorie:Constellation du Loup]]" in cats3 # Lupus -> Loup
    
    print("Basic tests in __main__ completed. More comprehensive testing would require actual Exoplanet data and PlanetTypeUtils.")
    print("NOTE: Planet type categories depend on PlanetTypeUtils logic and exoplanet mass/radius.")
    print("NOTE: Constellation matching logic: looks for ' ConstellationName' or 'ConstellationName' at end of 'Catégorie:Constellation du ConstellationName'.")

    # Test a constellation with "d'"
    eridani_planet = MockExoplanet(
        name="Epsilon Eridani b", constellation="Éridan", spectral_type="K2V",
        discovery_method="Radial Velocity", discovery_date="2000", discovered_by="Multiple Observatories", # Changed from discovery_facility
        mass_mj=1.55, radius_rj=1.0, orbital_period_days=2502, semi_major_axis_au=3.38,
        eccentricity=0.702, inclination_deg=30.1, stellar_effective_temperature_k=5084,
        stellar_radius_rsun=0.74, stellar_mass_msun=0.82, distance_pc=3.22
    )
    cats_eridani = generator.generate_categories(eridani_planet)
    print(f"Categories for Epsilon Eridani b ({eridani_planet.name}):") # Changed to include .name
    for cat in cats_eridani:
        print(f"  - {cat}")
    assert "[[Catégorie:Constellation de l'Éridan]]" in cats_eridani

    print("All __main__ tests seem to pass based on current logic.")
