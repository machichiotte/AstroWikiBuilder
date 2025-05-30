# src/data_collectors/nasa_exoplanet_archive.py
import pandas as pd
from typing import List, Optional, Dict, Any
import logging
import re
import math

from bs4 import BeautifulSoup

from src.data_collectors.base_collector import BaseExoplanetCollector
from src.models.exoplanet import Exoplanet
from src.models.star import Star

from src.models.reference import DataPoint, Reference, SourceType

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NASAExoplanetArchiveCollector(BaseExoplanetCollector):
    def __init__(
        self,
        cache_dir: str = "data/cache/nasa_exoplanet_archive",
        use_mock_data: bool = False,
    ):
        super().__init__(cache_dir, use_mock_data)

    def _get_default_cache_filename(self) -> str:
        return "nasa_mock_data.csv"

    def _get_download_url(self) -> str:
        return "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+*+from+PSCompPars&format=csv"

    def _get_source_type(self) -> SourceType:
        return SourceType.NEA

    def _get_source_reference_url(self) -> str:
        return "https://exoplanetarchive.ipac.caltech.edu/"

    def _get_required_columns(self) -> List[str]:
        return ["pl_name", "hostname", "discoverymethod", "disc_year"]

    def _get_csv_reader_kwargs(self) -> Dict[str, Any]:
        # Le fichier téléchargé de NASA n'a pas de lignes de commentaire typiques à ignorer avec '#' au début.
        # Si le fichier que vous sauvegardez/mockez en a, ajustez ici.
        return {}

    def load_data(self) -> tuple[List[Exoplanet], List[Star]]:
        df = self._get_data_frame()
        if df is None or df.empty:
            logger.info("Aucune donnée à traiter.")
            return [], []

        exoplanets: List[Exoplanet] = []
        stars: List[Star] = []
        base_ref = Reference(
            source=self._get_source_type(),
            url=self._get_source_reference_url(),
            consultation_date=pd.Timestamp.now(
                tz="UTC"
            ),  # Date de consultation actuelle
            update_date=self._get_data_update_date(
                df
            ),  # Date de mise à jour des données de la source
        )

        for _, row in df.iterrows():
            exoplanet = self._convert_row_to_exoplanet(row, base_ref)
            if exoplanet:
                exoplanets.append(exoplanet)

            star = self._convert_row_to_star(row, base_ref)
            if star:
                # Avoid duplicates if multiple planets for the same star are processed
                if not any(s.name.value == star.name.value for s in stars):
                    stars.append(star)
        return exoplanets, stars

    def _convert_row_to_exoplanet(
        self, row: pd.Series, ref: Reference
    ) -> Optional[Exoplanet]:
        try:
            pl_name_val = row.get("pl_name")
            hostname_val = row.get("hostname")

            if pd.isna(pl_name_val) or pd.isna(hostname_val):
                logger.warning(
                    f"Données de base manquantes pour l'exoplanète : {row.get('pl_name', 'Unknown')} (Source: NASA Exoplamet Archive)"
                )
                return None

            nea_ref = Reference(
                source=ref.source,
                update_date=ref.update_date,
                consultation_date=ref.consultation_date,
                planet_identifier=str(pl_name_val).strip(),
                star_identifier=str(hostname_val).strip(),
            )

            exoplanet = Exoplanet(
                name=str(row["pl_name"]).strip(),
                host_star=DataPoint(str(row["hostname"]).strip(), nea_ref),
                discovery_method=DataPoint(str(row["discoverymethod"]).strip(), nea_ref)
                if pd.notna(row["discoverymethod"])
                else None,
                discovery_date=DataPoint(str(row["disc_year"]).strip(), nea_ref)
                if pd.notna(row["disc_year"])
                else None,
            )

            (
                formatted_ra,
                formatted_dec,
                formatted_epoch,
                formatted_orb_per,
                formatted_inclination,
            ) = None, None, None, None, None
            if pd.notna(row.get("rastr")):
                formatted_ra = self._format_right_ascension(str(row["rastr"]).strip())
            if pd.notna(row.get("decstr")):
                formatted_dec = self._format_declination(str(row["decstr"]).strip())
            if pd.notna(row.get("pl_tranmidstr")):
                formatted_epoch = self._parse_epoch_string(row.get("pl_tranmidstr"))
            if pd.notna(row.get("pl_orbperstr")):
                formatted_orb_per = self._parse_epoch_string(row.get("pl_orbperstr"))
            if (
                pd.notna(row.get("pl_orbincl"))
                and pd.notna(row.get("pl_orbinclerr1"))
                and pd.notna(row.get("pl_orbinclerr2"))
            ):
                pl_orbincl_val = row["pl_orbincl"]
                pl_orbinclerr1_val = abs(
                    self._safe_float_conversion(row["pl_orbinclerr1"])
                )
                pl_orbinclerr2_val = abs(
                    self._safe_float_conversion(row["pl_orbinclerr2"])
                )
                if pl_orbinclerr1_val is not None and pl_orbinclerr2_val is not None:
                    formatted_inclination = f"{pl_orbincl_val}{{{{±|{pl_orbinclerr1_val}|{pl_orbinclerr2_val}}}}}"

            if formatted_ra:
                exoplanet.right_ascension = DataPoint(formatted_ra, nea_ref)
            if formatted_dec:
                exoplanet.declination = DataPoint(formatted_dec, nea_ref)
            if formatted_epoch:
                exoplanet.epoch = DataPoint(formatted_epoch, nea_ref)
            if formatted_orb_per:
                exoplanet.orbital_period = DataPoint(formatted_orb_per, nea_ref)
            if formatted_inclination:
                exoplanet.inclination = DataPoint(formatted_inclination, nea_ref)

            orbital_fields_map = {
                "semi_major_axis": ("pl_orbsmax", None),
                "eccentricity": ("pl_orbeccen", None),
                "argument_of_periastron": ("pl_orblper", None),
                "periastron_time": ("pl_orbtper", None),
            }

            for field, (csv_field, unit) in orbital_fields_map.items():
                value = self._safe_float_conversion(row.get(csv_field))
                if value is not None:
                    setattr(exoplanet, field, DataPoint(value, nea_ref, unit))

            # Caractéristiques physiques
            for field, csv_field, unit in [
                ("mass", "pl_bmassj", None),
                ("radius", "pl_radj", None),
                ("temperature", "pl_eqt", None),
            ]:
                value = self._safe_float_conversion(row.get(csv_field))
                if value is not None:
                    setattr(exoplanet, field, DataPoint(value, nea_ref, unit))

            # Informations sur l'étoile
            for field, csv_field, unit in [
                ("spectral_type", "st_spectype", None),
                ("distance", "sy_dist", None),
                ("apparent_magnitude", "sy_vmag", None),
            ]:
                value = row.get(csv_field)
                if pd.notna(value):
                    processed_value = (
                        self._safe_float_conversion(value)
                        if isinstance(value, (int, float, str))
                        and str(value).replace(".", "", 1).isdigit()
                        else str(value).strip()
                    )
                    if processed_value is not None:
                        setattr(
                            exoplanet, field, DataPoint(processed_value, nea_ref, unit)
                        )

            if pd.notna(row.get("pl_altname")):
                names = str(row["pl_altname"]).split(",")
                for name in names:
                    name = name.strip()
                    if name and name != exoplanet.name:
                        exoplanet.other_names.append(name)

            return exoplanet

        except Exception as e:
            logger.error(
                f"Erreur NASA lors de la conversion de la ligne : {row.get('pl_name', 'Unknown')}. Erreur: {e}",
                exc_info=True,
            )
            return None

    def _safe_float_conversion(self, value: Any) -> Optional[float]:
        """
        Safely converts a value to float, handling potential errors, NaN, and empty strings.
        """
        if value is None or (isinstance(value, str) and not value.strip()):
            return None
        if pd.isna(value):  # Handles numpy.nan, pandas.NaT, etc.
            return None
        try:
            return float(value)
        except (ValueError, TypeError):
            # logger.warning(f"Could not convert value '{value}' to float.") # Optional
            return None

    def _get_optional_float(self, row: pd.Series, col_name: str) -> Optional[float]:
        """Helper to get a float value from a row, converting safely."""
        return self._safe_float_conversion(row.get(col_name))

    def _get_optional_string(self, row: pd.Series, col_name: str) -> Optional[str]:
        """Helper to get a stripped string value from a row if it's not NA."""
        val = row.get(col_name)
        if pd.isna(val) or str(val).strip() == "":
            return None
        return str(val).strip()

    def _convert_row_to_star(self, row: pd.Series, ref: Reference) -> Optional[Star]:
        """
        Converts a pandas Series (row from a CSV/DataFrame) to a Star object,
        populating it with data based on predefined mappings.
        """
        try:
            hostname_val = self._get_optional_string(row, "hostname")
            if not hostname_val:
                logger.warning(
                    f"Star name (hostname) is missing or empty for a row. Skipping star creation. Row data: {row.to_dict()}"
                )
                return None
            star_name = hostname_val

            # Create a specific reference for this star, derived from the general reference
            star_ref = Reference(
                source=ref.source,
                update_date=ref.update_date,
                consultation_date=ref.consultation_date,
                star_identifier=star_name,
            )

            star = Star(name=DataPoint(star_name, star_ref))

            # --- Identifiers ---
            designations_list = [star_name]
            # Common catalog names to include in designations
            for col in ["hd_name", "hip_name", "tic_id", "gaia_id"]:
                val = self._get_optional_string(row, col)
                if val:
                    designations_list.append(val)
            # Remove duplicates by converting to set and back to list
            star.designations = DataPoint(list(set(designations_list)), star_ref)

            # --- Astrometry ---
            # Right Ascension (RA) - Preferring string version (e.g., "14h29m42.95s")
            rastr_val = self._get_optional_string(row, "rastr")
            if rastr_val:
                formatted_ra_star = self._format_right_ascension(rastr_val)
                star.right_ascension = DataPoint(formatted_ra_star, star_ref)
            else:  # Fallback to decimal degrees if string version is not available
                ra_deg_val = self._get_optional_float(row, "ra")
                if ra_deg_val is not None:
                    star.right_ascension = DataPoint(ra_deg_val, star_ref, "deg")

            # Declination (Dec) - Preferring string version (e.g., "-62d40m46.1s")
            decstr_val = self._get_optional_string(row, "decstr")
            if decstr_val:
                formatted_dec_star = self._format_declination(decstr_val)
                star.declination = DataPoint(formatted_dec_star, star_ref)
            else:  # Fallback to decimal degrees
                dec_deg_val = self._get_optional_float(row, "dec")
                if dec_deg_val is not None:
                    star.declination = DataPoint(dec_deg_val, star_ref, "deg")

            # Epoch (using discovery year as a general epoch for the data)
            # Note: Coordinate epoch (e.g., J2000) might be different and often isn't in basic CSVs.
            disc_year_val = self._get_optional_float(row, "disc_year")
            if disc_year_val is not None:
                star.epoch = DataPoint(str(int(disc_year_val)), star_ref)

            # Other numeric astrometry fields
            numeric_astro_map = {
                "radial_velocity": ("st_radv", None),  # Stellar Radial Velocity
                "proper_motion_ra": ("sy_pmra", None),  # System Proper Motion in RA
                "proper_motion_dec": (
                    "sy_pmdec",
                    "",
                ),  # System Proper Motion in Dec
                "parallax": ("sy_plx", None),  # System Parallax
            }
            for field, (csv_col, unit) in numeric_astro_map.items():
                value = self._get_optional_float(row, csv_col)
                if value is not None:
                    setattr(star, field, DataPoint(value, star_ref, unit))

            # Distance
            dist_pc_val = self._get_optional_float(row, "sy_dist")

            star.distance = DataPoint(dist_pc_val, star_ref, "")

            # --- Photometry ---
            # Apparent magnitudes in various bands
            photometry_map = {
                # Star model attribute : (CSV column, unit (None for magnitudes))
                "apparent_magnitude_u_band": ("sy_umag", None),  # U-band
                "apparent_magnitude_b_band": ("sy_bmag", None),  # B-band
                "apparent_magnitude_v_band": ("sy_vmag", None),  # V-band (explicit)
                "apparent_magnitude_g_band": ("sy_gmag", None),  # Gaia G-band
                "apparent_magnitude_r_band": ("sy_rmag", None),  # R-band
                "apparent_magnitude_i_band": ("sy_imag", None),  # I-band
                "apparent_magnitude_j_band": ("sy_jmag", None),  # J-band
                "apparent_magnitude_h_band": ("sy_hmag", None),  # H-band
                "apparent_magnitude_k_band": ("sy_kmag", None),  # K-band
            }
            magnitudes_retrieved = {}  # To store successfully retrieved magnitudes for color index calculation
            for field, (csv_col, unit) in photometry_map.items():
                value = self._get_optional_float(row, csv_col)
                if value is not None:
                    setattr(star, field, DataPoint(value, star_ref, unit))
                    magnitudes_retrieved[csv_col] = (
                        value  # Store by CSV column name for easy lookup
                    )

            # Calculate Color Indices (e.g., B-V)
            if "sy_umag" in magnitudes_retrieved and "sy_bmag" in magnitudes_retrieved:
                star.u_b_color = DataPoint(
                    round(
                        magnitudes_retrieved["sy_umag"]
                        - magnitudes_retrieved["sy_bmag"],
                        3,
                    ),
                    star_ref,
                )
            if "sy_bmag" in magnitudes_retrieved and "sy_vmag" in magnitudes_retrieved:
                star.b_v_color = DataPoint(
                    round(
                        magnitudes_retrieved["sy_bmag"]
                        - magnitudes_retrieved["sy_vmag"],
                        3,
                    ),
                    star_ref,
                )
            if "sy_vmag" in magnitudes_retrieved and "sy_rmag" in magnitudes_retrieved:
                star.v_r_color = DataPoint(
                    round(
                        magnitudes_retrieved["sy_vmag"]
                        - magnitudes_retrieved["sy_rmag"],
                        3,
                    ),
                    star_ref,
                )
            if "sy_rmag" in magnitudes_retrieved and "sy_imag" in magnitudes_retrieved:
                star.r_i_color = DataPoint(
                    round(
                        magnitudes_retrieved["sy_rmag"]
                        - magnitudes_retrieved["sy_imag"],
                        3,
                    ),
                    star_ref,
                )
            if "sy_jmag" in magnitudes_retrieved and "sy_kmag" in magnitudes_retrieved:
                star.j_k_color = DataPoint(
                    round(
                        magnitudes_retrieved["sy_jmag"]
                        - magnitudes_retrieved["sy_kmag"],
                        3,
                    ),
                    star_ref,
                )
            if "sy_jmag" in magnitudes_retrieved and "sy_hmag" in magnitudes_retrieved:
                star.j_h_color = DataPoint(
                    round(
                        magnitudes_retrieved["sy_jmag"]
                        - magnitudes_retrieved["sy_hmag"],
                        3,
                    ),
                    star_ref,
                )

            # Absolute Magnitude (M_V)
            # Formula: M = m - 5 * (log10(d_pc) - 1)
            app_mag_v = magnitudes_retrieved.get(
                "sy_vmag"
            )  # Use V-band apparent magnitude
            if app_mag_v is not None and dist_pc_val is not None and dist_pc_val > 0:
                abs_mag_val = app_mag_v - 5 * (math.log10(dist_pc_val) - 1)
                star.absolute_magnitude = DataPoint(
                    round(abs_mag_val, 3), star_ref
                )  # Unit is implicitly mag

            # --- Physical Characteristics ---
            spectral_type_val = self._get_optional_string(
                row, "st_spectype"
            )  # Stellar Spectral Type
            if spectral_type_val:
                star.spectral_type = DataPoint(spectral_type_val, star_ref)

            physical_char_map = {
                # Star model attribute :
                "temperature": ("st_teff", None),  # Stellar Effective Temperature
                "mass": ("st_mass", None),  # Stellar Mass (Solar masses)
                "radius": ("st_rad", None),  # Stellar Radius (Solar radii)
                "density": ("st_dens", None),  # Stellar Density
                "surface_gravity": (
                    "st_logg",
                    None,
                ),  # Stellar Surface Gravity (log10(cm/s^2))
                "luminosity": (
                    "st_lum",
                    None,
                ),  # Stellar Luminosity (log10(Solar Lum))
                "metallicity": (
                    "st_met",
                    None,
                ),  # Stellar Metallicity ([Fe/H] ratio)
                "rotation": (
                    "st_vsin",
                    None,
                ),
                "age": ("st_age", None),  # Stellar Age
            }
            for field, (csv_col, unit) in physical_char_map.items():
                value = self._get_optional_float(row, csv_col)
                if value is not None:
                    setattr(star, field, DataPoint(value, star_ref, unit))

            # --- System Components ---
            sys_components_map = {
                "stellar_components": (
                    "sy_snum",
                    None,
                ),
                "planets": ("sy_pnum", None),
            }
            for field, (csv_col, unit) in sys_components_map.items():
                val_str = self._get_optional_string(row, csv_col)
                if val_str:
                    try:
                        # Convert to float first to handle "2.0", then to int
                        count_val = int(float(val_str))
                        setattr(star, field, DataPoint(count_val, star_ref, unit))
                    except ValueError:
                        logger.warning(
                            f"Could not convert system component '{csv_col}' value '{val_str}' to int for {star_name}"
                        )

            # Note: Fields for secondary stellar components (e.g., mass_2, right_ascension_2) and
            # binary orbital parameters (e.g., semi_major_axis for star-star binary) are not
            # typically found in exoplanet host star CSVs like the one described by columns_exo_star.md.
            # If such data is available under different column names, this mapping would need to be extended.

            return star
        except KeyError as e:
            logger.error(
                f"KeyError while converting row to Star for {row.get('hostname', 'Unknown')}: {e}. "
                f"Available columns: {row.index.tolist()}",
                exc_info=True,  # Set to False in production if too verbose
            )
            return None
        except Exception as e:  # Catch any other unexpected errors
            logger.error(
                f"Unexpected error converting row to Star for {row.get('hostname', 'Unknown')}: {e}",
                exc_info=True,  # Set to False in production if too verbose
            )
            return None

    def _format_right_ascension(self, rastr_val: str) -> str:
        """
        Formats a right ascension string by replacing 'h', 'm', 's'
        with '/' as needed for Wikipedia formatting.

        Example: "12h34m56s" becomes "12/34/56"
        """
        if not isinstance(rastr_val, str):
            # Handle cases where it might not be a string (e.g., NaN, other types)
            return str(rastr_val)  # Or raise an error, or return a default value

        formatted_ra = rastr_val.replace("h", "/").replace("m", "/").replace("s", "")
        return formatted_ra

    def _format_declination(self, decstr_val: str) -> str:
        """
        Formats a declination string by replacing 'd', 'm', 's'
        with '/' as needed for Wikipedia formatting.

        Example: "+23d45m01s" becomes "+23/45/01"
        """
        if not isinstance(decstr_val, str):
            # Handle cases where it might not be a string
            return str(decstr_val)

        formatted_dec = decstr_val.replace("d", "/").replace("m", "/").replace("s", "")
        return formatted_dec

    def _parse_epoch_string(self, epoch_str: str) -> Optional[str]:
        """
        Parses the epoch string (pl_tranmidstr) which can be in several formats:
        1. "2458950.09242&plusmn0.00076" -> "2458950.09242 ± 0.00076"
        2. "<div><span class=supersubNumber">2458360.0754</span><span class="superscript">+0.0049</span><span class="subscript">-0.0078</span></div>"
           -> "2458360.0754{{±|0.0049|0.0078}}"
        3. "2458360.0754" (a simple numerical value) -> "2458360.0754"
        4. "&gt789" -> "> 789"
        5. "&lt1084" -> "< 1084"

        Returns the formatted string or None if parsing fails.
        """
        if pd.isna(epoch_str) or not isinstance(epoch_str, str):
            return None

        epoch_str_val = epoch_str.strip()

        # Case 1: Simple string with &plusmn
        if "&plusmn" in epoch_str_val:
            return epoch_str_val.replace("&plusmn", " ± ")

        # Case 2: HTML snippet
        elif "div" in epoch_str_val and "<span" in epoch_str_val:
            # Pre-process the HTML to fix the common malformation: class=value" -> class="value"
            fixed_html_str = re.sub(r'class=(\w+)"', r'class="\1"', epoch_str_val)
            soup = BeautifulSoup(fixed_html_str, "html5lib")

            base_value_span = soup.find("span", class_="supersubNumber")
            superscript_span = soup.find("span", class_="superscript")
            subscript_span = soup.find("span", class_="subscript")

            if base_value_span:
                formatted_epoch = base_value_span.get_text().strip()
                error_part = ""

                pos_error = (
                    superscript_span.get_text().strip().replace("+", "")
                    if superscript_span
                    else ""
                )
                neg_error = (
                    subscript_span.get_text().strip().replace("-", "")
                    if subscript_span
                    else ""
                )

                if pos_error and neg_error:
                    error_part = f"{{{{±|{pos_error}|{neg_error}}}}}"
                elif pos_error:
                    error_part = f"{{{{±|{pos_error}|}}}}"
                elif neg_error:
                    error_part = f"{{{{±||{neg_error}}}}}"

                return formatted_epoch + error_part
            else:
                logger.warning(
                    f"Could not find base value span in HTML epoch (even after fixing and html5lib): {epoch_str_val}"
                )
                return None

        # Case 4 & 5: Greater than or Less than (e.g., "&gt789", "&lt1084")
        elif epoch_str_val.startswith("&gt"):
            return f"> {epoch_str_val[3:].strip()}"
        elif epoch_str_val.startswith("&lt"):
            return f"< {epoch_str_val[3:].strip()}"

        # Case 3: Simple numerical value (as a last resort)
        else:
            try:
                float(epoch_str_val)
                return epoch_str_val
            except ValueError:
                logger.warning(f"Unrecognized epoch format: {epoch_str_val}")
                return None
