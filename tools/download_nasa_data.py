#!/usr/bin/env python3
"""
Script pour télécharger les données fraîches du NASA Exoplanet Archive.
Usage: poetry run python download_nasa_data.py
"""

from src.collectors.implementations.nasa_exoplanet_archive_collector import (
    NasaExoplanetArchiveCollector,
)

if __name__ == "__main__":
    print("🚀 Téléchargement des données NASA Exoplanet Archive...")

    # Créer le collecteur
    collector = NasaExoplanetArchiveCollector(use_mock=False)

    # Le téléchargement se fait automatiquement lors de l'appel à collect_entities_from_source
    print("📡 Récupération des données...")
    exoplanets, stars = collector.collect_entities_from_source()

    print("✅ Téléchargement terminé !")
    print(f"   - {len(exoplanets)} exoplanètes récupérées")
    print(f"   - {len(stars)} étoiles récupérées")
    print(f"   - Fichier sauvegardé dans: {collector.cache_file}")
