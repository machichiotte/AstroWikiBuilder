import pandas as pd
from typing import List, Optional
from datetime import datetime
import logging
from src.models.exoplanet import Exoplanet
from src.models.reference import DataPoint, Reference, SourceType

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ExoplanetEUCollector:
    def __init__(self, csv_path: str):
        """
        Initialize the collector with the path to the downloaded CSV file
        """
        self.csv_path = csv_path
        self.required_columns = ['name', 'star_name', 'detection_type', 'discovered']
    
    def fetch_data(self) -> List[Exoplanet]:
        """
        Fetch data from Exoplanet.eu CSV file and convert to Exoplanet objects
        """
        try:
            df = pd.read_csv(self.csv_path)
            logger.info(f"Colonnes trouvées dans le CSV EPE : {list(df.columns)}")
            
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
            logger.error(f"Erreur lors de la lecture du CSV EPE : {str(e)}")
            return []
    
    def _create_reference(self) -> Reference:
        """Crée une référence pour les données EPE"""
        return Reference(
            source=SourceType.EPE,
            date=datetime.now(),
            url="https://exoplanet.eu/"
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
        Convert a row from the Exoplanet.eu CSV to an Exoplanet object
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
                discovery_method=DataPoint(str(row['detection_type']).strip(), ref) if pd.notna(row['detection_type']) else None,
                discovery_date=DataPoint(str(row['discovered']).strip(), ref) if pd.notna(row['discovered']) else None
            )
            
            # Caractéristiques orbitales
            for field, csv_field in [
                ('semi_major_axis', 'semi_major_axis'),
                ('eccentricity', 'eccentricity'),
                ('orbital_period', 'orbital_period'),
                ('inclination', 'inclination'),
                ('argument_of_periastron', 'omega'),
                ('periastron_time', 'tperi')
            ]:
                value = self._safe_float_conversion(row.get(csv_field))
                if value is not None:
                    setattr(exoplanet, field, DataPoint(value, ref))
            
            # Caractéristiques physiques
            for field, csv_field in [
                ('mass', 'mass'),
                ('radius', 'radius'),
                ('temperature', 'temp_calculated')
            ]:
                value = self._safe_float_conversion(row.get(csv_field))
                if value is not None:
                    setattr(exoplanet, field, DataPoint(value, ref))
            
            # Informations sur l'étoile
            for field, csv_field in [
                ('spectral_type', 'star_sp_type'),
                ('star_temperature', 'star_teff'),
                ('star_radius', 'star_radius'),
                ('star_mass', 'star_mass'),
                ('distance', 'star_distance'),
                ('apparent_magnitude', 'mag_v')
            ]:
                value = row.get(csv_field)
                if pd.notna(value):
                    if isinstance(value, (int, float)):
                        value = self._safe_float_conversion(value)
                    setattr(exoplanet, field, DataPoint(value, ref))
            
            # Découverte
            if pd.notna(row.get('planet_status')):
                exoplanet.status = DataPoint(str(row['planet_status']).strip(), ref)
            
            # Autres noms
            if pd.notna(row.get('alternate_names')):
                names = str(row['alternate_names']).split(',')
                for name in names:
                    name = name.strip()
                    if name and name != exoplanet.name:
                        exoplanet.other_names.append(name)
            
            return exoplanet
            
        except Exception as e:
            logger.error(f"Erreur lors de la conversion de la ligne en Exoplanet : {str(e)}")
            return None 