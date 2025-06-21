# src/core/config.py
import logging

# Configuration du logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger: logging.Logger = logging.getLogger(__name__)

# Configuration des chemins
DEFAULT_OUTPUT_DIR = "data/generated"
DEFAULT_DRAFTS_DIR = "data/drafts"
DEFAULT_CACHE_DIR = "data/cache"

# Configuration des User-Agents
DEFAULT_WIKI_USER_AGENT = (
    "AstroWikiBuilder/1.1 (bot; machichiotte@gmail.com or your_project_contact_page)"
)

# Configuration des sources de données
AVAILABLE_SOURCES: list[str] = [
    "nasa_exoplanet_archive",
    "exoplanet_eu",
    "open_exoplanet",
]

# Chemins de cache pour les différentes sources
CACHE_PATHS: dict[str, dict[str, str]] = {
    "nasa_exoplanet_archive": {
        "mock": "generated/random_exoplanets_100.csv",
        "real": "cache/nasa_exoplanet_archive/nea_mock_complete.csv",
    },
    "exoplanet_eu": {
        "mock": "cache/exoplanet_eu_mock.csv",
        "real": "cache/exoplanet_eu_downloaded.csv",
    },
    "open_exoplanet": {
        "mock": "cache/open_exoplanet_mock.csv",
        "real": "cache/open_exoplanet_downloaded.txt",
    },
}
