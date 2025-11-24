from unittest.mock import Mock, patch

import pytest

from src.generators.articles.exoplanet.sections.category_section import CategorySection
from src.models.entities.exoplanet_entity import Exoplanet


class TestCategorySection:
    @pytest.fixture
    def section(self):
        # Mock the rules file loading
        with patch(
            "src.generators.base.category_rules_manager.CategoryRulesManager.__init__",
            return_value=None,
        ):
            section = CategorySection()
            section._category_rules_manager = Mock()
            section._category_rules_manager.generate_categories_for.return_value = [
                "[[Catégorie:Exoplanète]]",
                "[[Catégorie:Géante gazeuse]]",
            ]
            section._category_rules_manager.rules = {
                "exoplanet": {
                    "mapped": {
                        "planet_type": {"Géante gazeuse": "[[Catégorie:Géante gazeuse]]"},
                        "disc_facility": {
                            "Kepler": "[[Catégorie:Exoplanète découverte grâce à Kepler]]"
                        },
                    }
                }
            }
            section.planet_type_util = Mock()
            section.planet_type_util.determine_exoplanet_classification.return_value = (
                "Géante gazeuse"
            )
            return section

    def test_generate(self, section):
        exoplanet = Exoplanet(pl_name="Test Planet")
        content = section.generate(exoplanet)
        assert "[[Catégorie:Exoplanète]]" in content
        assert "[[Catégorie:Géante gazeuse]]" in content

    def test_generate_empty(self, section):
        exoplanet = Exoplanet(pl_name="Test Planet")
        section._category_rules_manager.generate_categories_for.return_value = []
        content = section.generate(exoplanet)
        assert content == ""

    def test_map_planet_type_to_category(self, section):
        exoplanet = Exoplanet(pl_name="Test Planet")
        category = section.map_planet_type_to_category(exoplanet)
        assert category == "[[Catégorie:Géante gazeuse]]"

    def test_map_planet_type_to_category_not_in_mapping(self, section):
        exoplanet = Exoplanet(pl_name="Test Planet")
        section.planet_type_util.determine_exoplanet_classification.return_value = "Unknown Type"
        category = section.map_planet_type_to_category(exoplanet)
        assert category is None

    def test_map_planet_type_to_category_exception(self, section):
        exoplanet = Exoplanet(pl_name="Test Planet")
        section.planet_type_util.determine_exoplanet_classification.side_effect = Exception(
            "Test error"
        )
        category = section.map_planet_type_to_category(exoplanet)
        assert category is None

    def test_map_discovery_program_to_category_exact_match(self, section):
        exoplanet = Exoplanet(pl_name="Test Planet")
        exoplanet.disc_program = Mock()
        exoplanet.disc_program.value = "Kepler"
        category = section.map_discovery_program_to_category(exoplanet)
        assert category == "[[Catégorie:Exoplanète découverte grâce à Kepler]]"

    def test_map_discovery_program_to_category_partial_match(self, section):
        exoplanet = Exoplanet(pl_name="Test Planet")
        exoplanet.disc_program = Mock()
        exoplanet.disc_program.value = "Kepler Mission"
        category = section.map_discovery_program_to_category(exoplanet)
        assert category == "[[Catégorie:Exoplanète découverte grâce à Kepler]]"

    def test_map_discovery_program_to_category_no_program(self, section):
        exoplanet = Exoplanet(pl_name="Test Planet")
        exoplanet.disc_program = None
        category = section.map_discovery_program_to_category(exoplanet)
        assert category is None

    def test_map_constellation_to_category(self, section):
        exoplanet = Exoplanet(pl_name="Test Planet", sy_constellation="Orion")
        category = section.map_constellation_to_category(exoplanet)
        assert category == "Exoplanète de la constellation de Orion"

    def test_map_constellation_to_category_no_constellation(self, section):
        exoplanet = Exoplanet(pl_name="Test Planet")
        exoplanet.sy_constellation = None
        category = section.map_constellation_to_category(exoplanet)
        assert category is None
