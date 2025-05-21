import pandas as pd
from typing import List, Optional
from datetime import datetime
import logging
import os
from src.models.exoplanet import Exoplanet
from src.models.reference import DataPoint, Reference, SourceType

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NASAExoplanetCollector:
    BASE_URL = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+*+from+PSCompPars&format=csv"
    MOCK_DATA_PATH = "data/nasa_mock_data.csv"
    
    def __init__(self, use_mock_data: bool = False):
        self.required_columns = ['pl_name', 'hostname', 'discoverymethod', 'disc_year']
        self.use_mock_data = use_mock_data
        
        # Créer le dossier data s'il n'existe pas
        os.makedirs("data", exist_ok=True)
    
    def fetch_data(self) -> List[Exoplanet]:
        """
        Fetch data from NASA Exoplanet Archive and convert to Exoplanet objects
        """
        try:
            if self.use_mock_data:
                if not os.path.exists(self.MOCK_DATA_PATH):
                    logger.error(f"Fichier de données mockées non trouvé : {self.MOCK_DATA_PATH}")
                    return []
                df = pd.read_csv(self.MOCK_DATA_PATH)
                logger.info("Utilisation des données mockées")
            else:
                df = pd.read_csv(self.BASE_URL)
                # Sauvegarder les données pour une utilisation future
                df.to_csv(self.MOCK_DATA_PATH, index=False)
                logger.info(f"Données sauvegardées dans {self.MOCK_DATA_PATH}")
            
            logger.info(f"Colonnes trouvées dans le CSV NASA : {list(df.columns)}")
            
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
            logger.error(f"Erreur lors de la lecture du CSV NASA : {str(e)}")
            return []
    
    def _create_reference(self) -> Reference:
        """Crée une référence pour les données NASA"""
        return Reference(
            source=SourceType.NASA,
            date=datetime.now(),
            url="https://exoplanetarchive.ipac.caltech.edu/"
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
        Convert a row from NASA Exoplanet Archive to an Exoplanet object
        """
        try:
            ref = self._create_reference()
            
            # Validation des données de base
            if pd.isna(row['pl_name']) or pd.isna(row['hostname']):
                logger.warning(f"Données de base manquantes pour l'exoplanète : {row.get('pl_name', 'Unknown')}")
                return None
            
            # Création de l'objet Exoplanet avec les données de base
            exoplanet = Exoplanet(
                name=str(row['pl_name']).strip(),
                host_star=DataPoint(str(row['hostname']).strip(), ref),
                discovery_method=DataPoint(str(row['discoverymethod']).strip(), ref) if pd.notna(row['discoverymethod']) else None,
                discovery_date=DataPoint(str(row['disc_year']).strip(), ref) if pd.notna(row['disc_year']) else None
            )
            
            # Caractéristiques orbitales
            for field, csv_field in [
                ('semi_major_axis', 'pl_orbsmax'),
                ('eccentricity', 'pl_orbeccen'),
                ('orbital_period', 'pl_orbper'),
                ('inclination', 'pl_orbincl'),
                ('argument_of_periastron', 'pl_orblper'),
                ('periastron_time', 'pl_orbtper')
            ]:
                value = self._safe_float_conversion(row.get(csv_field))
                if value is not None:
                    setattr(exoplanet, field, DataPoint(value, ref))
            
            # Caractéristiques physiques
            for field, csv_field in [
                ('mass', 'pl_bmassj'),
                ('radius', 'pl_radj'),
                ('temperature', 'pl_eqt')
            ]:
                value = self._safe_float_conversion(row.get(csv_field))
                if value is not None:
                    setattr(exoplanet, field, DataPoint(value, ref))
            
            # Informations sur l'étoile
            for field, csv_field in [
                ('spectral_type', 'st_spectype'),
                ('star_temperature', 'st_teff'),
                ('star_radius', 'st_rad'),
                ('star_mass', 'st_mass'),
                ('distance', 'sy_dist'),
                ('apparent_magnitude', 'sy_vmag')
            ]:
                value = row.get(csv_field)
                if pd.notna(value):
                    if isinstance(value, (int, float)):
                        value = self._safe_float_conversion(value)
                    setattr(exoplanet, field, DataPoint(value, ref))
            
            # Autres noms
            if pd.notna(row.get('pl_altname')):
                names = str(row['pl_altname']).split(',')
                for name in names:
                    name = name.strip()
                    if name and name != exoplanet.name:
                        exoplanet.other_names.append(name)
            
            return exoplanet
            
        except Exception as e:
            logger.error(f"Erreur lors de la conversion de la ligne en Exoplanet : {str(e)}")
            return None 