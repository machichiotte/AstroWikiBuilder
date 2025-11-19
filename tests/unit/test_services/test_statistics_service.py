# tests/unit/test_services/test_statistics_service.py
"""
Tests pour StatisticsService.
"""

from src.services.processors.statistics_service import StatisticsService
from src.models.entities.exoplanet import Exoplanet, ValueWithUncertainty
from src.models.entities.star import Star
from src.models.references.reference import Reference, SourceType
from datetime import datetime


class TestStatisticsService:
    """Tests du service de statistiques."""

    def test_initialization(self):
        """Test d'initialisation du service."""
        service = StatisticsService()
        assert service is not None

    def test_generate_statistics_exoplanet_empty_list(self):
        """Test avec liste vide d'exoplanètes."""
        service = StatisticsService()
        stats = service.generate_statistics_exoplanet([])

        assert stats["total"] == 0
        assert stats["discovery_methods"] == {}
        assert stats["discovery_years"] == {}

    def test_generate_statistics_exoplanet_with_data(self):
        """Test avec données d'exoplanètes."""
        service = StatisticsService()

        # Créer des exoplanètes de test
        ref = Reference(
            source=SourceType.NEA,
            update_date=datetime.now(),
            consultation_date=datetime.now(),
        )

        exo1 = Exoplanet(
            pl_name="Test 1 b",
            pl_mass=ValueWithUncertainty(value=0.5),
            pl_radius=ValueWithUncertainty(value=1.0),
            pl_discovery_method="Transit",
            pl_discovery_year=2020,
            reference=ref,
        )

        exo2 = Exoplanet(
            pl_name="Test 2 b",
            pl_mass=ValueWithUncertainty(value=1.5),
            pl_radius=ValueWithUncertainty(value=1.2),
            pl_discovery_method="Radial Velocity",
            pl_discovery_year=2020,
            reference=ref,
        )

        exo3 = Exoplanet(
            pl_name="Test 3 b",
            pl_mass=ValueWithUncertainty(value=0.3),
            pl_radius=ValueWithUncertainty(value=0.8),
            pl_discovery_method="Transit",
            pl_discovery_year=2021,
            reference=ref,
        )

        stats = service.generate_statistics_exoplanet([exo1, exo2, exo3])

        # Vérifications
        assert stats["total"] == 3
        assert stats["discovery_methods"]["Transit"] == 2
        assert stats["discovery_methods"]["Radial Velocity"] == 1
        assert stats["discovery_years"][2020] == 2
        assert stats["discovery_years"][2021] == 1

    def test_generate_statistics_star_empty_list(self):
        """Test avec liste vide d'étoiles."""
        service = StatisticsService()
        stats = service.generate_statistics_star([])

        assert stats["total_stars"] == 0
        assert stats["spectral_types"] == {}

    def test_generate_statistics_star_with_data(self):
        """Test avec données d'étoiles."""
        service = StatisticsService()

        ref = Reference(
            source=SourceType.NEA,
            update_date=datetime.now(),
            consultation_date=datetime.now(),
        )

        star1 = Star(st_name="Star 1", st_spectral_type="G2V", reference=ref)

        star2 = Star(st_name="Star 2", st_spectral_type="K0V", reference=ref)

        star3 = Star(st_name="Star 3", st_spectral_type="G2V", reference=ref)

        stats = service.generate_statistics_star([star1, star2, star3])

        assert stats["total_stars"] == 3
        assert stats["spectral_types"]["G2V"] == 2
        assert stats["spectral_types"]["K0V"] == 1

    def test_mass_ranges_classification(self):
        """Test de la classification par plages de masse."""
        service = StatisticsService()

        ref = Reference(
            source=SourceType.NEA,
            update_date=datetime.now(),
            consultation_date=datetime.now(),
        )

        # Différentes plages de masse (en masses de Jupiter)
        exo_light = Exoplanet(
            pl_name="Light",
            pl_mass=ValueWithUncertainty(value=0.5),  # 0-1 MJ
            reference=ref,
        )

        exo_medium = Exoplanet(
            pl_name="Medium",
            pl_mass=ValueWithUncertainty(value=3.0),  # 2-5 MJ
            reference=ref,
        )

        exo_heavy = Exoplanet(
            pl_name="Heavy",
            pl_mass=ValueWithUncertainty(value=12.0),  # 10+ MJ
            reference=ref,
        )

        stats = service.generate_statistics_exoplanet(
            [exo_light, exo_medium, exo_heavy]
        )

        assert "mass_ranges" in stats
        assert stats["mass_ranges"]["0-1"] == 1
        assert stats["mass_ranges"]["2-5"] == 1
        assert stats["mass_ranges"]["10+"] == 1
