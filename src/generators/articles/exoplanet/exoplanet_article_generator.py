# src/generators/articles/exoplanet/exoplanet_article_generator.py

import locale
import re

from src.generators.articles.exoplanet.sections import (
    CategorySection,
    CompositionSection,
    DiscoverySection,
    FormationMechanismSection,
    HabitabilitySection,
    HostStarSection,
    InfoboxSection,
    InsolationSection,
    IntroductionSection,
    NomenclatureSection,
    ObservationPotentialSection,
    OrbitSection,
    PhysicalCharacteristicsSection,
    SeeAlsoSection,
    SystemArchitectureSection,
    TidalLockingSection,
)
from src.generators.base.base_wikipedia_article_generator import (
    BaseWikipediaArticleGenerator,
)
from src.models.entities.exoplanet_entity import Exoplanet
from src.services.processors.reference_manager import ReferenceManager


class ExoplanetWikipediaArticleGenerator(BaseWikipediaArticleGenerator):
    """
    Classe pour générer les articles Wikipedia des exoplanètes
    """

    def __init__(self):
        try:
            locale.setlocale(locale.LC_ALL, "fr_FR.UTF-8")
        except locale.Error:
            pass

        reference_manager = ReferenceManager()
        stub_type = "exoplanète"
        portals = ["astronomie", "exoplanètes"]

        # On passe None pour category_generator car on le gère nous-même via CategorySection
        super().__init__(reference_manager, None, stub_type, portals)

        self.category_section = CategorySection()
        self.infobox_section = InfoboxSection(self.reference_manager)

        # Create shared utilities for sections
        from src.utils.astro.classification.exoplanet_comparison_util import ExoplanetComparisonUtil
        from src.utils.formatters.article_formatter import ArticleFormatter

        article_util = ArticleFormatter()
        comparison_util = ExoplanetComparisonUtil()

        # Initialize all 14 section generators (13 sections + intro which needs both utils)
        self.introduction_section = IntroductionSection(comparison_util, article_util)
        self.nomenclature_section = NomenclatureSection(article_util)
        self.host_star_section = HostStarSection(article_util)
        self.discovery_section = DiscoverySection(article_util)
        self.physical_characteristics_section = PhysicalCharacteristicsSection(article_util)
        self.composition_section = CompositionSection(article_util)
        self.orbit_section = OrbitSection(article_util)
        self.insolation_section = InsolationSection(article_util)
        self.tidal_locking_section = TidalLockingSection(article_util)
        self.habitability_section = HabitabilitySection(article_util)
        self.system_architecture_section = SystemArchitectureSection(article_util)
        self.observation_potential_section = ObservationPotentialSection(article_util)
        self.formation_mechanism_section = FormationMechanismSection(article_util)
        self.see_also_section = SeeAlsoSection()

    def compose_wikipedia_article_content(self, exoplanet: Exoplanet) -> str:
        """
        Assemble tout le contenu structuré de l'article Wikipédia pour l'exoplanète.
        """
        parts = [
            self._build_top_content(exoplanet),
            self._compose_main_content(exoplanet),
            self._build_bottom_content(exoplanet),
        ]

        article = "\n\n".join(filter(None, parts))
        return self.replace_first_reference_with_full(article, exoplanet)

    def _build_top_content(self, exoplanet: Exoplanet) -> str:
        """
        Compose le contenu du haut de l'article : stub, infobox et introduction.
        """
        parts = [
            self.compose_stub_and_source(),
            self.infobox_section.generate(exoplanet),
            self.introduction_section.generate(exoplanet),
        ]
        return "\n\n".join(filter(None, parts))

    def _compose_main_content(self, exoplanet: Exoplanet) -> str:
        """
        Compose le contenu principal de l'article en appelant toutes les sections de contenu.
        """
        sections = [
            self.nomenclature_section.generate(exoplanet),
            self.host_star_section.generate(exoplanet),
            self.discovery_section.generate(exoplanet),
            self.physical_characteristics_section.generate(exoplanet),
            self.composition_section.generate(exoplanet),
            self.orbit_section.generate(exoplanet),
            self.insolation_section.generate(exoplanet),
            self.tidal_locking_section.generate(exoplanet),
            self.habitability_section.generate(exoplanet),
            self.system_architecture_section.generate(exoplanet),
            self.observation_potential_section.generate(exoplanet),
            self.formation_mechanism_section.generate(exoplanet),
        ]

        return "\n\n".join(filter(None, sections))

    def _build_bottom_content(self, exoplanet: Exoplanet) -> str:
        """
        Compose le contenu du bas de l'article : références, palettes, voir aussi, portails et catégories.
        """
        parts = [
            self.build_references_section(),
            self.build_palettes_section(exoplanet),
            self.see_also_section.generate(exoplanet),
            self.build_portails_section(),
            self.build_category_section(exoplanet),
        ]
        return "\n\n".join(filter(None, parts))

    def build_category_section(self, exoplanet: Exoplanet) -> str:
        """
        Génère la section des catégories via CategorySection.
        Surcharge la méthode de base qui utilisait self.category_generator.
        """
        return self.category_section.generate(exoplanet)

    def replace_first_reference_with_full(self, content: str, exoplanet: Exoplanet) -> str:
        """
        Remplace uniquement la première référence courte par sa version complète.
        """
        if not exoplanet.reference:
            return content

        full_ref = exoplanet.reference.to_wiki_ref(is_short=False)
        ref_name = exoplanet.reference.source.value
        short_ref_pattern = rf'<ref name="{ref_name}"\s*/>'

        return re.sub(short_ref_pattern, full_ref, content, count=1)
