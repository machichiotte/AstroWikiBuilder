import unittest
import os
from datetime import datetime

from src.data_collectors.exoplanet_eu import ExoplanetEUCollector
from src.models.exoplanet import Exoplanet
from src.models.reference import DataPoint, SourceType, Reference

class TestExoplanetEUCollector(unittest.TestCase):
    def setUp(self):
        """
        Set up for each test method.
        This method is called before each test function is executed.
        """
        # Construct path relative to the tests directory or use an absolute path
        # Assuming the script is run from the root of the project
        self.mock_csv_path = os.path.join(
            os.path.dirname(__file__), 
            'mock_data', 
            'exoplanet_eu_sample.csv'
        )
        self.collector = ExoplanetEUCollector(cache_path=self.mock_csv_path, use_mock_data=True)
        
        # Expected reference for mock data - used for assertions
        # The date in the mock CSV is 2023-10-26, but the collector's last_update_date is datetime.now()
        # For consistency in tests, we might need to mock datetime.now() or accept this dynamic nature.
        # For now, we'll create a reference based on a fixed date if our main goal is to check SourceType and URL.
        # However, the Exoplanet model's DataPoint will get a Reference from collector._create_reference()
        # which uses datetime.now(). So, we will assert based on what the collector *actually* does.

    def test_fetch_data_success_and_basic_parsing(self):
        """
        Test successful data fetching and parsing of valid exoplanets.
        Verifies correct number of planets and attributes of a sample planet.
        """
        exoplanets = self.collector.fetch_data()
        
        # Based on exoplanet_eu_sample.csv:
        # Valid: PlanetA, PlanetB, PlanetE, PlanetF, PlanetG, PlanetH, PlanetL, PlanetP, PlanetQ, PlanetR (10)
        # Invalid name/star_name: (empty), PlanetD (2 skipped)
        # Invalid status: PlanetN (1 skipped by Exoplanet model, not collector directly)
        # Malformed criticals (detection, discovered): PlanetJ (1 skipped by Exoplanet model)
        # Empty criticals: PlanetK, PlanetM (2 skipped by Exoplanet model)
        # Malformed numbers for attributes but exoplanet created: PlanetI, PlanetO
        # The collector itself should primarily filter based on pd.read_csv and then Exoplanet model filters.
        # The Exoplanet model skips if name or star_name is missing.
        # It also skips if detection_type or discovered is missing as these are basic requirements.
        # The sample data has:
        # PlanetA - valid
        # PlanetB - valid (many NaNs for non-critical)
        # (No name) - skipped by Exoplanet model
        # PlanetD (No star_name) - skipped by Exoplanet model
        # PlanetE - valid (NaN for semi_major_axis)
        # PlanetF - valid (invalid_mass, will be None)
        # PlanetG - valid
        # PlanetH - valid
        # PlanetI - valid (all attributes are text, will be None after conversion)
        # PlanetJ - No detection_type or discovered - skipped by Exoplanet model
        # PlanetK - No detection_type or discovered - skipped by Exoplanet model
        # PlanetL - valid
        # PlanetM - No detection_type or discovered - skipped by Exoplanet model
        # PlanetN - valid (InvalidStatus, but Exoplanet model will create it, status might be None or default)
        # PlanetO - valid (all numeric attributes are text, will be None)
        # PlanetP - valid
        # PlanetQ - valid
        # PlanetR - valid
        # Expected count: PlanetA, B, E, F, G, H, I, N, O, P, Q, R = 12
        self.assertEqual(len(exoplanets), 12, f"Expected 12 exoplanets, got {len(exoplanets)}")

        # Find PlanetA for detailed check
        planet_a = next((p for p in exoplanets if p.name == "PlanetA"), None)
        self.assertIsNotNone(planet_a)
        
        self.assertEqual(planet_a.name, "PlanetA")
        self.assertIsInstance(planet_a.host_star, DataPoint)
        self.assertEqual(planet_a.host_star.value, "StarA")
        self.assertEqual(planet_a.host_star.reference.source, SourceType.EPE)
        
        self.assertIsInstance(planet_a.discovery_method, DataPoint)
        self.assertEqual(planet_a.discovery_method.value, "Radial Velocity")
        self.assertEqual(planet_a.discovery_method.reference.source, SourceType.EPE)
        
        self.assertIsInstance(planet_a.discovery_date, DataPoint)
        self.assertEqual(planet_a.discovery_date.value, "2020") # Stored as string
        self.assertEqual(planet_a.discovery_date.reference.source, SourceType.EPE)
        
        self.assertIsInstance(planet_a.mass, DataPoint)
        self.assertEqual(planet_a.mass.value, 1.0)
        self.assertEqual(planet_a.mass.reference.source, SourceType.EPE)
        
        self.assertIsInstance(planet_a.radius, DataPoint)
        self.assertEqual(planet_a.radius.value, 1.0)
        
        self.assertIsInstance(planet_a.semi_major_axis, DataPoint)
        self.assertEqual(planet_a.semi_major_axis.value, 1.0)
        
        self.assertIsInstance(planet_a.eccentricity, DataPoint)
        self.assertEqual(planet_a.eccentricity.value, 0.1)
        
        self.assertIsInstance(planet_a.orbital_period, DataPoint)
        self.assertEqual(planet_a.orbital_period.value, 365.0)

        self.assertIsInstance(planet_a.inclination, DataPoint)
        self.assertEqual(planet_a.inclination.value, 89.0)

        self.assertIsInstance(planet_a.argument_of_periastron, DataPoint) # omega
        self.assertEqual(planet_a.argument_of_periastron.value, 90.0)

        self.assertIsInstance(planet_a.periastron_time, DataPoint) # tperi
        self.assertEqual(planet_a.periastron_time.value, 2450000.0)

        self.assertIsInstance(planet_a.spectral_type, DataPoint) # star_sp_type
        self.assertEqual(planet_a.spectral_type.value, "G2V")
        
        self.assertIsInstance(planet_a.star_temperature, DataPoint) # star_teff
        self.assertEqual(planet_a.star_temperature.value, 5700)

        self.assertIsInstance(planet_a.star_radius, DataPoint)
        self.assertEqual(planet_a.star_radius.value, 1.0)

        self.assertIsInstance(planet_a.star_mass, DataPoint)
        self.assertEqual(planet_a.star_mass.value, 1.0)

        self.assertIsInstance(planet_a.distance, DataPoint) # star_distance
        self.assertEqual(planet_a.distance.value, 10.0)

        self.assertIsInstance(planet_a.apparent_magnitude, DataPoint) # mag_v
        self.assertEqual(planet_a.apparent_magnitude.value, 5.0)
        
        self.assertIsInstance(planet_a.status, DataPoint)
        self.assertEqual(planet_a.status.value, "Confirmed")
        
        self.assertIn("A1", planet_a.other_names)
        self.assertIn("A2", planet_a.other_names)

        # Verify a planet with some missing non-critical data (PlanetB)
        planet_b = next((p for p in exoplanets if p.name == "PlanetB"), None)
        self.assertIsNotNone(planet_b)
        self.assertEqual(planet_b.name, "PlanetB")
        self.assertEqual(planet_b.host_star.value, "StarB")
        self.assertEqual(planet_b.discovery_method.value, "Transit")
        self.assertEqual(planet_b.discovery_date.value, "2021")
        self.assertEqual(planet_b.mass.value, 0.5)
        self.assertEqual(planet_b.radius.value, 0.8)
        self.assertEqual(planet_b.semi_major_axis.value, 0.8)
        self.assertEqual(planet_b.eccentricity.value, 0.05)
        self.assertEqual(planet_b.orbital_period.value, 200.0)
        self.assertIsNone(planet_b.inclination) # Missing in CSV
        self.assertIsNone(planet_b.argument_of_periastron) # Missing in CSV
        self.assertIsNone(planet_b.periastron_time) # Missing in CSV
        self.assertEqual(planet_b.status.value, "Unconfirmed")
        self.assertIn("PlanetB_alt", planet_b.other_names)

    # test_fetch_data_handles_missing_critical_info will be implicitly covered by the count in test_fetch_data_success
    # as the Exoplanet model's _convert_row_to_exoplanet handles skipping rows with missing name/star_name/detection_type/discovered

    def test_fetch_data_handles_malformed_data(self):
        """
        Test that malformed numerical data results in None for the specific DataPoint value,
        but the exoplanet object is still created if critical info is present.
        """
        exoplanets = self.collector.fetch_data()

        # PlanetF has 'invalid_mass' for mass
        planet_f = next((p for p in exoplanets if p.name == "PlanetF"), None)
        self.assertIsNotNone(planet_f, "PlanetF should be parsed.")
        self.assertIsInstance(planet_f.mass, DataPoint, "Mass should be a DataPoint object even if value is None.")
        self.assertIsNone(planet_f.mass.value, "Mass for PlanetF should be None due to malformed data 'invalid_mass'.")
        self.assertEqual(planet_f.radius.value, 1.2) # Other valid data should be present

        # PlanetE has 'NaN' for semi_major_axis
        planet_e = next((p for p in exoplanets if p.name == "PlanetE"), None)
        self.assertIsNotNone(planet_e, "PlanetE should be parsed.")
        self.assertIsInstance(planet_e.semi_major_axis, DataPoint)
        self.assertIsNone(planet_e.semi_major_axis.value, "Semi-major axis for PlanetE should be None due to 'NaN'.")
        
        # PlanetI has text for all numeric fields
        planet_i = next((p for p in exoplanets if p.name == "PlanetI"), None)
        self.assertIsNotNone(planet_i, "PlanetI should be parsed.")
        self.assertIsNone(planet_i.mass.value)
        self.assertIsNone(planet_i.radius.value)
        self.assertIsNone(planet_i.semi_major_axis.value)
        self.assertIsNone(planet_i.eccentricity.value)
        self.assertIsNone(planet_i.orbital_period.value)
        self.assertIsNone(planet_i.inclination.value)
        self.assertIsNone(planet_i.argument_of_periastron.value)
        self.assertIsNone(planet_i.periastron_time.value)
        self.assertIsNone(planet_i.star_temperature.value)
        self.assertIsNone(planet_i.star_radius.value)
        self.assertIsNone(planet_i.star_mass.value)
        self.assertIsNone(planet_i.distance.value)
        self.assertIsNone(planet_i.apparent_magnitude.value)
        self.assertEqual(planet_i.spectral_type.value, "G2V") # String field should be fine
        self.assertEqual(planet_i.status.value, "Confirmed")

    def test_fetch_data_empty_file(self):
        """Test fetching data from an empty or effectively empty (headers/comments only) CSV file."""
        empty_mock_path = os.path.join(os.path.dirname(__file__), 'mock_data', 'empty_exoplanet_eu.csv')
        with open(empty_mock_path, 'w') as f:
            f.write("#This is a comment only file\n")
            f.write("#name,star_name,detection_type,discovered\n") # Commented out header
            
        collector = ExoplanetEUCollector(cache_path=empty_mock_path, use_mock_data=True)
        exoplanets = collector.fetch_data()
        
        self.assertEqual(len(exoplanets), 0, "Should return an empty list for an empty or comment-only file.")
        os.remove(empty_mock_path) # Clean up

    def test_fetch_data_file_not_found(self):
        """Test fetching data when the mock CSV file does not exist."""
        non_existent_path = os.path.join(os.path.dirname(__file__), 'mock_data', 'non_existent_file.csv')
        
        # Ensure file does not exist before test
        if os.path.exists(non_existent_path):
            os.remove(non_existent_path)
            
        collector = ExoplanetEUCollector(cache_path=non_existent_path, use_mock_data=True)
        
        # Patch logging to check for warnings
        with patch.object(collector.logger, 'warning') as mock_log_warning:
            exoplanets = collector.fetch_data()
            self.assertEqual(len(exoplanets), 0, "Should return an empty list if file not found.")
            mock_log_warning.assert_any_call(f"Mock file not found: {non_existent_path}")

if __name__ == '__main__':
    unittest.main()
