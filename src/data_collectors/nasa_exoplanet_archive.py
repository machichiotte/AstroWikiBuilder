# src/data_collectors/nasa_exoplanet_archive.py
import pandas as pd
from typing import List, Optional, Dict, Any
import logging

from src.data_collectors.base_collector import BaseExoplanetCollector
from src.models.exoplanet import Exoplanet
from src.models.reference import DataPoint, Reference, SourceType

logger = logging.getLogger(__name__)


class NASAExoplanetArchiveCollector(BaseExoplanetCollector):
    # BASE_URL est maintenant géré par _get_download_url
    # MOCK_DATA_PATH (qui est le cache_path) est géré par la classe de base

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

    def _convert_row_to_exoplanet(
        self, row: pd.Series, ref: Reference
    ) -> Optional[Exoplanet]:
        try:
            if pd.isna(row["pl_name"]) or pd.isna(row["hostname"]):
                logger.warning(
                    f"Données de base manquantes pour l'exoplanète : {row.get('pl_name', 'Unknown')} (Source: NASA)"
                )
                return None

            (
                formatted_ra,
                formatted_dec,
                formatted_epoch,
                formatted_orbital_period,
                formatted_inclination,
            ) = None, None, None, None, None
            if pd.notna(row.get("rastr")):
                rastr_val = str(row["rastr"]).strip()
                formatted_ra = (
                    rastr_val.replace("h", "/").replace("m", "/").replace("s", "")
                )
            if pd.notna(row.get("decstr")):
                decstr_val = str(row["decstr"]).strip()
                formatted_dec = (
                    decstr_val.replace("d", "/").replace("m", "/").replace("s", "")
                )
            if pd.notna(row.get("pl_tranmidstr")):
                pl_tranmidstr_val = str(row["pl_tranmidstr"]).strip()
                formatted_epoch = pl_tranmidstr_val.replace("&plusmn", " ± ")
            if pd.notna(row.get("pl_orbperstr")):
                pl_orbperstr_val = str(row["pl_orbperstr"]).strip()
                if "&plusmn" in pl_orbperstr_val:
                    base_orb_period, error_orb_period = pl_orbperstr_val.split(
                        "&plusmn"
                    )
                    formatted_orbital_period = f"{base_orb_period.strip()}{{±|{error_orb_period.strip()}|{error_orb_period.strip()}}}"
                else:
                    formatted_orbital_period = pl_orbperstr_val
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
                )  # abs car err2 est souvent négatif
                if pl_orbinclerr1_val is not None and pl_orbinclerr2_val is not None:
                    formatted_inclination = f"{pl_orbincl_val}{{±|{pl_orbinclerr1_val}|{pl_orbinclerr2_val}}}"

            exoplanet = Exoplanet(
                name=str(row["pl_name"]).strip(),
                host_star=DataPoint(str(row["hostname"]).strip(), ref),
                discovery_method=DataPoint(str(row["discoverymethod"]).strip(), ref)
                if pd.notna(row["discoverymethod"])
                else None,
                discovery_date=DataPoint(str(row["disc_year"]).strip(), ref)
                if pd.notna(row["disc_year"])
                else None,
            )
            # Assignation des valeurs formatées si elles existent
            if formatted_ra:
                exoplanet.right_ascension = DataPoint(formatted_ra, ref)
            if formatted_dec:
                exoplanet.declination = DataPoint(formatted_dec, ref)
            if formatted_epoch:
                exoplanet.epoch = DataPoint(formatted_epoch, ref)

            # Pour orbital_period et inclination, NASA a des colonnes spécifiques (pl_orbper, pl_orbincl) pour les valeurs numériques
            # et des colonnes _str pour les chaînes avec erreurs.
            # Le code original utilise les versions _str pour ces champs dans Exoplanet.
            # Si les versions numériques sont préférées pour d'autres champs, il faut clarifier.
            # Ici, on garde la logique de prendre la version formatée si elle existe.
            if formatted_orbital_period:
                exoplanet.orbital_period = DataPoint(formatted_orbital_period, ref)
            if formatted_inclination:
                exoplanet.inclination = DataPoint(formatted_inclination, ref)

            # Caractéristiques orbitales (numériques, avec unités)
            # Note : certains champs comme orbital_period et inclination sont déjà settés plus haut avec des formats spécifiques
            # S'ils ne doivent pas être écrasés, ajuster la logique.
            # Pour l'instant, on va setter les valeurs numériques si les versions formatées n'ont pas été utilisées.
            orbital_fields_map = {
                "semi_major_axis": ("pl_orbsmax", "ua"),
                "eccentricity": ("pl_orbeccen", None),
                "argument_of_periastron": ("pl_orblper", "°"),
                "periastron_time": ("pl_orbtper", "j"),
            }
            # On ajoute orbital_period et inclination seulement s'ils n'ont pas été settés par les versions formatées
            if not exoplanet.orbital_period and pd.notna(row.get("pl_orbper")):
                orbital_fields_map["orbital_period"] = ("pl_orbper", "j")
            if not exoplanet.inclination and pd.notna(row.get("pl_orbincl")):
                orbital_fields_map["inclination"] = ("pl_orbincl", "°")

            for field, (csv_field, unit) in orbital_fields_map.items():
                value = self._safe_float_conversion(row.get(csv_field))
                if value is not None:
                    setattr(exoplanet, field, DataPoint(value, ref, unit))

            # Caractéristiques physiques
            for field, csv_field, unit in [
                ("mass", "pl_bmassj", "M_J"),
                ("radius", "pl_radj", "R_J"),
                ("temperature", "pl_eqt", "K"),
            ]:
                value = self._safe_float_conversion(row.get(csv_field))
                if value is not None:
                    setattr(exoplanet, field, DataPoint(value, ref, unit))

            # Informations sur l'étoile
            for field, csv_field, unit in [
                ("spectral_type", "st_spectype", None),
                ("star_temperature", "st_teff", "K"),
                ("star_radius", "st_rad", "R_S"),
                ("star_mass", "st_mass", "M_S"),
                ("distance", "sy_dist", "pc"),
                ("apparent_magnitude", "sy_vmag", None),
            ]:
                value = row.get(csv_field)
                if pd.notna(value):
                    # La conversion float est déjà gérée si c'est un nombre, sinon on prend la chaîne
                    processed_value = (
                        self._safe_float_conversion(value)
                        if isinstance(value, (int, float, str))
                        and str(value).replace(".", "", 1).isdigit()
                        else str(value).strip()
                    )
                    if processed_value is not None:
                        setattr(exoplanet, field, DataPoint(processed_value, ref, unit))

            if pd.notna(row.get("pl_altname")):  # NASA utilise 'pl_altname'
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
