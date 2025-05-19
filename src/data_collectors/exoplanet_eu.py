import pandas as pd
from typing import List
from datetime import datetime
from src.models.exoplanet import Exoplanet
from src.models.reference import DataPoint, Reference, SourceType

class ExoplanetEUCollector:
    def __init__(self, csv_path: str):
        """
        Initialize the collector with the path to the downloaded CSV file
        """
        self.csv_path = csv_path
    
    def fetch_data(self) -> List[Exoplanet]:
        """
        Fetch data from Exoplanet.eu CSV file and convert to Exoplanet objects
        """
        try:
            df = pd.read_csv(self.csv_path)
           # print("Colonnes du CSV EPE :", list(df.columns))
            print(df.head(3))
            
            exoplanets = []
            for _, row in df.iterrows():
                try:
                    exoplanet = self._convert_row_to_exoplanet(row)
                    if exoplanet:
                        exoplanets.append(exoplanet)
                except Exception as e:
                    print(f"Erreur sur la ligne : {row}")
                    print(e)
            
            return exoplanets
            
        except Exception as e:
            print(f"Erreur lors de la lecture du CSV EPE : {e}")
            return []
    
    def _create_reference(self) -> Reference:
        """Crée une référence pour les données EPE"""
        return Reference(
            source=SourceType.EPE,
            date=datetime.now(),
            url="https://exoplanet.eu/"
        )
    
    def _convert_row_to_exoplanet(self, row: pd.Series) -> Exoplanet:
        """
        Convert a row from the Exoplanet.eu CSV to an Exoplanet object
        """
        try:
            ref = self._create_reference()
            
            # Création de l'objet Exoplanet avec les données de base
            exoplanet = Exoplanet(
                name=row['name'],
                host_star=DataPoint(row['star_name'], ref),
                discovery_method=DataPoint(row['detection_type'], ref),
                discovery_date=DataPoint(row['discovered'], ref)
            )
            
            # Caractéristiques orbitales
            if pd.notna(row['semi_major_axis']):
                exoplanet.semi_major_axis = DataPoint(float(row['semi_major_axis']), ref)
            if pd.notna(row['eccentricity']):
                exoplanet.eccentricity = DataPoint(float(row['eccentricity']), ref)
            if pd.notna(row['orbital_period']):
                exoplanet.orbital_period = DataPoint(float(row['orbital_period']), ref)
            if pd.notna(row['inclination']):
                exoplanet.inclination = DataPoint(float(row['inclination']), ref)
            if pd.notna(row['omega']):
                exoplanet.argument_of_periastron = DataPoint(float(row['omega']), ref)
            if pd.notna(row['tperi']):
                exoplanet.periastron_time = DataPoint(float(row['tperi']), ref)
            
            # Caractéristiques physiques
            if pd.notna(row['mass']):
                exoplanet.mass = DataPoint(float(row['mass']), ref)
            if pd.notna(row['radius']):
                exoplanet.radius = DataPoint(float(row['radius']), ref)
            if pd.notna(row['temp_calculated']):
                exoplanet.temperature = DataPoint(float(row['temp_calculated']), ref)
            
            # Informations sur l'étoile
            if pd.notna(row['star_sp_type']):
                exoplanet.spectral_type = DataPoint(row['star_sp_type'], ref)
            if pd.notna(row['star_teff']):
                exoplanet.star_temperature = DataPoint(float(row['star_teff']), ref)
            if pd.notna(row['star_radius']):
                exoplanet.star_radius = DataPoint(float(row['star_radius']), ref)
            if pd.notna(row['star_mass']):
                exoplanet.star_mass = DataPoint(float(row['star_mass']), ref)
            if pd.notna(row['star_distance']):
                exoplanet.distance = DataPoint(float(row['star_distance']), ref)
            if pd.notna(row['mag_v']):
                exoplanet.apparent_magnitude = DataPoint(float(row['mag_v']), ref)
            
            # Découverte
            if pd.notna(row['planet_status']):
                exoplanet.status = DataPoint(row['planet_status'], ref)
            
            # Autres noms
            if pd.notna(row['alternate_names']):
                names = row['alternate_names'].split(',')
                for name in names:
                    name = name.strip()
                    if name and name != exoplanet.name:  # Ne pas ajouter le nom principal
                        exoplanet.other_names.append(name)
            
            return exoplanet
            
        except (ValueError, KeyError) as e:
            print(f"Error converting row to Exoplanet: {e}")
            return None 