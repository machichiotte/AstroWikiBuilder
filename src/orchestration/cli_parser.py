# src/orchestration/cli_parser.py
"""
Module de parsing des arguments de ligne de commande.

Responsabilité :
- Configurer et parser les arguments CLI avec argparse
"""

import argparse

from src.core.config import (
    AVAILABLE_SOURCES,
    DEFAULT_CONSOLIDATED_DIR,
    DEFAULT_DRAFTS_DIR,
    DEFAULT_OUTPUT_DIR,
    logger,
)


def parse_cli_arguments() -> argparse.Namespace:
    """
    Configure et parse les arguments de la ligne de commande.

    Returns:
        argparse.Namespace: Arguments parsés

    Example:
        >>> args = parse_cli_arguments()
        >>> print(args.sources)
        ['nasa_exoplanet_archive']
    """
    parser = argparse.ArgumentParser(
        description="Générateur d'articles Wikipedia pour les exoplanètes"
    )

    parser.add_argument(
        "--sources",
        nargs="+",
        choices=AVAILABLE_SOURCES,
        default=["nasa_exoplanet_archive"],
        help="Sources de données à utiliser (par défaut: nasa_exoplanet_archive)",
    )

    parser.add_argument(
        "--use-mock",
        nargs="+",
        choices=AVAILABLE_SOURCES,
        default=[],
        help="Utiliser les données mockées pour les sources spécifiées",
    )

    parser.add_argument(
        "--skip-wikipedia-check",
        action="store_true",
        help="Générer tous les brouillons sans vérifier l'existence sur Wikipedia (mode test)",
    )

    parser.add_argument(
        "--output-dir",
        type=str,
        default=DEFAULT_OUTPUT_DIR,
        help=f'Directory for storing output files. Default: "{DEFAULT_OUTPUT_DIR}"',
    )

    parser.add_argument(
        "--consolidated-dir",
        type=str,
        default=DEFAULT_CONSOLIDATED_DIR,
        help=f'Directory for storing consolidated files. Default: "{DEFAULT_CONSOLIDATED_DIR}"',
    )

    parser.add_argument(
        "--drafts-dir",
        type=str,
        default=DEFAULT_DRAFTS_DIR,
        help=f'Directory for storing generated Wikipedia draft articles. Default: "{DEFAULT_DRAFTS_DIR}"',
    )

    parser.add_argument(
        "--generate-exoplanets",
        action="store_true",
        default=True,
        help="Générer les brouillons d'exoplanètes (activé par défaut)",
    )

    parser.add_argument(
        "--no-generate-exoplanets",
        dest="generate_exoplanets",
        action="store_false",
        help="Ne PAS générer les brouillons d'exoplanètes",
    )

    parser.add_argument(
        "--generate-stars",
        action="store_true",
        default=True,
        help="Générer les brouillons d'étoiles (activé par défaut)",
    )

    parser.add_argument(
        "--no-generate-stars",
        dest="generate_stars",
        action="store_false",
        help="Ne PAS générer les brouillons d'étoiles",
    )

    args = parser.parse_args()
    logger.info(
        f"Arguments reçus : Sources={args.sources}, Mocks={args.use_mock}, "
        f"SkipWikiCheck={args.skip_wikipedia_check}, "
        f"GenerateExoplanets={args.generate_exoplanets}, GenerateStars={args.generate_stars}, "
        f"OutputDir={args.output_dir}, DraftsDir={args.drafts_dir}"
    )
    return args
