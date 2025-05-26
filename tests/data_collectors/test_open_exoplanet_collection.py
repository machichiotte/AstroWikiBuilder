import unittest
import os
from datetime import datetime

from src.data_collectors.open_exoplanet_collection import OpenExoplanetCollector
from src.models.exoplanet import Exoplanet
from src.models.reference import DataPoint, SourceType, Reference

class TestOpenExoplanetCollector(unittest.TestCase):
    def setUp(self):
        """
        Set up for each test method.
        """
        self.mock_txt_path = os.path.join(
            os.path.dirname(__file__),
            'mock_data',
            'open_exoplanet_sample.txt'
        )
        self.collector = OpenExoplanetCollector(cache_path=self.mock_txt_path, use_mock_data=True)

    def test_fetch_data_success_and_basic_parsing(self):
        """
        Test successful data fetching and parsing of valid exoplanets from OEC.
        """
        exoplanets = self.collector.fetch_data()

        # Based on open_exoplanet_sample.txt:
        # Valid: OECPlanetA, OECPlanetB, OECPlanetE, OECPlanetF, OECPlanetG, OECPlanetH, OECPlanetL, OECPlanetM (8)
        # Invalid name/star_name: (empty name), OECPlanetD (empty star_name) (2 skipped)
        # Malformed criticals (discovery_method, discovery_year): OECPlanetI (1 skipped by Exoplanet model)
        # Empty criticals: OECPlanetJ, OECPlanetK (2 skipped by Exoplanet model)
        # Expected count: 8
        self.assertEqual(len(exoplanets), 8, f"Expected 8 exoplanets, got {len(exoplanets)}")

        # Find OECPlanetA for detailed check
        planet_a = next((p for p in exoplanets if p.name == "OECPlanetA"), None)
        self.assertIsNotNone(planet_a)
        
        self.assertEqual(planet_a.name, "OECPlanetA")
        self.assertIsInstance(planet_a.host_star, DataPoint)
        self.assertEqual(planet_a.host_star.value, "OECStarA")
        self.assertEqual(planet_a.host_star.reference.source, SourceType.OEC)
        
        self.assertIsInstance(planet_a.discovery_method, DataPoint)
        self.assertEqual(planet_a.discovery_method.value, "Radial Velocity") # Mock data uses "Radial Velocity", instructions example was "RV"
        self.assertEqual(planet_a.discovery_method.reference.source, SourceType.OEC)
        
        self.assertIsInstance(planet_a.discovery_date, DataPoint)
        self.assertEqual(planet_a.discovery_date.value, "2020") # Stored as string
        self.assertEqual(planet_a.discovery_date.reference.source, SourceType.OEC)
        
        self.assertIsInstance(planet_a.mass, DataPoint)
        self.assertEqual(planet_a.mass.value, 1.0)
        
        self.assertIsInstance(planet_a.radius, DataPoint)
        self.assertEqual(planet_a.radius.value, 1.0)
        
        self.assertIsInstance(planet_a.semi_major_axis, DataPoint) # 'semimajoraxis' in CSV
        self.assertEqual(planet_a.semi_major_axis.value, 1.0)
        
        self.assertIsInstance(planet_a.eccentricity, DataPoint)
        self.assertEqual(planet_a.eccentricity.value, 0.1)
        
        self.assertIsInstance(planet_a.orbital_period, DataPoint) # 'period' in CSV
        self.assertEqual(planet_a.orbital_period.value, 365.0)

        self.assertIsInstance(planet_a.inclination, DataPoint)
        self.assertEqual(planet_a.inclination.value, 89.0)

        self.assertIsInstance(planet_a.argument_of_periastron, DataPoint) # 'longitudeofperiastron' in CSV
        self.assertEqual(planet_a.argument_of_periastron.value, 90.0)

        self.assertIsInstance(planet_a.periastron_time, DataPoint) # 'periastrontime' in CSV
        self.assertEqual(planet_a.periastron_time.value, 2450001.0)

        self.assertIsInstance(planet_a.spectral_type, DataPoint) # 'spectraltype' in CSV
        self.assertEqual(planet_a.spectral_type.value, "G0")
        
        self.assertIsInstance(planet_a.star_temperature, DataPoint)
        self.assertEqual(planet_a.star_temperature.value, 5800)

        self.assertIsInstance(planet_a.star_radius, DataPoint)
        self.assertEqual(planet_a.star_radius.value, 1.1)

        self.assertIsInstance(planet_a.star_mass, DataPoint)
        self.assertEqual(planet_a.star_mass.value, 1.1)

        self.assertIsInstance(planet_a.distance, DataPoint)
        self.assertEqual(planet_a.distance.value, 12.0)

        self.assertIsInstance(planet_a.apparent_magnitude, DataPoint) # 'apparentmagnitude' in CSV
        self.assertEqual(planet_a.apparent_magnitude.value, 6.0)
        
        self.assertIsNone(planet_a.status) # OEC data does not have 'planet_status' field
        
        self.assertIn("OA1", planet_a.other_names) # 'alt_names' in CSV

    def test_fetch_data_handles_malformed_data(self):
        """
        Test that malformed numerical data results in None for the specific DataPoint value in OEC.
        """
        exoplanets = self.collector.fetch_data()

        # OECPlanetF has 'bad_mass' for mass
        planet_f = next((p for p in exoplanets if p.name == "OECPlanetF"), None)
        self.assertIsNotNone(planet_f, "OECPlanetF should be parsed.")
        self.assertIsInstance(planet_f.mass, DataPoint)
        self.assertIsNone(planet_f.mass.value, "Mass for OECPlanetF should be None due to 'bad_mass'.")
        self.assertEqual(planet_f.radius.value, 1.2)

        # OECPlanetE has 'NaN' for semimajoraxis
        planet_e = next((p for p in exoplanets if p.name == "OECPlanetE"), None)
        self.assertIsNotNone(planet_e, "OECPlanetE should be parsed.")
        self.assertIsInstance(planet_e.semi_major_axis, DataPoint)
        self.assertIsNone(planet_e.semi_major_axis.value, "Semi-major axis for OECPlanetE should be None due to 'NaN'.")

        # OECPlanetH has text for all numeric fields
        planet_h = next((p for p in exoplanets if p.name == "OECPlanetH"), None)
        self.assertIsNotNone(planet_h, "OECPlanetH should be parsed.")
        self.assertIsNone(planet_h.mass.value)
        self.assertIsNone(planet_h.radius.value)
        self.assertIsNone(planet_h.semi_major_axis.value)
        # ... and so on for other numeric fields as tested for ExoplanetEU

    def test_fetch_data_empty_file(self):
        """Test fetching data from an empty OEC file."""
        empty_mock_path = os.path.join(os.path.dirname(__file__), 'mock_data', 'empty_oec.txt')
        with open(empty_mock_path, 'w') as f:
            f.write("#name,star_name,discovery_method,discovery_year\n") # Only header or comment
            
        collector = OpenExoplanetCollector(cache_path=empty_mock_path, use_mock_data=True)
        exoplanets = collector.fetch_data()
        
        self.assertEqual(len(exoplanets), 0)
        os.remove(empty_mock_path)

    def test_fetch_data_file_not_found(self):
        """Test fetching data when the OEC mock file does not exist."""
        non_existent_path = os.path.join(os.path.dirname(__file__), 'mock_data', 'non_existent_oec.txt')
        if os.path.exists(non_existent_path):
            os.remove(non_existent_path)
            
        collector = OpenExoplanetCollector(cache_path=non_existent_path, use_mock_data=True)
        
        with patch.object(collector.logger, 'warning') as mock_log_warning:
            exoplanets = collector.fetch_data()
            self.assertEqual(len(exoplanets), 0)
            mock_log_warning.assert_any_call(f"Mock file not found: {non_existent_path}")

if __name__ == '__main__':
    unittest.main()
