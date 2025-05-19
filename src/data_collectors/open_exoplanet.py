import requests
import csv
from io import StringIO
from typing import List
from datetime import datetime
from src.models.exoplanet import Exoplanet
from src.models.reference import DataPoint, Reference, SourceType

class OpenExoplanetCollector:
    BASE_URL = "https://raw.githubusercontent.com/OpenExoplanetCatalogue/oec_tables/master/comma_separated/open_exoplanet_catalogue.txt"
    
    def __init__(self):
        self.session = requests.Session()
    
    def fetch_data(self) -> List[Exoplanet]:
        """
        Fetch data from Open Exoplanet Catalogue and convert to Exoplanet objects
        """
        try:
            print(f"URL de l'API OEP : {self.BASE_URL}")
            
            response = self.session.get(self.BASE_URL)
            response.raise_for_status()
            
            if not response.text or len(response.text) < 100:
                print("Réponse brute de l'API OEP :")
                print(response.text)
                return []
            
            # Parse CSV data
            csv_data = StringIO(response.text)
            reader = csv.DictReader(csv_data)
            
            exoplanets = []
            for row in reader:
                try:
                    exoplanet = self._convert_row_to_exoplanet(row)
                    if exoplanet:
                        exoplanets.append(exoplanet)
                except Exception as e:
                    print(f"Erreur sur la ligne : {row}")
                    print(e)
            
            return exoplanets
            
        except requests.RequestException as e:
            print(f"Error fetching data from Open Exoplanet Catalogue: {e}")
            return []
        except Exception as e:
            print(f"Erreur lors du parsing du CSV OEP : {e}")
            print(response.text)
            return []
    
    def _create_reference(self) -> Reference:
        """Crée une référence pour les données OEP"""
        return Reference(
            source=SourceType.OEP,
            date=datetime.now(),
            url="https://www.openexoplanetcatalogue.com/"
        )
    
    def _get_value(self, row: dict, key: str) -> str:
        """Récupère une valeur du dictionnaire"""
        return row.get(key)
    
    def _get_float(self, row: dict, key: str) -> float:
        """Récupère un nombre flottant du dictionnaire"""
        value = self._get_value(row, key)
        try:
            return float(value) if value is not None else None
        except (ValueError, TypeError):
            return None
    
    def _convert_row_to_exoplanet(self, row: dict) -> Exoplanet:
        """
        Convert a row from the Open Exoplanet Catalogue to an Exoplanet object
        """
        try:
            ref = self._create_reference()
            
            # Récupération des données de base
            name = self._get_value(row, "name")
            if not name:
                return None
            
            # Création de l'objet Exoplanet avec les données de base
            exoplanet = Exoplanet(
                name=name,
                host_star=DataPoint(self._get_value(row, "star_name"), ref),
                discovery_method=DataPoint(self._get_value(row, "discoverymethod"), ref),
                discovery_date=DataPoint(self._get_value(row, "discoveryyear"), ref)
            )
            
            # Caractéristiques orbitales
            semi_major_axis = self._get_float(row, "semimajoraxis")
            if semi_major_axis is not None:
                exoplanet.semi_major_axis = DataPoint(semi_major_axis, ref)
            
            eccentricity = self._get_float(row, "eccentricity")
            if eccentricity is not None:
                exoplanet.eccentricity = DataPoint(eccentricity, ref)
            
            orbital_period = self._get_float(row, "period")
            if orbital_period is not None:
                exoplanet.orbital_period = DataPoint(orbital_period, ref)
            
            inclination = self._get_float(row, "inclination")
            if inclination is not None:
                exoplanet.inclination = DataPoint(inclination, ref)
            
            # Caractéristiques physiques
            mass = self._get_float(row, "mass")
            if mass is not None:
                exoplanet.mass = DataPoint(mass, ref)
            
            radius = self._get_float(row, "radius")
            if radius is not None:
                exoplanet.radius = DataPoint(radius, ref)
            
            temperature = self._get_float(row, "temperature")
            if temperature is not None:
                exoplanet.temperature = DataPoint(temperature, ref)
            
            # Informations sur l'étoile
            spectral_type = self._get_value(row, "spectraltype")
            if spectral_type:
                exoplanet.spectral_type = DataPoint(spectral_type, ref)
            
            star_temperature = self._get_float(row, "star_temperature")
            if star_temperature:
                exoplanet.star_temperature = DataPoint(star_temperature, ref)
            
            star_radius = self._get_float(row, "star_radius")
            if star_radius:
                exoplanet.star_radius = DataPoint(star_radius, ref)
            
            star_mass = self._get_float(row, "star_mass")
            if star_mass:
                exoplanet.star_mass = DataPoint(star_mass, ref)
            
            distance = self._get_float(row, "distance")
            if distance:
                exoplanet.distance = DataPoint(distance, ref)
            
            constellation = self._get_value(row, "constellation")
            if constellation:
                exoplanet.constellation = DataPoint(constellation, ref)
            
            apparent_magnitude = self._get_float(row, "apparentmagnitude")
            if apparent_magnitude:
                exoplanet.apparent_magnitude = DataPoint(apparent_magnitude, ref)
            
            # Autres noms
            alt_names = self._get_value(row, "alt_names")
            if alt_names:
                for alt_name in alt_names.split(','):
                    alt_name = alt_name.strip()
                    if alt_name and alt_name != name:
                        exoplanet.other_names[alt_name] = DataPoint(alt_name, ref)
            
            return exoplanet
            
        except (ValueError, KeyError) as e:
            print(f"Error converting row to Exoplanet: {e}")
            return None 