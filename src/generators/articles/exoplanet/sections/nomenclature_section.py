# src/generators/articles/exoplanet/sections/nomenclature_section.py

from src.models.entities.exoplanet_entity import Exoplanet
from src.utils.formatters.article_formatter import ArticleFormatter


class NomenclatureSection:
    """Génère la section nomenclature pour les articles d'exoplanètes."""

    def __init__(self, article_util: ArticleFormatter):
        self.article_util = article_util

    def generate(self, exoplanet: Exoplanet) -> str:
        """
        Génère un paragraphe standard expliquant la convention de nommage IAU.

        Returns:
            str: Contenu de la section ou chaîne vide si pas de nom
        """
        if not exoplanet.pl_name:
            return ""

        content = "== Nomenclature ==\n"
        content += (
            "La convention de l'[[Union astronomique internationale]] (UAI) pour la désignation des exoplanètes "
            "consiste à ajouter une lettre minuscule à la suite du nom de l'étoile hôte, en commençant par la lettre « b » "
            "pour la première planète découverte dans le système (la lettre « a » désignant l'étoile elle-même). "
            "Les planètes suivantes reçoivent les lettres « c », « d », etc., dans l'ordre de leur découverte.\n"
        )
        return content
