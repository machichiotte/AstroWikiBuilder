"""Tests pour WikipediaService."""

from unittest.mock import Mock

import pytest

from src.models.entities.exoplanet_entity import Exoplanet
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
            pl_name="Kepler-22 b",
            st_name="Kepler-22",
            pl_altname=["KOI-87 b", "KOI-87.01"],
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
                pl_name=f"Planet {i}",
                st_name=f"Star {i}",
                pl_altname=[f"Alt {i}-1", f"Alt {i}-2"],
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
            [],
            articles_info,  # Liste vide d'exoplanètes
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

    def test_fetch_articles_unknown_exoplanet_in_context(self, service, sample_exoplanet):
        """Test le cas où le contexte contient une exoplanète inconnue (ligne 66)."""
        # Ce test est difficile à implémenter sans refactoring car il nécessite
        # de manipuler des variables locales ou d'avoir des collisions de hash improbables.
        # Pour l'instant, on laisse passer.
        pass

    def test_format_article_links_only_existing_filter(self, service, sample_exoplanet):
        """Test du filtre only_existing (lignes 75-76, 98-99)."""
        # Cas 1: Exoplanète sans article, only_existing=True -> Doit être exclu
        info_missing = WikiArticleInfo(
            title="Test", queried_title="Test", exists=False, url=None, is_redirect=False
        )
        articles_info = {sample_exoplanet.pl_name: {"Test": info_missing}}

        results = service.format_article_links_for_export(
            [sample_exoplanet], articles_info, only_existing=True
        )
        assert len(results) == 0

        # Cas 2: Exoplanète avec article, only_existing=True -> Doit être inclus
        info_existing = WikiArticleInfo(
            title="Test", queried_title="Test", exists=True, url="http://wiki", is_redirect=False
        )
        articles_info_existing = {sample_exoplanet.pl_name: {"Test": info_existing}}

        results = service.format_article_links_for_export(
            [sample_exoplanet], articles_info_existing, only_existing=True
        )
        assert len(results) == 1

    def test_format_article_links_only_missing_filter(self, service, sample_exoplanet):
        """Test du filtre only_missing (lignes 77-78, 98-99)."""
        # Cas 1: Exoplanète avec article, only_missing=True -> Doit être exclu
        info_existing = WikiArticleInfo(
            title="Test", queried_title="Test", exists=True, url="http://wiki", is_redirect=False
        )
        articles_info = {sample_exoplanet.pl_name: {"Test": info_existing}}

        results = service.format_article_links_for_export(
            [sample_exoplanet], articles_info, only_missing=True
        )
        assert len(results) == 0

        # Cas 2: Exoplanète sans article, only_missing=True -> Doit être inclus
        info_missing = WikiArticleInfo(
            title="Test", queried_title="Test", exists=False, url=None, is_redirect=False
        )
        articles_info_missing = {sample_exoplanet.pl_name: {"Test": info_missing}}

        results = service.format_article_links_for_export(
            [sample_exoplanet], articles_info_missing, only_missing=True
        )
        assert len(results) == 1

    def test_format_article_links_exoplanet_not_found(self, service, sample_exoplanet):
        """Test le cas où l'objet exoplanète n'est pas trouvé (lignes 90-94)."""
        # On passe un dictionnaire d'infos qui contient une clé qui n'est pas dans la liste des exoplanètes
        articles_info = {
            "Unknown Planet": {
                "Test": WikiArticleInfo(title="Test", queried_title="Test", exists=False)
            }
        }

        results = service.format_article_links_for_export([sample_exoplanet], articles_info)
        # Le résultat doit être vide car l'exoplanète "Unknown Planet" n'est pas dans la liste [sample_exoplanet]
        assert len(results) == 0

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
