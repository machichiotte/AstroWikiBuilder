# src/mappers/nasa_exoplanet_archive_mapper.py
from typing import Dict, Any, Optional
from src.models.reference import Reference, SourceType, DataPoint
from src.models.star import Star
from src.models.exoplanet import Exoplanet

from datetime import datetime


class NasaExoplanetArchiveMapper:
    """Mapper pour convertir les données NASA Exoplanet Archive vers le modèle Star"""

    # Mapping des colonnes NASA vers les attributs Star
    NASA_TO_STAR_MAPPING = {
        # Identifiants
        "hostname": "name",
        # Coordonnées
        "ra": "right_ascension",
        "dec": "declination",
        "sy_pmra": "proper_motion_ra",
        "sy_pmdec": "proper_motion_dec",
        "sy_plx": "parallax",
        "sy_dist": "distance_general",
        # Magnitudes
        "sy_bmag": "apparent_magnitude_b_band",
        "sy_vmag": "apparent_magnitude_v_band",
        "sy_jmag": "apparent_magnitude_j_band",
        "sy_hmag": "apparent_magnitude_h_band",
        "sy_kmag": "apparent_magnitude_k_band",
        "sy_gmag": "apparent_magnitude_g_band",
        "sy_rmag": "apparent_magnitude_r_band",
        "sy_imag": "apparent_magnitude_i_band",
        "sy_umag": "apparent_magnitude_u_band",
        "sy_zmag": "apparent_magnitude_z_band",
        "sy_w1mag": "apparent_magnitude_w1_band",
        "sy_w2mag": "apparent_magnitude_w2_band",
        "sy_w3mag": "apparent_magnitude_w3_band",
        "sy_w4mag": "apparent_magnitude_w4_band",
        "sy_gaiamag": "apparent_magnitude_gaia_band",
        "sy_tmag": "apparent_magnitude_t_band",
        "sy_kepmag": "apparent_magnitude_kep_band",
        # Propriétés stellaires
        "st_teff": "temperature",
        "st_mass": "mass",
        "st_rad": "radius",
        "st_met": "metallicity",
        "st_logg": "surface_gravity",
        "st_lum": "luminosity",
        "st_dens": "density",
        "st_age": "age",
        "st_spectype": "spectral_type",
        "st_radv": "radial_velocity",
        "st_rotp": "rotation",
        "st_vsin": "rotation",  # v*sin(i) - peut être mappé sur rotation
    }

    # Mapping des colonnes NASA vers les attributs Exoplanet
    NASA_TO_EXOPLANET_MAPPING = {
        # Identifiants
        "pl_name": "name",
        # ÉTOILE
        "hostname": "star_name",
        # "": "epoch_star",
        "ra": "right_ascension",
        "dec": "declination",
        "sy_dist": "distance_general",
        "st_spectype": "spectral_type",
        "sy_vmag": "apparent_magnitude",
        # PLANÈTE
        # Type
        "": "type",
        # Caractéristiques orbitales
        "pl_orbsmax": "semi_major_axis",
        "pl_orblper": "argument_of_periastron",
        # "": "apoastron",
        "pl_orbeccen": "eccentricity",
        "pl_orbper": "period",
        "pl_angsep": "angular_distance",
        "pl_orbtper": "periastron_time",
        "pl_orbincl": "inclination",
        # "": "longitude_of_periastron",
        # "": "epoch",
        # Caractéristiques physiques
        "pl_bmassj": "mass",
        "pl_msinij": "minimum_mass",
        "pl_radj": "radius",
        "pl_dens": "density",
        # "": "surface_gravity",
        # "": "rotation_period",
        "pl_eqt": "temperature",
        # "": "albedo_bond",
        # Atmosphère
        # "": "pression",
        # "": "composition",
        # "": "wind_speed",
        # Découverte
        # "": "discoverers",
        # "": "program",
        "discoverymethod": "method",
        "disc_year": "discovery_date",
        "disc_facility": "discovery_site",
        # "": "pre_discovery",
        # "": "detection_type",
        # "": "status",
        # Informations supplémentaires
        "pl_altname": "other_names",
    }

    # Unités par défaut pour certains champs NASA
    DEFAULT_UNITS = {
        "ra": "deg",
        "dec": "deg",
        "sy_pmra": "mas/yr",
        "sy_pmdec": "mas/yr",
        "sy_plx": "mas",
        "sy_dist": "pc",
        "st_teff": "K",
        "st_mass": "M☉",
        "st_rad": "R☉",
        "st_met": "dex",
        "st_logg": "log(cm/s²)",
        "st_lum": "L☉",
        "st_dens": "g/cm³",
        "st_age": "Gyr",
        "st_radv": "km/s",
        "st_rotp": "days",
        "st_vsin": "km/s",
        "pl_orbper": "days",  # Unit for orbital period
        "pl_angsep": "arcsec",  # Unit for angular separation
        "pl_orbincl": "deg",  # Unit for orbital inclination
        "pl_msinij": "Mjup",  # Unit for minimum mass (Jupiter masses)
        "pl_dens": "g/cm³",  # Unit for planetary density
        "pl_eqt": "K",  # Unit for equilibrium temperature
        "pl_radj": "Rjup",  # Unit for planetary radius (Jupiter radii)
        "pl_bmassj": "Mjup",  # Unit for planetary mass (Jupiter masses)
    }

    def map_nasa_data_to_star(self, nasa_data: Dict[str, Any]) -> Star:
        """Convertit un dictionnaire de données NASA vers un objet Star"""
        star = Star()

        # Create a NASA reference for all data points originating from this source
        nasa_reference = Reference(
            source=SourceType.NEA,
            update_date=datetime.now(),  # TODO ici il faudrait plutot recuperer la dte depuis le retour de l'api, la date de mise a jour des donnees dans l'api
            consultation_date=datetime.now(),
            star_identifier=nasa_data.get("hostname"),
        )

        for nasa_field, star_attribute in self.NASA_TO_STAR_MAPPING.items():
            if nasa_field in nasa_data:
                value = nasa_data[nasa_field]

                # Créer un DataPoint avec la valeur et l'unité par défaut
                if value is not None and str(value).strip():
                    unit = self.DEFAULT_UNITS.get(nasa_field)
                    datapoint = DataPoint(
                        value=value, unit=unit, reference=nasa_reference
                    )
                    setattr(
                        star, star_attribute, datapoint
                    )  # TODO comprendre a quoi ca sert

        # Traitement spécial pour les désignations
        designations = self._extract_designations(nasa_data)
        if designations:
            star.designations = DataPoint(value=designations)

        # Autres traitements
        # Special handling for right_ascension (rastr or ra)
        if "rastr" in nasa_data and nasa_data["rastr"]:
            formatted_ra = self._format_right_ascension_str(nasa_data["rastr"])
            if formatted_ra:
                star.right_ascension = DataPoint(
                    value=formatted_ra, reference=nasa_reference
                )
        elif "ra" in nasa_data and nasa_data["ra"] is not None:
            try:
                ra_deg = float(nasa_data["ra"])
                formatted_ra_deg = self._format_right_ascension_deg(ra_deg)
                if formatted_ra_deg:
                    star.right_ascension = DataPoint(
                        value=formatted_ra_deg, reference=nasa_reference
                    )
            except (ValueError, TypeError):
                # Handle cases where 'ra' might not be a valid number
                pass

        # Special handling for declination (decstr or dec)
        if "decstr" in nasa_data and nasa_data["decstr"]:
            formatted_dec = self._format_declination_str(nasa_data["decstr"])
            if formatted_dec:
                star.declination = DataPoint(
                    value=formatted_dec, reference=nasa_reference
                )
        elif "dec" in nasa_data and nasa_data["dec"] is not None:
            try:
                dec_deg = float(nasa_data["dec"])
                formatted_dec_deg = self._format_declination_deg(dec_deg)
                if formatted_dec_deg:
                    star.declination = DataPoint(
                        value=formatted_dec_deg, reference=nasa_reference
                    )
            except (ValueError, TypeError):
                # Handle cases where 'dec' might not be a valid number
                pass
        return star

    def map_nasa_data_to_exoplanet(self, nasa_data: Dict[str, Any]) -> Exoplanet:
        """Convertit un dictionnaire de données NASA vers un objet Exoplanet"""
        exoplanet = Exoplanet()
        # Create a NASA reference for all data points originating from this source
        nasa_reference = Reference(
            source=SourceType.NEA,
            update_date=datetime.now(),  # TODO ici il faudrait plutot recuperer la dte depuis le retour de l'api, la date de mise a jour des donnees dans l'api
            consultation_date=datetime.now(),
            star_identifier=nasa_data.get("hostname"),
            planet_identifier=nasa_data.get("pl_name"),
        )

        for nasa_field, exoplanet_attribute in self.NASA_TO_EXOPLANET_MAPPING.items():
            if nasa_field in nasa_data:
                value = nasa_data[nasa_field]

                # Créer un DataPoint avec la valeur et l'unité par défaut
                if value is not None and str(value).strip():
                    unit = self.DEFAULT_UNITS.get(nasa_field)
                    datapoint = DataPoint(value=value, unit=unit)
                    setattr(exoplanet, exoplanet_attribute, datapoint)

        # Special handling for right_ascension (rastr or ra)
        if "rastr" in nasa_data and nasa_data["rastr"]:
            formatted_ra = self._format_right_ascension_str(nasa_data["rastr"])
            if formatted_ra:
                exoplanet.right_ascension = DataPoint(
                    value=formatted_ra, reference=nasa_reference
                )
        elif "ra" in nasa_data and nasa_data["ra"] is not None:
            try:
                ra_deg = float(nasa_data["ra"])
                formatted_ra_deg = self._format_right_ascension_deg(ra_deg)
                if formatted_ra_deg:
                    exoplanet.right_ascension = DataPoint(
                        value=formatted_ra_deg, reference=nasa_reference
                    )
            except (ValueError, TypeError):
                # Handle cases where 'ra' might not be a valid number
                pass

        # Special handling for declination (decstr or dec)
        if "decstr" in nasa_data and nasa_data["decstr"]:
            formatted_dec = self._format_declination_str(nasa_data["decstr"])
            if formatted_dec:
                exoplanet.declination = DataPoint(
                    value=formatted_dec, reference=nasa_reference
                )
        elif "dec" in nasa_data and nasa_data["dec"] is not None:
            try:
                dec_deg = float(nasa_data["dec"])
                formatted_dec_deg = self._format_declination_deg(dec_deg)
                if formatted_dec_deg:
                    exoplanet.declination = DataPoint(
                        value=formatted_dec_deg, reference=nasa_reference
                    )
            except (ValueError, TypeError):
                # Handle cases where 'dec' might not be a valid number
                pass

        if "pl_orbincl" in nasa_data and nasa_data["pl_orbincl"] is not None:
            try:
                pl_orbincl_val = float(nasa_data["pl_orbincl"])
                formatted_inclination = f"{pl_orbincl_val}"
                if (
                    "pl_orbinclerr1" in nasa_data
                    and "pl_orbinclerr2" in nasa_data
                    and nasa_data["pl_orbinclerr1"] is not None
                    and nasa_data["pl_orbinclerr2"] is not None
                ):
                    pl_orbinclerr1_val = float(nasa_data["pl_orbinclerr1"])
                    pl_orbinclerr2_val = float(nasa_data["pl_orbinclerr2"])
                    formatted_inclination = f"{pl_orbincl_val}{{{{±|{pl_orbinclerr1_val}|{pl_orbinclerr2_val}}}}}"
                    exoplanet.inclination = DataPoint(
                        value=formatted_inclination, reference=nasa_reference
                    )
                else:
                    exoplanet.inclination = DataPoint(
                        value=pl_orbincl_val, reference=nasa_reference
                    )
            except (ValueError, TypeError):
                pass

        if "pl_tranmidstr" in nasa_data and nasa_data["pl_tranmidstr"] is not None:
            try:
                pl_tranmidstr = float(nasa_data["pl_tranmidstr"])
                formatted_epoch = self._parse_epoch_string(pl_tranmidstr)
                if formatted_epoch:
                    exoplanet.epoch = DataPoint(
                        value=formatted_epoch, reference=nasa_reference
                    )
            except (ValueError, TypeError):
                pass

        if "pl_orbperstr" in nasa_data and nasa_data["pl_orbperstr"] is not None:
            try:
                pl_orbperstr = float(nasa_data["pl_orbperstr"])
                formatted_orb_per = self._parse_epoch_string(pl_orbperstr)
                if formatted_orb_per:
                    exoplanet.orbital_period = DataPoint(
                        value=formatted_orb_per, reference=nasa_reference
                    )
            except (ValueError, TypeError):
                pass

        return exoplanet

    def _extract_designations(self, nasa_data: Dict[str, Any]) -> Optional[list]:
        """Extrait les différentes désignations d'une étoile"""
        designation_fields = ["hostname", "hd_name", "hip_name", "tic_id"]
        designations = []

        for field in designation_fields:
            if field in nasa_data and nasa_data[field]:
                value = str(nasa_data[field]).strip()
                if value and value not in designations:
                    designations.append(value)

        return designations if designations else None

    def _format_right_ascension_str(self, rastr_val: str) -> str:
        """
        Formats a right ascension string by replacing 'h', 'm', 's'
        with '/' as needed for Wikipedia formatting.

        Example: "12h34m56s" becomes "12/34/56"
        """
        if not isinstance(rastr_val, str):
            # Handle cases where it might not be a string (e.g., NaN, other types)
            return ""  # Return empty string for invalid input

        formatted_ra = rastr_val.replace("h", "/").replace("m", "/").replace("s", "")

        return formatted_ra.strip()

    def _format_declination_str(self, decstr_val: str) -> str:
        """
        Formats a declination string by replacing 'd', 'm', 's'
        with '/' as needed for Wikipedia formatting.

        Example: "+23d45m01s" becomes "+23/45/01"
        """
        if not isinstance(decstr_val, str):
            # Handle cases where it might not be a string
            return ""  # Return empty string for invalid input

        formatted_dec = decstr_val.replace("d", "/").replace("m", "/").replace("s", "")

        return formatted_dec.strip()

    def _format_right_ascension_deg(self, ra_deg: float) -> str:
        """
        Formats a right ascension in degrees to HH/MM/SS.ss.
        Example: 296.2300306 becomes 19/44/55.21
        """
        if ra_deg is None:
            return ""

        # Convert degrees to hours
        hours_float = ra_deg / 15.0
        hours = int(hours_float)
        minutes_float = (hours_float - hours) * 60
        minutes = int(minutes_float)
        seconds_float = (minutes_float - minutes) * 60

        # Format seconds to two decimal places
        seconds = f"{seconds_float:.2f}"

        return f"{hours:02d}/{minutes:02d}/{seconds}"

    def _format_declination_deg(self, dec_deg: float) -> str:
        """
        Formats a declination in degrees to +/-DD/MM/SS.ss.
        Example: 50.2752091 becomes +50/16/30.75
        """
        if dec_deg is None:
            return ""

        sign = "+" if dec_deg >= 0 else "-"
        abs_dec_deg = abs(dec_deg)

        degrees = int(abs_dec_deg)
        arcminutes_float = (abs_dec_deg - degrees) * 60
        arcminutes = int(arcminutes_float)
        arcseconds_float = (arcminutes_float - arcminutes) * 60

        # Format arcseconds to two decimal places
        arcseconds = f"{arcseconds_float:.2f}"

        return f"{sign}{degrees:02d}/{arcminutes:02d}/{arcseconds}"

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
        import pandas as pd
        from bs4 import BeautifulSoup
        import re
        import logging

        logger = logging.getLogger(__name__)

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

        # Case 3 & 4: Greater than or Less than (e.g., "&gt789", "&lt1084")
        elif epoch_str_val.startswith("&gt"):
            return f"> {epoch_str_val[3:].strip()}"
        elif epoch_str_val.startswith("&lt"):
            return f"< {epoch_str_val[3:].strip()}"

        # Case 5: Simple numerical value (as a last resort)
        else:
            try:
                float(epoch_str_val)
                return epoch_str_val
            except ValueError:
                logger.warning(f"Unrecognized epoch format: {epoch_str_val}")
                return None
