# src/utils/wikipedia_star_generator.py
import locale
import datetime
import pytz
from src.models.star import Star
from src.utils.star.star_infobox_generator import StarInfoboxGenerator
from src.utils.formatting.format_utils import FormatUtils

from .reference_manager import ReferenceManager


class WikipediaStarGenerator:
    """
    Classe pour générer les articles Wikipedia des étoiles.
    Actuellement, ne génère que l'infobox.
    """

    def __init__(self):
        """
        Initialise le générateur d'article pour une étoile.
        """
        # Future: Initialize other generators like introduction, categories, etc.
        self.reference_manager = ReferenceManager()
        # Assuming StarInfoboxGenerator and FormatUtils might need ReferenceManager
        self.infobox_generator = StarInfoboxGenerator()
        self.format_utils = FormatUtils()
        self._setup_locale()

    def _setup_locale(self):
        """Sets up the locale for French date formatting."""
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
                    print(
                        f"French locale (fr_FR.UTF-8, fr_FR, french_France) not available. "
                        f"Using default system locale: {default_locale or 'C.UTF-8'}. "
                        "Date formatting may not be in French."
                    )

    def _get_formatted_french_utc_plus_1_date(self) -> str:
        """
        Returns the current date as a string formatted "mois année" in French (e.g., "juillet 2024").
        Uses Europe/Paris timezone which is UTC+1 or UTC+2 depending on DST.
        """
        now_utc = datetime.datetime.now(pytz.utc)
        paris_tz = pytz.timezone("Europe/Paris")
        now_paris = now_utc.astimezone(paris_tz)
        return now_paris.strftime("%B %Y").lower()

    def generate_article_content(self, star: Star) -> str:
        self.reference_manager.reset_references()
        article_parts = []

        current_date = self._get_formatted_french_utc_plus_1_date()

        # Stub and Source Templates
        article_parts.append("{{Ébauche|étoile}}")
        article_parts.append(
            f"{{{{Source unique|date={current_date}}}}}"
        )  # Ensure double curly braces for template

        # Infobox
        infobox_content = self.infobox_generator.generate_star_infobox(star)
        if infobox_content:  # Add infobox only if it's not empty
            article_parts.append(infobox_content)

        # Introduction
        star_name_display = (
            star.name.value if star.name and star.name.value else "Cette étoile"
        )
        introduction = f"\n'''{star_name_display}''' est une étoile"

        if star.spectral_type and star.spectral_type.value:
            introduction += f" de type spectral {star.spectral_type.value}"

        introduction += "."

        if star.constellation and star.constellation.value:
            introduction += f" Elle est située dans la constellation [[{star.constellation.value}]]."

        if (
            star.distance_pc and star.distance_pc.value is not None
        ):  # Check value is not None
            try:
                # Ensure distance_pc.value is float for formatting
                distance_val = float(star.distance_pc.value)
                formatted_distance = self.format_utils.format_numeric_value(
                    distance_val, precision=2
                )
                if (
                    formatted_distance
                ):  # Check if formatting returned a non-empty string
                    introduction += f" Elle se trouve à environ {formatted_distance} [[parsec|parsecs]] de la [[Terre]]."
            except (ValueError, TypeError):
                # Handle case where distance_pc.value cannot be converted to float
                print(
                    f"Warning: Could not format distance_pc for {star_name_display}, value: {star.distance_pc.value}"
                )

        article_parts.append(introduction)

        # References Section
        article_parts.append("\n== Références ==")
        article_parts.append(
            "{{références}}"
        )  # Ensure double curly braces for template

        # Portals
        article_parts.append(
            "\n{{Portail|astronomie|étoiles}}"
        )  # Ensure double curly braces for template

        # Categories
        categories = [
            "\n[[Category:Étoiles]]"
        ]  # Start with a newline for the first category
        if star.constellation and star.constellation.value:
            categories.append(f"[[Category:{star.constellation.value}]]")

        article_parts.extend(categories)

        return "\n\n".join(
            filter(None, article_parts)
        )  # Join with double newlines, filter out empty parts
