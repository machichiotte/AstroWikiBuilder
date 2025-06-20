# src/generators/wikipedia_star_generator.py
import locale
from typing import List
from src.models.entities.star import Star
from src.models.entities.exoplanet import Exoplanet
from src.generators.star.star_infobox_generator import StarInfoboxGenerator
from src.utils.formatters.article_formatters import ArticleUtils
from src.services.processors.reference_manager import ReferenceManager
from src.generators.star.star_category_generator import StarCategoryGenerator
from src.generators.base_article_generator import BaseArticleGenerator
from src.generators.star.star_content_generator import StarContentGenerator


class ArticleStarGenerator(BaseArticleGenerator):
    """
    Classe pour générer les articles Wikipedia des étoiles.
    Refactoring inspiré du modèle exoplanète.
    """

    def __init__(self):
        reference_manager = ReferenceManager()
        category_generator = StarCategoryGenerator()
        stub_type = "étoile"
        portals: list[str] = ["astronomie", "étoiles"]

        super().__init__(reference_manager, category_generator, stub_type, portals)

        self.infobox_generator = StarInfoboxGenerator(self.reference_manager)
        self.article_utils = ArticleUtils()
        self.content_generator = StarContentGenerator()
        try:
            locale.setlocale(locale.LC_ALL, "fr_FR.UTF-8")
        except locale.Error:
            pass  # Optionnel : gérer fallback si besoin

    def compose_article_content(
        self, star: Star, exoplanets: List[Exoplanet] = None
    ) -> str:
        """
        Génère l'ensemble du contenu de l'article Wikipédia pour une étoile.
        Si des exoplanètes sont fournies, elles seront intégrées dans le contenu.
        """
        parts = []

        # 1. Templates de base (stub + source)
        parts.append(self.compose_stub_and_source())

        # 2. Infobox
        parts.append(self.infobox_generator.generate(star))

        # 3. Introduction
        parts.append(self.build_introduction_section(star))

        # 4. Contenu principal
        parts.append(self.content_generator.compose_full_article(star))

        # 5. Section des exoplanètes (si disponibles)
        if exoplanets:
            parts.append(self.build_exoplanets_section(star, exoplanets))

        # 6. Références et portails
        parts.append(self.build_references_section())

        # 7. Catégories
        parts.append(self.build_category_section(star))

        return "\n\n".join(filter(None, parts))

    def build_introduction_section(self, star: Star) -> str:
        """
        Génère l'introduction de l'article.
        """
        star_name: str = star.st_name if star.st_name else "Cette étoile"
        intro: str = f"'''{star_name}''' est une étoile"

        if star.st_spectral_type:
            intro += f" de type spectral {star.st_spectral_type}"

        intro += "."

        if star.st_constellation:
            intro += (
                f" Elle se trouve dans la constellation [[{star.st_constellation}]]."
            )

        if star.st_distance and star.st_distance.value is not None:
            try:
                dist_val = float(star.st_distance.value)
                formatted = f"{dist_val:.2f}"
                intro += f" Elle est située à environ {formatted} [[parsec|parsecs]] de la [[Terre]]."

            except ValueError:
                formatted = "unknown"

        return intro

    def build_placeholder_section(self, title: str, placeholder_text: str) -> str:
        """
        Génère une section vide avec un titre donné et un placeholder explicite.
        """
        return f"== {title} ==\n{placeholder_text}"

    def build_exoplanets_section(self, star: Star, exoplanets: List[Exoplanet]) -> str:
        """
        Génère une section listant les exoplanètes de l'étoile.
        """
        if not exoplanets:
            return ""

        star_name = star.st_name if star.st_name else "Cette étoile"
        section = "== Système planétaire ==\n"

        if len(exoplanets) == 1:
            section += f"{star_name} possède une exoplanète confirmée :\n\n"
        else:
            section += (
                f"{star_name} possède {len(exoplanets)} exoplanètes confirmées :\n\n"
            )

        # Liste des exoplanètes
        for i, exoplanet in enumerate(exoplanets, 1):
            section += f"* '''[[{exoplanet.pl_name}]]'''"

            # Ajouter des informations de base sur l'exoplanète
            if (
                hasattr(exoplanet, "pl_mass")
                and exoplanet.pl_mass
                and exoplanet.pl_mass.value
            ):
                try:
                    mass = float(exoplanet.pl_mass.value)
                    if mass < 0.1:
                        section += " (planète terrestre)"
                    elif mass < 10:
                        section += " (planète géante)"
                    else:
                        section += " (planète massive)"
                except (ValueError, TypeError):
                    pass

            if (
                hasattr(exoplanet, "pl_orbper")
                and exoplanet.pl_orbper
                and exoplanet.pl_orbper.value
            ):
                try:
                    period = float(exoplanet.pl_orbper.value)
                    section += f", période orbitale de {period:.1f} jours"
                except (ValueError, TypeError):
                    pass

            section += "\n"

        return section
