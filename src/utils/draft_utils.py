# src/utils/draft_utils.py
import os
import logging
from typing import List, Tuple

# Project imports
from src.models.exoplanet import Exoplanet
from src.utils.wikipedia_generator import WikipediaGenerator

# Configure un logger pour ce module spécifique
logger = logging.getLogger(__name__)

def clean_filename(filename: str) -> str:
    """
    Nettoie un nom de fichier en supprimant les caractères invalides
    et en simplifiant les underscores.
    """
    invalid_chars = '<>:"/\\|?*\t\n\r'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    while '__' in filename:
        filename = filename.replace('__', '_')
    filename = filename.strip('_')
    return filename

def generate_draft(exoplanet: Exoplanet) -> str:
    """
    Génère le contenu d'un brouillon d'article pour une exoplanète.
    """
    # Note : Vous pourriez aussi injecter le générateur si vous souhaitez
    # le configurer ou le partager davantage.
    generator = WikipediaGenerator()
    logger.debug(f"Génération du brouillon pour {exoplanet.name}...")
    content = generator.generate_article_content(exoplanet)
    logger.debug(f"Brouillon pour {exoplanet.name} généré.")
    return content

def save_drafts(missing_drafts: List[Tuple[str, str]],
                existing_drafts: List[Tuple[str, str]],
                drafts_dir: str = "drafts") -> None:
    """
    Sauvegarde les brouillons dans les fichiers et répertoires appropriés.
    """
    missing_dir = os.path.join(drafts_dir, "missing")
    existing_dir = os.path.join(drafts_dir, "existing")
    os.makedirs(missing_dir, exist_ok=True)
    os.makedirs(existing_dir, exist_ok=True)

    logger.info(f"Sauvegarde de {len(missing_drafts)} brouillons manquants dans {missing_dir}")
    for name, content in missing_drafts:
        safe_filename = clean_filename(name)
        filename = os.path.join(missing_dir, f"{safe_filename}.wiki")
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
        except IOError as e:
            logger.error(f"Impossible de sauvegarder le brouillon {filename}: {e}")
        except Exception as e:
            logger.error(f"Erreur inattendue lors de la sauvegarde de {filename}: {e}")

    logger.info(f"Sauvegarde de {len(existing_drafts)} brouillons existants dans {existing_dir}")
    for name, content in existing_drafts:
        safe_filename = clean_filename(name)
        filename = os.path.join(existing_dir, f"{safe_filename}.wiki")
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
        except IOError as e:
            logger.error(f"Impossible de sauvegarder le brouillon {filename}: {e}")
        except Exception as e:
            logger.error(f"Erreur inattendue lors de la sauvegarde de {filename}: {e}")