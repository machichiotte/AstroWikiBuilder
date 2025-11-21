import pytest

from src.generators.articles.exoplanet.parts.exoplanet_see_also_generator import (
    ExoplanetSeeAlsoGenerator,
)
from src.models.entities.exoplanet_entity import Exoplanet


class TestExoplanetSeeAlsoGenerator:
    @pytest.fixture
    def generator(self):
        return ExoplanetSeeAlsoGenerator()

    def test_generate_kepler_planet(self, generator):
        exoplanet = Exoplanet()
        exoplanet.pl_name = "Kepler-99 b"
        exoplanet.pl_altname = ["KOI-305.01"]

        result = generator.generate(exoplanet)

        assert "== Voir aussi ==" in result
        assert "=== Articles connexes ===" in result
        assert "[[Liste des planètes découvertes grâce au télescope spatial Kepler" in result
        assert "=== Liens externes ===" in result
        # EPE
        assert "{{EPE|id=kepler-99_b|nom=Kepler-99 b}}" in result
        # NEA
        assert "{{NEA|id=Kepler-99+b|nom=Kepler-99 b}}" in result
        # Simbad with KOI
        assert "{{Simbad|id=Kepler-99b|nom=KOI-305.01}}" in result
        # Kepler Mission (temporarily disabled)
        # assert "http://kepler.nasa.gov/Mission/discoveries/kepler99b/" in result
        assert "http://kepler.nasa.gov/Mission/discoveries/kepler99b/" not in result

    def test_generate_non_kepler_planet(self, generator):
        exoplanet = Exoplanet()
        exoplanet.pl_name = "WASP-12 b"
        exoplanet.pl_altname = []

        result = generator.generate(exoplanet)

        assert "== Voir aussi ==" in result
        assert "=== Articles connexes ===" not in result
        assert "=== Liens externes ===" in result
        # EPE
        assert "{{EPE|id=wasp-12_b|nom=WASP-12 b}}" in result
        # NEA
        assert "{{NEA|id=WASP-12+b|nom=WASP-12 b}}" in result
        # Simbad without KOI
        assert "{{Simbad|id=WASP-12b|nom=WASP-12 b}}" in result
        # No Kepler Mission link
        assert "http://kepler.nasa.gov/Mission/discoveries/" not in result

    def test_generate_planet_without_koi(self, generator):
        exoplanet = Exoplanet()
        exoplanet.pl_name = "Kepler-10 b"
        exoplanet.pl_altname = ["Another Name"]

        result = generator.generate(exoplanet)

        # Simbad should use pl_name if no KOI found
        assert "{{Simbad|id=Kepler-10b|nom=Kepler-10 b}}" in result

    def test_generate_empty_planet(self, generator):
        exoplanet = Exoplanet()
        result = generator.generate(exoplanet)
        assert result == ""
