# src/generators/article_star_generator.py
import locale
import re
from typing import List, Optional
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
        portals: list[str] = ["astronomie", "étoiles", "exoplanètes"]

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
        full_ref = star.reference.to_wiki_ref(short=False)
        short_ref = star.reference.to_wiki_ref(short=True)

        # Extraire le nom de la référence (ex: "NEA")
        ref_name = star.reference.source.value

        # Pattern pour trouver les références simples
        short_ref_pattern = rf'<ref name="{ref_name}"\s*/>'

        # Remplacer seulement la première occurrence
        content, count = re.subn(short_ref_pattern, full_ref, content, count=1)

        return content

    def build_introduction_section(self, star: Star) -> str:
        """
        Génère l'introduction de l'article.
        """
        star_name: str = star.st_name if star.st_name else "Cette étoile"
        intro: str = f"'''{star_name}''' est une étoile"

        if star.st_spectral_type:
            intro += f" de type spectral {star.st_spectral_type}"

        intro += "."

        if star.sy_constellation:
            intro += (
                f" Elle se trouve dans la constellation [[{star.sy_constellation}]]."
            )

        if star.st_distance and star.st_distance.value is not None:
            try:
                dist_val = float(star.st_distance.value)
                formatted = f"{dist_val:.2f}"
                intro += f" Elle est située à environ {{{{unité|{formatted}|[[parsec]]s}}}} de la [[Terre]]."

            except ValueError:
                formatted = "unknown"

        return intro

    def build_placeholder_section(self, title: str, placeholder_text: str) -> str:
        """
        Génère une section vide avec un titre donné et un placeholder explicite.
        """
        return f"== {title} ==\n{placeholder_text}"

    def _format_uncertainty(
        self,
        value: float,
        error_positive: Optional[float],
        error_negative: Optional[float],
    ) -> str:
        """
        Formate une valeur avec ses incertitudes selon les cas possibles.
        """
        if error_positive is not None and error_negative is not None:
            if error_positive == error_negative:
                return f"{value:.2f} ± {error_positive:.2f}"
            else:
                return f"{value:.2f} +{error_positive:.2f} -{error_negative:.2f}"
        elif error_positive is not None:
            return f"{value:.2f} +{error_positive:.2f}"
        elif error_negative is not None:
            return f"{value:.2f} -{error_negative:.2f}"
        else:
            return f"{value:.2f}"

    def build_exoplanets_section(self, star: Star, exoplanets: List[Exoplanet]) -> str:
        """
        Génère une section listant les exoplanètes de l'étoile avec le template Wikipedia.
        """
        if not exoplanets:
            return ""

        star_name = star.st_name if star.st_name else "Cette étoile"
        section = "== Système planétaire ==\n"

        # Template de début
        section += "{{Système planétaire début\n"
        section += f"| nom = {star_name}\n"
        section += "}}\n"

        # Templates pour chaque exoplanète
        # Trier les exoplanètes par nom alphabétique avant de les ajouter à la section
        exoplanets.sort(key=lambda exoplanet: exoplanet.pl_name)

        for exoplanet in exoplanets:
            pl_name: str = exoplanet.pl_name
            section += "{{Système planétaire\n"
            section += f"| exoplanète = [[{pl_name}]]\n"

            # Masse
            if exoplanet.pl_mass and exoplanet.pl_mass.value is not None:
                try:
                    mass = float(exoplanet.pl_mass.value)
                    formatted_mass = self._format_uncertainty(
                        mass,
                        exoplanet.pl_mass.error_positive,
                        exoplanet.pl_mass.error_negative,
                    )
                    section += f"| masse = {formatted_mass}\n"
                except (ValueError, TypeError):
                    section += "| masse = \n"
            else:
                section += "| masse = \n"

            # Rayon
            if exoplanet.pl_radius and exoplanet.pl_radius.value is not None:
                try:
                    radius = float(exoplanet.pl_radius.value)
                    formatted_radius = self._format_uncertainty(
                        radius,
                        exoplanet.pl_radius.error_positive,
                        exoplanet.pl_radius.error_negative,
                    )
                    section += f"| rayon = {formatted_radius}\n"
                except (ValueError, TypeError):
                    section += "| rayon = \n"
            else:
                section += "| rayon = \n"

            # Demi-grand axe
            if (
                exoplanet.pl_semi_major_axis
                and exoplanet.pl_semi_major_axis.value is not None
            ):
                try:
                    axis = float(exoplanet.pl_semi_major_axis.value)
                    formatted_axis = self._format_uncertainty(
                        axis,
                        exoplanet.pl_semi_major_axis.error_positive,
                        exoplanet.pl_semi_major_axis.error_negative,
                    )
                    section += f"| demi grand axe = {formatted_axis}\n"
                except (ValueError, TypeError):
                    section += "| demi grand axe = \n"
            else:
                section += "| demi grand axe = \n"

            # Période
            if (
                exoplanet.pl_orbital_period
                and exoplanet.pl_orbital_period.value is not None
            ):
                try:
                    period = float(exoplanet.pl_orbital_period.value)
                    if period.is_integer():
                        section += f"| période = {int(period)}\n"
                    else:
                        section += f"| période = {period:.2f}\n"
                except (ValueError, TypeError):
                    section += "| période = \n"
            else:
                section += "| période = \n"

            # Excentricité
            if (
                exoplanet.pl_eccentricity
                and exoplanet.pl_eccentricity.value is not None
            ):
                try:
                    ecc = float(exoplanet.pl_eccentricity.value)
                    section += f"| excentricité = {ecc:.3f}\n"
                except (ValueError, TypeError):
                    section += "| excentricité = \n"
            else:
                section += "| excentricité = \n"

            # Inclinaison
            if exoplanet.pl_inclination and exoplanet.pl_inclination.value is not None:
                try:
                    incl = float(exoplanet.pl_inclination.value)
                    formatted_incl = self._format_uncertainty(
                        incl,
                        exoplanet.pl_inclination.error_positive,
                        exoplanet.pl_inclination.error_negative,
                    )
                    section += f"| inclinaison = {formatted_incl}\n"
                except (ValueError, TypeError):
                    section += "| inclinaison = \n"
            else:
                section += "| inclinaison = \n"

            section += "}}\n"

        # Template de fin
        section += "{{Système planétaire fin}}\n"

        return section
