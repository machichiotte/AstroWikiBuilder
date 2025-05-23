# src/data_collectors/open_exoplanet_collection.py
import pandas as pd
import requests
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
    
    def __init__(self, csv_path: str):
        self.csv_path = csv_path
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

    def collect_data(self) -> List[Exoplanet]:
        """
        Collecte les données des exoplanètes depuis l'API Open Exoplanet Catalogue
        """
        try:
            # Télécharger les données
            response = requests.get(self.BASE_URL)
            response.raise_for_status()
            
            # Sauvegarder les données brutes
            with open(self.csv_path, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            # Lire les données avec pandas
            df = pd.read_csv(self.csv_path)
            
            # Convertir les lignes en objets Exoplanet
            exoplanets = []
            for _, row in df.iterrows():
                exoplanet = self._convert_row_to_exoplanet(row)
                if exoplanet:
                    exoplanets.append(exoplanet)
            
            return exoplanets
            
        except Exception as e:
            logger.error(f"Erreur lors de la collecte des données : {e}")
            return [] 