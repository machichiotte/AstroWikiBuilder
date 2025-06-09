# src/mappers/nasa_exoplanet_archive_mapper.py
from typing import Dict, Any, Optional
from src.models.reference import Reference, SourceType, DataPoint
from src.models.data_source_star import DataSourceStar
from src.models.data_source_exoplanet import DataSourceExoplanet

from datetime import datetime
from src.utils.formatters.infobox_field_formatters import FieldFormatter
from src.constants.field_mappings import FIELD_DEFAULT_UNITS_STAR, FIELD_DEFAULT_UNITS_EXOPLANET
import math


class NasaExoplanetArchiveMapper:
    """Mapper pour convertir les données NEA Exoplanet Archive vers le modèle Star"""

    # Mapping des colonnes NEA vers les attributs Star
    NEA_TO_STAR_MAPPING = {
        # Identifiants
        "hostname": "st_name",
        # Coordonnées
        "ra": "st_right_ascension",
        "dec": "st_declination",
        "sy_pmra": "st_proper_motion_ra",
        "sy_pmdec": "st_proper_motion_dec",
        "sy_plx": "st_parallax",
        "sy_dist": "st_distance",

        # Magnitudes
        "sy_bmag": "st_mag_b",
        "sy_vmag": "st_mag_v",
        "sy_jmag": "st_mag_j",
        "sy_hmag": "st_mag_h",
        "sy_kmag": "st_mag_k",
        "sy_gmag": "st_mag_g",
        "sy_rmag": "st_mag_r",
        "sy_imag": "st_mag_i",
        "sy_umag": "st_mag_u",
        "sy_zmag": "st_mag_z",
        "sy_w1mag": "st_mag_w1",
        "sy_w2mag": "st_mag_w2",
        "sy_w3mag": "st_mag_w3",
        "sy_w4mag": "st_mag_w4",
        "sy_gaiamag": "st_mag_gaia",
        "sy_tmag": "st_mag_t",
        "sy_kepmag": "st_mag_kep",
        # Propriétés stellaires
        "st_teff": "st_temperature",
        "st_mass": "st_mass",
        "st_rad": "st_radius",
        "st_met": "st_metallicity",
        "st_logg": "st_surface_gravity",
        "st_lum": "st_luminosity",
        "st_dens": "st_density",
        "st_age": "st_age",
        "st_spectype": "st_spectral_type",
        "st_radv": "st_radial_velocity",
        "st_rotp": "st_rotation",
    }

    # Mapping des colonnes NEA vers les attributs Exoplanet
    NEA_TO_EXOPLANET_MAPPING = {
        # Identifiants
        "pl_name": "pl_name",
        "pl_altname": "pl_altname",

        # Étoile hôte
        "hostname": "st_name",
        # "": "st_epoch",
        "ra": "st_right_ascension",
        "dec": "st_declination",
        "sy_dist": "st_distance",
        "st_spectype": "st_spectral_type",
        "sy_vmag": "st_apparent_magnitude",

        # PLANÈTE

        # Caractéristiques orbitales
        "pl_orbsmax": "pl_semi_major_axis",
        # "": "pl_periastron",
        # "": "pl_apoastron",
        "pl_orbeccen": "pl_eccentricity",
        "pl_orbper": "pl_orbital_period",
        "pl_angsep": "pl_angular_distance",
        "pl_orbtper": "pl_periastron_time",
        "pl_orbincl": "pl_inclination",
        "pl_orblper": "pl_argument_of_periastron",
        # "": "pl_epoch",

        # Caractéristiques physiques
        "pl_bmassj": "pl_mass",
        "pl_msinij": "pl_minimum_mass",
        "pl_radj": "pl_radius",
        "pl_dens": "pl_density",
        # "": "pl_gravity",
        # "": "pl_rotation_period",
        "pl_eqt": "pl_temperature",
        # "": "pl_albedo_bond",

        # Atmosphère
        # "": "pl_pressure",
        # "": "pl_composition",
        # "": "pl_wind_speed",

        # Découverte
        # "": "disc_by",
        # "": "disc_program",
        "discoverymethod": "disc_method",
        "disc_year": "disc_year",
        "disc_facility": "disc_facility",
        # "": "pre_discovery",
        # "": "detection_type",
        # "": "status",
        # Informations supplémentaires
    }

    # Unités par défaut pour certains champs NEA
    NEA_DEFAULT_UNITS: dict[str, str] = {
        # --- Coordonnées et mouvements ---
        "ra": "°",                     # Ascension droite
        "dec": "°",                    # Déclinaison
        "sy_pmra": "mas/an",          # mouvement propre en RA
        "sy_pmdec": "mas/an",         # mouvement propre en DEC
        "sy_plx": "mas",              # parallaxe
        "sy_dist": "pc",              # parsecs

        # --- Étoile (préfixe st_) ---
        "st_teff": "K",               # Température effective
        "st_mass": "M☉",              # Masse stellaire
        "st_rad": "R☉",               # Rayon stellaire
        "st_met": "[Fe/H]",           # Métallicité (dex mais exprimée [Fe/H])
        "st_logg": "log g",           # Gravité de surface log g
        "st_lum": "L☉",               # Luminosité stellaire
        "st_dens": "g/cm³",           # Densité stellaire
        "st_age": "Ga",               # Âge stellaire
        "st_radv": "km/s",            # Vitesse radiale
        "st_rotp": "j",               # Période de rotation (jours)
        "st_vsin": "km/s",            # Vitesse de rotation projetée

        # --- Planète (préfixe pl_) ---
        "pl_orbper": "j",             # Période orbitale (jours)
        "pl_angsep": "″",             # Séparation angulaire (arcsec)
        "pl_orbincl": "°",            # Inclinaison orbitale
        "pl_msinij": "MJ",            # Masse minimum (Jupiter)
        "pl_bmassj": "MJ",            # Masse brute (Jupiter)
        "pl_radj": "RJ",              # Rayon (Jupiter)
        "pl_dens": "g/cm³",           # Densité planétaire
        "pl_eqt": "K",                # Température d'équilibre
    }

    def map_nea_data_to_star(self, nea_data: Dict[str, Any]) -> DataSourceStar:
        """Convertit un dictionnaire de données NEA vers un objet Star"""
        star = DataSourceStar()

        # Create a NEA reference for all data points originating from this source
        nea_reference = Reference(
            source=SourceType.NEA,
            # TODO ici il faudrait plutot recuperer la dte depuis le retour de l'api, la date de mise a jour des donnees dans l'api
            update_date=datetime.now(),
            consultation_date=datetime.now(),
            star_identifier=nea_data.get("hostname"),
        )

        for nea_field, star_attribute in self.NEA_TO_STAR_MAPPING.items():
            if nea_field in nea_data:
                value = nea_data[nea_field]

                # Créer un DataPoint avec la valeur et l'unité par défaut
                if value is not None and str(value).strip() and not (isinstance(value, float) and math.isnan(value)):
                    unit = None

                    if self.NEA_DEFAULT_UNITS.get(nea_field) and self.NEA_DEFAULT_UNITS.get(nea_field) != FIELD_DEFAULT_UNITS_STAR.get(star_attribute):
                        unit = FIELD_DEFAULT_UNITS_STAR.get(star_attribute)

                    datapoint = DataPoint(
                        value=value, unit=unit, reference=nea_reference
                    )

                    setattr(star, star_attribute, datapoint)

        # Traitement spécial pour les désignations
        designations = self._extract_star_altname(nea_data)
        if designations:
            star.st_altname = DataPoint(value=designations)

        # Autres traitements
        # Special handling for right_ascension (rastr or ra)
        if "rastr" in nea_data and nea_data["rastr"]:
            formatted_ra = self._format_right_ascension_str(nea_data["rastr"])
            if formatted_ra:
                star.st_right_ascension.value = formatted_ra

        elif "ra" in nea_data and nea_data["ra"] is not None:
            try:
                ra_deg = float(nea_data["ra"])
                formatted_ra_deg = self._format_right_ascension_deg(ra_deg)
                if formatted_ra_deg:
                    star.st_right_ascension = DataPoint(
                        value=formatted_ra_deg, reference=nea_reference
                    )
            except (ValueError, TypeError):
                # Handle cases where 'ra' might not be a valid number
                pass

        # Special handling for declination (decstr or dec)
        if "decstr" in nea_data and nea_data["decstr"]:
            formatted_dec = self._format_declination_str(nea_data["decstr"])
            if formatted_dec:
                star.st_declination = DataPoint(
                    value=formatted_dec, reference=nea_reference
                )
        elif "dec" in nea_data and nea_data["dec"] is not None:
            try:
                dec_deg = float(nea_data["dec"])
                formatted_dec_deg = self._format_declination_deg(dec_deg)
                if formatted_dec_deg:
                    star.st_declination = DataPoint(
                        value=formatted_dec_deg, reference=nea_reference
                    )
            except (ValueError, TypeError):
                # Handle cases where 'dec' might not be a valid number
                pass
        return star

    def map_nea_data_to_exoplanet(self, nea_data: Dict[str, Any]) -> DataSourceExoplanet:
        """Convertit un dictionnaire de données NEA vers un objet Exoplanet"""
        exoplanet = DataSourceExoplanet()

        # Create a NEA reference for all data points originating from this source
        nea_reference = Reference(
            source=SourceType.NEA,
            # TODO ici il faudrait plutot recuperer la date depuis le retour de l'api, la date de mise a jour des donnees dans l'api
            update_date=datetime.now(),
            consultation_date=datetime.now(),
            star_identifier=nea_data.get("hostname"),
            planet_identifier=nea_data.get("pl_name"),
        )

        for nea_field, exoplanet_attribute in self.NEA_TO_EXOPLANET_MAPPING.items():
            if nea_field in nea_data:
                value = nea_data[nea_field]

                # Liste des champs à formater
                numeric_fields = {
                    "pl_orbsmax", "pl_angsep", "pl_bmassj", "pl_msinij", "pl_radj", "pl_dens", "pl_eqt",
                    "sy_dist", "st_teff", "st_mass", "st_rad", "st_met", "st_logg", "st_lum", "st_dens", "st_age"
                }

                if nea_field in numeric_fields and value not in (None, ""):
                    value = FieldFormatter.format_numeric_no_trailing_zeros(
                        value)

                # Créer un DataPoint avec la valeur et l'unité par défaut
                if value is not None and str(value).strip():
                    unit = self.NEA_DEFAULT_UNITS.get(nea_field)
                    datapoint = DataPoint(
                        value=value, unit=unit, reference=nea_reference)
                    setattr(exoplanet, exoplanet_attribute, datapoint)

                if value is not None and str(value).strip() and not (isinstance(value, float) and math.isnan(value)):
                    unit = None

                    if self.NEA_DEFAULT_UNITS.get(nea_field) and self.NEA_DEFAULT_UNITS.get(nea_field) != FIELD_DEFAULT_UNITS_EXOPLANET.get(exoplanet_attribute):
                        unit = FIELD_DEFAULT_UNITS_EXOPLANET.get(
                            exoplanet_attribute)

                    datapoint = DataPoint(
                        value=value, unit=unit, reference=nea_reference
                    )

                    setattr(exoplanet, exoplanet_attribute, datapoint)

        # Special handling for right_ascension (rastr or ra)
        if "rastr" in nea_data and nea_data["rastr"]:
            formatted_ra = self._format_right_ascension_str(nea_data["rastr"])
            if formatted_ra:
                exoplanet.st_right_ascension = DataPoint(
                    value=formatted_ra, reference=nea_reference
                )
        elif "ra" in nea_data and nea_data["ra"] is not None:
            try:
                ra_deg = float(nea_data["ra"])
                formatted_ra_deg = self._format_right_ascension_deg(ra_deg)
                if formatted_ra_deg:
                    exoplanet.st_right_ascension = DataPoint(
                        value=formatted_ra_deg, reference=nea_reference
                    )
            except (ValueError, TypeError):
                # Handle cases where 'ra' might not be a valid number
                pass

        # Special handling for declination (decstr or dec)
        if "decstr" in nea_data and nea_data["decstr"]:
            formatted_dec = self._format_declination_str(nea_data["decstr"])
            if formatted_dec:
                exoplanet.st_declination = DataPoint(
                    value=formatted_dec, reference=nea_reference
                )
        elif "dec" in nea_data and nea_data["dec"] is not None:
            try:
                dec_deg = float(nea_data["dec"])
                formatted_dec_deg = self._format_declination_deg(dec_deg)
                if formatted_dec_deg:
                    exoplanet.st_declination = DataPoint(
                        value=formatted_dec_deg, reference=nea_reference
                    )
            except (ValueError, TypeError):
                # Handle cases where 'dec' might not be a valid number
                pass

        if "pl_orbincl" in nea_data and nea_data["pl_orbincl"] is not None:
            try:
                pl_orbincl_val = float(nea_data["pl_orbincl"])
                formatted_inclination = f"{pl_orbincl_val}"
                if (
                    "pl_orbinclerr1" in nea_data
                    and "pl_orbinclerr2" in nea_data
                    and nea_data["pl_orbinclerr1"] is not None
                    and nea_data["pl_orbinclerr2"] is not None
                ):
                    pl_orbinclerr1_val = float(nea_data["pl_orbinclerr1"])
                    pl_orbinclerr2_val = float(nea_data["pl_orbinclerr2"])
                    formatted_inclination = f"{pl_orbincl_val}{{{{±|{pl_orbinclerr1_val}|{pl_orbinclerr2_val}}}}}"
                    exoplanet.pl_inclination = DataPoint(
                        value=formatted_inclination, reference=nea_reference
                    )
                else:
                    exoplanet.pl_inclination = DataPoint(
                        value=pl_orbincl_val, reference=nea_reference
                    )
            except (ValueError, TypeError):
                pass

        if "pl_tranmidstr" in nea_data and nea_data["pl_tranmidstr"] is not None:
            try:
                pl_tranmidstr = float(nea_data["pl_tranmidstr"])
                formatted_epoch = self._parse_epoch_string(pl_tranmidstr)
                if formatted_epoch:
                    exoplanet.pl_epoch = DataPoint(
                        value=formatted_epoch, reference=nea_reference
                    )
            except (ValueError, TypeError):
                pass

        if "pl_orbperstr" in nea_data and nea_data["pl_orbperstr"] is not None:
            try:
                pl_orbperstr = float(nea_data["pl_orbperstr"])
                formatted_orb_per = self._parse_epoch_string(pl_orbperstr)
                if formatted_orb_per:
                    exoplanet.pl_orbital_period = DataPoint(
                        value=formatted_orb_per, reference=nea_reference
                    )
            except (ValueError, TypeError):
                pass

        return exoplanet

    def _extract_star_altname(self, nea_data: Dict[str, Any]) -> Optional[list]:
        """Extrait les différentes désignations d'une étoile, en filtrant les valeurs invalides.
        Ne rajoute pas hostname (nom principal) et évite les doublons avec hostname.
        """
        st_altname_fields = ["hd_name", "hip_name", "tic_id"]
        alt_names = []

        hostname = str(nea_data.get("hostname", "")).strip()
        invalid_values = {"nan", "none", ""}

        for field in st_altname_fields:
            if field in nea_data and nea_data[field]:
                value = str(nea_data[field]).strip()
                # Filtre les valeurs invalides et les doublons avec hostname
                if (
                    value
                    and value.lower() not in invalid_values
                    and value != hostname
                    and value not in alt_names
                ):
                    alt_names.append(value)

        return alt_names if alt_names else None

    def _format_right_ascension_str(self, rastr_val: str) -> str:
        """
        Formats a right ascension string by replacing 'h', 'm', 's'
        with '/' as needed for Wikipedia formatting.

        Example: "12h34m56s" becomes "12/34/56"
        """
        if not isinstance(rastr_val, str):
            # Handle cases where it might not be a string (e.g., NaN, other types)
            return ""  # Return empty string for invalid input

        formatted_ra = rastr_val.replace(
            "h", "/").replace("m", "/").replace("s", "")

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

        formatted_dec = decstr_val.replace(
            "d", "/").replace("m", "/").replace("s", "")

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
            fixed_html_str = re.sub(
                r'class=(\w+)"', r'class="\1"', epoch_str_val)
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
