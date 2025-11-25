# src/generators/articles/star/sections/photometry_section.py

from src.models.entities.star_entity import Star
from src.utils.formatters.article_formatter import ArticleFormatter


class PhotometrySection:
    """Génère la section photométrie pour les articles d'étoiles."""

    def __init__(self, article_util: ArticleFormatter):
        self.article_util = article_util

    def generate(self, star: Star) -> str:
        """Génère la section photométrie avec un tableau des magnitudes."""
        # Collecter toutes les magnitudes disponibles
        magnitudes = self._collect_magnitudes(star)

        if not magnitudes:
            return ""

        section = "== Photométrie ==\n\n"
        section += "Le tableau suivant présente les magnitudes apparentes de l'étoile dans différentes bandes photométriques :\n\n"

        # Créer le tableau Wikipedia
        section += '{| class="wikitable"\n'
        section += "! Bande !! Magnitude !! Système\n"

        for band_info in magnitudes:
            section += "|-\n"
            section += f"| {band_info['band']} || {band_info['value']} || {band_info['system']}\n"

        section += "|}\n"

        return section

    def _collect_magnitudes(self, star: Star) -> list[dict]:
        """Collecte toutes les magnitudes disponibles."""
        magnitudes = []

        # Johnson (U, B, V)
        if star.st_mag_u and star.st_mag_u.value is not None:
            magnitudes.append(
                {"band": "U", "value": self._format_magnitude(star.st_mag_u), "system": "Johnson"}
            )

        if star.st_mag_b and star.st_mag_b.value is not None:
            magnitudes.append(
                {"band": "B", "value": self._format_magnitude(star.st_mag_b), "system": "Johnson"}
            )

        if star.st_mag_v and star.st_mag_v.value is not None:
            magnitudes.append(
                {"band": "V", "value": self._format_magnitude(star.st_mag_v), "system": "Johnson"}
            )

        # Sloan (g, r, i)
        if star.st_mag_g and star.st_mag_g.value is not None:
            magnitudes.append(
                {"band": "g", "value": self._format_magnitude(star.st_mag_g), "system": "Sloan"}
            )

        if star.st_mag_r and star.st_mag_r.value is not None:
            magnitudes.append(
                {"band": "r", "value": self._format_magnitude(star.st_mag_r), "system": "Sloan"}
            )

        if star.st_mag_i and star.st_mag_i.value is not None:
            magnitudes.append(
                {"band": "i", "value": self._format_magnitude(star.st_mag_i), "system": "Sloan"}
            )

        # 2MASS (J, H, K)
        if star.st_mag_j and star.st_mag_j.value is not None:
            magnitudes.append(
                {"band": "J", "value": self._format_magnitude(star.st_mag_j), "system": "2MASS"}
            )

        if star.st_mag_h and star.st_mag_h.value is not None:
            magnitudes.append(
                {"band": "H", "value": self._format_magnitude(star.st_mag_h), "system": "2MASS"}
            )

        if star.st_mag_k and star.st_mag_k.value is not None:
            magnitudes.append(
                {"band": "K", "value": self._format_magnitude(star.st_mag_k), "system": "2MASS"}
            )

        return magnitudes

    def _format_magnitude(self, mag_value) -> str:
        """Formate une magnitude avec son incertitude."""
        if not mag_value or mag_value.value is None:
            return ""

        value_str = self.article_util.format_number_as_french_string(mag_value.value)

        if mag_value.error_positive is not None and mag_value.error_negative is not None:
            if mag_value.error_positive == mag_value.error_negative:
                err_str = self.article_util.format_number_as_french_string(mag_value.error_positive)
                return f"{value_str} ± {err_str}"
            else:
                err_pos = self.article_util.format_number_as_french_string(mag_value.error_positive)
                err_neg = self.article_util.format_number_as_french_string(
                    abs(mag_value.error_negative)
                )
                return f"{value_str} +{err_pos} −{err_neg}"

        return value_str
