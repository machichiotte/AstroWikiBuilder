# src/data_collectors/open_exoplanet_collection.py
import pandas as pd
from typing import List, Optional
from datetime import datetime
import logging
from src.models.exoplanet import Exoplanet
from src.models.reference import DataPoint, Reference, SourceType

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OpenExoplanetCollector:
    BASE_URL = "https://raw.githubusercontent.com/OpenExoplanetCatalogue/oec_tables/master/comma_separated/open_exoplanet_catalogue.txt"
    
    def __init__(self):
        self.required_columns = ['name', 'star_name', 'discoverymethod', 'discoveryyear']
    
    def fetch_data(self) -> List[Exoplanet]:
        """
        Fetch data from OpenExoplanet Catalogue and convert to Exoplanet objects
        """
        try:
            df = pd.read_csv(self.BASE_URL)
            logger.info(f"Colonnes trouvées dans le CSV OEC : {list(df.columns)}")
            
            # Vérification des colonnes requises
            missing_columns = [col for col in self.required_columns if col not in df.columns]
            if missing_columns:
                raise ValueError(f"Colonnes manquantes dans le CSV : {missing_columns}")
            
            exoplanets = []
            for index, row in df.iterrows():
                try:
                    exoplanet = self._convert_row_to_exoplanet(row)
                    if exoplanet:
                        exoplanets.append(exoplanet)
                except Exception as e:
                    logger.error(f"Erreur sur la ligne {index}: {str(e)}")
                    logger.debug(f"Données de la ligne : {row.to_dict()}")
            
            logger.info(f"Nombre d'exoplanètes traitées avec succès : {len(exoplanets)}")
            return exoplanets
            
        except Exception as e:
            logger.error(f"Erreur lors de la lecture du CSV OEC : {str(e)}")
            return []
    
    def _create_reference(self) -> Reference:
        """Crée une référence pour les données OEC"""
        return Reference(
            source=SourceType.OEC,
            date=datetime.now(),
            url="https://github.com/OpenExoplanetCatalogue/oec_tables"
        )
    
    def _safe_float_conversion(self, value: any) -> Optional[float]:
        """Convertit une valeur en float de manière sécurisée"""
        if pd.isna(value):
            return None
        try:
            return float(value)
        except (ValueError, TypeError):
            return None
    
    def _convert_row_to_exoplanet(self, row: pd.Series) -> Optional[Exoplanet]:
        """
        Convert a row from OpenExoplanet Catalogue to an Exoplanet object
        """
        try:
            ref = self._create_reference()
            
            # Validation des données de base
            if pd.isna(row['name']) or pd.isna(row['star_name']):
                logger.warning(f"Données de base manquantes pour l'exoplanète : {row.get('name', 'Unknown')}")
                return None
            
            # Création de l'objet Exoplanet avec les données de base
            exoplanet = Exoplanet(
                name=str(row['name']).strip(),
                host_star=DataPoint(str(row['star_name']).strip(), ref),
                discovery_method=DataPoint(str(row['discoverymethod']).strip(), ref) if pd.notna(row['discoverymethod']) else None,
                discovery_date=DataPoint(str(row['discoveryyear']).strip(), ref) if pd.notna(row['discoveryyear']) else None
            )
            
            # Caractéristiques orbitales
            for field, csv_field in [
                ('semi_major_axis', 'semimajoraxis'),
                ('eccentricity', 'eccentricity'),
                ('orbital_period', 'period'),
                ('inclination', 'inclination'),
                ('argument_of_periastron', 'longitudeofperiastron'),
                ('periastron_time', 'periastrontime')
            ]:
                value = self._safe_float_conversion(row.get(csv_field))
                if value is not None:
                    setattr(exoplanet, field, DataPoint(value, ref))
            
            # Caractéristiques physiques
            for field, csv_field in [
                ('mass', 'mass'),
                ('radius', 'radius'),
                ('temperature', 'temperature')
            ]:
                value = self._safe_float_conversion(row.get(csv_field))
                if value is not None:
                    setattr(exoplanet, field, DataPoint(value, ref))
            
            # Informations sur l'étoile
            for field, csv_field in [
                ('spectral_type', 'spectraltype'),
                ('star_temperature', 'star_temperature'),
                ('star_radius', 'star_radius'),
                ('star_mass', 'star_mass'),
                ('distance', 'distance'),
                ('apparent_magnitude', 'apparentmagnitude')
            ]:
                value = row.get(csv_field)
                if pd.notna(value):
                    if isinstance(value, (int, float)):
                        value = self._safe_float_conversion(value)
                    setattr(exoplanet, field, DataPoint(value, ref))
            
            # Autres noms
            if pd.notna(row.get('alt_names')):
                names = str(row['alt_names']).split(',')
                for name in names:
                    name = name.strip()
                    if name and name != exoplanet.name:
                        exoplanet.other_names.append(name)
            
            return exoplanet
            
        except Exception as e:
            logger.error(f"Erreur lors de la conversion de la ligne en Exoplanet : {str(e)}")
            return None 