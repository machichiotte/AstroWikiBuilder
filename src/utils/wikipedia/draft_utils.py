# src/utils/draft_utils.py
import os
import logging
from typing import List, Tuple, Dict

# Project imports
from src.models.entities.exoplanet import Exoplanet
from src.models.entities.star import Star
from src.generators.articles.exoplanet.exoplanet_article_generator import (
    ExoplanetWikipediaArticleGenerator,
)
from src.generators.articles.star.star_article_generator import (
    StarWikipediaArticleGenerator,
)

# Configure un logger pour ce module spécifique
logger = logging.getLogger(__name__)


# ============================================================================
# UTILITAIRES DE NOMENCLATURE DES FICHIERS
# ============================================================================


def sanitize_draft_filename(filename: str) -> str:
    """
    Nettoie un nom de fichier en supprimant les caractères invalides
    et en simplifiant les underscores.
    """
    # Si c'est un objet ValueWithUncertainty, on utilise sa valeur
    if hasattr(filename, "value"):
        filename = str(filename.value)
    else:
        filename = str(filename)

    invalid_chars = '<>:"/\\|?*\t\n\r'
    for char in invalid_chars:
        filename = filename.replace(char, "_")
    while "__" in filename:
        filename = filename.replace("__", "_")
    filename = filename.strip("_")
    return filename


# ============================================================================
# GÉNÉRATION DE CONTENU D'ARTICLES
# ============================================================================


def build_exoplanet_article_draft(exoplanet: Exoplanet) -> str:
    """
    Génère le contenu d'un brouillon d'article pour une exoplanète.
    """
    generator = ExoplanetWikipediaArticleGenerator()
    content: str = generator.compose_wikipedia_article_content(exoplanet)
    return content


def build_star_article_draft(star: Star, exoplanets: List[Exoplanet] = None) -> str:
    """
    Génère le contenu d'un brouillon d'article pour une étoile.
    Si une liste d'exoplanètes est fournie, elle sera intégrée dans le contenu.
    """
    generator = StarWikipediaArticleGenerator()
    content: str = generator.compose_wikipedia_article_content(
        star, exoplanets=exoplanets
    )
    return content


# ============================================================================
# SAUVEGARDE DES BROUILLONS PAR TYPE D'ENTITÉ
# ============================================================================


def write_separated_exoplanet_drafts(
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
    missing_dir: str = os.path.join(drafts_dir, "missing")
    existing_dir: str = os.path.join(drafts_dir, "existing")
    os.makedirs(missing_dir, exist_ok=True)
    os.makedirs(existing_dir, exist_ok=True)

    logger.info(
        f"Sauvegarde de {len(missing_drafts)} brouillons d'exoplanètes manquants dans {missing_dir}"
    )
    for name, content in missing_drafts:
        safe_filename: str = sanitize_draft_filename(name)
        filename: str = os.path.join(missing_dir, f"{safe_filename}.wiki")
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
        safe_filename = sanitize_draft_filename(name)
        filename = os.path.join(existing_dir, f"{safe_filename}.wiki")
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
        except IOError as e:
            logger.error(f"Impossible de sauvegarder le brouillon {filename}: {e}")
        except Exception as e:
            logger.error(f"Erreur inattendue lors de la sauvegarde de {filename}: {e}")


def write_separated_star_drafts(
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
    missing_dir: str = os.path.join(drafts_dir, "missing")
    existing_dir: str = os.path.join(drafts_dir, "existing")
    os.makedirs(missing_dir, exist_ok=True)
    os.makedirs(existing_dir, exist_ok=True)

    logger.info(
        f"Sauvegarde de {len(missing_drafts)} brouillons d'étoiles manquants dans {missing_dir}"
    )
    for name, content in missing_drafts:
        safe_filename: str = sanitize_draft_filename(name)
        filename: str = os.path.join(missing_dir, f"{safe_filename}.wiki")
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
        safe_filename = sanitize_draft_filename(name)
        filename = os.path.join(existing_dir, f"{safe_filename}.wiki")
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
        except IOError as e:
            logger.error(f"Impossible de sauvegarder le brouillon {filename}: {e}")
        except Exception as e:
            logger.error(f"Erreur inattendue lors de la sauvegarde de {filename}: {e}")


# ============================================================================
# SAUVEGARDE GÉNÉRIQUE DES BROUILLONS
# ============================================================================


def persist_drafts_by_entity_type(
    missing_drafts: Dict[str, str],
    existing_drafts: Dict[str, str],
    drafts_dir: str,
    entity_type: str,
) -> None:
    """
    Sauvegarde les brouillons dans les répertoires appropriés.

    Args:
        missing_drafts: Dictionnaire des brouillons manquants {nom: contenu}
        existing_drafts: Dictionnaire des brouillons existants {nom: contenu}
        drafts_dir: Répertoire de base pour les brouillons
        entity_type: Type d'entité ('exoplanet' ou 'star')
    """
    try:
        # Créer les répertoires s'ils n'existent pas
        missing_dir: str = os.path.join(drafts_dir, "missing")
        existing_dir: str = os.path.join(drafts_dir, "existing")

        # Créer les sous-répertoires pour le type d'entité
        missing_entity_dir: str = os.path.join(missing_dir, entity_type)
        existing_entity_dir: str = os.path.join(existing_dir, entity_type)

        os.makedirs(missing_entity_dir, exist_ok=True)
        os.makedirs(existing_entity_dir, exist_ok=True)

        # Sauvegarder les brouillons manquants
        for name, content in missing_drafts.items():
            filename: str = sanitize_draft_filename(name) + ".wiki"
            filepath: str = os.path.join(missing_entity_dir, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            # logger.info(f"Brouillon manquant sauvegardé : {filepath}")

        # Sauvegarder les brouillons existants
        for name, content in existing_drafts.items():
            filename = sanitize_draft_filename(name) + ".wiki"
            filepath = os.path.join(existing_entity_dir, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            # logger.info(f"Brouillon existant sauvegardé : {filepath}")

        total = len(missing_drafts) + len(existing_drafts)
        logger.info(
            f"Total de {total} brouillons sauvegardés dans : {missing_entity_dir} et {existing_entity_dir}"
        )

    except Exception as e:
        logger.error(f"Erreur lors de la sauvegarde des brouillons : {str(e)}")
        raise
