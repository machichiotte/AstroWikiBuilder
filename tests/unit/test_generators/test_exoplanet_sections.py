"""
Tests unitaires pour les sections de contenu d'exoplanètes.
"""

import pytest

from src.generators.articles.exoplanet.sections import (
    DiscoverySection,
    HabitabilitySection,
    HostStarSection,
    OrbitSection,
    PhysicalCharacteristicsSection,
)
from src.models.entities.exoplanet_entity import Exoplanet, ValueWithUncertainty
from src.utils.formatters.article_formatter import ArticleFormatter


class TestExoplanetSections:
    """Tests pour les sections individuelles d'exoplanètes."""

    @pytest.fixture
    def article_formatter(self):
        return ArticleFormatter()

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
                self.name = value  # Mock name attribute if needed

        return Exoplanet(
            pl_name="Test Planet b",
            disc_year=1999,
            disc_method=MethodEnum("Transit"),
        )

    # Tests pour OrbitSection
    def test_orbit_section_complete(self, article_formatter, exoplanet_with_orbit):
        """Test de la section orbite avec toutes les données."""
        section = OrbitSection(article_formatter)
        result = section.generate(exoplanet_with_orbit)

        assert result != ""
        assert "== Orbite ==" in result
        assert "UA" in result
        assert "excentricité" in result
        assert "période orbitale" in result
        assert "inclinaison" in result

    def test_orbit_section_empty(self, article_formatter):
        """Test avec une exoplanète sans données orbitales."""
        exoplanet = Exoplanet(pl_name="Test b")
        section = OrbitSection(article_formatter)
        result = section.generate(exoplanet)

        assert result == ""

    def test_orbit_section_partial(self, article_formatter):
        """Test avec seulement certaines données orbitales."""
        exoplanet = Exoplanet(
            pl_name="Test b",
            pl_semi_major_axis=ValueWithUncertainty(value=1.0),
        )
        section = OrbitSection(article_formatter)
        result = section.generate(exoplanet)

        assert result != ""
        assert "== Orbite ==" in result
        assert "UA" in result

    # Tests pour PhysicalCharacteristicsSection
    def test_physical_characteristics_complete(
        self, article_formatter, exoplanet_with_physical_chars
    ):
        """Test de la section caractéristiques physiques complète."""
        section = PhysicalCharacteristicsSection(article_formatter)
        result = section.generate(exoplanet_with_physical_chars)

        assert result != ""
        assert "== Caractéristiques physiques ==" in result
        assert "masse" in result
        assert "rayon" in result
        assert "température" in result

    def test_physical_characteristics_empty(self, article_formatter):
        """Test avec une exoplanète sans caractéristiques physiques."""
        exoplanet = Exoplanet(pl_name="Test b")
        section = PhysicalCharacteristicsSection(article_formatter)
        result = section.generate(exoplanet)

        assert result == ""

    def test_physical_characteristics_mass_labels(self, article_formatter):
        """Test des labels de masse (faible, modérée, imposante)."""
        section = PhysicalCharacteristicsSection(article_formatter)

        # Masse faible
        exo_low = Exoplanet(pl_name="Low", pl_mass=ValueWithUncertainty(value=0.05))
        result_low = section.generate(exo_low)
        assert "faible" in result_low

        # Masse modérée
        exo_mod = Exoplanet(pl_name="Mod", pl_mass=ValueWithUncertainty(value=0.5))
        result_mod = section.generate(exo_mod)
        assert "modérée" in result_mod

        # Masse imposante
        exo_high = Exoplanet(pl_name="High", pl_mass=ValueWithUncertainty(value=2.0))
        result_high = section.generate(exo_high)
        assert "imposante" in result_high

    def test_physical_characteristics_radius_labels(self, article_formatter):
        """Test des labels de rayon (compact, étendu)."""
        section = PhysicalCharacteristicsSection(article_formatter)

        # Rayon compact
        exo_compact = Exoplanet(
            pl_name="Compact", pl_radius=ValueWithUncertainty(value=0.3)
        )
        result_compact = section.generate(exo_compact)
        assert "compact" in result_compact

        # Rayon étendu
        exo_extended = Exoplanet(
            pl_name="Extended", pl_radius=ValueWithUncertainty(value=2.0)
        )
        result_extended = section.generate(exo_extended)
        assert "étendu" in result_extended

    def test_physical_characteristics_temp_labels(self, article_formatter):
        """Test des labels de température."""
        section = PhysicalCharacteristicsSection(article_formatter)

        # Température élevée
        exo_hot = Exoplanet(
            pl_name="Hot", pl_temperature=ValueWithUncertainty(value=800)
        )
        result_hot = section.generate(exo_hot)
        assert "élevée" in result_hot

        # Température extrême
        exo_extreme = Exoplanet(
            pl_name="Extreme", pl_temperature=ValueWithUncertainty(value=1500)
        )
        result_extreme = section.generate(exo_extreme)
        assert "extrême" in result_extreme

    # Tests pour DiscoverySection
    def test_discovery_section_complete(
        self, article_formatter, exoplanet_with_discovery
    ):
        """Test de la section découverte complète."""
        section = DiscoverySection(article_formatter)
        result = section.generate(exoplanet_with_discovery)

        assert result != ""
        assert "== Découverte ==" in result
        assert "1999" in result
        assert "transits" in result

    def test_discovery_section_empty(self, article_formatter):
        """Test avec une exoplanète sans année de découverte."""
        exoplanet = Exoplanet(pl_name="Test b")
        section = DiscoverySection(article_formatter)
        result = section.generate(exoplanet)

        assert result == ""

    def test_discovery_section_without_method(self, article_formatter):
        """Test avec seulement l'année de découverte."""
        exoplanet = Exoplanet(pl_name="Test b", disc_year=2020)
        section = DiscoverySection(article_formatter)
        result = section.generate(exoplanet)

        assert result != ""
        assert "2020" in result
        assert "découverte" in result

    def test_discovery_section_method_translations(self, article_formatter):
        """Test des traductions de méthodes de découverte."""
        section = DiscoverySection(article_formatter)

        # Créer un objet simple avec un attribut value pour simuler un enum
        class MethodEnum:
            def __init__(self, value):
                self.value = value
                self.name = value

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
            result = section.generate(exoplanet)
            assert expected_text in result

    # Tests pour HabitabilitySection
    def test_habitability_section_unknown(self, article_formatter):
        """Test habitabilité inconnue."""
        exoplanet = Exoplanet(pl_name="Test b")
        section = HabitabilitySection(article_formatter)
        result = section.generate(exoplanet)
        assert "ne sont pas déterminées" in result

    def test_habitability_section_too_hot(self, article_formatter):
        """Test habitabilité trop chaud."""
        exoplanet = Exoplanet(
            pl_name="Hot b", pl_temperature=ValueWithUncertainty(value=500)
        )
        section = HabitabilitySection(article_formatter)
        result = section.generate(exoplanet)
        assert "trop chaude" in result
        assert "500" in result

    def test_habitability_section_too_cold(self, article_formatter):
        """Test habitabilité trop froid."""
        exoplanet = Exoplanet(
            pl_name="Cold b", pl_temperature=ValueWithUncertainty(value=100)
        )
        section = HabitabilitySection(article_formatter)
        result = section.generate(exoplanet)
        assert "trop froide" in result
        assert "100" in result

    def test_habitability_section_habitable(self, article_formatter):
        """Test zone habitable théorique."""
        exoplanet = Exoplanet(
            pl_name="Earth 2.0", pl_temperature=ValueWithUncertainty(value=288)
        )
        section = HabitabilitySection(article_formatter)
        result = section.generate(exoplanet)
        assert "zone habitable" in result
        assert "288" in result

    # Tests pour HostStarSection
    def test_host_star_section_empty(self, article_formatter):
        """Test avec étoile vide."""
        exoplanet = Exoplanet(pl_name="Test b")
        section = HostStarSection(article_formatter)
        result = section.generate(exoplanet)
        assert result == ""

    def test_host_star_section_name_only(self, article_formatter):
        """Test avec seulement le nom de l'étoile."""
        exoplanet = Exoplanet(pl_name="Test b", st_name="Test Star")
        section = HostStarSection(article_formatter)
        result = section.generate(exoplanet)
        assert "== Étoile hôte ==" in result
        assert "Test Star" in result
        assert "type spectral" not in result

    def test_host_star_section_full_info(self, article_formatter):
        """Test avec toutes les infos de l'étoile."""
        exoplanet = Exoplanet(
            pl_name="Test b",
            st_name="Test Star",
            st_spectral_type="G2V",
            st_mass=ValueWithUncertainty(value=1.0),
            st_metallicity=ValueWithUncertainty(value=0.1),
            st_age=ValueWithUncertainty(value=4.5),
        )
        section = HostStarSection(article_formatter)
        result = section.generate(exoplanet)
        assert "== Étoile hôte ==" in result
        assert "Test Star" in result
        assert "G2V" in result
        assert "masse de 1" in result
        assert "métallicité de 0,1" in result
        assert "âgée de 4,5" in result

    def test_host_star_section_partial_info(self, article_formatter):
        """Test avec info partielle de l'étoile."""
        exoplanet = Exoplanet(
            pl_name="Test b",
            st_name="Test Star",
            st_spectral_type="K5",
        )
        section = HostStarSection(article_formatter)
        result = section.generate(exoplanet)
        assert "== Étoile hôte ==" in result
        assert "type spectral K5" in result
        assert "masse" not in result
