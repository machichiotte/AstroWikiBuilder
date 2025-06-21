# src/generators/article_star_generator.py
import locale
import re
from typing import List, Optional
from src.constants.field_mappings import (
    CONSTELLATION_GENDER,
)
from src.models.entities.star import Star
from src.models.entities.exoplanet import Exoplanet
from src.generators.star.header.star_infobox_generator import StarInfoboxGenerator
from src.utils.formatters.article_formatters import ArticleUtils
from src.services.processors.reference_manager import ReferenceManager
from src.generators.star.footer.star_category_generator import StarCategoryGenerator
from src.generators.base_article_generator import BaseArticleGenerator
from src.generators.star.content.star_content_generator import StarContentGenerator
from src.utils.astro.classification.star_type_utils import StarTypeUtils
from src.utils.lang.phrase.constellation import phrase_de_la_constellation

from src.generators.star.content.star_introduction_generator import (
    StarIntroductionGenerator,
)


class ArticleStarGenerator(BaseArticleGenerator):
    """
    Classe pour générer les articles Wikipedia des étoiles.
    Refactoring inspiré du modèle exoplanète.
    """

    def __init__(self):
        reference_manager = ReferenceManager()
        category_generator = StarCategoryGenerator()

        stub_type = "étoile"
        portals: list[str] = ["astronomie", "étoiles", "exoplanètes"]

        super().__init__(reference_manager, category_generator, stub_type, portals)

        self.introduction_generator = StarIntroductionGenerator()
        self.infobox_generator = StarInfoboxGenerator(self.reference_manager)
        self.article_utils = ArticleUtils()
        self.star_type_utils = StarTypeUtils()
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

        # 1. Header
        parts.append(self.compose_stub_and_source())
        parts.append(self.infobox_generator.generate(star))

        # 2. Content
        parts.append(self.introduction_generator.compose_star_introduction(star))
        parts.append(self.content_generator.compose_star_content(star, exoplanets))

        # 3. Footer
        parts.append(self.build_references_section())
        parts.append(self.build_palettes_section(star))
        parts.append(self.build_portails_section())
        parts.append(self.build_category_section(star))

        # Assembler le contenu
        article_content = "\n\n".join(filter(None, parts))

        # Post-traitement : remplacer la première occurrence de chaque référence simple par la version complète
        return self._process_references(article_content, star)

    def _process_references(self, content: str, star: Star) -> str:
        """
        Post-traitement : remplace la première occurrence de chaque référence simple
        par la version complète, laisse les suivantes en version simple.
        """
        if not star.reference:
            return content

        # Créer la référence complète
        full_ref = star.reference.to_wiki_ref(is_short=False)
        # short_ref = star.reference.to_wiki_ref(is_short=True)

        # Extraire le nom de la référence (ex: "NEA")
        ref_name = star.reference.source.value

        # Pattern pour trouver les références simples
        short_ref_pattern = rf'<ref name="{ref_name}"\s*/>'

        # Remplacer seulement la première occurrence
        content, count = re.subn(short_ref_pattern, full_ref, content, count=1)

        return content

    def build_palettes_section(self, object: Star) -> Optional[str]:
        """
        Construit une section de palette Wiki correctement accordée,
        ex. : {{Palette|Étoiles du Dragon}}, {{Palette|Étoiles de la Lyre}}, {{Palette|Étoiles de l'Éridan}}
        """

        if not object.sy_constellation:
            return None

        constellation = object.sy_constellation.strip()
        gender = CONSTELLATION_GENDER.get(constellation)

        if not gender:
            return None

        # return f"{{{{Palette|Étoiles {article}{constellation}}}}}\n"
        str_constellation = phrase_de_la_constellation(constellation)
        return f"{{{{Palette|Étoiles {str_constellation}}}}}\n"
