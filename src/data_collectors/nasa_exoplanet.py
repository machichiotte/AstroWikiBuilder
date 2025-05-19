import requests
import pandas as pd
import io
from typing import List
from datetime import datetime
from src.models.exoplanet import Exoplanet
from src.models.reference import DataPoint, Reference, SourceType

class NASAExoplanetCollector:
    BASE_URL = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+*+from+PSCompPars&format=csv"
    
    def __init__(self):
        self.session = requests.Session()
    
    def fetch_data(self) -> List[Exoplanet]:
        """
        Fetch data from NASA Exoplanet Archive and convert to Exoplanet objects
        """
        try:
            # Debug: afficher l'URL complète
            print(f"URL de l'API NASA : {self.BASE_URL}")
            
            response = self.session.get(self.BASE_URL)
            response.raise_for_status()
            
            # Debug: afficher le texte brut si le CSV semble vide ou incorrect
            if not response.text or len(response.text) < 100:
                print("Réponse brute de l'API NASA :")
                print(response.text)
            
            # Read CSV data
            df = pd.read_csv(io.StringIO(response.text))
            print("Colonnes du CSV NASA :", list(df.columns))
            print(df.head(3))
            
            # Convert to Exoplanet objects
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
            
        except requests.RequestException as e:
            print(f"Error fetching data from NASA Exoplanet Archive: {e}")
            return []
        except Exception as e:
            print(f"Erreur lors du parsing du CSV NASA : {e}")
            print(response.text)
            return []
    
    def _create_reference(self) -> Reference:
        """Crée une référence pour les données NASA"""
        return Reference(
            source=SourceType.NASA,
            date=datetime.now(),
            url="https://exoplanetarchive.ipac.caltech.edu/"
        )
    
    def _convert_row_to_exoplanet(self, row: pd.Series) -> Exoplanet:
        """
        Convert a row from the NASA Exoplanet Archive to an Exoplanet object
        """
        try:
            ref = self._create_reference()
            
            # Création de l'objet Exoplanet avec les données de base
            exoplanet = Exoplanet(
                name=row['pl_name'],
                host_star=DataPoint(row['hostname'], ref),
                discovery_method=DataPoint(row['discoverymethod'], ref),
                discovery_date=DataPoint(row['disc_year'], ref)
            )
            
            # Caractéristiques orbitales
            if pd.notna(row['pl_orbsmax']):
                exoplanet.semi_major_axis = DataPoint(float(row['pl_orbsmax']), ref)
            if pd.notna(row['pl_orbeccen']):
                exoplanet.eccentricity = DataPoint(float(row['pl_orbeccen']), ref)
            if pd.notna(row['pl_orbper']):
                exoplanet.orbital_period = DataPoint(float(row['pl_orbper']), ref)
            if pd.notna(row['pl_orbincl']):
                exoplanet.inclination = DataPoint(float(row['pl_orbincl']), ref)
            
            # Caractéristiques physiques
            if pd.notna(row['pl_bmasse']):
                exoplanet.mass = DataPoint(float(row['pl_bmasse']), ref)
            if pd.notna(row['pl_rade']):
                exoplanet.radius = DataPoint(float(row['pl_rade']), ref)
            if pd.notna(row['pl_eqt']):
                exoplanet.temperature = DataPoint(float(row['pl_eqt']), ref)
            
            # Informations sur l'étoile
            if pd.notna(row['st_spectype']):
                exoplanet.spectral_type = DataPoint(row['st_spectype'], ref)
            if pd.notna(row['st_teff']):
                exoplanet.star_temperature = DataPoint(float(row['st_teff']), ref)
            if pd.notna(row['st_rad']):
                exoplanet.star_radius = DataPoint(float(row['st_rad']), ref)
            if pd.notna(row['st_mass']):
                exoplanet.star_mass = DataPoint(float(row['st_mass']), ref)
            
            return exoplanet
            
        except (ValueError, KeyError) as e:
            print(f"Error converting row to Exoplanet: {e}")
            return None 