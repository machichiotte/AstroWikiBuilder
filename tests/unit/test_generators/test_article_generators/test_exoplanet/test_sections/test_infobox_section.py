# tests/unit/test_generators/test_article_generators/test_exoplanet/test_sections/test_infobox_section.py

"""Tests for InfoboxSection."""

from datetime import datetime

import pytest

from src.generators.articles.exoplanet.sections.infobox_section import InfoboxSection
from src.models.entities.exoplanet_entity import Exoplanet, ValueWithUncertainty
from src.models.references.reference import Reference, SourceType
from src.services.processors.reference_manager import ReferenceManager


@pytest.fixture
def reference_manager():
    """Create a ReferenceManager instance."""
    return ReferenceManager()


@pytest.fixture
def section(reference_manager):
    """Create an InfoboxSection instance."""
    return InfoboxSection(reference_manager)


class TestInfoboxSection:
    """Test suite for InfoboxSection."""

    def test_generate_basic_infobox(self, section):
        """Test basic infobox generation."""
        exoplanet = Exoplanet(
            pl_name="Test b",
            st_name="Test",
        )
        result = section.generate(exoplanet)

        assert "{{Infobox Exoplanète" in result
        assert "}}" in result

    def test_generate_with_alternative_identifiers(self, section):
        """Test infobox with alternative catalog identifiers."""
        exoplanet = Exoplanet(
            pl_name="Test b",
            st_name="Test",
            hd_name="HD 12345",
            hip_name="HIP 67890",
            tic_id="TIC 111222333",
            gaia_id="Gaia DR3 4444555666",
        )
        result = section.generate(exoplanet)

        assert "HD 12345" in result
        assert "HIP 67890" in result
        assert "TIC 111222333" in result
        assert "Gaia DR3 4444555666" in result

    def test_generate_with_partial_identifiers(self, section):
        """Test infobox with only some identifiers."""
        exoplanet = Exoplanet(
            pl_name="Test b",
            st_name="Test",
            hd_name="HD 12345",
            gaia_id="Gaia DR3 4444555666",
        )
        result = section.generate(exoplanet)

        assert "HD 12345" in result
        assert "Gaia DR3 4444555666" in result
        assert "HIP" not in result or "HIP =" not in result

    def test_generate_with_controversy_flag(self, section):
        """Test infobox with controversy flag."""
        exoplanet = Exoplanet(
            pl_name="Test b",
            st_name="Test",
            pl_controv_flag="1",
        )
        result = section.generate(exoplanet)

        assert "controverse" in result or "1" in result

    def test_generate_with_physical_characteristics(self, section):
        """Test infobox with physical characteristics."""
        exoplanet = Exoplanet(
            pl_name="Test b",
            st_name="Test",
            pl_mass=ValueWithUncertainty(value=1.5),
            pl_radius=ValueWithUncertainty(value=1.2),
            pl_density=ValueWithUncertainty(value=1.3),
        )
        result = section.generate(exoplanet)

        assert "masse" in result
        assert "rayon" in result
        assert "masse volumique" in result

    def test_generate_with_discovery_info(self, section):
        """Test infobox with discovery information."""
        exoplanet = Exoplanet(
            pl_name="Test b",
            st_name="Test",
            disc_year=2020,
            disc_method="Transit",
            disc_facility="Kepler",
        )
        result = section.generate(exoplanet)

        # Check that the infobox contains the discovery information
        assert "Transit" in result
        assert "Kepler" in result or "Télescope spatial Kepler" in result

    def test_generate_with_reference(self, section):
        """Test infobox with reference."""
        ref = Reference(
            source=SourceType.NEA,
            update_date=datetime(2024, 1, 1),
            consultation_date=datetime(2024, 1, 15),
            star_id="Test",
            planet_id="Test b",
        )
        exoplanet = Exoplanet(
            pl_name="Test b",
            st_name="Test",
            reference=ref,
        )
        result = section.generate(exoplanet)

        assert "{{Infobox Exoplanète" in result

    def test_generate_empty_exoplanet(self, section):
        """Test infobox with minimal exoplanet data."""
        exoplanet = Exoplanet(pl_name="Test b")
        result = section.generate(exoplanet)

        assert "{{Infobox Exoplanète" in result
        assert "}}" in result
