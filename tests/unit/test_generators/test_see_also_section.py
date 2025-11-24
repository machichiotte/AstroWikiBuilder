import pytest

from src.generators.articles.exoplanet.sections.see_also_section import SeeAlsoSection
from src.models.entities.exoplanet_entity import Exoplanet


class TestSeeAlsoSection:
    @pytest.fixture
    def section(self):
        return SeeAlsoSection()

    def test_generate_empty(self, section):
        exoplanet = Exoplanet(pl_name="Test Planet")
        content = section.generate(exoplanet)
        # No Kepler name, so no related articles, but should have external links
        assert "Voir aussi" in content
        assert "Liens externes" in content

    def test_generate_no_planet_name(self, section):
        exoplanet = Exoplanet(pl_name=None)
        content = section.generate(exoplanet)
        assert content == ""

    def test_generate_with_kepler_name(self, section):
        exoplanet = Exoplanet(pl_name="Kepler-452 b")
        content = section.generate(exoplanet)
        assert "Articles connexes" in content
        assert "Kepler (télescope spatial)" in content
        assert "Liste des planètes découvertes grâce au télescope spatial" in content

    def test_generate_related_articles_kepler(self, section):
        exoplanet = Exoplanet(pl_name="Kepler-22 b")
        content = section._generate_related_articles(exoplanet)
        assert "Articles connexes" in content
        assert "Kepler" in content

    def test_generate_related_articles_non_kepler(self, section):
        exoplanet = Exoplanet(pl_name="HD 209458 b")
        content = section._generate_related_articles(exoplanet)
        assert content == ""

    def test_generate_external_links(self, section):
        exoplanet = Exoplanet(pl_name="Test Planet")
        content = section._generate_external_links(exoplanet)
        assert "Liens externes" in content
        assert "EPE" in content
        assert "NEA" in content
        assert "Simbad" in content

    def test_generate_external_links_no_name(self, section):
        exoplanet = Exoplanet(pl_name=None)
        content = section._generate_external_links(exoplanet)
        assert content == ""

    def test_generate_epe_link(self, section):
        result = section._generate_epe_link("HD 209458 b")
        assert result == "{{EPE|id=hd_209458_b|nom=HD 209458 b}}"

    def test_generate_nasa_link(self, section):
        result = section._generate_nasa_link("HD 209458 b")
        assert result == "{{NEA|id=HD+209458+b|nom=HD 209458 b}}"

    def test_generate_simbad_link_no_koi(self, section):
        exoplanet = Exoplanet(pl_name="HD 209458 b")
        result = section._generate_simbad_link(exoplanet)
        assert result == "{{Simbad|id=HD209458b|nom=HD 209458 b}}"

    def test_generate_simbad_link_with_koi(self, section):
        exoplanet = Exoplanet(pl_name="Kepler-22 b")
        exoplanet.pl_altname = ["KOI-87", "Other Name"]
        result = section._generate_simbad_link(exoplanet)
        assert result == "{{Simbad|id=Kepler-22b|nom=KOI-87}}"

    def test_generate_simbad_link_no_altname(self, section):
        exoplanet = Exoplanet(pl_name="Test Planet")
        exoplanet.pl_altname = None
        result = section._generate_simbad_link(exoplanet)
        assert result == "{{Simbad|id=TestPlanet|nom=Test Planet}}"
