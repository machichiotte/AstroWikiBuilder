"""Tests for Star CategorySection."""

from unittest.mock import Mock, patch

import pytest

from src.generators.articles.star.sections.category_section import CategorySection
from src.models.entities.star_entity import Star


class TestStarCategorySection:
    """Test suite for Star CategorySection."""

    @pytest.fixture
    def section(self):
        """Create a CategorySection instance with mocked dependencies."""
        with patch(
            "src.generators.base.category_rules_manager.CategoryRulesManager"
        ) as MockRulesManager:
            mock_manager = MockRulesManager.return_value
            mock_manager.rules = {
                "star": {
                    "mapped": {
                        "prefix_catalog": {
                            "KEPLER-": "Objet du catalogue Kepler",
                            "KOI-": "Objet du catalogue KOI",
                        },
                        "st_spectral_type": {
                            "G": "Étoile de type spectral G",
                        },
                        "luminosity_class": {
                            "V": "Étoile de la séquence principale",
                        },
                    }
                }
            }

            section = CategorySection()
            section._category_rules_manager = mock_manager
            section.star_type_util = Mock()
            return section

    def test_map_catalog_prefix_to_category_kepler_number(self, section):
        """Test Kepler object formatting with number."""
        star = Star(st_name="Kepler-10")
        category = section.map_catalog_prefix_to_category(star)
        assert "Objet du catalogue Kepler|0010" in category

    def test_map_catalog_prefix_to_category_kepler_non_number(self, section):
        """Test Kepler object formatting with non-number."""
        star = Star(st_name="Kepler-Abc")
        category = section.map_catalog_prefix_to_category(star)
        assert "Objet du catalogue Kepler|ABC" in category

    def test_map_catalog_prefix_to_category_alt_names(self, section):
        """Test with alternative names."""
        star = Star(st_name="Kepler-10", st_altname=["KOI-72"])
        category = section.map_catalog_prefix_to_category(star)
        assert "Objet du catalogue Kepler|0010" in category
        assert "Objet du catalogue KOI|72" in category

    def test_map_catalog_prefix_to_category_empty_name(self, section):
        """Test with empty name."""
        star = Star(st_name="")
        category = section.map_catalog_prefix_to_category(star)
        assert category is None

    def test_map_catalog_prefix_to_category_empty_alt_name(self, section):
        """Test with empty alternative name."""
        star = Star(st_name="Kepler-10", st_altname=[""])
        category = section.map_catalog_prefix_to_category(star)
        assert "Objet du catalogue Kepler|0010" in category

    def test_map_spectral_type_to_category_unknown(self, section):
        """Test unknown spectral type."""
        star = Star(st_name="Test Star")
        section.star_type_util.extract_spectral_class_from_star.return_value = "X"
        category = section.map_spectral_type_to_category(star)
        assert category == "Étoile de type spectral X"

    def test_map_luminosity_class_to_category_unknown(self, section):
        """Test unknown luminosity class."""
        star = Star(st_name="Test Star")
        section.star_type_util.extract_luminosity_class_from_star.return_value = "VII"
        category = section.map_luminosity_class_to_category(star)
        assert category == "Classe de luminosité VII"

    def test_map_star_type_to_category_variable(self, section):
        """Test variable star type."""
        star = Star(st_name="Test Star")
        section.star_type_util.determine_star_types_from_properties.return_value = [
            "Étoile variable de type Mira"
        ]
        category = section.map_star_type_to_category(star)
        assert "Étoile variable de type Mira" in category

    def test_map_star_type_to_category_spectral(self, section):
        """Test standard spectral type star."""
        star = Star(st_name="Test Star")
        section.star_type_util.determine_star_types_from_properties.return_value = [
            "Étoile de type spectral G"
        ]
        category = section.map_star_type_to_category(star)
        assert "Étoile de type spectral G" in category

    def test_map_star_type_to_category_special(self, section):
        """Test special star type (e.g. Red Dwarf)."""
        star = Star(st_name="Test Star")
        section.star_type_util.determine_star_types_from_properties.return_value = ["Naine rouge"]
        category = section.map_star_type_to_category(star)
        assert "Naine rouge" in category

    def test_map_star_type_to_category_none(self, section):
        """Test no star type."""
        star = Star(st_name="Test Star")
        section.star_type_util.determine_star_types_from_properties.return_value = []
        category = section.map_star_type_to_category(star)
        assert category is None
