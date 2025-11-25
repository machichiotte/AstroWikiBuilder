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
        section += self._generate_discovery_sentence(exoplanet)
        section += self._generate_instrument_info(exoplanet)
        section += self._generate_publication_date(exoplanet)

        return section

    def _generate_discovery_sentence(self, exoplanet: Exoplanet) -> str:
        """Génère la phrase principale de découverte."""
        disc_method = self._get_translated_method(exoplanet.disc_method)
        date_str = self._format_discovery_date(exoplanet.disc_year)

        if disc_method:
            return f"L'exoplanète a été découverte par la méthode {disc_method} {date_str}.\n"
        return f"L'exoplanète a été découverte {date_str}.\n"

    def _get_translated_method(self, disc_method) -> str | None:
        """Traduit la méthode de découverte en français."""
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

        method_raw = disc_method.value if disc_method and hasattr(disc_method, "value") else ""
        return method_translations.get(method_raw, None)

    def _format_discovery_date(self, disc_year) -> str:
        """Formate la date de découverte."""
        date_value = disc_year
        if hasattr(date_value, "value"):
            date_value = date_value.value

        if hasattr(date_value, "year"):
            return f"en {self.article_util.format_year_without_decimals(date_value.year)}"
        return f"en {str(self.article_util.format_year_without_decimals(date_value))}"

    def _generate_instrument_info(self, exoplanet: Exoplanet) -> str:
        """Génère les informations sur le télescope et l'instrument."""
        telescope = exoplanet.disc_telescope
        instrument = exoplanet.disc_instrument

        if telescope and instrument:
            return f"La découverte a été réalisée grâce au télescope {telescope} et à l'instrument {instrument}.\n"
        if telescope:
            return f"La découverte a été réalisée grâce au télescope {telescope}.\n"
        if instrument:
            return f"La découverte a été réalisée grâce à l'instrument {instrument}.\n"
        return ""

    def _generate_publication_date(self, exoplanet: Exoplanet) -> str:
        """Génère l'information sur la date de publication."""
        if not exoplanet.disc_pubdate:
            return ""

        pub_date = exoplanet.disc_pubdate
        if len(pub_date) < 7:
            return ""

        year = pub_date[:4]
        month = pub_date[5:7]
        month_name = self._get_month_name(month)

        if month_name:
            return f"La découverte a été annoncée en {month_name} {year}.\n"
        return ""

    def _get_month_name(self, month: str) -> str | None:
        """Retourne le nom du mois en français."""
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
        return month_names.get(month)
