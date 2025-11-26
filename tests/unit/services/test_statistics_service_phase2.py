import pytest

from src.models.entities.exoplanet_entity import Exoplanet, ValueWithUncertainty
from src.models.entities.star_entity import Star
from src.services.processors.statistics_service import StatisticsService


class TestStatisticsServicePhase2:
    """Tests pour les nouvelles statistiques Phase 2"""

    @pytest.fixture
    def statistics_service(self):
        return StatisticsService()

    # Tests Exoplanètes

    def test_periastron_data_stats(self, statistics_service):
        exoplanets = [
            Exoplanet(
                pl_name="Test 1",
                pl_periastron_time=ValueWithUncertainty(2459000.5),
                pl_argument_of_periastron=ValueWithUncertainty(90.0),
            ),
            Exoplanet(pl_name="Test 2", pl_periastron_time=ValueWithUncertainty(2459100.0)),
            Exoplanet(pl_name="Test 3", pl_argument_of_periastron=ValueWithUncertainty(45.0)),
            Exoplanet(pl_name="Test 4"),
        ]

        stats = statistics_service.generate_statistics_exoplanet(exoplanets)

        assert stats["periastron_data_availability"]["with_periastron_time"] == 2
        assert stats["periastron_data_availability"]["with_argument_of_periastron"] == 2
        assert stats["periastron_data_availability"]["with_both"] == 1
        assert stats["periastron_data_availability"]["with_neither"] == 1

    def test_occultation_depth_stats(self, statistics_service):
        exoplanets = [
            Exoplanet(pl_name="Test 1", pl_occultation_depth=ValueWithUncertainty(0.0005)),
            Exoplanet(pl_name="Test 2", pl_occultation_depth=ValueWithUncertainty(0.005)),
            Exoplanet(pl_name="Test 3", pl_occultation_depth=ValueWithUncertainty(0.05)),
            Exoplanet(pl_name="Test 4", pl_occultation_depth=ValueWithUncertainty(0.15)),
            Exoplanet(pl_name="Test 5"),
        ]

        stats = statistics_service.generate_statistics_exoplanet(exoplanets)

        assert stats["occultation_stats"]["with_occultation_depth"] == 4
        assert stats["occultation_stats"]["occultation_depth_ranges"]["< 0.001"] == 1
        assert stats["occultation_stats"]["occultation_depth_ranges"]["0.001-0.01"] == 1
        assert stats["occultation_stats"]["occultation_depth_ranges"]["0.01-0.1"] == 1
        assert stats["occultation_stats"]["occultation_depth_ranges"]["> 0.1"] == 1

    def test_moon_statistics(self, statistics_service):
        exoplanets = [
            Exoplanet(pl_name="Test 1", sy_mnum=1),
            Exoplanet(pl_name="Test 2", sy_mnum=2),
            Exoplanet(pl_name="Test 3", sy_mnum=3),
            Exoplanet(pl_name="Test 4", sy_mnum=5),
            Exoplanet(pl_name="Test 5", sy_mnum=0),
            Exoplanet(pl_name="Test 6"),
        ]

        stats = statistics_service.generate_statistics_exoplanet(exoplanets)

        assert stats["moon_statistics"]["systems_with_moons"] == 4
        assert stats["moon_statistics"]["total_moons"] == 11
        assert stats["moon_statistics"]["moon_count_distribution"]["1"] == 1
        assert stats["moon_statistics"]["moon_count_distribution"]["2-3"] == 2
        assert stats["moon_statistics"]["moon_count_distribution"]["4+"] == 1

    # Tests Étoiles

    def test_star_age_stats(self, statistics_service):
        stars = [
            Star(st_name="Test 1", st_age=ValueWithUncertainty(0.5)),
            Star(st_name="Test 2", st_age=ValueWithUncertainty(3.0)),
            Star(st_name="Test 3", st_age=ValueWithUncertainty(7.0)),
            Star(st_name="Test 4", st_age=ValueWithUncertainty(12.0)),
            Star(st_name="Test 5"),
        ]

        stats = statistics_service.generate_statistics_star(stars)

        assert stats["star_age_stats"]["with_age_data"] == 4
        assert stats["star_age_stats"]["age_ranges"]["< 1 Gyr"] == 1
        assert stats["star_age_stats"]["age_ranges"]["1-5 Gyr"] == 1
        assert stats["star_age_stats"]["age_ranges"]["5-10 Gyr"] == 1
        assert stats["star_age_stats"]["age_ranges"]["> 10 Gyr"] == 1

    def test_stellar_activity_stats(self, statistics_service):
        stars = [
            Star(st_name="Test 1", st_log_rhk=ValueWithUncertainty(-4.3)),
            Star(st_name="Test 2", st_log_rhk=ValueWithUncertainty(-4.6)),
            Star(st_name="Test 3", st_log_rhk=ValueWithUncertainty(-4.9)),
            Star(st_name="Test 4", st_log_rhk=ValueWithUncertainty(-5.2)),
            Star(st_name="Test 5"),
        ]

        stats = statistics_service.generate_statistics_star(stars)

        assert stats["stellar_activity_stats"]["with_activity_data"] == 4
        assert stats["stellar_activity_stats"]["activity_levels"]["très active"] == 1
        assert stats["stellar_activity_stats"]["activity_levels"]["active"] == 1
        assert stats["stellar_activity_stats"]["activity_levels"]["modérée"] == 1
        assert stats["stellar_activity_stats"]["activity_levels"]["calme"] == 1

    def test_proper_motion_stats(self, statistics_service):
        stars = [
            Star(st_name="Test 1", sy_pm=ValueWithUncertainty(5.0)),
            Star(st_name="Test 2", sy_pm=ValueWithUncertainty(25.0)),
            Star(st_name="Test 3", sy_pm=ValueWithUncertainty(75.0)),
            Star(st_name="Test 4", sy_pm=ValueWithUncertainty(150.0)),
            Star(st_name="Test 5"),
        ]

        stats = statistics_service.generate_statistics_star(stars)

        assert stats["proper_motion_stats"]["with_total_pm"] == 4
        assert stats["proper_motion_stats"]["pm_ranges"]["< 10 mas/an"] == 1
        assert stats["proper_motion_stats"]["pm_ranges"]["10-50 mas/an"] == 1
        assert stats["proper_motion_stats"]["pm_ranges"]["50-100 mas/an"] == 1
        assert stats["proper_motion_stats"]["pm_ranges"]["> 100 mas/an"] == 1

    def test_ecliptic_coordinates_stats(self, statistics_service):
        stars = [
            Star(st_name="Test 1", elon=ValueWithUncertainty(45.0), elat=ValueWithUncertainty(5.0)),
            Star(
                st_name="Test 2", elon=ValueWithUncertainty(90.0), elat=ValueWithUncertainty(20.0)
            ),
            Star(
                st_name="Test 3", elon=ValueWithUncertainty(180.0), elat=ValueWithUncertainty(45.0)
            ),
            Star(
                st_name="Test 4", elon=ValueWithUncertainty(270.0), elat=ValueWithUncertainty(75.0)
            ),
            Star(st_name="Test 5"),
        ]

        stats = statistics_service.generate_statistics_star(stars)

        assert stats["ecliptic_coordinates_stats"]["with_ecliptic_coords"] == 4
        assert stats["ecliptic_coordinates_stats"]["ecliptic_latitude_ranges"]["< 10°"] == 1
        assert stats["ecliptic_coordinates_stats"]["ecliptic_latitude_ranges"]["10-30°"] == 1
        assert stats["ecliptic_coordinates_stats"]["ecliptic_latitude_ranges"]["30-60°"] == 1
        assert stats["ecliptic_coordinates_stats"]["ecliptic_latitude_ranges"]["> 60°"] == 1

    def test_stellar_multiplicity_stats(self, statistics_service):
        stars = [
            Star(st_name="Test 1", sy_star_count=1),
            Star(st_name="Test 2", sy_star_count=2),
            Star(st_name="Test 3", sy_star_count=3),
            Star(st_name="Test 4", sy_star_count=5),
            Star(st_name="Test 5"),
        ]

        stats = statistics_service.generate_statistics_star(stars)

        assert stats["stellar_multiplicity_stats"]["single_stars"] == 1
        assert stats["stellar_multiplicity_stats"]["binary_systems"] == 1
        assert stats["stellar_multiplicity_stats"]["triple_systems"] == 1
        assert stats["stellar_multiplicity_stats"]["higher_order_systems"] == 1
