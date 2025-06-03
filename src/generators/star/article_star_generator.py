# src/generators/wikipedia_star_generator.py
import locale
import datetime
import pytz
from src.models.data_source_star import DataSourceStar
from src.generators.star.star_infobox_generator_v2 import StarInfoboxGenerator
from src.utils.formatters.article_utils import ArticleUtils
from src.services.reference_manager import ReferenceManager


class ArticleStarGenerator:
    """
    Classe pour générer les articles Wikipedia des étoiles.
    Refactoring inspiré du modèle exoplanète :
      - fonctions dédiées pour chaque section (infobox, introduction, références, catégories)
      - placeholders pour les sections futures (ex. : historique, description détaillée)
    """

    def __init__(self):
        """
        Initialise le générateur d'article pour une étoile.
        """
        self.reference_manager = ReferenceManager()
        self.infobox_generator = StarInfoboxGenerator()
        self.article_utils = ArticleUtils()
        self._setup_locale()

    def _setup_locale(self):
        """
        Configure la locale pour un formatage français (dates, etc.).
        """
        try:
            locale.setlocale(locale.LC_ALL, "fr_FR.UTF-8")
        except locale.Error:
            try:
                locale.setlocale(locale.LC_ALL, "fr_FR")
            except locale.Error:
                try:
                    locale.setlocale(locale.LC_ALL, "french_France")
                except locale.Error:
                    default_locale = locale.getdefaultlocale()[0]
                    locale.setlocale(locale.LC_ALL, default_locale or "C.UTF-8")
                    # Si la locale française n'est pas disponible, on émet un avertissement
                    print(
                        f"French locale not available. Using default: {default_locale or 'C.UTF-8'}."
                    )

    def _get_formatted_french_utc_plus_1_date(self) -> str:
        """
        Retourne la date courante formatée "mois année" en français (zone Europe/Paris).
        """
        now_utc = datetime.datetime.now(pytz.utc)
        paris_tz = pytz.timezone("Europe/Paris")
        now_paris = now_utc.astimezone(paris_tz)
        return now_paris.strftime("%B %Y").lower()

    def generate_article_content(self, star: DataSourceStar) -> str:
        """
        Génère l'ensemble du contenu de l'article Wikipédia pour une étoile.
        Appelle des sous-fonctions dédiées pour chaque partie.
        """
        self.reference_manager.reset_references()
        parts = []

        # 1. Templates de base (stub + source)
        parts.append(self._generate_stub_and_source())

        # 2. Infobox
        parts.append(self._generate_infobox_section(star))

        # 3. Introduction
        parts.append(self._generate_introduction_section(star))

        # 4. Section Placeholder (ex. History, Description détaillée, etc.)
        parts.append(
            self._generate_placeholder_section(
                "Description détaillée", "Contenu à implémenter…"
            )
        )

        # 5. Références et portails
        parts.append(self._generate_references_and_portals())

        # 6. Catégories
        parts.append(self._generate_categories_section(star))

        # On assemble le tout en filtrant les chaînes vides
        return "\n\n".join(filter(None, parts))

    def _generate_stub_and_source(self) -> str:
        """
        Retourne la ligne {{Ébauche|étoile}} et le template {{Source unique}} avec la date.
        """
        current_date = self._get_formatted_french_utc_plus_1_date()
        stub = "{{Ébauche|étoile}}"
        source = f"{{{{Source unique|date={current_date}}}}}"
        return f"{stub}\n{source}"

    def _generate_infobox_section(self, star: DataSourceStar) -> str:
        """
        Génère l'infobox de l'étoile via StarInfoboxGenerator.
        Si l'infobox est vide, on retourne une chaîne vide.
        """
        infobox_content = self.infobox_generator.generate_star_infobox(star)
        return infobox_content or ""

    def _generate_introduction_section(self, star: DataSourceStar) -> str:
        """
        Génère l'introduction de l'article.
        Placeholders pour les données manquantes ou non initialisées.
        """
        # Nom de l'étoile ou placeholder
        star_name = star.name.value if star.name and star.name.value else "Cette étoile"
        intro = f"'''{star_name}''' est une étoile"

        # Type spectral
        if star.spectral_type and star.spectral_type.value:
            intro += f" de type spectral {star.spectral_type.value}"

        intro += "."

        # Constellation
        if star.constellation and star.constellation.value:
            intro += (
                f" Elle se trouve dans la constellation [[{star.constellation.value}]]."
            )
        else:
            intro += " Constellation : {{Placeholder|constellation}}."

        # Distance (parsec), formaté ou placeholder
        if star.distance_pc and star.distance_pc.value is not None:
            try:
                dist_val = float(star.distance_pc.value)
                formatted = self.article_utils.format_numeric_value(
                    dist_val, precision=2
                )
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

    def _generate_references_and_portals(self) -> str:
        """
        Construit la section Références, inclut le portail Astronomie/Étoiles.
        """
        refs = "== Références ==\n{{références}}"
        portals = "{{Portail|astronomie|étoiles}}"
        return f"{refs}\n\n{portals}"

    def _generate_categories_section(self, star: DataSourceStar) -> str:
        """
        Ajoute les catégories associées à l'étoile (au minimum Category:Étoiles).
        Si la constellation est disponible, on ajoute aussi Category:NomConstellation.
        """
        categories = ["[[Category:Étoiles]]"]
        if star.constellation and star.constellation.value:
            categories.append(f"[[Category:{star.constellation.value}]]")
        else:
            categories.append("[[Category:Constellation inconnue]]")  # placeholder
        return "\n".join(categories)
