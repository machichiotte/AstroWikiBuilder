# src/generators/articles/star/parts/star_content_generator.py


# ============================================================================
# IMPORTS
# ============================================================================

from src.models.entities.exoplanet_entity import Exoplanet
from src.models.entities.star_entity import Star
from src.utils.formatters.article_formatter import ArticleFormatter
from src.utils.lang.phrase.constellation import phrase_dans_constellation


class StarContentGenerator:
    """
    Générateur de contenu pour les articles d'étoiles.
    Responsable de la génération des différentes sections de l'article.
    """

    # ============================================================================
    # INITIALISATION
    # ============================================================================
    def __init__(self):
        self.article_util = ArticleFormatter()

    # ============================================================================
    # MÉTHODE PRINCIPALE
    # ============================================================================
    def compose_star_content(self, star: Star, exoplanet: Exoplanet) -> str:
        """
        Génère l'ensemble du contenu de l'article pour une étoile.
        """
        sections: list[str] = [
            self.build_physical_section(star),
            self.build_observation_section(star),
            # self.build_environment_section(star),
            # self.write_history_paragraph(star),
            self.build_exoplanets_section(star, exoplanet),
        ]

        # Filtrer les sections vides et les combiner
        return "\n\n".join(filter(None, sections))

    # ============================================================================
    # GÉNÉRATION DES SECTIONS DE CONTENU
    # ============================================================================

    # --- CARACTÉRISTIQUES PHYSIQUES ---
    def build_physical_section(self, star: Star) -> str:
        """
        Génère la section des caractéristiques physiques de l'étoile.
        """
        if not any(
            [
                star.st_spectral_type,
                star.st_temperature,
                star.st_mass,
                star.st_radius,
                star.st_luminosity,
            ]
        ):
            return ""

        content: list[str] = ["== Caractéristiques physiques ==\n"]

        if star.st_spectral_type and star.st_spectral_type:
            content.append(f"Cette étoile est de type spectral {star.st_spectral_type}.")

        if star.st_temperature and star.st_temperature.value:
            temp: str = self.article_util.format_number_as_french_string(star.st_temperature.value)
            content.append(f"Sa température effective est d'environ {temp} [[kelvin|K]].")

        if star.st_mass and star.st_mass.value:
            mass: str = self.article_util.format_number_as_french_string(star.st_mass.value)
            content.append(f"Sa masse est estimée à {mass} fois celle du [[Soleil]].")

        if star.st_radius and star.st_radius.value:
            radius: str = self.article_util.format_number_as_french_string(star.st_radius.value)
            content.append(f"Son rayon est d'environ {radius} fois celui du Soleil.")

        if star.st_luminosity and star.st_luminosity.value:
            lum: str = self.article_util.format_number_as_french_string(star.st_luminosity.value)
            content.append(f"Sa luminosité est d'environ {lum} fois celle du Soleil.")

        return "\n".join(content)

    # --- OBSERVATION ---
    def build_observation_section(self, star: Star) -> str:
        """
        Génère la section sur l'observation de l'étoile.
        """
        if not any([star.st_apparent_magnitude, star.st_right_ascension, star.st_declination]):
            return ""

        content: list[str] = ["== Observation ==\n"]

        if star.st_apparent_magnitude and star.st_apparent_magnitude.value:
            mag: str = self.article_util.format_number_as_french_string(star.st_magnitude.value)
            content.append(f"Sa magnitude apparente est de {mag}.")

        if star.st_right_ascension and star.st_declination:
            ra: str = star.st_right_ascension
            dec: str = star.st_declination

            ra_parts = ra.split("/")
            ra_str = f"{{{{ascension droite|{ra_parts[0]}|{ra_parts[1]}|{ra_parts[2].replace('.', ',')}}}}}"
            dec_parts = dec.split("/")
            dec_str = f"{{{{déclinaison|{dec_parts[0]}|{dec_parts[1]}|{dec_parts[2].replace('.', ',')}}}}}"
            content.append(
                f"Ses [[coordonnées célestes]] sont : [[ascension droite]] {ra_str}, [[Déclinaison (astronomie)|déclinaison]] {dec_str}."
            )

        return "\n".join(content)

    # --- ENVIRONNEMENT STELLAIRE ---
    def build_environment_section(self, star: Star) -> str:
        """
        Génère la section sur l'environnement stellaire.
        """
        if not any([star.sy_constellation, star.st_distance]):
            return ""

        content: list[str] = ["== Environnement stellaire ==\n"]
        if star.sy_constellation:
            str_constellation = phrase_dans_constellation(star.sy_constellation, True)
            content.append(f"L'étoile se trouve {str_constellation}.")

        if star.st_distance:
            dist_val = float(star.st_distance.value)
            formatted = f"{dist_val:.2f}"
            content.append(
                f"Elle est située à environ {{{{unité|{formatted}|[[parsec]]s}}}} de la [[Terre]]."
            )

        return "\n".join(content)

    # --- HISTOIRE ---
    def write_history_paragraph(self, star: Star) -> str:
        """
        Génère la section historique de l'étoile.
        """
        if not star.st_name:
            return ""

        content = ["== Histoire ==\n"]
        content.append(
            f"L'étoile {star.st_name} a été découverte et cataloguée dans le cadre des observations astronomiques modernes."
        )

        return "\n".join(content)

    # --- SYSTEM PLANETAIRE ---
    def build_exoplanets_section(self, star: Star, exoplanets: list[Exoplanet]) -> str:
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
            if exoplanet.pl_semi_major_axis and exoplanet.pl_semi_major_axis.value is not None:
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
            if exoplanet.pl_orbital_period and exoplanet.pl_orbital_period.value is not None:
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
            if exoplanet.pl_eccentricity and exoplanet.pl_eccentricity.value is not None:
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

    def _format_uncertainty(
        self,
        value: float,
        error_positive: float | None,
        error_negative: float | None,
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
