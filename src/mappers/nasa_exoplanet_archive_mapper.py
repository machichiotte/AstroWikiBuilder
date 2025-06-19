# ============================================================================
# IMPORTS
# ============================================================================
from typing import Any, Optional
from src.models.references.reference import Reference, SourceType
from src.models.entities.exoplanet import ValueWithUncertainty
from src.utils.astro.constellation_utils import ConstellationUtils
from src.models.entities.exoplanet import Exoplanet
from src.models.entities.star import Star
from src.models.entities.nea_entity import (
    NEA_TO_STAR_MAPPING,
    NEA_TO_EXOPLANET_MAPPING,
    NEA_ENTITY,
)
from datetime import datetime
import math


def is_invalid_raw_value(value: Any) -> bool:
    try:
        if value is None:
            return True
        str_val = str(value).strip().lower()
        return str_val in {"", "nan", "none"}
    except Exception:
        return True


# ============================================================================
# DÉCLARATION DE LA CLASSE NasaExoplanetArchiveMapper
# ============================================================================
class NasaExoplanetArchiveMapper:
    """Mapper pour convertir les données NEA Exoplanet Archive vers le modèle Exoplanet"""

    def __init__(self):
        self.constellation_utils = ConstellationUtils()

    # ============================================================================
    # MAPPING PRINCIPAL : STAR
    # ============================================================================
    def map_star_from_nea_record(self, nea_data: NEA_ENTITY) -> Star:
        """Convertit les données NEA en objet Star."""
        reference = self.build_reference_from_nea(nea_data, False)

        star = Star(
            st_name=nea_data.get("hostname", ""),
            reference=reference,
        )

        # Mapper les champs selon le mapping défini
        for nea_field, attribute in NEA_TO_STAR_MAPPING.items():
            if (
                nea_field in nea_data
                and attribute != "st_name"
                and attribute != "pl_name"
            ):
                raw_value = nea_data[nea_field]
                if is_invalid_raw_value(raw_value):
                    print(
                        f"Ignored {nea_field} ({attribute}) due to invalid value: {raw_value}"
                    )
                    continue

                if raw_value is not None:
                    if attribute not in (
                        "st_declination",
                        "st_right_ascension",
                        "st_spectral_type",
                    ):
                        value_with_uncertainty: ValueWithUncertainty | None = (
                            self.convert_to_value_with_uncertainty(value=raw_value)
                        )
                        if value_with_uncertainty:
                            setattr(star, attribute, value_with_uncertainty)
                    else:
                        setattr(star, attribute, raw_value)

        # Traitement spécial pour les désignations
        st_altnames = self.extract_star_alternative_names(nea_data)
        if st_altnames:
            star.st_altname = st_altnames

        # Traitement des coordonnées
        self.set_coordinates_and_constellation(star, nea_data, reference)

        return star

    # ============================================================================
    # MAPPING PRINCIPAL : EXOPLANET
    # ============================================================================
    def map_exoplanet_from_nea_record(self, nea_data: NEA_ENTITY) -> Exoplanet:
        """Mappe les données NEA vers un objet Exoplanet."""
        reference = self.build_reference_from_nea(nea_data, True)

        exoplanet = Exoplanet(
            pl_name=nea_data.get("pl_name"),
            st_name=nea_data.get("hostname"),
            reference=reference,
        )

        # Traitement des coordonnées
        self.set_coordinates_and_constellation(exoplanet, nea_data, reference)

        # Traitement des autres champs avec ValueWithUncertainty
        for nea_field, attribute in NEA_TO_EXOPLANET_MAPPING.items():
            if (
                nea_field in nea_data
                and attribute != "pl_name"
                and attribute != "st_name"
                and attribute != "reference"
            ):
                raw_value = nea_data[nea_field]

                if (
                    attribute != "st_declination"
                    or attribute != "st_right_ascension"
                    or attribute != "st_spectral_type"
                    or attribute != "disc_method"
                    or attribute != "disc_facility"
                ):
                    if raw_value:
                        if isinstance(
                            raw_value, str
                        ) and self.is_composite_formatted_string(raw_value):
                            parsed_vwu = self.parse_composite_formatted_value(raw_value)
                            if parsed_vwu:
                                setattr(exoplanet, attribute, parsed_vwu)

                        else:
                            try:
                                numeric_value = float(raw_value)
                                error_positive = nea_data.get(f"{nea_field}_err1")
                                error_negative = nea_data.get(f"{nea_field}_err2")

                                err1_clean = (
                                    float(
                                        str(error_positive)
                                        .replace("+", "")
                                        .replace("-", "")
                                    )
                                    if error_positive
                                    else None
                                )
                                err2_clean = (
                                    float(
                                        str(error_negative)
                                        .replace("+", "")
                                        .replace("-", "")
                                    )
                                    if error_negative
                                    else None
                                )

                                value_with_uncertainty = ValueWithUncertainty(
                                    value=numeric_value,
                                    error_positive=err1_clean,
                                    error_negative=err2_clean,
                                    sign="±" if err1_clean or err2_clean else None,
                                )
                                setattr(exoplanet, attribute, value_with_uncertainty)

                            except (ValueError, TypeError):
                                # C'est un string "pur" (ex: identifiant, classe spectrale, etc.)
                                setattr(exoplanet, attribute, raw_value)

        # Traitement spécial pour les désignations
        pl_altnames = self.extract_exoplanet_alternative_names(nea_data)
        if pl_altnames:
            exoplanet.pl_altname = pl_altnames

        # Traitement des coordonnées
        self.set_coordinates_and_constellation(exoplanet, nea_data, reference)

        return exoplanet

    # ============================================================================
    # UTILITAIRES DE MAPPING ET DE FORMATAGE
    # ============================================================================
    def build_reference_from_nea(
        self, nea_data: NEA_ENTITY, isPlanet: False
    ) -> Reference:
        """Crée une référence NEA pour les points de données."""
        return Reference(
            source=SourceType.NEA,
            update_date=datetime.now(),
            consultation_date=datetime.now(),
            star_id=nea_data.get("hostname"),
            planet_id=nea_data.get("pl_name") if isPlanet else None,
        )

    def set_coordinates_and_constellation(
        self, obj: Any, nea_data: NEA_ENTITY, reference: Reference
    ) -> None:
        """Traite les coordonnées (RA et DEC) pour un objet."""
        # Traitement de l'ascension droite
        if "rastr" in nea_data and nea_data["rastr"]:
            formatted_ra = self._format_right_ascension_str(nea_data["rastr"])
            if formatted_ra:
                obj.st_right_ascension = formatted_ra
        elif "ra" in nea_data and nea_data["ra"] is not None:
            try:
                ra_deg = float(nea_data["ra"])
                formatted_ra_deg = self._format_right_ascension_deg(ra_deg)
                if formatted_ra_deg:
                    obj.st_right_ascension = formatted_ra_deg
            except (ValueError, TypeError):
                pass

        # Traitement de la déclinaison
        if "decstr" in nea_data and nea_data["decstr"]:
            formatted_dec = self._format_declination_str(nea_data["decstr"])
            if formatted_dec:
                obj.st_declination = formatted_dec
        elif "dec" in nea_data and nea_data["dec"] is not None:
            try:
                dec_deg = float(nea_data["dec"])
                formatted_dec_deg = self._format_declination_deg(dec_deg)
                if formatted_dec_deg:
                    obj.st_declination = formatted_dec_deg
            except (ValueError, TypeError):
                pass

        # Calcul de la constellation
        if obj.st_right_ascension and obj.st_declination:
            constellation = self.constellation_utils.get_constellation_name(
                obj.st_right_ascension, obj.st_declination
            )
            if constellation:
                obj.st_constellation = constellation

    def extract_star_alternative_names(self, nea_data: NEA_ENTITY) -> Optional[list]:
        """Extrait les différentes désignations d'une étoile, en filtrant les valeurs invalides.
        Ne rajoute pas hostname (nom principal) et évite les doublons avec hostname.
        """
        st_altname_fields: list[str] = ["hd_name", "hip_name", "tic_id"]
        alt_names: list = []

        hostname: str = str(nea_data.get("hostname", "")).strip()
        invalid_values: set[str] = {"nan", "none", ""}

        for field in st_altname_fields:
            if field in nea_data and nea_data[field]:
                value: str = str(nea_data[field]).strip()
                # Filtre les valeurs invalides et les doublons avec hostname
                if (
                    value
                    and value.lower() not in invalid_values
                    and value != hostname
                    and value not in alt_names
                ):
                    alt_names.append(value)

        return alt_names if alt_names else None

    def extract_exoplanet_alternative_names(
        self, nea_data: NEA_ENTITY
    ) -> Optional[list]:
        """Extrait les différentes désignations d'une étoile, en filtrant les valeurs invalides.
        Ne rajoute pas hostname (nom principal) et évite les doublons avec hostname.
        """

        return None

    def convert_to_value_with_uncertainty(
        self,
        value: str | float,
        error_positive: Optional[float] = None,
        error_negative: Optional[float] = None,
        sign: Optional[str] = None,
    ) -> Optional[ValueWithUncertainty]:
        """Crée une valeur avec incertitude."""

        if (
            value is not None
            and str(value).strip()
            and not (isinstance(value, float) and math.isnan(value))
        ):
            return ValueWithUncertainty(
                value=value,
                error_positive=error_positive,
                error_negative=error_negative,
                sign=sign,
            )
        return None

    def format_trimmed_numeric_string(self, value):
        try:
            fval = float(value)
            return f"{fval:.5f}".rstrip("0").rstrip(".")
        except Exception:
            return str(value)

    def is_composite_formatted_string(self, raw_value: str) -> bool:
        """Heuristique pour détecter si une chaîne contient une valeur composite (HTML, entités HTML, etc.)"""
        raw_value = raw_value.strip()
        return any(
            sub in raw_value for sub in ("<span", "<div", "&plusmn", "&gt", "&lt")
        )

    def parse_composite_formatted_value(
        raw_value: str,
    ) -> Optional[ValueWithUncertainty]:
        """
        Parses the composite string (pl_tranmidstr) which can be in several formats:
        1. "2458950.09242&plusmn0.00076" -> [2458950.09242,0.00076, , ±]
        2. "<div><span class=supersubNumber">2458360.0754</span><span class="superscript">+0.0049</span><span class="subscript">-0.0078</span></div>"
           -> [2458360.0754,0.0049,0.0078,±]"
        3. "2458360.0754" (a simple numerical value) -> [2458360.0754,,,]
        4. "&gt789" -> [789, , >]
        5. "&lt1084" -> [1084, , <]

        Returns the formatted string or None if parsing fails.
        """
        import pandas as pd
        from bs4 import BeautifulSoup
        import re
        import logging

        logger = logging.getLogger(__name__)

        if pd.isna(raw_value) or not isinstance(raw_value, str):
            return None

        epoch_str_val = raw_value.strip()

        # Cas 1 : format avec &plusmn
        if "&plusmn" in epoch_str_val:
            try:
                parts = epoch_str_val.split("&plusmn")
                value = float(parts[0].strip())
                error = float(parts[1].strip()) if len(parts) > 1 else None
                return ValueWithUncertainty(
                    value=value, error_positive=error, error_negative=error, sign="±"
                )
            except ValueError:
                logger.warning(f"Erreur de parsing dans '&plusmn': {epoch_str_val}")
                return None

        # Cas 2 : HTML
        elif "<div" in epoch_str_val and "<span" in epoch_str_val:
            fixed_html_str = re.sub(r'class=(\w+)"', r'class="\1"', epoch_str_val)
            soup = BeautifulSoup(fixed_html_str, "html5lib")

            try:
                val = soup.find("span", class_="supersubNumber")
                pos = soup.find("span", class_="superscript")
                neg = soup.find("span", class_="subscript")

                value = float(val.get_text().strip()) if val else None
                err_pos = (
                    float(pos.get_text().strip().replace("+", "")) if pos else None
                )
                err_neg = (
                    float(neg.get_text().strip().replace("-", "")) if neg else None
                )

                return ValueWithUncertainty(
                    value=value,
                    error_positive=err_pos,
                    error_negative=err_neg,
                    sign="±",
                )
            except Exception as e:
                logger.warning(
                    f"Erreur de parsing HTML: {e} | contenu: {epoch_str_val}"
                )
                return None

        # Cas 3 : &gt
        elif epoch_str_val.startswith("&gt"):
            try:
                value = float(epoch_str_val[3:].strip())
                return ValueWithUncertainty(value=value, sign=">")
            except ValueError:
                logger.warning(f"Erreur parsing &gt : {epoch_str_val}")
                return None

        # Cas 4 : &lt
        elif epoch_str_val.startswith("&lt"):
            try:
                value = float(epoch_str_val[3:].strip())
                return ValueWithUncertainty(value=value, sign="<")
            except ValueError:
                logger.warning(f"Erreur parsing &lt : {epoch_str_val}")
                return None

        # Cas 5 : simple valeur numérique
        else:
            try:
                value = float(epoch_str_val)
                return ValueWithUncertainty(value=value)
            except ValueError:
                logger.warning(f"Format d'époque non reconnu : {epoch_str_val}")
                return None

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
