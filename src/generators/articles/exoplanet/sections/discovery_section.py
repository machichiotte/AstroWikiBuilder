# src/generators/articles/exoplanet/sections/discovery_section.py

from src.models.entities.exoplanet_entity import Exoplanet
from src.utils.formatters.article_formatter import ArticleFormatter


class DiscoverySection:
    """Génère la section découverte pour les articles d'exoplanètes."""

    def __init__(self, article_util: ArticleFormatter):
        self.article_util = article_util

    def generate(self, exoplanet: Exoplanet) -> str:
        """
        Génère la section de découverte.

        Returns:
            str: Contenu de la section ou chaîne vide si pas de date
        """
        if not exoplanet.disc_year:
            return ""

        section = "== Découverte ==\n"

        method_translations: dict[str, str] = {
            "Transit": "des transits",
            "Radial Velocity": "des vitesses radiales",
            "Imaging": "de l'imagerie directe",
            "Microlensing": "de la microlentille gravitationnelle",
            "Timing": "du chronométrage",
            "Astrometry": "de l'astrométrie",
            "Orbital Brightness Modulation": "de la modulation de luminosité orbitale",
            "Eclipse Timing Variations": "des variations temporelles d'éclipses",
            "Pulsar Timing": "du chronométrage de pulsar",
            "Pulsation Timing Variations": "des variations temporelles de pulsation",
            "Disk Kinematics": "de la cinématique du disque",
            "Transit Timing Variations": "des variations temporelles de transit",
        }

        method_raw = (
            exoplanet.disc_method.value
            if exoplanet.disc_method and hasattr(exoplanet.disc_method, "value")
            else ""
        )
        disc_method: str | None = method_translations.get(method_raw, None)

        date_value = exoplanet.disc_year
        if hasattr(date_value, "value"):
            date_value = date_value.value

        if hasattr(date_value, "year"):
            date_str: str = f"en {self.article_util.format_year_without_decimals(date_value.year)}"
        else:
            date_str: str = f"en {str(self.article_util.format_year_without_decimals(date_value))}"

        if disc_method:
            section += f"L'exoplanète a été découverte par la méthode {disc_method} {date_str}.\n"
        else:
            section += f"L'exoplanète a été découverte {date_str}.\n"

        # Ajout des détails sur l'instrument et le télescope
        telescope = exoplanet.disc_telescope
        instrument = exoplanet.disc_instrument

        if telescope and instrument:
            section += f"La découverte a été réalisée grâce au télescope {telescope} et à l'instrument {instrument}.\n"
        elif telescope:
            section += f"La découverte a été réalisée grâce au télescope {telescope}.\n"
        elif instrument:
            section += f"La découverte a été réalisée grâce à l'instrument {instrument}.\n"

        # Ajout de la date de publication
        if exoplanet.disc_pubdate:
            pub_date = exoplanet.disc_pubdate
            # Formatage simple si c'est une chaîne YYYY-MM
            if len(pub_date) >= 7:
                year = pub_date[:4]
                month = pub_date[5:7]
                month_names = {
                    "01": "janvier",
                    "02": "février",
                    "03": "mars",
                    "04": "avril",
                    "05": "mai",
                    "06": "juin",
                    "07": "juillet",
                    "08": "août",
                    "09": "septembre",
                    "10": "octobre",
                    "11": "novembre",
                    "12": "décembre",
                }
                month_name = month_names.get(month)
                if month_name:
                    section += f"La découverte a été annoncée en {month_name} {year}.\n"

        return section
