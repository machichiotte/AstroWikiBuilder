# src/generators/articles/star/star_article_generator.py

import locale
import re
from typing import List, Optional

from src.constants.wikipedia_field_config import CONSTELLATION_GENDER_FR
from src.models.entities.star import Star
from src.models.entities.exoplanet_model import Exoplanet
from src.services.processors.reference_manager import ReferenceManager
from src.generators.base.base_wikipedia_article_generator import (
    BaseWikipediaArticleGenerator,
)
from src.generators.articles.star.parts.star_infobox_generator import (
    StarInfoboxGenerator,
)
from src.generators.articles.star.parts.star_category_generator import (
    StarCategoryGenerator,
)
from src.generators.articles.star.parts.star_content_generator import (
    StarContentGenerator,
)
from src.generators.articles.star.parts.star_introduction_generator import (
    StarIntroductionGenerator,
)
from src.utils.formatters.article_formatters import ArticleUtils
from src.utils.astro.classification.star_type_utils import StarTypeUtils
from src.utils.lang.phrase.constellation import phrase_de_la_constellation


class StarWikipediaArticleGenerator(BaseWikipediaArticleGenerator):
    """
    Générateur complet d'article Wikipédia pour une étoile.
    Produit les différentes sections à partir de générateurs spécialisés.
    """

    def __init__(self):
        try:
            locale.setlocale(locale.LC_ALL, "fr_FR.UTF-8")
        except locale.Error:
            pass

        reference_manager = ReferenceManager()
        category_generator = StarCategoryGenerator()

        super().__init__(
            reference_manager=reference_manager,
            category_generator=category_generator,
            stub_type="étoile",
            portals=["astronomie", "étoiles", "exoplanètes"],
        )

        self.infobox_generator = StarInfoboxGenerator(self.reference_manager)
        self.introduction_generator = StarIntroductionGenerator()
        self.content_generator = StarContentGenerator()
        self.article_utils = ArticleUtils()
        self.star_type_utils = StarTypeUtils()

    def compose_wikipedia_article_content(
        self, star: Star, exoplanets: Optional[List[Exoplanet]] = None
    ) -> str:
        """
        Construit l'article Wikipédia pour une étoile, incluant éventuellement ses exoplanètes.
        """
        parts = [
            self.compose_stub_and_source(),
            self.infobox_generator.build_infobox(star),
            self.introduction_generator.compose_star_introduction(star),
            self.content_generator.compose_star_content(star, exoplanets),
            self.build_references_section(),
            self.build_palettes_section(star),
            self.build_portails_section(),
            self.build_category_section(star),
        ]

        article = "\n\n".join(filter(None, parts))
        return self.replace_first_reference_with_full(article, star)

    def replace_first_reference_with_full(self, content: str, star: Star) -> str:
        """
        Remplace uniquement la première occurrence d'une référence par sa version complète.
        """
        if not star.reference:
            return content

        full_ref = star.reference.to_wiki_ref(is_short=False)
        ref_name = star.reference.source.value
        short_ref_pattern = rf'<ref name="{ref_name}"\s*/>'
        return re.sub(short_ref_pattern, full_ref, content, count=1)

    def build_palettes_section(self, star: Star) -> Optional[str]:
        """
        Construit une section {{Palette|Étoiles de la Constellation}} si possible.
        """
        if not star.sy_constellation:
            return None

        gender = CONSTELLATION_GENDER_FR.get(star.sy_constellation.strip())
        if not gender:
            return None

        formatted_constellation = phrase_de_la_constellation(
            star.sy_constellation.strip()
        )
        return f"{{{{Palette|Étoiles {formatted_constellation}}}}}\n"
