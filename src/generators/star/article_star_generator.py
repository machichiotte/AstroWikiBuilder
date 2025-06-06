# src/generators/wikipedia_star_generator.py
import locale
from src.models.data_source_star import DataSourceStar
from src.generators.star.star_infobox_generator_v2 import StarInfoboxGenerator
from src.utils.formatters.article_utils import ArticleUtils
from src.services.reference_manager import ReferenceManager
from src.generators.star.star_category_generator import StarCategoryGenerator
from src.generators.base_article_generator import BaseArticleGenerator


class ArticleStarGenerator(BaseArticleGenerator):
    """
    Classe pour générer les articles Wikipedia des étoiles.
    Refactoring inspiré du modèle exoplanète.
    """

    def __init__(self):
        reference_manager = ReferenceManager()
        category_generator = StarCategoryGenerator()
        stub_type = "étoile"
        portals = ["astronomie", "étoiles"]

        super().__init__(reference_manager, category_generator, stub_type, portals)

        self.infobox_generator = StarInfoboxGenerator(self.reference_manager)
        self.article_utils = ArticleUtils()
        try:
            locale.setlocale(locale.LC_ALL, "fr_FR.UTF-8")
        except locale.Error:
            pass  # Optionnel : gérer fallback si besoin

    def generate_article_content(self, star: DataSourceStar) -> str:
        """
        Génère l'ensemble du contenu de l'article Wikipédia pour une étoile.
        """
        self.reference_manager.reset_references()
        parts = []

        # 1. Templates de base (stub + source)
        parts.append(self._generate_stub_and_source())

        # 2. Infobox
        parts.append(self.infobox_generator.generate(star))

        # 3. Introduction
        parts.append(self._generate_introduction_section(star))

        # 4. Section Placeholder (ex. Description détaillée)
        parts.append(
            self._generate_placeholder_section(
                "Description détaillée", "Contenu à implémenter…"
            )
        )

        # 5. Références et portails
        parts.append(self._generate_references_section())

        # 6. Catégories
        parts.append(self._generate_category_section(star))

        return "\n\n".join(filter(None, parts))

    def _generate_introduction_section(self, star: DataSourceStar) -> str:
        """
        Génère l'introduction de l'article.
        """
        star_name = star.name.value if star.name and star.name.value else "Cette étoile"
        intro = f"'''{star_name}''' est une étoile"

        if star.spectral_type and star.spectral_type.value:
            intro += f" de type spectral {star.spectral_type.value}"

        intro += "."

        if star.constellation and star.constellation.value:
            intro += f" Elle se trouve dans la constellation [[{star.constellation.value}]]."
        else:
            intro += " Constellation : {{Placeholder|constellation}}."

        if star.distance_pc and star.distance_pc.value is not None:
            try:
                dist_val = float(star.distance_pc.value)
                formatted = self.article_utils.format_numeric_value(dist_val, precision=2)
                intro += f" Elle est située à environ {formatted} [[parsec|parsecs]] de la [[Terre]]."
            except (ValueError, TypeError):
                intro += " Distance : {{Placeholder|distance en parsecs}}."
        else:
            intro += " Distance : {{Placeholder|distance en parsecs}}."

        return intro

    def _generate_placeholder_section(self, title: str, placeholder_text: str) -> str:
        """
        Génère une section vide avec un titre donné et un placeholder explicite.
        """
        return f"== {title} ==\n{placeholder_text}"
