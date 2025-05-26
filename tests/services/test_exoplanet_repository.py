import unittest
from datetime import datetime

from src.services.exoplanet_repository import ExoplanetRepository
from src.models.exoplanet import Exoplanet
from src.models.reference import DataPoint, Reference, SourceType

class TestExoplanetRepository(unittest.TestCase):
    def setUp(self):
        """
        Set up for each test method.
        This method is called before each test function is executed.
        """
        self.repository = ExoplanetRepository()
        self.ref1 = Reference(source=SourceType.NASA, update_date=datetime(2023, 1, 1), url="http://nasa.exoplanet.archive/planet1")
        self.ref2 = Reference(source=SourceType.EPE, update_date=datetime(2023, 1, 2), url="http://exoplanet.eu/planet2")
        self.ref3 = Reference(source=SourceType.OEC, update_date=datetime(2023, 1, 3), url="http://openexoplanetcatalogue.com/planet3")

    def test_initialization(self):
        """Test repository is initialized correctly."""
        self.assertEqual(self.repository.get_count(), 0)
        self.assertEqual(self.repository.get_all_exoplanets(), [])

    def test_add_single_exoplanet(self):
        """Test adding a single exoplanet to the repository."""
        planet1 = Exoplanet(name="Planet A")
        planet1.host_star = DataPoint("Star A", self.ref1)
        
        self.repository.add_exoplanets([planet1], "test_source_1")
        
        self.assertEqual(self.repository.get_count(), 1)
        retrieved_planet = self.repository.get_exoplanet_by_name("Planet A")
        self.assertIsNotNone(retrieved_planet)
        self.assertEqual(retrieved_planet.name, "Planet A")
        self.assertEqual(retrieved_planet.host_star.value, "Star A")
        self.assertIn(planet1, self.repository.get_all_exoplanets())

    def test_add_multiple_exoplanets(self):
        """Test adding multiple exoplanets from a single source."""
        planet1 = Exoplanet(name="Planet X")
        planet1.mass = DataPoint(1.0, self.ref1)
        planet2 = Exoplanet(name="Planet Y")
        planet2.radius = DataPoint(1.0, self.ref2)
        
        self.repository.add_exoplanets([planet1, planet2], "test_source_multi")
        
        self.assertEqual(self.repository.get_count(), 2)
        self.assertEqual(self.repository.get_exoplanet_by_name("Planet X").mass.value, 1.0)
        self.assertEqual(self.repository.get_exoplanet_by_name("Planet Y").radius.value, 1.0)

    def test_add_exoplanet_with_no_name(self):
        """Test that an exoplanet with no name is not added."""
        planet_no_name1 = Exoplanet(name="")
        planet_no_name2 = Exoplanet(name=None) # type: ignore 
        # Exoplanet model might enforce name to be string, but repository should handle it defensively
        
        self.repository.add_exoplanets([planet_no_name1], "test_source_no_name")
        self.assertEqual(self.repository.get_count(), 0, "Repository should not add planet with empty name string.")
        
        # Testing with a fresh repository for the None case, as previous call might have logged warnings.
        self.repository = ExoplanetRepository() 
        self.repository.add_exoplanets([planet_no_name2], "test_source_none_name")
        self.assertEqual(self.repository.get_count(), 0, "Repository should not add planet with None name.")

    def test_merge_exoplanet_data(self):
        """Test merging data for an exoplanet from different sources."""
        planet_v1 = Exoplanet(name="TestMergePlanet")
        planet_v1.mass = DataPoint(1.0, self.ref1)
        planet_v1.radius = DataPoint(1.0, self.ref1)
        planet_v1.add_source_info("source1", self.ref1.update_date)

        self.repository.add_exoplanets([planet_v1], "source1")
        
        planet_v2 = Exoplanet(name="TestMergePlanet") # Same name
        planet_v2.mass = DataPoint(1.1, self.ref2) # Updated mass, more recent reference
        planet_v2.orbital_period = DataPoint(100.0, self.ref2) # New data point
        planet_v2.add_source_info("source2", self.ref2.update_date)

        self.repository.add_exoplanets([planet_v2], "source2")
        
        self.assertEqual(self.repository.get_count(), 1, "Should only be one planet after merge.")
        
        merged_planet = self.repository.get_exoplanet_by_name("TestMergePlanet")
        self.assertIsNotNone(merged_planet)
        
        # Verify data points were merged correctly based on Exoplanet.merge_with logic
        # (typically prefers data from more recent reference or specific rules)
        self.assertEqual(merged_planet.mass.value, 1.1, "Mass should be updated from source2 (more recent).")
        self.assertEqual(merged_planet.mass.reference.source, SourceType.EPE)
        
        self.assertEqual(merged_planet.radius.value, 1.0, "Radius should remain from source1.")
        self.assertEqual(merged_planet.radius.reference.source, SourceType.NASA)
        
        self.assertIsNotNone(merged_planet.orbital_period, "Orbital period should be added from source2.")
        self.assertEqual(merged_planet.orbital_period.value, 100.0)
        self.assertEqual(merged_planet.orbital_period.reference.source, SourceType.EPE)

        # Check that source information is aggregated
        self.assertIn("source1", merged_planet.source_info)
        self.assertIn("source2", merged_planet.source_info)
        self.assertEqual(merged_planet.source_info["source1"], self.ref1.update_date)
        self.assertEqual(merged_planet.source_info["source2"], self.ref2.update_date)


    def test_get_exoplanet_by_name_not_found(self):
        """Test getting a non-existent exoplanet by name returns None."""
        planet_exists = Exoplanet(name="ExistingPlanet")
        self.repository.add_exoplanets([planet_exists], "source_exists")
        
        retrieved_planet = self.repository.get_exoplanet_by_name("NonExistentPlanet")
        self.assertIsNone(retrieved_planet)

if __name__ == '__main__':
    unittest.main()
