# src/utils/wikipedia_star_generator.py
from src.models.star import Star, DataPoint  # DataPoint needed for example usage
from src.utils.star_infobox_generator import StarInfoboxGenerator


class WikipediaStarGenerator:
    """
    Classe pour générer les articles Wikipedia des étoiles.
    Actuellement, ne génère que l'infobox.
    """

    def __init__(self):
        """
        Initialise le générateur d'article pour une étoile.
        """
        self.infobox_generator = StarInfoboxGenerator()
        # Future: Initialize other generators like introduction, categories, etc.

    def generate_article_content(self, star: Star) -> str:
        """
        Génère le contenu complet de l'article Wikipedia pour une étoile.
        Pour l'instant, cela ne comprend que l'infobox.
        """
        if not isinstance(star, Star):
            raise TypeError("Input must be a Star object.")

        # Générer les différentes sections
        infobox = self.infobox_generator.generate_star_infobox(star)

        # Assembler l'article (pour l'instant, juste l'infobox)
        # Future: Add introduction, sections, references, categories
        # article = f"""{{{{Ébauche|étoile}}}} {/* Placeholder for a stub template if desired */}\n\n"""
        article = ""
        article += infobox

        # Future: Add other sections like:
        # introduction = self.introduction_generator.generate_star_introduction(star)
        # article += f"\n{introduction}\n"
        # article += "\n== Caractéristiques ==\n" # Example section
        # article += "\n== Système planétaire ==\n" # If applicable
        # article += "\n== Références ==\n{{références}}\n"
        # article += "\n{{Portail|astronomie|étoiles}}\n" # Example portal
        # categories = self.category_generator.generate_star_categories(star)
        # for category in categories:
        #     article += f"{category}\n"

        return article


# Example Usage:
if __name__ == "__main__":
    # Sample Star Data (mimicking the structure from star.py and star_infobox_generator.py)
    sirius_data_for_article = {
        "name": DataPoint("Sirius"),
        "image": DataPoint("Sirius_A_and_B_artwork.jpg"),
        "caption": DataPoint("Artistic impression of Sirius A and B"),
        "epoch": DataPoint("J2000.0"),
        "right_ascension": DataPoint("06h 45m 08.9173s"),
        "declination": DataPoint("-16° 42′ 58.017″"),
        "constellation": DataPoint("Grand Chien"),
        "apparent_magnitude": DataPoint("-1.46"),
        "spectral_type": DataPoint("A1V + DA2"),
        "distance": DataPoint(value=2.64, unit="pc"),
        "mass": DataPoint(value=2.063, unit="M☉"),
        "radius": DataPoint(value=1.711, unit="R☉"),
        "temperature": DataPoint(value=9940, unit="K"),
        "age": DataPoint(value="237–247", unit="Myr"),
        "designations": DataPoint(
            ["Alpha Canis Majoris", "α CMa", "HD 48915", "HR 2491"]
        ),
    }
    sirius_star_object = Star(**sirius_data_for_article)

    # Instantiate the WikipediaStarGenerator
    star_article_generator = WikipediaStarGenerator()

    # Generate the article content
    article_content = star_article_generator.generate_article_content(
        sirius_star_object
    )

    # Print the generated content
    print("--- Generated Wikipedia Article Content for Sirius ---")
    print(article_content)

    # Another example: Proxima Centauri
    proxima_data_for_article = {
        "name": DataPoint("Proxima Centauri"),
        "epoch": DataPoint("J2000.0"),
        "constellation": DataPoint("Centaure"),
        "distance": DataPoint(value=1.30197, unit="pc"),
        "spectral_type": DataPoint("M5.5Ve"),
        "apparent_magnitude": DataPoint("11.13"),
        "mass": DataPoint(value=0.1221, unit="M☉"),
        "radius": DataPoint(value=0.1542, unit="R☉"),
        "temperature": DataPoint(value=3042, unit="K"),
        "age": DataPoint(value="4.85", unit="Gyr"),
        "designations": DataPoint(
            "V645 Cen, Alpha Centauri C, HIP 70890"
        ),  # String, Star.__post_init__ handles it
    }
    proxima_star_object = Star(**proxima_data_for_article)

    article_content_proxima = star_article_generator.generate_article_content(
        proxima_star_object
    )
    print("\n--- Generated Wikipedia Article Content for Proxima Centauri ---")
    print(article_content_proxima)
