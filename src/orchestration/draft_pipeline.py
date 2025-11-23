# src/orchestration/draft_pipeline.py
"""
Module de gestion du pipeline de génération de brouillons Wikipedia.

Responsabilité :
- Générer les brouillons d'articles pour les exoplanètes
- Générer les brouillons d'articles pour les étoiles
- Persister les brouillons sur le disque
"""

from src.core.config import logger
from src.models.entities.exoplanet_entity import Exoplanet
from src.models.entities.star_entity import Star
from src.services.processors.data_processor import DataProcessor
from src.utils.wikipedia.draft_util import (
    build_exoplanet_article_draft,
    build_star_article_draft,
    persist_drafts_by_entity_type,
)


def generate_and_persist_exoplanet_drafts(
    processor: DataProcessor,
    drafts_dir: str,
) -> None:
    """
    Génère et sauvegarde les brouillons d'articles pour les exoplanètes.

    Args:
        processor: Instance du DataProcessor
        drafts_dir: Répertoire de sortie pour les brouillons

    Example:
        >>> generate_and_persist_exoplanet_drafts(processor, "data/drafts")
    """
    exoplanets: list[Exoplanet] = processor.collect_all_exoplanets()
    total = len(exoplanets)
    logger.info(f"Génération de {total} brouillons d'exoplanètes...")

    # Créer un index des exoplanètes par nom d'étoile hôte
    exoplanets_by_star_name: dict[str, list[Exoplanet]] = {}
    for exoplanet in exoplanets:
        if isinstance(exoplanet, Exoplanet) and exoplanet.st_name:
            star_name = str(exoplanet.st_name)
            exoplanets_by_star_name.setdefault(star_name, []).append(exoplanet)

    logger.info(f"Index créé pour {len(exoplanets_by_star_name)} systèmes planétaires")

    exoplanet_drafts = {}
    for idx, exoplanet in enumerate(exoplanets, 1):
        exoplanet_name: str = exoplanet.pl_name

        if isinstance(exoplanet, Exoplanet):
            if idx % 100 == 0 or idx == total:
                logger.info(f"Progression: {idx}/{total} exoplanètes traitées...")

            # Récupérer les planètes du même système
            system_planets = []
            if exoplanet.st_name:
                system_planets = exoplanets_by_star_name.get(str(exoplanet.st_name), [])

            exoplanet_drafts[exoplanet_name] = build_exoplanet_article_draft(
                exoplanet, system_planets=system_planets
            )
        else:
            logger.warning(
                f"Objet ignoré (type: {type(exoplanet)}) pour {exoplanet_name}"
            )

    logger.info(f"Nombre total de brouillons générés: {len(exoplanet_drafts)}")
    persist_drafts_by_entity_type(
        exoplanet_drafts,
        {},
        drafts_dir,
        "exoplanet",
    )


def generate_and_persist_star_drafts(
    processor: DataProcessor,
    drafts_dir: str,
    exoplanets: list[Exoplanet] = None,
) -> None:
    """
    Génère et sauvegarde les brouillons d'articles pour les étoiles.

    Si des exoplanètes sont fournies, elles seront utilisées pour enrichir
    le contenu des étoiles (liens vers les planètes découvertes).

    Args:
        processor: Instance du DataProcessor
        drafts_dir: Répertoire de sortie pour les brouillons
        exoplanets: Liste optionnelle d'exoplanètes pour enrichissement

    Example:
        >>> exos = processor.collect_all_exoplanets()
        >>> generate_and_persist_star_drafts(processor, "data/drafts", exos)
    """
    stars: list[Star] = processor.collect_all_stars()
    total = len(stars)
    logger.info(f"Génération de {total} brouillons d'étoiles...")

    # Créer un index des exoplanètes par nom d'étoile hôte
    exoplanets_by_star_name: dict[str, list[Exoplanet]] = {}
    if exoplanets:
        for exoplanet in exoplanets:
            if hasattr(exoplanet, "st_name") and exoplanet.st_name:
                star_name = str(exoplanet.st_name)
                exoplanets_by_star_name.setdefault(star_name, []).append(exoplanet)

        logger.info(
            f"Index créé pour {len(exoplanets_by_star_name)} étoiles avec exoplanètes"
        )

    star_drafts = {}
    for idx, star in enumerate(stars, 1):
        star_name: str = getattr(star, "st_name", "UNKNOWN")

        if isinstance(star, Star):
            if idx % 100 == 0 or idx == total:
                logger.info(f"Progression: {idx}/{total} étoiles traitées...")

            star_exoplanets = exoplanets_by_star_name.get(star_name, [])
            star_drafts[star_name] = build_star_article_draft(
                star, exoplanets=star_exoplanets
            )
        else:
            logger.warning(f"Objet ignoré (type: {type(star)}) pour {star_name}")

    logger.info(f"Nombre total de brouillons générés: {len(star_drafts)}")
    persist_drafts_by_entity_type(
        star_drafts,
        {},
        drafts_dir,
        "star",
    )
