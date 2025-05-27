import unittest
from unittest.mock import patch, MagicMock

from src.utils.category_generator import CategoryGenerator
from src.models.exoplanet import Exoplanet 
# Assuming Exoplanet and other necessary models can be imported or mocked.
# If direct import and instantiation of Exoplanet is complex, 
# consider using MagicMock for the exoplanet object itself,
# and setting attributes on the mock.

# Minimal mock for Exoplanet attribute holder (like a simple namespace)
class MockAttribute:
    def __init__(self, value):
        self.value = value

class TestCategoryGenerator(unittest.TestCase):

    @patch('src.utils.category_generator.parse_categories')
    @patch('src.utils.category_generator.PlanetTypeUtils')
    def test_generate_categories_all_predefined(self, MockPlanetTypeUtils, mock_parse_categories):
        # Mock `parse_categories` return value
        mock_parse_categories.return_value = {
            "Constellations": ["[[Catégorie:Constellation du Cygne]]"],
            "Discovery Methods": ["[[Catégorie:Exoplanète découverte par la méthode des transits]]"],
            "Discovery Years": ["[[Catégorie:Exoplanète découverte en 2000]]"],
            "Discovery Instruments/Telescopes": ["[[Catégorie:Exoplanète découverte grâce à Kepler]]"]
        }

        # Mock PlanetTypeUtils
        mock_planet_type_instance = MockPlanetTypeUtils.return_value
        mock_planet_type_instance.get_planet_type.return_value = "Jupiter chaud"

        # Create CategoryGenerator instance
        generator = CategoryGenerator()

        # Create a mock Exoplanet object 
        mock_exoplanet = MagicMock(spec=Exoplanet)
        mock_exoplanet.constellation = MockAttribute("Cygne")
        mock_exoplanet.discovery_method = MockAttribute("Transit")
        
        # Mocking discovery_date for year extraction
        mock_date_obj = MagicMock()
        mock_date_obj.year = 2000
        mock_exoplanet.discovery_date = MockAttribute(mock_date_obj)
        
        mock_exoplanet.discovered_by = MockAttribute("Kepler") # This should match an entry in generator.instrument_map
        mock_exoplanet.spectral_type = MockAttribute("G2V")
        
        categories = generator.generate_categories(mock_exoplanet)

        expected_categories = sorted([
            "[[Catégorie:Exoplanète]]",
            "[[Catégorie:Constellation du Cygne]]",
            "[[Catégorie:Exoplanète découverte par la méthode des transits]]",
            "[[Catégorie:Exoplanète découverte en 2000]]",
            "[[Catégorie:Exoplanète découverte grâce à Kepler]]",
            "[[Catégorie:Exoplanète orbitant une étoile de type G]]", 
            "[[Catégorie:Exoplanète de type Jupiter chaud]]" 
        ])
        self.assertEqual(sorted(categories), expected_categories)

    @patch('src.utils.category_generator.parse_categories')
    @patch('src.utils.category_generator.PlanetTypeUtils')
    def test_generate_categories_no_predefined_match(self, MockPlanetTypeUtils, mock_parse_categories):
        mock_parse_categories.return_value = {
            "Constellations": ["[[Catégorie:Constellation de Lyra]]"], # Different constellation
            "Discovery Methods": ["[[Catégorie:Exoplanète découverte par microlentille gravitationnelle]]"], # Different method
            "Discovery Years": ["[[Catégorie:Exoplanète découverte en 2010]]"], # Different year
            "Discovery Instruments/Telescopes": ["[[Catégorie:Exoplanète découverte grâce au télescope spatial Hubble]]"] # Different instrument
        }
        mock_planet_type_instance = MockPlanetTypeUtils.return_value
        mock_planet_type_instance.get_planet_type.return_value = "Super-Terre"

        generator = CategoryGenerator()
        mock_exoplanet = MagicMock(spec=Exoplanet)
        mock_exoplanet.constellation = MockAttribute("Cygne")
        mock_exoplanet.discovery_method = MockAttribute("Transit")
        mock_date_obj = MagicMock()
        mock_date_obj.year = 2000
        mock_exoplanet.discovery_date = MockAttribute(mock_date_obj)
        mock_exoplanet.discovered_by = MockAttribute("Kepler")
        mock_exoplanet.spectral_type = MockAttribute("M1V")

        categories = generator.generate_categories(mock_exoplanet)
        expected_categories = sorted([
            "[[Catégorie:Exoplanète]]",
            "[[Catégorie:Exoplanète orbitant une étoile de type M]]",
            "[[Catégorie:Exoplanète de type Super-Terre]]"
        ])
        self.assertEqual(sorted(categories), expected_categories)

    @patch('src.utils.category_generator.parse_categories')
    @patch('src.utils.category_generator.PlanetTypeUtils')
    def test_generate_categories_partial_match(self, MockPlanetTypeUtils, mock_parse_categories):
        mock_parse_categories.return_value = {
            "Constellations": ["[[Catégorie:Constellation du Cygne]]"], # Match
            "Discovery Methods": ["[[Catégorie:Exoplanète découverte par microlentille gravitationnelle]]"], # No match
            "Discovery Years": ["[[Catégorie:Exoplanète découverte en 2000]]"], # Match
            "Discovery Instruments/Telescopes": ["[[Catégorie:Exoplanète découverte grâce au télescope spatial Hubble]]"] # No match
        }
        mock_planet_type_instance = MockPlanetTypeUtils.return_value
        mock_planet_type_instance.get_planet_type.return_value = "Naine gazeuse"

        generator = CategoryGenerator()
        mock_exoplanet = MagicMock(spec=Exoplanet)
        mock_exoplanet.constellation = MockAttribute("Cygne")
        mock_exoplanet.discovery_method = MockAttribute("Transit") # Will use internal map, but won't find in predefined
        mock_date_obj = MagicMock()
        mock_date_obj.year = 2000
        mock_exoplanet.discovery_date = MockAttribute(mock_date_obj)
        mock_exoplanet.discovered_by = MockAttribute("TESS") # Will use internal map, but won't find in predefined
        mock_exoplanet.spectral_type = MockAttribute("K5V")

        categories = generator.generate_categories(mock_exoplanet)
        expected_categories = sorted([
            "[[Catégorie:Exoplanète]]",
            "[[Catégorie:Constellation du Cygne]]",
            "[[Catégorie:Exoplanète découverte en 2000]]",
            "[[Catégorie:Exoplanète orbitant une étoile de type K]]",
            "[[Catégorie:Exoplanète de type Naine gazeuse]]"
        ])
        self.assertEqual(sorted(categories), expected_categories)

    @patch('src.utils.category_generator.parse_categories')
    @patch('src.utils.category_generator.PlanetTypeUtils')
    def test_generate_categories_optional_fields_none(self, MockPlanetTypeUtils, mock_parse_categories):
        # As per prompt, this test now uses empty predefined lists.
        mock_parse_categories.return_value = { 
            "Constellations": [], "Discovery Methods": [], "Discovery Years": [], "Discovery Instruments/Telescopes": []
        }
        mock_planet_type_instance = MockPlanetTypeUtils.return_value
        mock_planet_type_instance.get_planet_type.return_value = "Rocheuse"

        generator = CategoryGenerator()
        mock_exoplanet = MagicMock(spec=Exoplanet)
        mock_exoplanet.constellation = None 
        mock_exoplanet.discovery_method = MockAttribute("Transit") # Predefined list is empty, internal map will hit but not add
        mock_exoplanet.discovery_date = None
        mock_exoplanet.discovered_by = None
        mock_exoplanet.spectral_type = None 

        categories = generator.generate_categories(mock_exoplanet)
        expected_categories = sorted([
            "[[Catégorie:Exoplanète]]",
            "[[Catégorie:Exoplanète de type Rocheuse]]"
        ])
        self.assertEqual(sorted(categories), expected_categories)

    @patch('src.utils.category_generator.parse_categories')
    @patch('src.utils.category_generator.PlanetTypeUtils')
    def test_generate_categories_planet_type_unknown_or_exception(self, MockPlanetTypeUtils, mock_parse_categories):
        mock_parse_categories.return_value = {} # Empty
        
        mock_planet_type_instance = MockPlanetTypeUtils.return_value
        # generator = CategoryGenerator() # Not strictly needed before setting mock_planet_type_instance behavior
        generator = CategoryGenerator() # Initialize generator
        mock_exoplanet = MagicMock(spec=Exoplanet)
        mock_exoplanet.constellation = None
        mock_exoplanet.discovery_method = None
        mock_exoplanet.discovery_date = None
        mock_exoplanet.discovered_by = None
        mock_exoplanet.spectral_type = None
        
        # Test with "Unknown" planet type
        mock_planet_type_instance.get_planet_type.return_value = "Unknown"
        categories = generator.generate_categories(mock_exoplanet)
        self.assertEqual(sorted(categories), sorted(["[[Catégorie:Exoplanète]]"]))

        # Test with get_planet_type raising an exception
        mock_planet_type_instance.get_planet_type.side_effect = Exception("Test error")
        categories = generator.generate_categories(mock_exoplanet)
        self.assertEqual(sorted(categories), sorted(["[[Catégorie:Exoplanète]]"]))
        
    @patch('src.utils.category_generator.parse_categories')
    @patch('src.utils.category_generator.PlanetTypeUtils')
    def test_discovery_year_as_string(self, MockPlanetTypeUtils, mock_parse_categories):
        mock_parse_categories.return_value = {
            "Discovery Years": ["[[Catégorie:Exoplanète découverte en 2023]]"]
            # Other lists can be empty or absent for this test's focus
        }
        mock_planet_type_instance = MockPlanetTypeUtils.return_value
        mock_planet_type_instance.get_planet_type.return_value = "TestType"
        generator = CategoryGenerator()
        mock_exoplanet = MagicMock(spec=Exoplanet)
        mock_exoplanet.constellation = None
        mock_exoplanet.discovery_method = None
        mock_exoplanet.discovery_date = MockAttribute("2023") # Year as string
        mock_exoplanet.discovered_by = None # Ensure this is None as per prompt's expected list
        mock_exoplanet.spectral_type = None # Ensure this is None as per prompt's expected list

        categories = generator.generate_categories(mock_exoplanet)
        expected = sorted([
            "[[Catégorie:Exoplanète]]", 
            "[[Catégorie:Exoplanète découverte en 2023]]", 
            "[[Catégorie:Exoplanète de type TestType]]"
            ])
        self.assertEqual(sorted(categories), expected)

    # This test was added in my previous iterations and is good to keep.
    @patch('src.utils.category_generator.parse_categories')
    @patch('src.utils.category_generator.PlanetTypeUtils')
    def test_instrument_partial_match_in_map(self, MockPlanetTypeUtils, mock_parse_categories):
        mock_parse_categories.return_value = {
            "Discovery Instruments/Telescopes": ["[[Catégorie:Exoplanète découverte grâce à Kepler]]"]
            # Other lists can be empty or absent
        }
        mock_planet_type_instance = MockPlanetTypeUtils.return_value
        mock_planet_type_instance.get_planet_type.return_value = "TestType"
        
        generator = CategoryGenerator() 
        
        mock_exoplanet = MagicMock(spec=Exoplanet)
        mock_exoplanet.constellation = None
        mock_exoplanet.discovery_method = None
        mock_exoplanet.discovery_date = None
        mock_exoplanet.discovered_by = MockAttribute("Kepler Space Telescope") # Partial match case
        mock_exoplanet.spectral_type = None

        categories = generator.generate_categories(mock_exoplanet)
        expected = sorted([
            "[[Catégorie:Exoplanète]]",
            "[[Catégorie:Exoplanète découverte grâce à Kepler]]", 
            "[[Catégorie:Exoplanète de type TestType]]"
        ])
        self.assertEqual(sorted(categories), expected)

if __name__ == '__main__':
    unittest.main()
