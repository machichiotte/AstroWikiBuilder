import requests
import xml.etree.ElementTree as ET
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
            
            # Parse XML data
            root = ET.fromstring(response.text)
            print("Racine XML OEP :", root.tag)
            
            exoplanets = []
            for system in root.findall(".//system"):
                try:
                    exoplanet = self._convert_system_to_exoplanet(system)
                    if exoplanet:
                        exoplanets.append(exoplanet)
                except Exception as e:
                    print(f"Erreur sur le système : {system}")
                    print(e)
            
            return exoplanets
            
        except requests.RequestException as e:
            print(f"Error fetching data from Open Exoplanet Catalogue: {e}")
            return []
        except Exception as e:
            print(f"Erreur lors du parsing du XML OEP : {e}")
            print(response.text)
            return []
    
    def _create_reference(self) -> Reference:
        """Crée une référence pour les données OEP"""
        return Reference(
            source=SourceType.OEP,
            date=datetime.now(),
            url="https://www.openexoplanetcatalogue.com/"
        )
    
    def _get_text(self, element: ET.Element, tag: str) -> str:
        """Récupère le texte d'un élément XML"""
        child = element.find(tag)
        return child.text if child is not None else None
    
    def _get_float(self, element: ET.Element, tag: str) -> float:
        """Récupère un nombre flottant d'un élément XML"""
        text = self._get_text(element, tag)
        return float(text) if text is not None else None
    
    def _convert_system_to_exoplanet(self, system: ET.Element) -> Exoplanet:
        """
        Convert a system from the Open Exoplanet Catalogue to an Exoplanet object
        """
        try:
            ref = self._create_reference()
            
            # Récupération des données de base
            name = self._get_text(system, "name")
            if not name:
                return None
            
            # Création de l'objet Exoplanet avec les données de base
            exoplanet = Exoplanet(
                name=name,
                host_star=DataPoint(self._get_text(system, "star/name"), ref),
                discovery_method=DataPoint(self._get_text(system, "discoverymethod"), ref),
                discovery_date=DataPoint(self._get_text(system, "discoveryyear"), ref)
            )
            
            # Caractéristiques orbitales
            semi_major_axis = self._get_float(system, "semimajoraxis")
            if semi_major_axis is not None:
                exoplanet.semi_major_axis = DataPoint(semi_major_axis, ref)
            
            eccentricity = self._get_float(system, "eccentricity")
            if eccentricity is not None:
                exoplanet.eccentricity = DataPoint(eccentricity, ref)
            
            orbital_period = self._get_float(system, "period")
            if orbital_period is not None:
                exoplanet.orbital_period = DataPoint(orbital_period, ref)
            
            inclination = self._get_float(system, "inclination")
            if inclination is not None:
                exoplanet.inclination = DataPoint(inclination, ref)
            
            # Caractéristiques physiques
            mass = self._get_float(system, "mass")
            if mass is not None:
                exoplanet.mass = DataPoint(mass, ref)
            
            radius = self._get_float(system, "radius")
            if radius is not None:
                exoplanet.radius = DataPoint(radius, ref)
            
            temperature = self._get_float(system, "temperature")
            if temperature is not None:
                exoplanet.temperature = DataPoint(temperature, ref)
            
            # Informations sur l'étoile
            star = system.find("star")
            if star is not None:
                spectral_type = self._get_text(star, "spectraltype")
                if spectral_type:
                    exoplanet.spectral_type = DataPoint(spectral_type, ref)
                
                star_temperature = self._get_float(star, "temperature")
                if star_temperature:
                    exoplanet.star_temperature = DataPoint(star_temperature, ref)
                
                star_radius = self._get_float(star, "radius")
                if star_radius:
                    exoplanet.star_radius = DataPoint(star_radius, ref)
                
                star_mass = self._get_float(star, "mass")
                if star_mass:
                    exoplanet.star_mass = DataPoint(star_mass, ref)
                
                distance = self._get_float(star, "distance")
                if distance:
                    exoplanet.distance = DataPoint(distance, ref)
                
                constellation = self._get_text(star, "constellation")
                if constellation:
                    exoplanet.constellation = DataPoint(constellation, ref)
                
                apparent_magnitude = self._get_float(star, "apparentmagnitude")
                if apparent_magnitude:
                    exoplanet.apparent_magnitude = DataPoint(apparent_magnitude, ref)
            
            # Autres noms
            for alt_name in system.findall("name"):
                if alt_name.text != name:
                    exoplanet.other_names[alt_name.text] = DataPoint(alt_name.text, ref)
            
            return exoplanet
            
        except (ValueError, KeyError) as e:
            print(f"Error converting system to Exoplanet: {e}")
            return None 