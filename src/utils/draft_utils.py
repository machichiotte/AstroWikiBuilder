# src/utils/draft_utils.py
import os
import logging
from typing import List, Tuple

# Project imports
from src.models.exoplanet import Exoplanet
from src.models.star import Star # Added for star drafts
from src.utils.wikipedia_exoplanet_generator import WikipediaExoplanetGenerator
from src.utils.wikipedia_star_generator import WikipediaStarGenerator # Added for star drafts

# Configure un logger pour ce module spécifique
logger = logging.getLogger(__name__)


def clean_filename(filename: str) -> str:
    """
    Nettoie un nom de fichier en supprimant les caractères invalides
    et en simplifiant les underscores.
    """
    invalid_chars = '<>:"/\\|?*\t\n\r'
    for char in invalid_chars:
        filename = filename.replace(char, "_")
    while "__" in filename:
        filename = filename.replace("__", "_")
    filename = filename.strip("_")
    return filename


def generate_exoplanet_draft(exoplanet: Exoplanet) -> str:
    """
    Génère le contenu d'un brouillon d'article pour une exoplanète.
    """
    # Note : Vous pourriez aussi injecter le générateur si vous souhaitez
    # le configurer ou le partager davantage.
    generator = WikipediaExoplanetGenerator()
    logger.debug(f"Génération du brouillon pour l'exoplanète {exoplanet.name}...")
    content = generator.generate_article_content(exoplanet)
    logger.debug(f"Brouillon pour l'exoplanète {exoplanet.name} généré.")
    return content


def generate_star_draft(star: Star) -> str:
    """
    Génère le contenu d'un brouillon d'article pour une étoile.

    Args:
        star: L'objet Star pour lequel générer le brouillon.

    Returns:
        Le contenu du brouillon généré.
    """
    generator = WikipediaStarGenerator()
    # Star.name is a DataPoint object, so access its .value attribute for the actual name string.
    star_name_val = star.name.value if star.name and hasattr(star.name, 'value') else "Unknown Star"
    logger.debug(f"Génération du brouillon pour l'étoile {star_name_val}...")
    content = generator.generate_article_content(star)
    logger.debug(f"Brouillon pour l'étoile {star_name_val} généré.")
    return content


def save_exoplanet_drafts(
    missing_drafts: List[Tuple[str, str]],
    existing_drafts: List[Tuple[str, str]],
    drafts_dir: str = "drafts/exoplanet",
) -> None:
    """
    Sauvegarde les brouillons d'exoplanètes dans les fichiers et répertoires appropriés.

    Args:
        missing_drafts: Une liste de tuples (nom, contenu) pour les brouillons manquants.
        existing_drafts: Une liste de tuples (nom, contenu) pour les brouillons existants.
        drafts_dir: Le répertoire de base pour sauvegarder les brouillons d'exoplanètes.
    """
    missing_dir = os.path.join(drafts_dir, "missing")
    existing_dir = os.path.join(drafts_dir, "existing")
    os.makedirs(missing_dir, exist_ok=True)
    os.makedirs(existing_dir, exist_ok=True)

    logger.info(
        f"Sauvegarde de {len(missing_drafts)} brouillons d'exoplanètes manquants dans {missing_dir}"
    )
    for name, content in missing_drafts:
        safe_filename = clean_filename(name)
        filename = os.path.join(missing_dir, f"{safe_filename}.wiki")
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
        except IOError as e:
            logger.error(f"Impossible de sauvegarder le brouillon {filename}: {e}")
        except Exception as e:
            logger.error(f"Erreur inattendue lors de la sauvegarde de {filename}: {e}")

    logger.info(
        f"Sauvegarde de {len(existing_drafts)} brouillons d'exoplanètes existants dans {existing_dir}"
    )
    for name, content in existing_drafts:
        safe_filename = clean_filename(name)
        filename = os.path.join(existing_dir, f"{safe_filename}.wiki")
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
        except IOError as e:
            logger.error(f"Impossible de sauvegarder le brouillon {filename}: {e}")
        except Exception as e:
            logger.error(f"Erreur inattendue lors de la sauvegarde de {filename}: {e}")


def save_star_drafts(
    missing_drafts: List[Tuple[str, str]],
    existing_drafts: List[Tuple[str, str]],
    drafts_dir: str = "drafts/star",
) -> None:
    """
    Sauvegarde les brouillons d'étoiles dans les fichiers et répertoires appropriés.

    Args:
        missing_drafts: Une liste de tuples (nom, contenu) pour les brouillons manquants.
        existing_drafts: Une liste de tuples (nom, contenu) pour les brouillons existants.
        drafts_dir: Le répertoire de base pour sauvegarder les brouillons d'étoiles.
    """
    missing_dir = os.path.join(drafts_dir, "missing")
    existing_dir = os.path.join(drafts_dir, "existing")
    os.makedirs(missing_dir, exist_ok=True)
    os.makedirs(existing_dir, exist_ok=True)

    logger.info(
        f"Sauvegarde de {len(missing_drafts)} brouillons d'étoiles manquants dans {missing_dir}"
    )
    for name, content in missing_drafts:
        safe_filename = clean_filename(name)
        filename = os.path.join(missing_dir, f"{safe_filename}.wiki")
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
        except IOError as e:
            logger.error(f"Impossible de sauvegarder le brouillon {filename}: {e}")
        except Exception as e:
            logger.error(f"Erreur inattendue lors de la sauvegarde de {filename}: {e}")

    logger.info(
        f"Sauvegarde de {len(existing_drafts)} brouillons d'étoiles existants dans {existing_dir}"
    )
    for name, content in existing_drafts:
        safe_filename = clean_filename(name)
        filename = os.path.join(existing_dir, f"{safe_filename}.wiki")
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
        except IOError as e:
            logger.error(f"Impossible de sauvegarder le brouillon {filename}: {e}")
        except Exception as e:
            logger.error(f"Erreur inattendue lors de la sauvegarde de {filename}: {e}")
