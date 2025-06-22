# src/generators/articles/exoplanet/exoplanet_article_generator.py

import locale
import re

from src.generators.articles.exoplanet.parts.exoplanet_content_generator import (
    ExoplanetContentGenerator,
)
from src.models.entities.exoplanet import Exoplanet

from src.utils.formatters.article_formatters import ArticleUtils
from src.utils.astro.constellation_utils import ConstellationUtils

from src.utils.astro.classification.exoplanet_comparison_utils import (
    ExoplanetComparisonUtils,
)
from src.utils.astro.classification.exoplanet_type_utils import ExoplanetTypeUtils
from src.generators.articles.exoplanet.parts.exoplanet_infobox_generator import (
    ExoplanetInfoboxGenerator,
)
from src.generators.articles.exoplanet.parts.exoplanet_introduction_generator import (
    ExoplanetIntroductionGenerator,
)
from src.generators.articles.exoplanet.parts.exoplanet_category_generator import (
    ExoplanetCategoryGenerator,
)
from src.services.processors.reference_manager import ReferenceManager
from src.generators.base.base_wikipedia_article_generator import (
    BaseWikipediaArticleGenerator,
)


class ExoplanetWikipediaArticleGenerator(BaseWikipediaArticleGenerator):
    """
    Classe pour générer les articles Wikipedia des exoplanètes
    """

    def __init__(self):
        locale.setlocale(locale.LC_ALL, "fr_FR.UTF-8")

        reference_manager = ReferenceManager()
        category_generator = ExoplanetCategoryGenerator()
        stub_type = "exoplanète"
        portals = ["astronomie", "exoplanètes"]

        super().__init__(reference_manager, category_generator, stub_type, portals)

        self.infobox_generator = ExoplanetInfoboxGenerator(self.reference_manager)
        self.article_utils = ArticleUtils()
        self.constellation_utils = ConstellationUtils()
        self.comparison_utils = ExoplanetComparisonUtils()
        self.planet_type_utils = ExoplanetTypeUtils()
        self.introduction_generator = ExoplanetIntroductionGenerator(
            self.comparison_utils, self.article_utils
        )

        self.content_generator = ExoplanetContentGenerator()

    def compose_wikipedia_article_content(self, exoplanet: Exoplanet) -> str:
        """
        Assemble tout le contenu structuré de l’article Wikipédia pour l’exoplanète.
        """
        parts = [
            self.compose_stub_and_source(),
            self.infobox_generator.build_infobox(exoplanet),
            self.introduction_generator.compose_exoplanet_introduction(exoplanet),
            self.content_generator.compose_exoplanet_content(exoplanet),
            self.build_references_section(),
            self.build_palettes_section(exoplanet),
            self.build_portails_section(),
            self.build_category_section(exoplanet),
        ]

        article = "\n\n".join(filter(None, parts))
        return self.replace_first_reference_with_full(article, exoplanet)

    def replace_first_reference_with_full(
        self, content: str, exoplanet: Exoplanet
    ) -> str:
        """
        Remplace uniquement la première référence courte par sa version complète.
        """
        if not exoplanet.reference:
            return content

        full_ref = exoplanet.reference.to_wiki_ref(is_short=False)
        ref_name = exoplanet.reference.source.value
        short_ref_pattern = rf'<ref name="{ref_name}"\s*/>'

        return re.sub(short_ref_pattern, full_ref, content, count=1)
