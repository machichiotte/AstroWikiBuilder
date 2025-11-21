"""
Tests unitaires pour ExoplanetContentGenerator.
"""

import pytest

from src.generators.articles.exoplanet.parts.exoplanet_content_generator import (
    ExoplanetContentGenerator,
)
from src.models.entities.exoplanet_entity import Exoplanet, ValueWithUncertainty


class TestExoplanetContentGenerator:
    """Tests pour le générateur de contenu d'exoplanètes."""

    @pytest.fixture
    def generator(self):
        """Fixture pour créer une instance du générateur."""
        return ExoplanetContentGenerator()

    @pytest.fixture
    def exoplanet_with_orbit(self):
        """Exoplanète avec données orbitales complètes."""
        return Exoplanet(
            pl_name="Test Planet b",
            pl_semi_major_axis=ValueWithUncertainty(value=0.047),
            pl_eccentricity=ValueWithUncertainty(value=0.014),
            pl_orbital_period=ValueWithUncertainty(value=3.52),
            pl_inclination=ValueWithUncertainty(value=86.7),
        )

    @pytest.fixture
    def exoplanet_with_physical_chars(self):
        """Exoplanète avec caractéristiques physiques."""
        return Exoplanet(
            pl_name="Test Planet b",
            pl_mass=ValueWithUncertainty(value=0.69),
            pl_radius=ValueWithUncertainty(value=1.38),
            pl_temperature=ValueWithUncertainty(value=1450),
        )

    @pytest.fixture
    def exoplanet_with_discovery(self):
        """Exoplanète avec informations de découverte."""

        class MethodEnum:
            def __init__(self, value):
                self.value = value

        return Exoplanet(
            pl_name="Test Planet b",
            disc_year=1999,
            disc_method=MethodEnum("Transit"),
        )

    # Tests pour build_orbit_section
    def test_build_orbit_section_complete(self, generator, exoplanet_with_orbit):
        """Test de la section orbite avec toutes les données."""
        result = generator.build_orbit_section(exoplanet_with_orbit)

        assert result != ""
        assert "== Orbite ==" in result
        assert "UA" in result
        assert "excentricité" in result
        assert "période orbitale" in result
        assert "inclinaison" in result

    def test_build_orbit_section_empty(self, generator):
        """Test avec une exoplanète sans données orbitales."""
        exoplanet = Exoplanet(pl_name="Test b")
        result = generator.build_orbit_section(exoplanet)

        assert result == ""

    def test_build_orbit_section_partial(self, generator):
        """Test avec seulement certaines données orbitales."""
        exoplanet = Exoplanet(
            pl_name="Test b",
            pl_semi_major_axis=ValueWithUncertainty(value=1.0),
        )
        result = generator.build_orbit_section(exoplanet)

        assert result != ""
        assert "== Orbite ==" in result
        assert "UA" in result

    # Tests pour build_physical_characteristics_section
    def test_build_physical_characteristics_complete(
        self, generator, exoplanet_with_physical_chars
    ):
        """Test de la section caractéristiques physiques complète."""
        result = generator.build_physical_characteristics_section(exoplanet_with_physical_chars)

        assert result != ""
        assert "== Caractéristiques physiques ==" in result
        assert "masse" in result
        assert "rayon" in result
        assert "température" in result

    def test_build_physical_characteristics_empty(self, generator):
        """Test avec une exoplanète sans caractéristiques physiques."""
        exoplanet = Exoplanet(pl_name="Test b")
        result = generator.build_physical_characteristics_section(exoplanet)

        assert result == ""

    def test_build_physical_characteristics_mass_labels(self, generator):
        """Test des labels de masse (faible, modérée, imposante)."""
        # Masse faible
        exo_low = Exoplanet(pl_name="Low", pl_mass=ValueWithUncertainty(value=0.05))
        result_low = generator.build_physical_characteristics_section(exo_low)
        assert "faible" in result_low

        # Masse modérée
        exo_mod = Exoplanet(pl_name="Mod", pl_mass=ValueWithUncertainty(value=0.5))
        result_mod = generator.build_physical_characteristics_section(exo_mod)
        assert "modérée" in result_mod

        # Masse imposante
        exo_high = Exoplanet(pl_name="High", pl_mass=ValueWithUncertainty(value=2.0))
        result_high = generator.build_physical_characteristics_section(exo_high)
        assert "imposante" in result_high

    def test_build_physical_characteristics_radius_labels(self, generator):
        """Test des labels de rayon (compact, étendu)."""
        # Rayon compact
        exo_compact = Exoplanet(pl_name="Compact", pl_radius=ValueWithUncertainty(value=0.3))
        result_compact = generator.build_physical_characteristics_section(exo_compact)
        assert "compact" in result_compact

        # Rayon étendu
        exo_extended = Exoplanet(pl_name="Extended", pl_radius=ValueWithUncertainty(value=2.0))
        result_extended = generator.build_physical_characteristics_section(exo_extended)
        assert "étendu" in result_extended

    def test_build_physical_characteristics_temp_labels(self, generator):
        """Test des labels de température."""
        # Température élevée
        exo_hot = Exoplanet(pl_name="Hot", pl_temperature=ValueWithUncertainty(value=800))
        result_hot = generator.build_physical_characteristics_section(exo_hot)
        assert "élevée" in result_hot

        # Température extrême
        exo_extreme = Exoplanet(pl_name="Extreme", pl_temperature=ValueWithUncertainty(value=1500))
        result_extreme = generator.build_physical_characteristics_section(exo_extreme)
        assert "extrême" in result_extreme

    # Tests pour build_discovery_section
    def test_build_discovery_section_complete(self, generator, exoplanet_with_discovery):
        """Test de la section découverte complète."""
        result = generator.build_discovery_section(exoplanet_with_discovery)

        assert result != ""
        assert "== Découverte ==" in result
        assert "1999" in result
        assert "transits" in result

    def test_build_discovery_section_empty(self, generator):
        """Test avec une exoplanète sans année de découverte."""
        exoplanet = Exoplanet(pl_name="Test b")
        result = generator.build_discovery_section(exoplanet)

        assert result == ""

    def test_build_discovery_section_without_method(self, generator):
        """Test avec seulement l'année de découverte."""
        exoplanet = Exoplanet(pl_name="Test b", disc_year=2020)
        result = generator.build_discovery_section(exoplanet)

        assert result != ""
        assert "2020" in result
        assert "découverte" in result

    def test_build_discovery_section_method_translations(self, generator):
        """Test des traductions de méthodes de découverte."""

        # Créer un objet simple avec un attribut value pour simuler un enum
        class MethodEnum:
            def __init__(self, value):
                self.value = value

        methods_to_test = [
            (MethodEnum("Radial Velocity"), "vitesses radiales"),
            (MethodEnum("Imaging"), "imagerie directe"),
            (MethodEnum("Microlensing"), "microlentille"),
        ]

        for method, expected_text in methods_to_test:
            exoplanet = Exoplanet(
                pl_name="Test b",
                disc_year=2000,
                disc_method=method,
            )
            result = generator.build_discovery_section(exoplanet)
            assert expected_text in result

    # Tests pour compose_exoplanet_content
    def test_compose_exoplanet_content_all_sections(self, generator):
        """Test de la composition complète avec toutes les sections."""
        exoplanet = Exoplanet(
            pl_name="Complete Planet b",
            pl_mass=ValueWithUncertainty(value=1.0),
            pl_semi_major_axis=ValueWithUncertainty(value=0.5),
            disc_year=2010,
        )
        result = generator.compose_exoplanet_content(exoplanet)

        assert result != ""
        assert "== Caractéristiques physiques ==" in result
        assert "== Orbite ==" in result
        assert "== Découverte ==" in result

    def test_compose_exoplanet_content_empty(self, generator):
        """Test avec une exoplanète sans données."""
        exoplanet = Exoplanet(pl_name="Empty b")
        result = generator.compose_exoplanet_content(exoplanet)

        assert result == ""

    def test_compose_exoplanet_content_partial(self, generator):
        """Test avec seulement certaines sections."""
        exoplanet = Exoplanet(
            pl_name="Partial b",
            disc_year=2015,
        )
        result = generator.compose_exoplanet_content(exoplanet)

        assert result != ""
        assert "== Découverte ==" in result
        assert "== Caractéristiques physiques ==" not in result
        assert "== Orbite ==" not in result
