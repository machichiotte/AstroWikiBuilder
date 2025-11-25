# tests/unit/test_generators/test_article_generators/test_exoplanet/test_sections/test_physical_characteristics_section.py

from unittest.mock import MagicMock
import pytest

from src.generators.articles.exoplanet.sections.physical_characteristics_section import (
    PhysicalCharacteristicsSection,
)
from src.models.entities.exoplanet_entity import Exoplanet, ValueWithUncertainty


@pytest.fixture
def article_util():
    """Mock de ArticleFormatter."""
    mock = MagicMock()
    mock.format_number_as_french_string.side_effect = (
        lambda x, precision: f"{x:.{precision}f}".replace(".", ",")
    )
    return mock


@pytest.fixture
def section(article_util):
    """Instance de PhysicalCharacteristicsSection."""
    return PhysicalCharacteristicsSection(article_util)


class TestPhysicalCharacteristicsSection:
    """Tests pour PhysicalCharacteristicsSection."""

    def test_generate_with_all_characteristics(self, section):
        """Test avec masse, rayon, densité et température."""
        exoplanet = Exoplanet(
            pl_name="Test b",
            st_name="Test",
            pl_mass=ValueWithUncertainty(value=1.2),
            pl_radius=ValueWithUncertainty(value=1.1),
            pl_density=ValueWithUncertainty(value=1.4),
            pl_temperature=ValueWithUncertainty(value=1200),
        )

        result = section.generate(exoplanet)

        assert "== Caractéristiques physiques ==" in result
        assert "masse" in result
        assert "rayon" in result
        assert "densité" in result
        assert "température" in result
        assert "1,2" in result  # masse
        assert "1,1" in result  # rayon
        assert "1,40" in result  # densité
        assert "proche de Jupiter" in result  # comparaison

    def test_generate_with_density_only(self, section):
        """Test avec uniquement la densité."""
        exoplanet = Exoplanet(
            pl_name="Test b",
            st_name="Test",
            pl_density=ValueWithUncertainty(value=2.5),
        )

        result = section.generate(exoplanet)

        assert "== Caractéristiques physiques ==" in result
        assert "densité" in result
        assert "2,50" in result
        assert "plus dense que les géantes gazeuses" in result

    def test_generate_without_density(self, section):
        """Test sans densité (comportement existant maintenu)."""
        exoplanet = Exoplanet(
            pl_name="Test b",
            st_name="Test",
            pl_mass=ValueWithUncertainty(value=0.5),
            pl_radius=ValueWithUncertainty(value=0.8),
        )

        result = section.generate(exoplanet)

        assert "== Caractéristiques physiques ==" in result
        assert "masse" in result
        assert "rayon" in result
        assert "densité" not in result

    def test_generate_with_no_data(self, section):
        """Test sans aucune donnée."""
        exoplanet = Exoplanet(pl_name="Test b", st_name="Test")

        result = section.generate(exoplanet)

        assert result == ""

    def test_compare_to_solar_system_very_low_density(self, section):
        """Test comparaison avec densité très faible (< Saturne)."""
        result = section._compare_to_solar_system(0.5)
        assert result == "moins dense que Saturne"

    def test_compare_to_solar_system_saturn_like(self, section):
        """Test comparaison avec densité similaire à Saturne."""
        result = section._compare_to_solar_system(0.8)
        assert result == "comparable à Saturne"

    def test_compare_to_solar_system_jupiter_like(self, section):
        """Test comparaison avec densité similaire à Jupiter."""
        result = section._compare_to_solar_system(1.3)
        assert result == "proche de Jupiter"

    def test_compare_to_solar_system_neptune_like(self, section):
        """Test comparaison avec densité entre Jupiter et Neptune."""
        result = section._compare_to_solar_system(1.7)
        assert result == "entre Jupiter et Neptune"

    def test_compare_to_solar_system_high_density(self, section):
        """Test comparaison avec densité élevée (gazeuse dense)."""
        result = section._compare_to_solar_system(3.0)
        assert result == "plus dense que les géantes gazeuses"

    def test_compare_to_solar_system_intermediate(self, section):
        """Test comparaison avec densité intermédiaire."""
        result = section._compare_to_solar_system(4.5)
        assert result == "de densité intermédiaire"

    def test_compare_to_solar_system_terrestrial(self, section):
        """Test comparaison avec densité tellurique."""
        result = section._compare_to_solar_system(5.5)
        assert result == "comparable aux planètes telluriques comme la Terre"

    def test_format_density_description_valid(self, section):
        """Test formatage d'une densité valide."""
        result = section._format_density_description(1.33)
        assert result is not None
        assert "1,33" in result
        assert "g/cm³" in result
        assert "proche de Jupiter" in result

    def test_format_density_description_invalid(self, section):
        """Test formatage d'une densité invalide."""
        result = section._format_density_description("invalid")
        assert result is None

    def test_format_mass_description_low_mass(self, section):
        """Test formatage d'une masse faible."""
        result = section._format_mass_description(0.05)
        assert result is not None
        assert "faible" in result

    def test_format_mass_description_moderate_mass(self, section):
        """Test formatage d'une masse modérée."""
        result = section._format_mass_description(0.5)
        assert result is not None
        assert "modérée" in result

    def test_format_mass_description_high_mass(self, section):
        """Test formatage d'une masse imposante."""
        result = section._format_mass_description(2.0)
        assert result is not None
        assert "imposante" in result

    def test_format_radius_description_compact(self, section):
        """Test formatage d'un rayon compact."""
        result = section._format_radius_description(0.3)
        assert result is not None
        assert "compact" in result

    def test_format_radius_description_normal(self, section):
        """Test formatage d'un rayon normal."""
        result = section._format_radius_description(1.0)
        assert result is not None
        assert "compact" not in result
        assert "étendu" not in result

    def test_format_radius_description_extended(self, section):
        """Test formatage d'un rayon étendu."""
        result = section._format_radius_description(2.0)
        assert result is not None
        assert "étendu" in result

    def test_format_temperature_description_low(self, section):
        """Test formatage d'une température basse."""
        result = section._format_temperature_description(300)
        assert result is not None
        assert "300" in result
        assert "élevée" not in result
        assert "extrême" not in result

    def test_format_temperature_description_high(self, section):
        """Test formatage d'une température élevée."""
        result = section._format_temperature_description(800)
        assert result is not None
        assert "élevée" in result

    def test_format_temperature_description_extreme(self, section):
        """Test formatage d'une température extrême."""
        result = section._format_temperature_description(1500)
        assert result is not None
        assert "extrême" in result

    def test_get_value_or_none_if_nan_with_valid_value(self, section):
        """Test extraction d'une valeur valide."""
        data = ValueWithUncertainty(value=1.5)
        result = section._get_value_or_none_if_nan(data)
        assert result == 1.5

    def test_get_value_or_none_if_nan_with_none(self, section):
        """Test extraction d'une valeur None."""
        result = section._get_value_or_none_if_nan(None)
        assert result is None

    def test_get_value_or_none_if_nan_with_nan_string(self, section):
        """Test extraction d'une chaîne 'nan'."""
        data = ValueWithUncertainty(value="nan")
        result = section._get_value_or_none_if_nan(data)
        assert result is None
