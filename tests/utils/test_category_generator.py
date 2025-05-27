import unittest
from unittest.mock import patch, MagicMock

from utils.exoplanet_category_generator import ExoplanetCategoryGenerator
from src.models.exoplanet import Exoplanet


class MockAttribute:
    def __init__(self, value):
        self.value = value


class TestCategoryGenerator(unittest.TestCase):
    def _assert_no_double_wrapping(self, categories):
        for cat_entry in categories:
            self.assertFalse(
                cat_entry.startswith("[[Catégorie:[[Catégorie:"),
                f"Category '{cat_entry}' is double-wrapped.",
            )

    @patch("src.utils.category_generator.parse_categories")
    @patch("src.utils.category_generator.PlanetTypeUtils")
    def test_generate_categories_all_predefined(
        self, MockPlanetTypeUtils, mock_parse_categories
    ):
        mock_parse_categories.return_value = {
            "Constellations": ["[[Catégorie:Constellation du Cygne]]"],
            "Discovery Methods": [
                "[[Catégorie:Exoplanète découverte par la méthode des transits]]"
            ],
            "Discovery Years": ["[[Catégorie:Exoplanète découverte en 2000]]"],
            "Discovery Instruments/Telescopes": [
                "[[Catégorie:Exoplanète découverte grâce à Kepler]]"
            ],
        }
        mock_planet_type_instance = MockPlanetTypeUtils.return_value
        mock_planet_type_instance.get_planet_type.return_value = "Jupiter chaud"
        generator = ExoplanetCategoryGenerator()
        mock_exoplanet = MagicMock(spec=Exoplanet)
        mock_exoplanet.constellation = MockAttribute("Cygne")
        mock_exoplanet.discovery_method = MockAttribute("Transit")
        mock_date_obj = MagicMock()
        mock_date_obj.year = 2000
        mock_exoplanet.discovery_date = MockAttribute(mock_date_obj)
        mock_exoplanet.discovered_by = MockAttribute("Kepler")
        mock_exoplanet.spectral_type = MockAttribute("G2V")

        categories = generator.generate_exoplanet_categories(mock_exoplanet)
        expected_categories = sorted(
            [
                "[[Catégorie:Exoplanète]]",
                "[[Catégorie:Constellation du Cygne]]",
                "[[Catégorie:Exoplanète découverte par la méthode des transits]]",
                "[[Catégorie:Exoplanète découverte en 2000]]",
                "[[Catégorie:Exoplanète découverte grâce à Kepler]]",
                "[[Catégorie:Exoplanète orbitant une étoile de type G]]",
                "[[Catégorie:Exoplanète de type Jupiter chaud]]",
            ]
        )
        self.assertEqual(sorted(categories), expected_categories)
        self._assert_no_double_wrapping(categories)

    @patch("src.utils.category_generator.parse_categories")
    @patch("src.utils.category_generator.PlanetTypeUtils")
    def test_generate_categories_no_predefined_match(
        self, MockPlanetTypeUtils, mock_parse_categories
    ):
        mock_parse_categories.return_value = {
            "Constellations": ["[[Catégorie:Constellation de Lyra]]"],
            "Discovery Methods": [
                "[[Catégorie:Exoplanète découverte par microlentille gravitationnelle]]"
            ],
            "Discovery Years": ["[[Catégorie:Exoplanète découverte en 2010]]"],
            "Discovery Instruments/Telescopes": [
                "[[Catégorie:Exoplanète découverte grâce au télescope spatial Hubble]]"
            ],
        }
        mock_planet_type_instance = MockPlanetTypeUtils.return_value
        mock_planet_type_instance.get_planet_type.return_value = "Super-Terre"
        generator = ExoplanetCategoryGenerator()
        mock_exoplanet = MagicMock(spec=Exoplanet)
        mock_exoplanet.constellation = MockAttribute("Cygne")
        mock_exoplanet.discovery_method = MockAttribute("Transit")
        mock_date_obj = MagicMock()
        mock_date_obj.year = 2000
        mock_exoplanet.discovery_date = MockAttribute(mock_date_obj)
        mock_exoplanet.discovered_by = MockAttribute("Kepler")
        mock_exoplanet.spectral_type = MockAttribute("M1V")

        categories = generator.generate_exoplanet_categories(mock_exoplanet)
        expected_categories = sorted(
            [
                "[[Catégorie:Exoplanète]]",
                "[[Catégorie:Exoplanète orbitant une étoile de type M]]",
                "[[Catégorie:Exoplanète de type Super-Terre]]",
            ]
        )
        self.assertEqual(sorted(categories), expected_categories)
        self._assert_no_double_wrapping(categories)

    @patch("src.utils.category_generator.parse_categories")
    @patch("src.utils.category_generator.PlanetTypeUtils")
    def test_generate_categories_partial_match(
        self, MockPlanetTypeUtils, mock_parse_categories
    ):
        mock_parse_categories.return_value = {
            "Constellations": ["[[Catégorie:Constellation du Cygne]]"],
            "Discovery Methods": [
                "[[Catégorie:Exoplanète découverte par microlentille gravitationnelle]]"
            ],
            "Discovery Years": ["[[Catégorie:Exoplanète découverte en 2000]]"],
            "Discovery Instruments/Telescopes": [
                "[[Catégorie:Exoplanète découverte grâce au télescope spatial Hubble]]"
            ],
        }
        mock_planet_type_instance = MockPlanetTypeUtils.return_value
        mock_planet_type_instance.get_planet_type.return_value = "Naine gazeuse"
        generator = ExoplanetCategoryGenerator()
        mock_exoplanet = MagicMock(spec=Exoplanet)
        mock_exoplanet.constellation = MockAttribute("Cygne")
        mock_exoplanet.discovery_method = MockAttribute("Transit")
        mock_date_obj = MagicMock()
        mock_date_obj.year = 2000
        mock_exoplanet.discovery_date = MockAttribute(mock_date_obj)
        mock_exoplanet.discovered_by = MockAttribute("TESS")
        mock_exoplanet.spectral_type = MockAttribute("K5V")

        categories = generator.generate_exoplanet_categories(mock_exoplanet)
        expected_categories = sorted(
            [
                "[[Catégorie:Exoplanète]]",
                "[[Catégorie:Constellation du Cygne]]",
                "[[Catégorie:Exoplanète découverte en 2000]]",
                "[[Catégorie:Exoplanète orbitant une étoile de type K]]",
                "[[Catégorie:Exoplanète de type Naine gazeuse]]",
            ]
        )
        self.assertEqual(sorted(categories), expected_categories)
        self._assert_no_double_wrapping(categories)

    @patch("src.utils.category_generator.parse_categories")
    @patch("src.utils.category_generator.PlanetTypeUtils")
    def test_generate_categories_optional_fields_none(
        self, MockPlanetTypeUtils, mock_parse_categories
    ):
        mock_parse_categories.return_value = {
            "Constellations": [],
            "Discovery Methods": [],
            "Discovery Years": [],
            "Discovery Instruments/Telescopes": [],
        }
        mock_planet_type_instance = MockPlanetTypeUtils.return_value
        mock_planet_type_instance.get_planet_type.return_value = "Rocheuse"
        generator = ExoplanetCategoryGenerator()
        mock_exoplanet = MagicMock(spec=Exoplanet)
        mock_exoplanet.constellation = None
        mock_exoplanet.discovery_method = MockAttribute("Transit")
        mock_exoplanet.discovery_date = None
        mock_exoplanet.discovered_by = None
        mock_exoplanet.spectral_type = None

        categories = generator.generate_exoplanet_categories(mock_exoplanet)
        expected_categories = sorted(
            ["[[Catégorie:Exoplanète]]", "[[Catégorie:Exoplanète de type Rocheuse]]"]
        )
        self.assertEqual(sorted(categories), expected_categories)
        self._assert_no_double_wrapping(categories)

    @patch("src.utils.category_generator.parse_categories")
    @patch("src.utils.category_generator.PlanetTypeUtils")
    def test_generate_categories_planet_type_unknown_or_exception(
        self, MockPlanetTypeUtils, mock_parse_categories
    ):
        mock_parse_categories.return_value = {}
        mock_planet_type_instance = MockPlanetTypeUtils.return_value
        generator = ExoplanetCategoryGenerator()
        mock_exoplanet = MagicMock(spec=Exoplanet)
        mock_exoplanet.constellation = None
        mock_exoplanet.discovery_method = None
        mock_exoplanet.discovery_date = None
        mock_exoplanet.discovered_by = None
        mock_exoplanet.spectral_type = None

        mock_planet_type_instance.get_planet_type.return_value = "Unknown"
        categories_unknown = generator.generate_exoplanet_categories(mock_exoplanet)
        self.assertEqual(
            sorted(categories_unknown), sorted(["[[Catégorie:Exoplanète]]"])
        )
        self._assert_no_double_wrapping(categories_unknown)

        mock_planet_type_instance.get_planet_type.side_effect = Exception("Test error")
        categories_exception = generator.generate_exoplanet_categories(mock_exoplanet)
        self.assertEqual(
            sorted(categories_exception), sorted(["[[Catégorie:Exoplanète]]"])
        )
        self._assert_no_double_wrapping(categories_exception)

    @patch("src.utils.category_generator.parse_categories")
    @patch("src.utils.category_generator.PlanetTypeUtils")
    def test_discovery_year_as_string(self, MockPlanetTypeUtils, mock_parse_categories):
        mock_parse_categories.return_value = {
            "Discovery Years": ["[[Catégorie:Exoplanète découverte en 2023]]"]
        }
        mock_planet_type_instance = MockPlanetTypeUtils.return_value
        mock_planet_type_instance.get_planet_type.return_value = "TestType"
        generator = ExoplanetCategoryGenerator()
        mock_exoplanet = MagicMock(spec=Exoplanet)
        mock_exoplanet.constellation = None
        mock_exoplanet.discovery_method = None
        mock_exoplanet.discovery_date = MockAttribute("2023")
        mock_exoplanet.discovered_by = None
        mock_exoplanet.spectral_type = None

        categories = generator.generate_exoplanet_categories(mock_exoplanet)
        expected = sorted(
            [
                "[[Catégorie:Exoplanète]]",
                "[[Catégorie:Exoplanète découverte en 2023]]",
                "[[Catégorie:Exoplanète de type TestType]]",
            ]
        )
        self.assertEqual(sorted(categories), expected)
        self._assert_no_double_wrapping(categories)

    @patch("src.utils.category_generator.parse_categories")
    @patch("src.utils.category_generator.PlanetTypeUtils")
    def test_instrument_partial_match_in_map(
        self, MockPlanetTypeUtils, mock_parse_categories
    ):
        mock_parse_categories.return_value = {
            "Discovery Instruments/Telescopes": [
                "[[Catégorie:Exoplanète découverte grâce à Kepler]]"
            ]
        }
        mock_planet_type_instance = MockPlanetTypeUtils.return_value
        mock_planet_type_instance.get_planet_type.return_value = "TestType"
        generator = ExoplanetCategoryGenerator()
        mock_exoplanet = MagicMock(spec=Exoplanet)
        mock_exoplanet.constellation = None
        mock_exoplanet.discovery_method = None
        mock_exoplanet.discovery_date = None
        mock_exoplanet.discovered_by = MockAttribute("Kepler Space Telescope")
        mock_exoplanet.spectral_type = None

        categories = generator.generate_exoplanet_categories(mock_exoplanet)
        expected = sorted(
            [
                "[[Catégorie:Exoplanète]]",
                "[[Catégorie:Exoplanète découverte grâce à Kepler]]",
                "[[Catégorie:Exoplanète de type TestType]]",
            ]
        )
        self.assertEqual(sorted(categories), expected)
        self._assert_no_double_wrapping(categories)

    @patch("src.utils.category_generator.parse_categories")
    @patch("src.utils.category_generator.PlanetTypeUtils")
    def test_planet_type_formatting_logic(
        self, MockPlanetTypeUtils, mock_parse_categories
    ):
        mock_parse_categories.return_value = {}
        mock_planet_type_instance = MockPlanetTypeUtils.return_value
        generator = ExoplanetCategoryGenerator()

        mock_exoplanet_plain = MagicMock(spec=Exoplanet)
        mock_exoplanet_plain.constellation = None
        mock_exoplanet_plain.discovery_method = None
        mock_exoplanet_plain.discovery_date = None
        mock_exoplanet_plain.discovered_by = None
        mock_exoplanet_plain.spectral_type = None

        # Scenario 1: PlanetTypeUtils returns a plain string
        mock_planet_type_instance.get_planet_type.return_value = "Super-Terre"
        categories_plain = generator.generate_exoplanet_categories(mock_exoplanet_plain)
        self.assertIn("[[Catégorie:Exoplanète de type Super-Terre]]", categories_plain)
        for cat in categories_plain:
            if "Super-Terre" in cat:
                self.assertEqual(cat, "[[Catégorie:Exoplanète de type Super-Terre]]")
        self._assert_no_double_wrapping(categories_plain)

        # Scenario 2: PlanetTypeUtils returns an already wrapped string
        mock_planet_type_instance.get_planet_type.return_value = (
            "[[Catégorie:Custom Planet Type]]"
        )
        mock_exoplanet_wrapped = MagicMock(spec=Exoplanet)
        mock_exoplanet_wrapped.constellation = None
        mock_exoplanet_wrapped.discovery_method = None
        mock_exoplanet_wrapped.discovery_date = None
        mock_exoplanet_wrapped.discovered_by = None
        mock_exoplanet_wrapped.spectral_type = None

        categories_wrapped = generator.generate_exoplanet_categories(
            mock_exoplanet_wrapped
        )
        self.assertIn("[[Catégorie:Custom Planet Type]]", categories_wrapped)
        for cat in categories_wrapped:
            if "Custom Planet Type" in cat:
                self.assertEqual(cat, "[[Catégorie:Custom Planet Type]]")
        self._assert_no_double_wrapping(categories_wrapped)

        self.assertIn("[[Catégorie:Exoplanète]]", categories_plain)
        self.assertIn("[[Catégorie:Exoplanète]]", categories_wrapped)


if __name__ == "__main__":
    unittest.main()
