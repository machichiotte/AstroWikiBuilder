import xml.etree.ElementTree as ET
import urllib.request
import gzip
import io
from typing import List
from src.models.exoplanet import Exoplanet

class OpenExoplanetCollector:
    def __init__(self):
        self.url = "https://github.com/OpenExoplanetCatalogue/oec_gzip/raw/master/systems.xml.gz"
    
    def fetch_data(self) -> List[Exoplanet]:
        """
        Fetch data from Open Exoplanet Catalogue and convert to Exoplanet objects
        """
        try:
            # Download and parse the XML file
            response = urllib.request.urlopen(self.url)
            xml_data = gzip.GzipFile(fileobj=io.BytesIO(response.read()))
            tree = ET.parse(xml_data)
            root = tree.getroot()
            
            exoplanets = []
            for system in root.findall(".//system"):
                for planet in system.findall(".//planet"):
                    exoplanet = self._convert_planet_to_exoplanet(planet, system)
                    if exoplanet:
                        exoplanets.append(exoplanet)
            
            return exoplanets
            
        except Exception as e:
            print(f"Error fetching data from Open Exoplanet Catalogue: {e}")
            return []
    
    def _convert_planet_to_exoplanet(self, planet: ET.Element, system: ET.Element) -> Exoplanet:
        """
        Convert a planet element from the Open Exoplanet Catalogue to an Exoplanet object
        """
        try:
            # Get star information
            star = system.find(".//star")
            star_name = star.findtext("name") if star is not None else None
            
            # Get discovery information
            discovery = planet.find(".//discovery")
            discovery_year = int(discovery.findtext("year")) if discovery is not None and discovery.findtext("year") is not None else None
            discovery_method = discovery.findtext("method") if discovery is not None else None
            
            # Helper function to safely convert to float
            def safe_float(value: str) -> float:
                if value is None or value.strip() == "":
                    return None
                try:
                    return float(value)
                except ValueError:
                    return None
            
            # Get mass information
            mass = safe_float(planet.findtext("mass"))
            mass_error = safe_float(planet.findtext("massError"))
            
            # Get radius information
            radius = safe_float(planet.findtext("radius"))
            radius_error = safe_float(planet.findtext("radiusError"))
            
            # Get orbital parameters
            orbital_period = safe_float(planet.findtext("period"))
            orbital_period_error = safe_float(planet.findtext("periodError"))
            
            semi_major_axis = safe_float(planet.findtext("semimajoraxis"))
            semi_major_axis_error = safe_float(planet.findtext("semimajoraxisError"))
            
            eccentricity = safe_float(planet.findtext("eccentricity"))
            eccentricity_error = safe_float(planet.findtext("eccentricityError"))
            
            inclination = safe_float(planet.findtext("inclination"))
            inclination_error = safe_float(planet.findtext("inclinationError"))
            
            # Get temperature information
            temperature = safe_float(planet.findtext("temperature"))
            temperature_error = safe_float(planet.findtext("temperatureError"))
            
            return Exoplanet(
                name=planet.findtext("name"),
                host_star=star_name,
                discovery_year=discovery_year,
                discovery_method=discovery_method,
                mass=mass,
                mass_error_min=mass_error,
                mass_error_max=mass_error,
                radius=radius,
                radius_error_min=radius_error,
                radius_error_max=radius_error,
                orbital_period=orbital_period,
                orbital_period_error_min=orbital_period_error,
                orbital_period_error_max=orbital_period_error,
                semi_major_axis=semi_major_axis,
                semi_major_axis_error_min=semi_major_axis_error,
                semi_major_axis_error_max=semi_major_axis_error,
                eccentricity=eccentricity,
                eccentricity_error_min=eccentricity_error,
                eccentricity_error_max=eccentricity_error,
                inclination=inclination,
                inclination_error_min=inclination_error,
                inclination_error_max=inclination_error,
                equilibrium_temperature=temperature,
                equilibrium_temperature_error_min=temperature_error,
                equilibrium_temperature_error_max=temperature_error,
                source="Open Exoplanet Catalogue"
            )
        except (ValueError, AttributeError) as e:
            print(f"Error converting planet to Exoplanet: {e}")
            return None 