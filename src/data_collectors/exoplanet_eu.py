import pandas as pd
from typing import List
from src.models.exoplanet import Exoplanet

class ExoplanetEUCollector:
    def __init__(self, csv_path: str):
        """
        Initialize the collector with the path to the downloaded CSV file
        """
        self.csv_path = csv_path
    
    def fetch_data(self) -> List[Exoplanet]:
        """
        Read data from the CSV file and convert to Exoplanet objects
        """
        try:
            df = pd.read_csv(self.csv_path)
            
            # Convert to Exoplanet objects
            exoplanets = []
            for _, row in df.iterrows():
                exoplanet = self._convert_row_to_exoplanet(row)
                if exoplanet:
                    exoplanets.append(exoplanet)
            
            return exoplanets
            
        except Exception as e:
            print(f"Error reading data from CSV file: {e}")
            return []
    
    def _convert_row_to_exoplanet(self, row: pd.Series) -> Exoplanet:
        """
        Convert a row from the Exoplanet.eu CSV to an Exoplanet object
        """
        try:
            return Exoplanet(
                name=row['name'],
                host_star=row['star_name'],
                discovery_year=int(row['discovered']) if pd.notna(row['discovered']) else None,
                discovery_method=row['detection_type'],
                mass=float(row['mass']) if pd.notna(row['mass']) else None,
                mass_error_min=float(row['mass_error_min']) if pd.notna(row['mass_error_min']) else None,
                mass_error_max=float(row['mass_error_max']) if pd.notna(row['mass_error_max']) else None,
                radius=float(row['radius']) if pd.notna(row['radius']) else None,
                radius_error_min=float(row['radius_error_min']) if pd.notna(row['radius_error_min']) else None,
                radius_error_max=float(row['radius_error_max']) if pd.notna(row['radius_error_max']) else None,
                orbital_period=float(row['orbital_period']) if pd.notna(row['orbital_period']) else None,
                orbital_period_error_min=float(row['orbital_period_error_min']) if pd.notna(row['orbital_period_error_min']) else None,
                orbital_period_error_max=float(row['orbital_period_error_max']) if pd.notna(row['orbital_period_error_max']) else None,
                semi_major_axis=float(row['semi_major_axis']) if pd.notna(row['semi_major_axis']) else None,
                semi_major_axis_error_min=float(row['semi_major_axis_error_min']) if pd.notna(row['semi_major_axis_error_min']) else None,
                semi_major_axis_error_max=float(row['semi_major_axis_error_max']) if pd.notna(row['semi_major_axis_error_max']) else None,
                eccentricity=float(row['eccentricity']) if pd.notna(row['eccentricity']) else None,
                eccentricity_error_min=float(row['eccentricity_error_min']) if pd.notna(row['eccentricity_error_min']) else None,
                eccentricity_error_max=float(row['eccentricity_error_max']) if pd.notna(row['eccentricity_error_max']) else None,
                inclination=float(row['inclination']) if pd.notna(row['inclination']) else None,
                inclination_error_min=float(row['inclination_error_min']) if pd.notna(row['inclination_error_min']) else None,
                inclination_error_max=float(row['inclination_error_max']) if pd.notna(row['inclination_error_max']) else None,
                equilibrium_temperature=float(row['temp_calculated']) if pd.notna(row['temp_calculated']) else None,
                equilibrium_temperature_error_min=float(row['temp_calculated_error_min']) if pd.notna(row['temp_calculated_error_min']) else None,
                equilibrium_temperature_error_max=float(row['temp_calculated_error_max']) if pd.notna(row['temp_calculated_error_max']) else None,
                source="The Extrasolar Planets Encyclopaedia"
            )
        except (ValueError, KeyError) as e:
            print(f"Error converting row to Exoplanet: {e}")
            return None 