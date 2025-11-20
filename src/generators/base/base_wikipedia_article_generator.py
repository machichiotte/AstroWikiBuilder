# src/generators/base/base_wikipedia_article_generator.py

import datetime

import pytz


class BaseWikipediaArticleGenerator:
    """
    Générateur abstrait d'articles Wikipédia.
    Gère les sections communes : ébauche, source, références, portails, catégories.
    Les sous-classes doivent se spécialiser pour un type d'objet (exoplanète, étoile, etc.).
    """

    def __init__(self, reference_manager, category_generator, stub_type: str, portals: list[str]):
        self.reference_manager = reference_manager
        self.category_generator = category_generator
        self.stub_type = stub_type
        self.portals = portals

    # --- En-tête d'article ---

    def compose_stub_and_source(self) -> str:
        """
        Génére l'ébauche et le modèle de source unique avec date dynamique.
        """
        current_date = self._format_french_month_year()
        stub = f"{{{{Ébauche|{self.stub_type}}}}}"
        source = f"{{{{Source unique|date={current_date}}}}}"
        return f"{stub}\n{source}"

    def _format_french_month_year(self) -> str:
        now_utc = datetime.datetime.now(pytz.utc)
        paris_tz = pytz.timezone("Europe/Paris")
        now_paris = now_utc.astimezone(paris_tz)
        return now_paris.strftime("%B %Y").lower()

    # --- Footer d'article ---

    def build_references_section(self) -> str:
        return "== Références ==\n{{références}}\n"

    def build_portails_section(self) -> str:
        return "{{Portail|" + "|".join(self.portals) + "}}\n"

    def build_palettes_section(self, obj) -> str | None:
        return None

    def build_category_section(self, obj) -> str:
        categories = self.category_generator.build_categories(obj)
        return "\n".join(categories) if categories else ""
