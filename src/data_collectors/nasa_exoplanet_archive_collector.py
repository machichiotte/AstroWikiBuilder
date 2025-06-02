# src/data_collectors/nasa_exoplanet_archive_collector.py
import pandas as pd
from typing import List, Optional, Dict, Any
import logging
import re

from bs4 import BeautifulSoup

from src.mappers.nasa_exoplanet_archive_mapper import NasaExoplanetArchiveMapper
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
        self.mapper = NasaExoplanetArchiveMapper()

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

    def _convert_row_to_star(self, row: pd.Series, ref: Reference) -> Optional[Star]:
        """
        Converts a pandas Series (row from a CSV/DataFrame) to a Star object,
        populating it with data based on predefined mappings.
        """
        try:
            nasa_data_dict = row.to_dict()
            # S'assurer que les données essentielles sont présentes avant d'appeler le mapper.
            if not nasa_data_dict.get("hostname"):
                logger.warning(
                    f"Star name (hostname) is missing or empty for a row. Skipping star creation. Row data: {nasa_data_dict}"
                )
                return None

            # Déléguer toute la logique de mappage et de création de l'objet au mapper.
            star = self.mapper.map_nasa_data_to_star(nasa_data_dict)
            return star
        except Exception as e:
            logger.error(
                f"Unexpected error converting row to Star using mapper for {row.get('hostname', 'Unknown')}: {e}",
                exc_info=True,
            )
            return None

    def _format_right_ascension_str(self, rastr_val: str) -> str:
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

    def _format_declination_str(self, decstr_val: str) -> str:
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

    def _convert_row_to_exoplanet2(
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
                formatted_ra = self._format_right_ascension_str(
                    str(row["rastr"]).strip()
                )
            if pd.notna(row.get("decstr")):
                formatted_dec = self._format_declination_str(str(row["decstr"]).strip())
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

    def _convert_row_to_exoplanet(
        self, row: pd.Series, ref: Reference
    ) -> Optional[Exoplanet]:
        """
        Converts a pandas Series (row from a CSV/DataFrame) to a Star object,
        populating it with data based on predefined mappings.
        """
        try:
            nasa_data_dict = row.to_dict()
            # S'assurer que les données essentielles sont présentes avant d'appeler le mapper.
            if not nasa_data_dict.get("pl_name"):
                logger.warning(
                    f"Exoplanet name (pl_name) is missing or empty for a row. Skipping exoplanet creation. Row data: {nasa_data_dict}"
                )
                return None

            # Déléguer toute la logique de mappage et de création de l'objet au mapper.
            star = self.mapper.map_nasa_data_to_exoplanet(nasa_data_dict)
            return star
        except Exception as e:
            logger.error(
                f"Unexpected error converting row to Exoplanet using mapper for {row.get('pl_name', 'Unknown')}: {e}",
                exc_info=True,
            )
            return None
