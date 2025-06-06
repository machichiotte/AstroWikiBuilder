# src/generators/exoplanet/exoplanet_category_generator_old.py
from typing import List, Dict, Optional, Set
from src.models.data_source_exoplanet import DataSourceExoplanet
from src.utils.exoplanet_type_utils import ExoplanetTypeUtils
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

        self.instrument_map: Dict[str, str] = {
            "Kepler": "[[Catégorie:Exoplanète découverte grâce à Kepler]]",
            "Kepler Space Telescope": "[[Catégorie:Exoplanète découverte grâce à Kepler]]",
            "Transiting Exoplanet Survey Satellite (TESS)": "[[Catégorie:Exoplanète découverte grâce au Transiting Exoplanet Survey Satellite]]",
            "TESS": "[[Catégorie:Exoplanète découverte grâce au Transiting Exoplanet Survey Satellite]]",
            "CoRoT": "[[Catégorie:Exoplanète découverte grâce au télescope spatial CoRoT]]",
            "Very Large Telescope (VLT)": "[[Catégorie:Exoplanète découverte grâce au Very Large Telescope (VLT)]]",
            "VLT": "[[Catégorie:Exoplanète découverte grâce au Very Large Telescope (VLT)]]",
            "Paranal Observatory": "[[Catégorie:Exoplanète découverte grâce au Very Large Telescope (VLT)]]",
            "Hubble Space Telescope": "[[Catégorie:Exoplanète découverte grâce au télescope spatial Hubble]]",
            "HST": "[[Catégorie:Exoplanète découverte grâce au télescope spatial Hubble]]",
            "HARPS": "[[Catégorie:Exoplanète découverte grâce à HARPS]]",
            "La Silla Observatory": "[[Catégorie:Exoplanète découverte grâce à HARPS]]",
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

    def _get_constellation_category(self, exoplanet: DataSourceExoplanet) -> Optional[str]:
        if (
            exoplanet.constellation
            and hasattr(exoplanet.constellation, "value")
            and exoplanet.constellation.value is not None
        ):
            constellation_input_value = exoplanet.constellation.value
            constellation_name: str
            if not isinstance(constellation_input_value, str):
                constellation_name = str(constellation_input_value)
            else:
                constellation_name = constellation_input_value

            if constellation_name:
                available_constellations = self.predefined_categories.get(
                    "Constellations", []
                )
                for cat_string in available_constellations:
                    match_cat_text = re.search(r"\[\[Catégorie:(.*?)\]\]", cat_string)
                    if match_cat_text:
                        text_part = match_cat_text.group(1)
                        if re.search(
                            r"\b" + re.escape(constellation_name) + r"\b",
                            text_part,
                            re.IGNORECASE,
                        ):
                            return cat_string
        return None

    def _get_discovery_method_category(self, exoplanet: DataSourceExoplanet) -> Optional[str]:
        if (
            exoplanet.discovery_method
            and hasattr(exoplanet.discovery_method, "value")
            and exoplanet.discovery_method.value
        ):
            method_value = exoplanet.discovery_method.value
            if method_value in self.discovery_method_map:
                target_category = self.discovery_method_map[method_value]
                available_discovery_methods = self.predefined_categories.get(
                    "Discovery Methods", []
                )
                if target_category in available_discovery_methods:
                    return target_category
        return None

    def _get_discovery_year_category(self, exoplanet: DataSourceExoplanet) -> Optional[str]:
        if (
            exoplanet.discovery_date
            and hasattr(exoplanet.discovery_date, "value")
            and exoplanet.discovery_date.value
        ):
            year = None
            if hasattr(
                exoplanet.discovery_date.value, "year"
            ):  # Handles datetime objects
                year = exoplanet.discovery_date.value.year
            else:  # Handles year as string or int
                try:
                    year = int(str(exoplanet.discovery_date.value))
                except ValueError:
                    pass  # Not a valid year format

            if year:
                target_category = f"[[Catégorie:Exoplanète découverte en {year}]]"
                available_discovery_years = self.predefined_categories.get(
                    "Discovery Years (from 1992 to 2025)", []
                )
                if target_category in available_discovery_years:
                    return target_category
        return None

    def _get_discovery_instrument_category(self, exoplanet: DataSourceExoplanet) -> Optional[str]:
        if (
            hasattr(exoplanet, "discovered_by")
            and exoplanet.discovered_by
            and hasattr(exoplanet.discovered_by, "value")
            and exoplanet.discovered_by.value is not None
        ):
            instrument_value = exoplanet.discovered_by.value
            instrument_value_str = (
                str(instrument_value)
                if not isinstance(instrument_value, str)
                else instrument_value
            )

            if instrument_value_str:
                available_discovery_instruments = self.predefined_categories.get(
                    "Discovery Instruments/Telescopes", []
                )

                # First, try direct mapping
                if instrument_value_str in self.instrument_map:
                    target_category = self.instrument_map[instrument_value_str]
                    if target_category in available_discovery_instruments:
                        return target_category
                else:
                    # If direct map fails, try to find a partial match in keys
                    for (
                        key_instrument,
                        mapped_cat_string,
                    ) in self.instrument_map.items():
                        if key_instrument in instrument_value_str:
                            if mapped_cat_string in available_discovery_instruments:
                                return mapped_cat_string
        return None

    def _get_planet_type_category(self, exoplanet: DataSourceExoplanet) -> Optional[str]:
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
                    # Original code added this directly if pre-formatted.
                    # To strictly adhere to predefined categories, this might need
                    # to be checked against a self.predefined_categories.get("Planet Types", [])
                    # if such a list were maintained. For now, preserving original behavior.
                    return planet_type_value
                # else:
                # The original code had a commented-out 'add' here (categories.add(...commented_out_f_string...)),
                # which means no category was added if planet_type_value was a simple string.
                # Thus, we return None in that case.
        except Exception:
            # This could happen if data is missing for get_planet_type (e.g. mass, radius)
            pass
        return None

    def generate_categories(self, exoplanet: DataSourceExoplanet) -> List[str]:
        categories: Set[str] = set(self.base_categories.copy())

        # List of getter methods for different category types
        category_sources = [
            self._get_constellation_category,
            self._get_discovery_method_category,
            self._get_discovery_year_category,
            self._get_discovery_instrument_category,
            self._get_planet_type_category,
        ]

        for source_func in category_sources:
            category = source_func(exoplanet)
            if category:
                categories.add(category)

        return sorted(list(categories))
