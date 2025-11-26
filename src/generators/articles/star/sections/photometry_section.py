# src/generators/articles/star/sections/photometry_section.py

from src.models.entities.star_entity import Star
from src.utils.formatters.article_formatter import ArticleFormatter


class PhotometrySection:
    """Génère la section photométrie pour les articles d'étoiles."""

    def __init__(self, article_util: ArticleFormatter):
        self.article_util = article_util

    def generate(self, star: Star) -> str:
        """Génère la section photométrie avec un tableau des magnitudes."""
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
        magnitudes.extend(self._collect_johnson_magnitudes(star))

        # Sloan (g, r, i)
        magnitudes.extend(self._collect_sloan_magnitudes(star))

        # 2MASS (J, H, K)
        magnitudes.extend(self._collect_2mass_magnitudes(star))

        # WISE (W1, W2, W3, W4)
        magnitudes.extend(self._collect_wise_magnitudes(star))

        # Gaia (G)
        magnitudes.extend(self._collect_gaia_magnitudes(star))

        # TESS (T)
        magnitudes.extend(self._collect_tess_magnitudes(star))

        # Kepler (Kp)
        magnitudes.extend(self._collect_kepler_magnitudes(star))

        return magnitudes

    def _collect_johnson_magnitudes(self, star: Star) -> list[dict]:
        """Collecte les magnitudes Johnson."""
        magnitudes = []

        mag_mapping = [
            (star.st_mag_u, "U"),
            (star.st_mag_b, "B"),
            (star.st_mag_v, "V"),
        ]

        for mag_value, band in mag_mapping:
            if mag_value and mag_value.value is not None:
                magnitudes.append(
                    {
                        "band": band,
                        "value": self._format_magnitude(mag_value),
                        "system": "Johnson",
                    }
                )

        return magnitudes

    def _collect_sloan_magnitudes(self, star: Star) -> list[dict]:
        """Collecte les magnitudes Sloan."""
        magnitudes = []

        mag_mapping = [
            (star.st_mag_g, "g"),
            (star.st_mag_r, "r"),
            (star.st_mag_i, "i"),
        ]

        for mag_value, band in mag_mapping:
            if mag_value and mag_value.value is not None:
                magnitudes.append(
                    {
                        "band": band,
                        "value": self._format_magnitude(mag_value),
                        "system": "Sloan",
                    }
                )

        return magnitudes

    def _collect_2mass_magnitudes(self, star: Star) -> list[dict]:
        """Collecte les magnitudes 2MASS."""
        magnitudes = []

        mag_mapping = [
            (star.st_mag_j, "J"),
            (star.st_mag_h, "H"),
            (star.st_mag_k, "K"),
        ]

        for mag_value, band in mag_mapping:
            if mag_value and mag_value.value is not None:
                magnitudes.append(
                    {
                        "band": band,
                        "value": self._format_magnitude(mag_value),
                        "system": "2MASS",
                    }
                )

        return magnitudes

    def _collect_wise_magnitudes(self, star: Star) -> list[dict]:
        """Collecte les magnitudes WISE."""
        magnitudes = []

        mag_mapping = [
            (star.st_mag_w1, "W1"),
            (star.st_mag_w2, "W2"),
            (star.st_mag_w3, "W3"),
            (star.st_mag_w4, "W4"),
        ]

        for mag_value, band in mag_mapping:
            if mag_value and mag_value.value is not None:
                magnitudes.append(
                    {
                        "band": band,
                        "value": self._format_magnitude(mag_value),
                        "system": "WISE",
                    }
                )

        return magnitudes

    def _collect_gaia_magnitudes(self, star: Star) -> list[dict]:
        """Collecte les magnitudes Gaia."""
        magnitudes = []

        if star.st_mag_gaia and star.st_mag_gaia.value is not None:
            magnitudes.append(
                {
                    "band": "G",
                    "value": self._format_magnitude(star.st_mag_gaia),
                    "system": "Gaia",
                }
            )

        return magnitudes

    def _collect_tess_magnitudes(self, star: Star) -> list[dict]:
        """Collecte les magnitudes TESS."""
        magnitudes = []

        if star.st_mag_t and star.st_mag_t.value is not None:
            magnitudes.append(
                {
                    "band": "T",
                    "value": self._format_magnitude(star.st_mag_t),
                    "system": "TESS",
                }
            )

        return magnitudes

    def _collect_kepler_magnitudes(self, star: Star) -> list[dict]:
        """Collecte les magnitudes Kepler."""
        magnitudes = []

        if star.st_mag_kep and star.st_mag_kep.value is not None:
            magnitudes.append(
                {
                    "band": "Kp",
                    "value": self._format_magnitude(star.st_mag_kep),
                    "system": "Kepler",
                }
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
            err_pos = self.article_util.format_number_as_french_string(mag_value.error_positive)
            err_neg = self.article_util.format_number_as_french_string(
                abs(mag_value.error_negative)
            )
            return f"{value_str} +{err_pos} −{err_neg}"

        return value_str
