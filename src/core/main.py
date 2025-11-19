# src/core/main.py
"""
Point d'entrée principal de l'application AstroWikiBuilder.

Ce module simplifié délègue toute la logique aux modules d'orchestration.
"""

from src.orchestration.cli_parser import parse_cli_arguments
from src.orchestration.pipeline_executor import execute_pipeline


def main() -> None:
    """
    Point d'entrée principal du programme.

    Parse les arguments CLI et exécute le pipeline complet.
    """
    args = parse_cli_arguments()
    execute_pipeline(args)


if __name__ == "__main__":
    main()
