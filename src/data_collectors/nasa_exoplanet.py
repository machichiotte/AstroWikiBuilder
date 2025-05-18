import requests
import pandas as pd
import io
from typing import List, Dict, Any
from src.models.exoplanet import Exoplanet

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
    
    def _convert_row_to_exoplanet(self, row: pd.Series) -> Exoplanet:
        """
        Convert a row from the NASA Exoplanet Archive to an Exoplanet object
        """
        try:
            return Exoplanet(
                name=row['pl_name'],
                host_star=row['hostname'],
                discovery_year=int(row['disc_year']),
                discovery_method=row['discoverymethod'],
                mass=float(row['pl_bmasse']) if pd.notna(row['pl_bmasse']) else None,
                mass_error_min=float(row['pl_bmasseerr1']) if pd.notna(row['pl_bmasseerr1']) else None,
                mass_error_max=float(row['pl_bmasseerr2']) if pd.notna(row['pl_bmasseerr2']) else None,
                radius=float(row['pl_rade']) if pd.notna(row['pl_rade']) else None,
                radius_error_min=float(row['pl_radeerr1']) if pd.notna(row['pl_radeerr1']) else None,
                radius_error_max=float(row['pl_radeerr2']) if pd.notna(row['pl_radeerr2']) else None,
                orbital_period=float(row['pl_orbper']) if pd.notna(row['pl_orbper']) else None,
                orbital_period_error_min=float(row['pl_orbpererr1']) if pd.notna(row['pl_orbpererr1']) else None,
                orbital_period_error_max=float(row['pl_orbpererr2']) if pd.notna(row['pl_orbpererr2']) else None,
                semi_major_axis=float(row['pl_orbsmax']) if pd.notna(row['pl_orbsmax']) else None,
                semi_major_axis_error_min=float(row['pl_orbsmaxerr1']) if pd.notna(row['pl_orbsmaxerr1']) else None,
                semi_major_axis_error_max=float(row['pl_orbsmaxerr2']) if pd.notna(row['pl_orbsmaxerr2']) else None,
                eccentricity=float(row['pl_orbeccen']) if pd.notna(row['pl_orbeccen']) else None,
                eccentricity_error_min=float(row['pl_orbeccenerr1']) if pd.notna(row['pl_orbeccenerr1']) else None,
                eccentricity_error_max=float(row['pl_orbeccenerr2']) if pd.notna(row['pl_orbeccenerr2']) else None,
                inclination=float(row['pl_orbincl']) if pd.notna(row['pl_orbincl']) else None,
                inclination_error_min=float(row['pl_orbinclerr1']) if pd.notna(row['pl_orbinclerr1']) else None,
                inclination_error_max=float(row['pl_orbinclerr2']) if pd.notna(row['pl_orbinclerr2']) else None,
                equilibrium_temperature=float(row['pl_eqt']) if pd.notna(row['pl_eqt']) else None,
                equilibrium_temperature_error_min=float(row['pl_eqterr1']) if pd.notna(row['pl_eqterr1']) else None,
                equilibrium_temperature_error_max=float(row['pl_eqterr2']) if pd.notna(row['pl_eqterr2']) else None,
                source="NASA Exoplanet Archive"
            )
        except (ValueError, KeyError) as e:
            print(f"Error converting row to Exoplanet: {e}")
            return None 