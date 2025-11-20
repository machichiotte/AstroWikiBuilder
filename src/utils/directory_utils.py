# src/utils/directory_utils.py
"""
Utilitaires pour la gestion des répertoires.

Responsabilité :
- Créer les répertoires nécessaires pour le projet
"""

import os

from src.core.config import logger


def create_output_directories(
    output_dir: str,
    drafts_dir: str,
    consolidated_dir: str = None,
) -> None:
    """
    Crée les répertoires de sortie nécessaires s'ils n'existent pas.

    Args:
        output_dir: Répertoire de sortie principal
        drafts_dir: Répertoire pour les brouillons Wikipedia
        consolidated_dir: Répertoire pour les données consolidées (optionnel)

    Example:
        >>> create_output_directories("data/output", "data/drafts", "data/consolidated")
    """
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(drafts_dir, exist_ok=True)

    if consolidated_dir:
        os.makedirs(consolidated_dir, exist_ok=True)
        logger.info(f"Répertoires de sortie créés : {output_dir}, {drafts_dir}, {consolidated_dir}")
    else:
        logger.info(f"Répertoires de sortie créés : {output_dir}, {drafts_dir}")
