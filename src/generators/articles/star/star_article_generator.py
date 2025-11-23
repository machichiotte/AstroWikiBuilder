import locale
import re

from src.constants.wikipedia_field_config import CONSTELLATION_GENDER_FR
from src.generators.articles.star.sections.category_section import (
    CategorySection,
)
from src.generators.articles.star.sections.environment_section import (
    EnvironmentSection,
)
from src.generators.articles.star.sections.history_section import (
    HistorySection,
)
from src.generators.articles.star.sections.infobox_section import (
    InfoboxSection,
)
from src.generators.articles.star.sections.introduction_section import (
    IntroductionSection,
)
from src.generators.articles.star.sections.observation_section import (
    ObservationSection,
)
from src.generators.articles.star.sections.physical_characteristics_section import (
    PhysicalCharacteristicsSection,
)
from src.generators.articles.star.sections.planetary_system_section import (
    PlanetarySystemSection,
)
from src.generators.base.base_wikipedia_article_generator import (
    BaseWikipediaArticleGenerator,
)
from src.models.entities.exoplanet_entity import Exoplanet
from src.models.entities.star_entity import Star
from src.services.processors.reference_manager import ReferenceManager
from src.utils.astro.classification.star_type_util import StarTypeUtil
from src.utils.formatters.article_formatter import ArticleFormatter
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
        # On passe None pour category_generator car on le gère nous-même via CategorySection
        super().__init__(
            reference_manager=reference_manager,
            category_generator=None,
            stub_type="étoile",
            portals=["astronomie", "étoiles", "exoplanètes"],
        )

        self.category_section = CategorySection()
        self.infobox_section = InfoboxSection(self.reference_manager)
        self.introduction_section = IntroductionSection()
        self.article_util = ArticleFormatter()
        self.star_type_util = StarTypeUtil()

        # Initialize granular sections
        self.physical_characteristics_section = PhysicalCharacteristicsSection(
            self.article_util
        )
        self.observation_section = ObservationSection(self.article_util)
        self.environment_section = EnvironmentSection()
        self.history_section = HistorySection()
        self.planetary_system_section = PlanetarySystemSection(self.article_util)

    def compose_wikipedia_article_content(
        self, star: Star, exoplanets: list[Exoplanet] | None = None
    ) -> str:
        """
        Construit l'article Wikipédia pour une étoile, incluant éventuellement ses exoplanètes.
        """
        parts = [
            self._build_top_content(star),
            self._compose_main_content(star, exoplanets),
            self._build_bottom_content(star),
        ]

        article = "\n\n".join(filter(None, parts))
        return self.replace_first_reference_with_full(article, star)

    def _build_top_content(self, star: Star) -> str:
        """
        Compose le contenu du haut de l'article : stub, infobox et introduction.
        """
        parts = [
            self.compose_stub_and_source(),
            self.infobox_section.generate(star),
            self.introduction_section.compose_star_introduction(star),
        ]
        return "\n\n".join(filter(None, parts))

    def _compose_main_content(
        self, star: Star, exoplanets: list[Exoplanet] | None
    ) -> str:
        """
        Compose le contenu principal de l'article en appelant toutes les sections de contenu.
        """
        sections = [
            self.physical_characteristics_section.generate(star),
            self.observation_section.generate(star),
            self.environment_section.generate(star),
            self.history_section.generate(star),
            self.planetary_system_section.generate(star, exoplanets or []),
        ]

        return "\n\n".join(filter(None, sections))

    def _build_bottom_content(self, star: Star) -> str:
        """
        Compose le contenu du bas de l'article : références, palettes, portails et catégories.
        """
        parts = [
            self.build_references_section(),
            self.build_palettes_section(star),
            self.build_portails_section(),
            self.build_category_section(star),
        ]
        return "\n\n".join(filter(None, parts))

    def build_category_section(self, star: Star) -> str:
        """
        Génère la section des catégories via CategorySection.
        Surcharge la méthode de base qui utilisait self.category_generator.
        """
        return self.category_section.generate(star)

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

    def build_palettes_section(self, star: Star) -> str | None:
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
