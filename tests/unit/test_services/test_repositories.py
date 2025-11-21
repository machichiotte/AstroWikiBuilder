# tests/unit/test_services/test_repositories.py
"""
Tests pour les repositories (ExoplanetRepository, StarRepository).
"""

from src.services.repositories.exoplanet_repository import ExoplanetRepository
from src.services.repositories.star_repository import StarRepository


class TestExoplanetRepository:
    """Tests du repository d'exoplanètes."""

    def test_initialization(self):
        """Test d'initialisation."""
        repo = ExoplanetRepository()
        assert repo is not None
        assert isinstance(repo.exoplanets, dict)

    def test_get_all_exoplanets_empty(self):
        """Test récupération liste vide."""
        repo = ExoplanetRepository()
        exoplanets = repo.get_all_exoplanets()

        assert isinstance(exoplanets, list)
        assert len(exoplanets) == 0

    def test_add_exoplanets_from_source(self, sample_exoplanet):
        """Test d'ajout d'exoplanètes depuis une source."""
        repo = ExoplanetRepository()

        repo.add_exoplanets([sample_exoplanet], "test_source")

        exoplanets = repo.get_all_exoplanets()
        assert len(exoplanets) == 1
        assert exoplanets[0].pl_name == "HD 209458 b"

    def test_add_multiple_exoplanets(self, sample_exoplanet):
        """Test d'ajout de multiples exoplanètes."""
        repo = ExoplanetRepository()

        from datetime import datetime

        from src.models.entities.exoplanet_entity import Exoplanet, ValueWithUncertainty
        from src.models.references.reference import Reference, SourceType

        ref2 = Reference(
            source=SourceType.NEA,
            update_date=datetime.now(),
            consultation_date=datetime.now(),
        )

        exo2 = Exoplanet(
            pl_name="Kepler-1 b",
            pl_mass=ValueWithUncertainty(value=0.8),
            reference=ref2,
        )

        repo.add_exoplanets([sample_exoplanet, exo2], "test_source")

        exoplanets = repo.get_all_exoplanets()
        assert len(exoplanets) == 2


class TestStarRepository:
    """Tests du repository d'étoiles."""

    def test_initialization(self):
        """Test d'initialisation."""
        repo = StarRepository()
        assert repo is not None
        assert isinstance(repo.stars, dict)

    def test_get_all_stars_empty(self):
        """Test récupération liste vide."""
        repo = StarRepository()
        stars = repo.get_all_stars()

        assert isinstance(stars, list)
        assert len(stars) == 0

    def test_add_stars_from_source(self, sample_star):
        """Test d'ajout d'étoiles depuis une source."""
        repo = StarRepository()

        repo.add_stars([sample_star], "test_source")

        stars = repo.get_all_stars()
        assert len(stars) == 1
        assert stars[0].st_name == "HD 209458"

    def test_add_multiple_stars(self, sample_star):
        """Test d'ajout de multiples étoiles."""
        repo = StarRepository()

        from datetime import datetime

        from src.models.entities.star_entity import Star
        from src.models.references.reference import Reference, SourceType

        ref2 = Reference(
            source=SourceType.NEA,
            update_date=datetime.now(),
            consultation_date=datetime.now(),
        )

        star2 = Star(st_name="Kepler-1", st_spectral_type="G0V", reference=ref2)

        repo.add_stars([sample_star, star2], "test_source")

        stars = repo.get_all_stars()
        assert len(stars) == 2
