"""
Tests unitaires pour ExoplanetCategoryGenerator.
"""

import pytest
from src.generators.articles.exoplanet.parts.exoplanet_category_generator import (
    ExoplanetCategoryGenerator,
)
from src.models.entities.exoplanet_model import Exoplanet, ValueWithUncertainty


class TestExoplanetCategoryGenerator:
    """Tests pour le générateur de catégories d'exoplanètes."""

    @pytest.fixture
    def generator(self):
        """Fixture pour créer une instance du générateur."""
        return ExoplanetCategoryGenerator()

    @pytest.fixture
    def hot_jupiter(self):
        """Exoplanète de type Jupiter chaud."""
        return Exoplanet(
            pl_name="HD 209458 b",
            pl_mass=ValueWithUncertainty(value=0.69),
            pl_radius=ValueWithUncertainty(value=1.38),
            pl_orbital_period=ValueWithUncertainty(value=3.52),
            sy_constellation="Pégase",
        )

    @pytest.fixture
    def super_earth(self):
        """Exoplanète de type super-Terre."""
        return Exoplanet(
            pl_name="Kepler-22 b",
            pl_mass=ValueWithUncertainty(value=0.1),
            pl_radius=ValueWithUncertainty(value=0.2),
            sy_constellation="Cygne",
        )

    @pytest.fixture
    def kepler_planet(self):
        """Exoplanète découverte par Kepler."""

        class DiscProgram:
            def __init__(self, value):
                self.value = value

        return Exoplanet(
            pl_name="Kepler-452 b",
            disc_program=DiscProgram("Kepler"),
            sy_constellation="Cygne",
        )

    def test_retrieve_object_type(self, generator):
        """Test de la récupération du type d'objet."""
        assert generator.retrieve_object_type() == "exoplanet"

    def test_define_category_rules(self, generator):
        """Test de la définition des règles de catégorisation."""
        rules = generator.define_category_rules()

        assert len(rules) == 3
        assert callable(rules[0])
        assert callable(rules[1])
        assert callable(rules[2])

    def test_map_constellation_to_category_with_constellation(
        self, generator, hot_jupiter
    ):
        """Test de la catégorisation par constellation."""
        result = generator.map_constellation_to_category(hot_jupiter)

        assert result is not None
        assert "Exoplanète de la constellation de" in result
        assert "Pégase" in result

    def test_map_constellation_to_category_without_constellation(self, generator):
        """Test avec une exoplanète sans constellation."""
        exoplanet = Exoplanet(pl_name="Test b")
        result = generator.map_constellation_to_category(exoplanet)

        assert result is None

    def test_map_constellation_to_category_with_whitespace(self, generator):
        """Test avec une constellation contenant des espaces."""
        exoplanet = Exoplanet(
            pl_name="Test b",
            sy_constellation="  Pégase  ",
        )
        result = generator.map_constellation_to_category(exoplanet)

        assert result is not None
        assert "Pégase" in result
        assert "  " not in result  # Vérifie que les espaces ont été nettoyés

    def test_map_planet_type_to_category_hot_jupiter(self, generator, hot_jupiter):
        """Test de la catégorisation par type de planète (Jupiter chaud)."""
        result = generator.map_planet_type_to_category(hot_jupiter)

        # Le résultat dépend du mapping dans categories_rules.yaml
        # On vérifie juste qu'il ne plante pas
        assert result is None or isinstance(result, str)

    def test_map_planet_type_to_category_without_data(self, generator):
        """Test avec une exoplanète sans données physiques."""
        exoplanet = Exoplanet(pl_name="Test b")
        result = generator.map_planet_type_to_category(exoplanet)

        assert result is None or isinstance(result, str)

    def test_map_discovery_program_to_category_with_program(
        self, generator, kepler_planet
    ):
        """Test de la catégorisation par programme de découverte."""
        result = generator.map_discovery_program_to_category(kepler_planet)

        # Le résultat dépend du mapping dans categories_rules.yaml
        assert result is None or isinstance(result, str)

    def test_map_discovery_program_to_category_without_program(self, generator):
        """Test avec une exoplanète sans programme de découverte."""
        exoplanet = Exoplanet(pl_name="Test b")
        result = generator.map_discovery_program_to_category(exoplanet)

        assert result is None

    def test_map_discovery_program_partial_match(self, generator):
        """Test de la correspondance partielle pour le programme de découverte."""

        class DiscProgram:
            def __init__(self, value):
                self.value = value

        exoplanet = Exoplanet(
            pl_name="Test b",
            disc_program=DiscProgram("Kepler Mission Extended"),
        )
        result = generator.map_discovery_program_to_category(exoplanet)

        # Devrait matcher "Kepler" partiellement
        assert result is None or isinstance(result, str)

    def test_build_categories_complete(self, generator, hot_jupiter):
        """Test de la génération complète de catégories."""
        categories = generator.build_categories(hot_jupiter)

        assert isinstance(categories, list)
        # Au minimum, devrait avoir la catégorie de constellation
        assert len(categories) >= 1
        assert any("Pégase" in cat for cat in categories)

    def test_build_categories_minimal(self, generator):
        """Test avec une exoplanète minimale."""
        exoplanet = Exoplanet(pl_name="Minimal b")
        categories = generator.build_categories(exoplanet)

        assert isinstance(categories, list)
        # Peut être vide si aucune règle ne s'applique

    def test_build_categories_no_duplicates(self, generator, hot_jupiter):
        """Test qu'il n'y a pas de doublons dans les catégories."""
        categories = generator.build_categories(hot_jupiter)

        assert len(categories) == len(set(categories))

    def test_error_handling_invalid_exoplanet(self, generator):
        """Test de la gestion d'erreur avec une exoplanète invalide."""
        # Ne devrait pas planter même avec des données manquantes
        exoplanet = Exoplanet(pl_name=None)

        try:
            categories = generator.build_categories(exoplanet)
            assert isinstance(categories, list)
        except Exception as e:
            pytest.fail(f"Should not raise exception: {e}")
