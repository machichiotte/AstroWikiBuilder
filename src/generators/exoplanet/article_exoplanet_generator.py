# src/generators/article_exoplanet_generator.py
import locale
import re

from src.generators.exoplanet.content.exoplanet_content_generator import (
    ExoplanetContentGenerator,
)
from src.models.entities.exoplanet import Exoplanet

from src.utils.formatters.article_formatters import ArticleUtils
from src.utils.astro.constellation_utils import ConstellationUtils

from src.utils.astro.classification.exoplanet_comparison_utils import (
    ExoplanetComparisonUtils,
)
from src.utils.astro.classification.exoplanet_type_utils import ExoplanetTypeUtils
from src.generators.exoplanet.header.exoplanet_infobox_generator import (
    ExoplanetInfoboxGenerator,
)
from src.generators.exoplanet.content.exoplanet_introduction_generator import (
    ExoplanetIntroductionGenerator,
)
from src.generators.exoplanet.footer.exoplanet_category_generator import (
    ExoplanetCategoryGenerator,
)
from src.services.processors.reference_manager import ReferenceManager
from src.generators.base_article_generator import BaseArticleGenerator


class ArticleExoplanetGenerator(BaseArticleGenerator):
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

    def compose_exoplanet_article(self, exoplanet: Exoplanet) -> str:
        """
        Génère l'ensemble du contenu de l'article Wikipédia pour une exoplanète.
        Appelle des sous-fonctions dédiées pour chaque partie.
        """
        parts = []

        # 1. Header
        parts.append(self.compose_stub_and_source())
        parts.append(self.infobox_generator.generate(exoplanet))

        # 2. Content
        parts.append(
            self.introduction_generator.compose_exoplanet_introduction(exoplanet)
        )
        parts.append(self.content_generator.compose_exoplanet_content(exoplanet))

        # 3. Footer
        parts.append(self.build_references_section())
        parts.append(self.build_palettes_section(exoplanet))
        parts.append(self.build_portails_section())
        parts.append(self.build_category_section(exoplanet))

        # Assembler le contenu
        article_content = "\n\n".join(filter(None, parts))

        # Post-traitement : remplacer la première occurrence de chaque référence simple par la version complète
        return self._process_references(article_content, exoplanet)

    def _process_references(self, content: str, exoplanet: Exoplanet) -> str:
        """
        Post-traitement : remplace la première occurrence de chaque référence simple
        par la version complète, laisse les suivantes en version simple.
        """
        if not exoplanet.reference:
            return content

        # Créer la référence complète
        full_ref = exoplanet.reference.to_wiki_ref(is_short=False)
        # short_ref = exoplanet.reference.to_wiki_ref(is_short=True)

        # Extraire le nom de la référence (ex: "NEA")
        ref_name = exoplanet.reference.source.value

        # Pattern pour trouver les références simples
        short_ref_pattern = rf'<ref name="{ref_name}"\s*/>'

        # Remplacer seulement la première occurrence
        content, count = re.subn(short_ref_pattern, full_ref, content, count=1)

        return content
