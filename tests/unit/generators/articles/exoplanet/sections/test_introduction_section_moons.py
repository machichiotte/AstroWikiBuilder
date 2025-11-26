from unittest.mock import Mock

import pytest

from src.generators.articles.exoplanet.sections.introduction_section import (
    IntroductionSection,
)
from src.models.entities.exoplanet_entity import Exoplanet
from src.utils.astro.classification.exoplanet_comparison_util import (
    ExoplanetComparisonUtil,
)
from src.utils.formatters.article_formatter import ArticleFormatter


@pytest.fixture
def mock_comparison_util():
    return Mock(spec=ExoplanetComparisonUtil)


@pytest.fixture
def mock_article_formatter():
    return Mock(spec=ArticleFormatter)


def test_introduction_with_one_moon(mock_comparison_util, mock_article_formatter):
    section = IntroductionSection(mock_comparison_util, mock_article_formatter)
    exoplanet = Exoplanet(pl_name="Test Planet b", st_name="Test Star", sy_snum=1, sy_mnum=1)

    content = section._compose_host_star_phrase(exoplanet)
    assert "accompagné d'une lune" in content


def test_introduction_with_multiple_moons(mock_comparison_util, mock_article_formatter):
    section = IntroductionSection(mock_comparison_util, mock_article_formatter)
    exoplanet = Exoplanet(pl_name="Test Planet b", st_name="Test Star", sy_snum=1, sy_mnum=3)

    content = section._compose_host_star_phrase(exoplanet)
    assert "accompagné de 3 lunes" in content


def test_introduction_without_moons(mock_comparison_util, mock_article_formatter):
    section = IntroductionSection(mock_comparison_util, mock_article_formatter)
    exoplanet = Exoplanet(pl_name="Test Planet b", st_name="Test Star", sy_snum=1, sy_mnum=0)

    content = section._compose_host_star_phrase(exoplanet)
    assert "lune" not in content
