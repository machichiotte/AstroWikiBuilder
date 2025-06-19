# src/generators/base_article_generator.py
import datetime
import pytz


class BaseArticleGenerator:
    """
    Classe de base pour générer des articles Wikipédia.
    Cette classe gère les sections communes comme les ébauches, les références,
    les catégories et les portails. Elle est conçue pour être étendue par des
    classes spécifiques pour différents types d'articles (exoplanètes, étoiles, etc.).
    """

    def __init__(self, reference_manager, category_generator, stub_type, portals):
        self.reference_manager = reference_manager
        self.category_generator = category_generator
        self.stub_type = stub_type
        self.portals = portals

    def format_french_month_year(self) -> str:
        now_utc = datetime.datetime.now(pytz.utc)
        paris_tz = pytz.timezone("Europe/Paris")
        now_paris = now_utc.astimezone(paris_tz)
        return now_paris.strftime("%B %Y").lower()

    def compose_stub_and_source(self) -> str:
        current_date = self.format_french_month_year()
        stub = f"{{{{Ébauche|{self.stub_type}}}}}"
        source = f"{{{{Source unique|date={current_date}}}}}"
        return f"{stub}\n{source}"

    def build_references_section(self) -> str:
        section = "== Références ==\n"
        section += "{{références}}\n"
        for portal in self.portals:
            section += f"{{{{Portail|{portal}}}}}\n"
        return section

    def build_category_section(self, obj) -> str:
        categories = self.category_generator.generate_categories(obj)
        if not categories:
            return ""
        section = ""
        for category in categories:
            section += f"{category}\n"
        return section.strip()
