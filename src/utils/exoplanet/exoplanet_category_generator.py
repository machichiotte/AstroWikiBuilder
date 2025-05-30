# src/utils/exoplanet_category_generator.py
from typing import List, Dict
from src.models.exoplanet import Exoplanet
from src.utils.exoplanet.exoplanet_type_utils import ExoplanetTypeUtils
from src.utils.wikipedia.category_parser import parse_categories
import re


class ExoplanetCategoryGenerator:
    """
    Classe pour générer les catégories des articles d'exoplanètes.
    """

    def __init__(self):
        self.predefined_categories: Dict[str, List[str]] = parse_categories()
        self.base_categories: List[str] = ["[[Catégorie:Exoplanète]]"]
        self.planet_type_utils = ExoplanetTypeUtils()

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

        self.instrument_map: Dict[str, str] = {  # Renamed from discovery_facility_map
            # Exact keys here should match exoplanet.discovered_by.value
            # Example: "Kepler Space Telescope" might be just "Kepler" in notes.
            # We need to be careful or use a contains check.
            # For now, let's assume the keys are somewhat aligned or use common names.
            "Kepler": "[[Catégorie:Exoplanète découverte grâce à Kepler]]",
            "Kepler Space Telescope": "[[Catégorie:Exoplanète découverte grâce à Kepler]]",
            "Transiting Exoplanet Survey Satellite (TESS)": "[[Catégorie:Exoplanète découverte grâce au Transiting Exoplanet Survey Satellite]]",
            "TESS": "[[Catégorie:Exoplanète découverte grâce au Transiting Exoplanet Survey Satellite]]",
            "CoRoT": "[[Catégorie:Exoplanète découverte grâce au télescope spatial CoRoT]]",
            "Very Large Telescope (VLT)": "[[Catégorie:Exoplanète découverte grâce au Very Large Telescope (VLT)]]",  # VLT is an instrument, facility Paranal
            "VLT": "[[Catégorie:Exoplanète découverte grâce au Very Large Telescope (VLT)]]",
            "Paranal Observatory": "[[Catégorie:Exoplanète découverte grâce au Very Large Telescope (VLT)]]",  # Assuming VLT for Paranal
            "Hubble Space Telescope": "[[Catégorie:Exoplanète découverte grâce au télescope spatial Hubble]]",
            "HST": "[[Catégorie:Exoplanète découverte grâce au télescope spatial Hubble]]",
            "HARPS": "[[Catégorie:Exoplanète découverte grâce à HARPS]]",  # HARPS is an instrument, facility La Silla
            "La Silla Observatory": "[[Catégorie:Exoplanète découverte grâce à HARPS]]",  # Assuming HARPS for La Silla
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

    def generate_exoplanet_categories(self, exoplanet: Exoplanet) -> List[str]:
        categories = set(
            self.base_categories.copy()
        )  # Use a set to avoid duplicates initially

        # Predefined categories from notes
        available_constellations = self.predefined_categories.get("Constellations", [])
        available_discovery_methods = self.predefined_categories.get(
            "Discovery Methods", []
        )
        available_discovery_years = self.predefined_categories.get(
            "Discovery Years (from 1992 to 2025)", []
        )
        available_discovery_instruments = self.predefined_categories.get(
            "Discovery Instruments/Telescopes", []
        )

        # Catégorie par constellation
        if (
            exoplanet.constellation
            and hasattr(exoplanet.constellation, "value")
            and exoplanet.constellation.value is not None
        ):
            constellation_input_value = exoplanet.constellation.value

            constellation_name: str
            if not isinstance(constellation_input_value, str):
                # If data is not string (e.g. a number mistakenly), convert to string.
                # This case should ideally not happen for proper constellation names.
                constellation_name = str(constellation_input_value)
            else:
                constellation_name = constellation_input_value

            if constellation_name:  # Proceed only if constellation_name is not empty
                for cat_string in available_constellations:
                    match_cat_text = re.search(r"\[\[Catégorie:(.*?)\]\]", cat_string)
                    if match_cat_text:
                        text_part = match_cat_text.group(
                            1
                        )  # e.g., "Constellation du Lion"
                        # Robust check for constellation name within the text part using regex word boundaries
                        # re.escape handles if constellation_name has special characters
                        if re.search(
                            r"\b" + re.escape(constellation_name) + r"\b",
                            text_part,
                            re.IGNORECASE,
                        ):
                            categories.add(cat_string)
                            break  # Found one, no need to check further

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
                    year = int(
                        str(exoplanet.discovery_date.value)
                    )  # Assuming it's a year string or int
                except ValueError:
                    pass  # Not a valid year

            if year:
                target_category = f"[[Catégorie:Exoplanète découverte en {year}]]"
                if target_category in available_discovery_years:
                    categories.add(target_category)

        # Catégorie par instrument/telescope de découverte
        # Using exoplanet.discovered_by.value as per task instructions
        if (
            hasattr(exoplanet, "discovered_by")
            and exoplanet.discovered_by
            and hasattr(exoplanet.discovered_by, "value")
            and exoplanet.discovered_by.value is not None
        ):
            instrument_value = exoplanet.discovered_by.value

            # Ensure instrument_value is a string for matching
            if not isinstance(instrument_value, str):
                instrument_value_str = str(instrument_value)
            else:
                instrument_value_str = instrument_value

            if instrument_value_str:  # Proceed only if not empty
                # First, try direct mapping
                if instrument_value_str in self.instrument_map:
                    target_category = self.instrument_map[instrument_value_str]
                    if target_category in available_discovery_instruments:
                        categories.add(target_category)
                else:
                    # If direct map fails, try to find a partial match in keys (e.g. "Kepler" for "Kepler Space Telescope")
                    for (
                        key_instrument,
                        mapped_cat_string,
                    ) in self.instrument_map.items():
                        if (
                            key_instrument in instrument_value_str
                        ):  # e.g. "Kepler" is in "Kepler Space Telescope"
                            if mapped_cat_string in available_discovery_instruments:
                                categories.add(mapped_cat_string)
                                break  # Add first match

        # Catégorie par type de planète (classification physique)
        try:
            planet_type_value = self.planet_type_utils.get_exoplanet_planet_type(
                exoplanet
            )
            if planet_type_value and planet_type_value != "Unknown":
                # Check if planet_type_value is already a fully wrapped category string
                if (
                    isinstance(planet_type_value, str)
                    and planet_type_value.startswith("[[Catégorie:")
                    and planet_type_value.endswith("]]")
                ):
                    categories.add(planet_type_value)  # Add as-is
                else:
                    # If not fully wrapped, or not a string, ensure it's stringified and then wrap it.
                    # (get_planet_type should ideally return a simple string type name or "Unknown")
                    categories.add(
                        #  f"[[Catégorie:Exoplanète de type {str(planet_type_value)}]]"
                    )
        except Exception:
            # This could happen if data is missing for get_planet_type (e.g. mass, radius)
            pass

        return sorted(list(categories))  # Return as a sorted list
