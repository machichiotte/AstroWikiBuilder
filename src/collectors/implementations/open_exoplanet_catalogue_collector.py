# src/collectors/implementations/open_exoplanet_catalogue_collector.py
import logging

import pandas as pd

from src.collectors.base_collector import BaseCollector
from src.models.entities.exoplanet_entity import Exoplanet, ValueWithUncertainty
from src.models.entities.star_entity import Star
from src.models.references.reference import SourceType

logger: logging.Logger = logging.getLogger(__name__)


class OpenExoplanetCatalogueCollector(BaseCollector):
    def __init__(self, cache_dir: str = "data/cache/oec", use_mock_data: bool = False):
        super().__init__(cache_dir, use_mock_data)

    def get_default_cache_filename(self) -> str:
        return "open_exoplanet_catalogue.txt"

    def get_data_download_url(self) -> str:
        return "https://raw.githubusercontent.com/OpenExoplanetCatalogue/oec_tables/master/comma_separated/open_exoplanet_catalogue.txt"

    def get_source_type(self) -> SourceType:
        return SourceType.OEC

    def get_source_reference_url(self) -> str:
        return "https://github.com/OpenExoplanetCatalogue/oec_tables"

    def get_required_csv_columns(self) -> list[str]:
        # Définissez ici les colonnes que vous considérez comme critiques pour OEC, par exemple:
        return ["name", "star_name"]  # À adapter selon les besoins réels

    # _get_csv_reader_kwargs n'a pas besoin d'être surchargé si le CSV OEC n'a pas de commentaires spéciaux

    def _set_orbital_characteristics(self, exoplanet: Exoplanet, row: pd.Series) -> None:
        for field, csv_field in [
            ("pl_semi_major_axis", "semimajoraxis"),
            ("pl_eccentricity", "eccentricity"),
            ("pl_orbital_period", "period"),
            ("pl_inclination", "inclination"),
            ("pl_argument_of_periastron", "longitudeofperiastron"),
            ("pl_periastron_time", "periastrontime"),
        ]:
            value: float | None = self.convert_to_float_if_possible(row.get(csv_field))
            if value is not None:
                setattr(exoplanet, field, ValueWithUncertainty(value=value))

    def _set_physical_characteristics(self, exoplanet: Exoplanet, row: pd.Series) -> None:
        for field, csv_field in [
            ("pl_mass", "mass"),
            ("pl_radius", "radius"),
            ("pl_temperature", "temperature"),
        ]:
            value = self.convert_to_float_if_possible(row.get(csv_field))
            if value is not None:
                setattr(exoplanet, field, ValueWithUncertainty(value=value))

    def _set_star_info(self, exoplanet: Exoplanet, row: pd.Series) -> None:
        for field, csv_field in [
            ("st_spectral_type", "spectraltype"),
            ("st_temperature", "star_temperature"),
            ("st_radius", "star_radius"),
            ("st_mass", "star_mass"),
            ("st_distance", "distance"),
            ("st_apparent_magnitude", "apparentmagnitude"),
        ]:
            value = row.get(csv_field)
            if pd.notna(value):
                processed_value = (
                    self.convert_to_float_if_possible(value)
                    if isinstance(value, int | float | str)
                    and str(value).replace(".", "", 1).isdigit()
                    else str(value).strip()
                )
                if processed_value is not None:
                    if isinstance(processed_value, int | float):
                        setattr(
                            exoplanet,
                            field,
                            ValueWithUncertainty(value=processed_value),
                        )
                    else:
                        setattr(exoplanet, field, processed_value)

    def _set_alt_names(self, exoplanet: Exoplanet, row: pd.Series) -> None:
        if pd.notna(row.get("alt_names")):
            names = str(row["alt_names"]).split(",")
            for name in names:
                name = name.strip()
                if name and name != exoplanet.pl_name:
                    exoplanet.pl_altname.append(name)

    def transform_row_to_exoplanet(self, row: pd.Series) -> Exoplanet | None:
        try:
            if pd.isna(row["name"]) or pd.isna(row["star_name"]):
                logger.warning(
                    f"Données de base manquantes pour l'exoplanète : {row.get('name', 'Unknown')} (Source: OEC)"
                )
                return None

            # Créer la référence via le ReferenceManager
            ref = self.reference_manager.create_reference(
                source_type=self.get_source_type(),
                star_id=str(row["star_name"]).strip(),
                planet_id=str(row["name"]).strip(),
            )

            exoplanet = Exoplanet(
                pl_name=str(row["name"]).strip(),
                st_name=str(row["star_name"]).strip(),
                reference=ref,
            )

            self._set_orbital_characteristics(exoplanet, row)
            self._set_physical_characteristics(exoplanet, row)
            self._set_star_info(exoplanet, row)
            self._set_alt_names(exoplanet, row)

            return exoplanet

        except Exception as e:
            logger.error(
                f"Erreur OEC lors de la conversion de la ligne : {row.get('name', 'Unknown')}. Erreur: {e}",
                exc_info=True,
            )
            return None

    def transform_row_to_star(self, row: pd.Series) -> Star | None:
        """
        Convertit une ligne du DataFrame en objet Star.

        Note: Open Exoplanet Catalogue ne fournit pas de données d'étoiles séparées.
        Les informations d'étoile sont déjà intégrées dans les objets Exoplanet.

        Returns:
            None: Toujours None car les données d'étoiles ne sont pas séparées
        """
        return None
