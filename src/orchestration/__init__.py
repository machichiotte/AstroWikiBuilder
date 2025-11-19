# src/orchestration/__init__.py
"""
Module d'orchestration pour le pipeline AstroWikiBuilder.

Ce module contient toute la logique d'orchestration du workflow principal,
séparant les responsabilités en composants modulaires.
"""

from src.orchestration.cli_parser import parse_cli_arguments
from src.orchestration.pipeline_executor import execute_pipeline

__all__ = [
    "parse_cli_arguments",
    "execute_pipeline",
]
