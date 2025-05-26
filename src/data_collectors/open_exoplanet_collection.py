# src/data_collectors/open_exoplanet_collection.py
import pandas as pd
import requests
import os
from typing import List, Optional
from datetime import datetime
import logging
from src.models.exoplanet import Exoplanet
from src.models.reference import DataPoint, Reference, SourceType
from src.utils.reference_manager import ReferenceManager

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OpenExoplanetCollector:
    BASE_URL = "https://raw.githubusercontent.com/OpenExoplanetCatalogue/oec_tables/master/comma_separated/open_exoplanet_catalogue.txt"
    
    def __init__(self, cache_path: str, use_mock_data: bool = False):
        self.cache_path = cache_path
        self.use_mock_data = use_mock_data
        self.reference_manager = ReferenceManager()
        self.last_update_date = datetime.now()  # Par défaut, on utilise la date actuelle
    
    def _create_reference(self) -> Reference:
        """Crée une référence pour les données OEC"""
        return self.reference_manager.create_reference(
            source=SourceType.OEC,
            update_date=self.last_update_date,
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
                discovery_method=DataPoint(str(row['discovery_method']).strip(), ref) if pd.notna(row['discovery_method']) else None,
                discovery_date=DataPoint(str(row['discovery_year']).strip(), ref) if pd.notna(row['discovery_year']) else None
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
            logger.error(f"Erreur lors de la conversion de la ligne : {e}")
            return None

    def fetch_data(self) -> List[Exoplanet]:
        """
        Collects data from the Open Exoplanet Catalogue or loads from cache.
        Handles mock data usage, downloading, saving, and reading data.
        """
        exoplanets = []
        df = None

        if self.use_mock_data:
            logger.info(f"Using mock data from {self.cache_path}")
            if not os.path.exists(self.cache_path):
                logger.warning(f"Mock file not found: {self.cache_path}")
                return []
            try:
                df = pd.read_csv(self.cache_path)
            except FileNotFoundError:
                logger.warning(f"Mock file not found: {self.cache_path}")
                return []
            except pd.errors.EmptyDataError:
                logger.error(f"No data found in mock file: {self.cache_path}. The file is empty.")
                return []
            except Exception as e:
                logger.error(f"An error occurred while reading mock file {self.cache_path}: {e}")
                return []
        else:
            logger.info(f"Attempting to fetch data from {self.BASE_URL} or load from cache {self.cache_path}")
            if os.path.exists(self.cache_path):
                logger.info(f"Cache file found at {self.cache_path}. Loading data from cache.")
                try:
                    df = pd.read_csv(self.cache_path)
                except pd.errors.EmptyDataError:
                    logger.warning(f"No data found in cached file: {self.cache_path}. The file is empty. Attempting download.")
                    df = None 
                except Exception as e:
                    logger.error(f"An error occurred while reading cached file {self.cache_path}: {e}. Attempting download.")
                    df = None 

            if df is None: 
                logger.info(f"Fetching data from {self.BASE_URL}")
                try:
                    response = requests.get(self.BASE_URL)
                    response.raise_for_status()  
                    
                    cache_dir = os.path.dirname(self.cache_path)
                    if cache_dir: 
                        os.makedirs(cache_dir, exist_ok=True)
                    
                    with open(self.cache_path, 'w', encoding='utf-8') as f:
                        f.write(response.text)
                    logger.info(f"Successfully downloaded and saved data to {self.cache_path}")
                    
                    df = pd.read_csv(self.cache_path)
                    
                except requests.exceptions.RequestException as e:
                    logger.error(f"Error downloading data from {self.BASE_URL}: {e}")
                    if os.path.exists(self.cache_path):
                        logger.info(f"Download failed. Attempting to load from existing cache {self.cache_path}")
                        try:
                            df = pd.read_csv(self.cache_path)
                        except Exception as cache_e:
                            logger.error(f"Failed to load from cache after download error: {cache_e}")
                            return []
                    else:
                        return []
                except pd.errors.EmptyDataError:
                    logger.error(f"No data found in downloaded file: {self.cache_path}. The file is empty.")
                    return []
                except Exception as e: 
                    logger.error(f"An error occurred while processing downloaded data from {self.cache_path}: {e}")
                    return []

        if df is not None:
            for _, row in df.iterrows():
                exoplanet = self._convert_row_to_exoplanet(row)
                if exoplanet:
                    exoplanets.append(exoplanet)
            logger.info(f"Successfully processed {len(exoplanets)} exoplanets from {self.cache_path if self.use_mock_data or df is not None else self.BASE_URL}.")
        
        return exoplanets