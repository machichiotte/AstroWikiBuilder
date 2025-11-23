# src/orchestration/data_pipeline.py
"""
Module de gestion du pipeline de données.

Responsabilité :
- Collecter les données depuis les sources
- Ingérer dans le processeur
- Exporter les données consolidées
- Générer et exporter les statistiques
"""

import json
import os
from typing import Any

from src.core.config import logger
from src.services.processors.data_processor import DataProcessor
from src.services.processors.statistics_service import StatisticsService


def fetch_and_ingest_data(collectors: dict[str, Any], processor: DataProcessor) -> None:
    """
    Récupère les données des collecteurs et les ingère dans le processeur.

    Args:
        collectors: Dictionnaire des collecteurs {source_name: collector_instance}
        processor: Instance du DataProcessor pour l'ingestion

    Raises:
        TypeError: Si les données retournées ne sont pas du bon type
    """
    for source_name, collector in collectors.items():
        logger.info(f"Collecte des données depuis {source_name}...")

        try:
            exoplanets, stars = collector.collect_entities_from_source()

            # Validation des types
            if not isinstance(exoplanets, list):
                raise TypeError(f"Exoplanets doit être une liste, reçu {type(exoplanets)}")

            if stars is not None and not isinstance(stars, list):
                raise TypeError(f"Stars doit être une liste ou None, reçu {type(stars)}")

        except Exception as e:
            logger.warning(f"Erreur lors de la collecte depuis {source_name}: {e}")
            continue

        # Ingestion des données
        if exoplanets:
            processor.ingest_exoplanets_from_source(exoplanets, source_name)
        else:
            logger.info(f"Aucune exoplanète récupérée depuis {source_name}.")

        if stars:
            processor.ingest_stars_from_source(stars, source_name)
        else:
            logger.info(f"Aucune étoile récupérée depuis {source_name}.")


def export_consolidated_data(processor: DataProcessor, output_dir: str, timestamp: str) -> None:
    """
    Exporte les données consolidées au format CSV.

    Args:
        processor: Instance du DataProcessor contenant les données
        output_dir: Répertoire de sortie
        timestamp: Timestamp pour nommer les fichiers
    """
    logger.info("Export des données consolidées...")
    try:
        consolidated_path = f"{output_dir}/consolidated/exoplanets_consolidated_{timestamp}.csv"
        processor.export_all_exoplanets("csv", consolidated_path)
    except Exception as e:
        logger.error(f"Erreur lors de l'export des données consolidées : {e}")


def generate_and_export_statistics(
    stat_service: StatisticsService,
    processor: DataProcessor,
    output_dir: str,
    timestamp: str = None,
) -> dict[str, Any]:
    """
    Génère les statistiques et les exporte en JSON.

    Args:
        stat_service: Instance du StatisticsService
        processor: Instance du DataProcessor
        output_dir: Répertoire de sortie
        timestamp: Timestamp optionnel pour nommer les fichiers

    Returns:
        Dict[str, Any]: Dictionnaire contenant toutes les statistiques
    """
    # Génération des statistiques
    stats = {
        "exoplanet": stat_service.generate_statistics_exoplanet(processor.collect_all_exoplanets()),
        "star": stat_service.generate_statistics_star(processor.collect_all_stars()),
    }

    # Affichage dans les logs
    _log_statistics(stats)

    # Export en JSON (optionnel)
    if timestamp:
        _export_statistics_json(stats, output_dir, timestamp)

    return stats


def _log_statistics(stats: dict[str, Any]) -> None:
    """
    Affiche les statistiques dans les logs.

    Args:
        stats: Dictionnaire des statistiques
    """
    # Statistiques des exoplanètes
    logger.info("Statistiques des exoplanètes collectées :")
    logger.info(f"  Total : {stats.get('exoplanet', {}).get('total', 0)}")

    logger.info("  Par méthode de découverte :")
    for method, count in stats.get("exoplanet", {}).get("discovery_methods", {}).items():
        logger.info(f"    - {method} : {count}")

    logger.info("  Par année de découverte :")
    for year, count in sorted(
        stats.get("exoplanet", {}).get("discovery_years", {}).items(),
        key=lambda x: str(x[0]),
    ):
        logger.info(f"    - {year} : {count}")

    logger.info("  Par plage de masse (MJ) :")
    for range_name, count in stats.get("exoplanet", {}).get("mass_ranges", {}).items():
        logger.info(f"    - {range_name} : {count}")

    logger.info("  Par plage de rayon (RJ) :")
    for range_name, count in stats.get("exoplanet", {}).get("radius_ranges", {}).items():
        logger.info(f"    - {range_name} : {count}")

    # Statistiques des étoiles
    logger.info("\nStatistiques des étoiles collectées :")
    logger.info(f"  Total : {stats.get('star', {}).get('total_stars', 0)}")

    logger.info("  Par type spectral :")
    for spectral_type, count in stats.get("star", {}).get("spectral_types", {}).items():
        logger.info(f"    - {spectral_type} : {count}")

    logger.info("  Par source de données :")
    for source, count in stats.get("star", {}).get("data_points_by_source", {}).items():
        logger.info(f"    - {source} : {count}")


def _export_statistics_json(stats: dict[str, Any], output_dir: str, timestamp: str) -> None:
    """
    Sauvegarde les statistiques dans un fichier JSON.

    Args:
        stats: Dictionnaire des statistiques
        output_dir: Répertoire de sortie
        timestamp: Timestamp pour nommer le fichier
    """
    stats_dir = os.path.join(output_dir, "statistics")
    os.makedirs(stats_dir, exist_ok=True)

    stats_path = os.path.join(stats_dir, f"statistics_{timestamp}.json")
    with open(stats_path, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    logger.info(f"Statistiques sauvegardées dans {stats_path}")
