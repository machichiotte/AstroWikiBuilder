"""Tests pour WikipediaService."""

from unittest.mock import Mock

import pytest

from src.models.entities.exoplanet_model import Exoplanet
from src.services.external.wikipedia_service import WikipediaService
from src.utils.wikipedia.wikipedia_checker import WikiArticleInfo, WikipediaChecker


class TestWikipediaService:
    """Tests pour WikipediaService."""

    @pytest.fixture
    def mock_checker(self):
        """Fixture pour créer un WikipediaChecker mocké."""
        return Mock(spec=WikipediaChecker)

    @pytest.fixture
    def service(self, mock_checker):
        """Fixture pour créer un WikipediaService."""
        return WikipediaService(wikipedia_checker=mock_checker)

    @pytest.fixture
    def sample_exoplanet(self):
        """Fixture pour créer une exoplanète de test."""
        return Exoplanet(
            pl_name="Kepler-22 b", st_name="Kepler-22", pl_altname=["KOI-87 b", "KOI-87.01"]
        )

    def test_init(self, mock_checker):
        """Test de l'initialisation."""
        service = WikipediaService(wikipedia_checker=mock_checker)
        assert service.wikipedia_checker == mock_checker

    def test_fetch_articles_for_exoplanet_batch_single_exoplanet(
        self, service, mock_checker, sample_exoplanet
    ):
        """Test de récupération d'articles pour une seule exoplanète."""
        # Mock du retour de check_article_existence_batch
        mock_checker.check_article_existence_batch.return_value = {
            "Kepler-22 b": WikiArticleInfo(
                exists=True,
                title="Kepler-22 b",
                queried_title="Kepler-22 b",
                url="https://fr.wikipedia.org/wiki/Kepler-22_b",
            ),
            "KOI-87 b": WikiArticleInfo(exists=False, title="KOI-87 b", queried_title="KOI-87 b"),
            "KOI-87.01": WikiArticleInfo(
                exists=False, title="KOI-87.01", queried_title="KOI-87.01"
            ),
        }

        result = service.fetch_articles_for_exoplanet_batch([sample_exoplanet])

        assert "Kepler-22 b" in result
        assert len(result["Kepler-22 b"]) == 3
        assert result["Kepler-22 b"]["Kepler-22 b"].exists is True
        assert result["Kepler-22 b"]["KOI-87 b"].exists is False
        mock_checker.check_article_existence_batch.assert_called_once()

    def test_fetch_articles_for_exoplanet_batch_multiple_exoplanets(self, service, mock_checker):
        """Test de récupération d'articles pour plusieurs exoplanètes."""
        exoplanets = [
            Exoplanet(pl_name="Planet A", st_name="Star A", pl_altname=[]),
            Exoplanet(pl_name="Planet B", st_name="Star B", pl_altname=["Alt B"]),
        ]

        mock_checker.check_article_existence_batch.return_value = {
            "Planet A": WikiArticleInfo(exists=True, title="Planet A", queried_title="Planet A"),
            "Planet B": WikiArticleInfo(exists=False, title="Planet B", queried_title="Planet B"),
            "Alt B": WikiArticleInfo(exists=False, title="Alt B", queried_title="Alt B"),
        }

        result = service.fetch_articles_for_exoplanet_batch(exoplanets)

        assert "Planet A" in result
        assert "Planet B" in result
        assert len(result["Planet A"]) == 1
        assert len(result["Planet B"]) == 2

    def test_fetch_articles_for_exoplanet_batch_large_batch(self, service, mock_checker):
        """Test de récupération avec plus de 50 titres (batch)."""
        # Créer 30 exoplanètes avec 2 noms alternatifs chacune = 90 titres
        exoplanets = [
            Exoplanet(
                pl_name=f"Planet {i}", st_name=f"Star {i}", pl_altname=[f"Alt {i}-1", f"Alt {i}-2"]
            )
            for i in range(30)
        ]

        # Mock pour retourner des résultats vides
        mock_checker.check_article_existence_batch.return_value = {}

        service.fetch_articles_for_exoplanet_batch(exoplanets)

        # Devrait être appelé 2 fois (90 titres / 50 = 2 batches)
        assert mock_checker.check_article_existence_batch.call_count == 2

    def test_format_article_links_for_export_all(self, service, sample_exoplanet):
        """Test de formatage de liens pour export (tous)."""
        articles_info = {
            "Kepler-22 b": {
                "Kepler-22 b": WikiArticleInfo(
                    exists=True,
                    title="Kepler-22 b",
                    queried_title="Kepler-22 b",
                    url="https://fr.wikipedia.org/wiki/Kepler-22_b",
                    is_redirect=False,
                ),
                "KOI-87 b": WikiArticleInfo(
                    exists=False, title="KOI-87 b", queried_title="KOI-87 b"
                ),
            }
        }

        result = service.format_article_links_for_export([sample_exoplanet], articles_info)

        assert len(result) == 2
        assert result[0]["exoplanet_primary_name"] == "Kepler-22 b"
        assert result[0]["article_exists"] is True
        assert result[1]["article_exists"] is False

    def test_format_article_links_for_export_only_existing(self, service, sample_exoplanet):
        """Test de formatage de liens pour export (seulement existants)."""
        articles_info = {
            "Kepler-22 b": {
                "Kepler-22 b": WikiArticleInfo(
                    exists=True,
                    title="Kepler-22 b",
                    queried_title="Kepler-22 b",
                    url="https://fr.wikipedia.org/wiki/Kepler-22_b",
                )
            }
        }

        result = service.format_article_links_for_export(
            [sample_exoplanet], articles_info, only_existing=True
        )

        assert len(result) == 1
        assert result[0]["article_exists"] is True

    def test_format_article_links_for_export_only_missing(self, service):
        """Test de formatage de liens pour export (seulement manquants)."""
        exoplanet = Exoplanet(pl_name="Missing Planet", st_name="Star X", pl_altname=[])

        articles_info = {
            "Missing Planet": {
                "Missing Planet": WikiArticleInfo(
                    exists=False, title="Missing Planet", queried_title="Missing Planet"
                )
            }
        }

        result = service.format_article_links_for_export(
            [exoplanet], articles_info, only_missing=True
        )

        assert len(result) == 1
        assert result[0]["article_exists"] is False

    def test_format_article_links_for_export_exoplanet_not_found(self, service):
        """Test de formatage quand l'exoplanète n'est pas trouvée."""
        articles_info = {
            "Unknown Planet": {
                "Unknown Planet": WikiArticleInfo(
                    exists=False, title="Unknown Planet", queried_title="Unknown Planet"
                )
            }
        }

        result = service.format_article_links_for_export(
            [], articles_info  # Liste vide d'exoplanètes
        )

        assert len(result) == 0

    def test_split_by_article_existence_with_existing(self, service):
        """Test de séparation avec articles existants."""
        articles_info = {
            "Planet A": {
                "Planet A": WikiArticleInfo(exists=True, title="Planet A", queried_title="Planet A")
            },
            "Planet B": {
                "Planet B": WikiArticleInfo(
                    exists=False, title="Planet B", queried_title="Planet B"
                )
            },
        }

        existing, missing = service.split_by_article_existence(articles_info)

        assert "Planet A" in existing
        assert "Planet B" in missing
        assert len(existing) == 1
        assert len(missing) == 1

    def test_split_by_article_existence_all_existing(self, service):
        """Test de séparation avec tous les articles existants."""
        articles_info = {
            "Planet A": {
                "Planet A": WikiArticleInfo(exists=True, title="Planet A", queried_title="Planet A")
            },
            "Planet B": {
                "Planet B": WikiArticleInfo(exists=True, title="Planet B", queried_title="Planet B")
            },
        }

        existing, missing = service.split_by_article_existence(articles_info)

        assert len(existing) == 2
        assert len(missing) == 0

    def test_split_by_article_existence_all_missing(self, service):
        """Test de séparation avec tous les articles manquants."""
        articles_info = {
            "Planet A": {
                "Planet A": WikiArticleInfo(
                    exists=False, title="Planet A", queried_title="Planet A"
                )
            },
            "Planet B": {
                "Planet B": WikiArticleInfo(
                    exists=False, title="Planet B", queried_title="Planet B"
                )
            },
        }

        existing, missing = service.split_by_article_existence(articles_info)

        assert len(existing) == 0
        assert len(missing) == 2

    def test_split_by_article_existence_mixed_results(self, service):
        """Test de séparation avec résultats mixtes (un article existe parmi plusieurs)."""
        articles_info = {
            "Planet A": {
                "Planet A": WikiArticleInfo(
                    exists=True, title="Planet A", queried_title="Planet A"
                ),
                "Alt A": WikiArticleInfo(exists=False, title="Alt A", queried_title="Alt A"),
            }
        }

        existing, missing = service.split_by_article_existence(articles_info)

        # Si au moins un article existe, l'exoplanète est dans "existing"
        assert "Planet A" in existing
        assert "Planet A" not in missing
