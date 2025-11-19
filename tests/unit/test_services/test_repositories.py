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

    def test_get_all_exoplanets_empty(self):
        """Test récupération liste vide."""
        repo = ExoplanetRepository()
        exoplanets = repo.get_all_exoplanets()

        assert isinstance(exoplanets, list)
        assert len(exoplanets) == 0

    def test_add_exoplanets_from_source(self, sample_exoplanet):
        """Test d'ajout d'exoplanètes depuis une source."""
        repo = ExoplanetRepository()

        repo.add_exoplanets_from_source([sample_exoplanet], "test_source")

        exoplanets = repo.get_all_exoplanets()
        assert len(exoplanets) == 1
        assert exoplanets[0].pl_name == "HD 209458 b"

    def test_add_multiple_exoplanets(self, sample_exoplanet):
        """Test d'ajout de multiples exoplanètes."""
        repo = ExoplanetRepository()

        # Créer une deuxième exoplanète
        from src.models.entities.exoplanet import Exoplanet, ValueWithUncertainty
        from src.models.references.reference import Reference, SourceType
        from datetime import datetime

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

        repo.add_exoplanets_from_source([sample_exoplanet, exo2], "test_source")

        exoplanets = repo.get_all_exoplanets()
        assert len(exoplanets) == 2

    def test_get_exoplanet_by_name(self, sample_exoplanet):
        """Test de récupération par nom."""
        repo = ExoplanetRepository()
        repo.add_exoplanets_from_source([sample_exoplanet], "test_source")

        exo = repo.get_exoplanet_by_name("HD 209458 b")
        assert exo is not None
        assert exo.pl_name == "HD 209458 b"

    def test_get_exoplanet_by_name_not_found(self):
        """Test quand l'exoplanète n'existe pas."""
        repo = ExoplanetRepository()

        exo = repo.get_exoplanet_by_name("Nonexistent")
        assert exo is None


class TestStarRepository:
    """Tests du repository d'étoiles."""

    def test_initialization(self):
        """Test d'initialisation."""
        repo = StarRepository()
        assert repo is not None

    def test_get_all_stars_empty(self):
        """Test récupération liste vide."""
        repo = StarRepository()
        stars = repo.get_all_stars()

        assert isinstance(stars, list)
        assert len(stars) == 0

    def test_add_stars_from_source(self, sample_star):
        """Test d'ajout d'étoiles depuis une source."""
        repo = StarRepository()

        repo.add_stars_from_source([sample_star], "test_source")

        stars = repo.get_all_stars()
        assert len(stars) == 1
        assert stars[0].st_name == "HD 209458"

    def test_add_multiple_stars(self, sample_star):
        """Test d'ajout de multiples étoiles."""
        repo = StarRepository()

        from src.models.entities.star import Star
        from src.models.references.reference import Reference, SourceType
        from datetime import datetime

        ref2 = Reference(
            source=SourceType.NEA,
            update_date=datetime.now(),
            consultation_date=datetime.now(),
        )

        star2 = Star(st_name="Kepler-1", st_spectral_type="G0V", reference=ref2)

        repo.add_stars_from_source([sample_star, star2], "test_source")

        stars = repo.get_all_stars()
        assert len(stars) == 2

    def test_get_star_by_name(self, sample_star):
        """Test de récupération par nom."""
        repo = StarRepository()
        repo.add_stars_from_source([sample_star], "test_source")

        star = repo.get_star_by_name("HD 209458")
        assert star is not None
        assert star.st_name == "HD 209458"

    def test_get_star_by_name_not_found(self):
        """Test quand l'étoile n'existe pas."""
        repo = StarRepository()

        star = repo.get_star_by_name("Nonexistent")
        assert star is None
