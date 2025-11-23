# tests/conftest.py
"""
Configuration pytest et fixtures partagées.
"""

from datetime import datetime

import pandas as pd
import pytest

from src.models.entities.exoplanet_entity import Exoplanet, ValueWithUncertainty
from src.models.entities.star_entity import Star
from src.models.references.reference import Reference, SourceType


@pytest.fixture
def sample_exoplanet() -> Exoplanet:
    """Crée une exoplanète de test."""
    reference = Reference(
        source=SourceType.NEA,
        update_date=datetime(2025, 1, 1),
        consultation_date=datetime(2025, 1, 15),
        star_id="HD 209458",
        planet_id="HD 209458 b",
    )

    return Exoplanet(
        pl_name="HD 209458 b",
        pl_mass=ValueWithUncertainty(
            value=0.69, error_positive=0.05, error_negative=0.05
        ),
        pl_radius=ValueWithUncertainty(
            value=1.35, error_positive=0.05, error_negative=0.05
        ),
        pl_orbital_period=ValueWithUncertainty(
            value=3.5247, error_positive=0.0001, error_negative=0.0001
        ),
        st_name="HD 209458",
        disc_method="Transit",
        disc_year=1999,
        reference=reference,
    )


@pytest.fixture
def sample_star() -> Star:
    """Crée une étoile de test."""
    reference = Reference(
        source=SourceType.NEA,
        update_date=datetime(2025, 1, 1),
        consultation_date=datetime(2025, 1, 15),
        star_id="HD 209458",
    )

    return Star(
        st_name="HD 209458",
        st_spectral_type="G0V",
        sy_constellation="Pégase",
        st_distance=ValueWithUncertainty(
            value=47.1, error_positive=0.5, error_negative=0.5
        ),
        reference=reference,
    )


@pytest.fixture
def sample_dataframe() -> pd.DataFrame:
    """Crée un DataFrame de test."""
    data = {
        "pl_name": ["Kepler-1 b", "Kepler-2 b"],
        "pl_bmasse": [0.5, 1.2],
        "pl_rade": [1.0, 1.5],
        "pl_orbper": [2.8, 4.5],
        "discoverymethod": ["Transit", "Radial Velocity"],
        "disc_year": [2010, 2011],
        "hostname": ["Kepler-1", "Kepler-2"],
        "st_spectype": ["G2V", "K0V"],
        "sy_dist": [100.5, 150.2],
    }
    return pd.DataFrame(data)


@pytest.fixture
def mock_cache_dir(tmp_path) -> str:
    """Crée un répertoire de cache temporaire."""
    cache_dir = tmp_path / "cache"
    cache_dir.mkdir()
    return str(cache_dir)
