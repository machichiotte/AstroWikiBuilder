# src/generators/articles/star/sections/content_section.py

from src.models.entities.exoplanet_entity import Exoplanet
from src.models.entities.star_entity import Star
from src.utils.formatters.article_formatter import ArticleFormatter
from src.utils.lang.phrase.constellation import phrase_dans_constellation


class ContentSection:
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
    def _add_spectral_type(self, star: Star, content: list[str]) -> None:
        if star.st_spectral_type:
            content.append(f"Cette étoile est de type spectral {star.st_spectral_type}.")

    def _add_temperature(self, star: Star, content: list[str]) -> None:
        if star.st_temperature and star.st_temperature.value:
            temp: str = self.article_util.format_number_as_french_string(star.st_temperature.value)
            content.append(f"Sa température effective est d'environ {temp} [[kelvin|K]].")

    def _add_mass(self, star: Star, content: list[str]) -> None:
        if star.st_mass and star.st_mass.value:
            mass: str = self.article_util.format_number_as_french_string(star.st_mass.value)
            content.append(f"Sa masse est estimée à {mass} fois celle du [[Soleil]].")

    def _add_radius(self, star: Star, content: list[str]) -> None:
        if star.st_radius and star.st_radius.value:
            radius: str = self.article_util.format_number_as_french_string(star.st_radius.value)
            content.append(f"Son rayon est d'environ {radius} fois celui du Soleil.")

    def _add_luminosity(self, star: Star, content: list[str]) -> None:
        if star.st_luminosity and star.st_luminosity.value:
            lum: str = self.article_util.format_number_as_french_string(star.st_luminosity.value)
            content.append(f"Sa luminosité est d'environ {lum} fois celle du Soleil.")

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

        self._add_spectral_type(star, content)
        self._add_temperature(star, content)
        self._add_mass(star, content)
        self._add_radius(star, content)
        self._add_luminosity(star, content)

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
    def _format_field_with_uncertainty(self, value_obj) -> str:
        """Helper to format a value with its uncertainty."""
        if value_obj and value_obj.value is not None:
            try:
                val = float(value_obj.value)
                return self._format_uncertainty(
                    val,
                    value_obj.error_positive,
                    value_obj.error_negative,
                )
            except (ValueError, TypeError):
                pass
        return ""

    def _generate_planet_template(self, exoplanet: Exoplanet) -> str:
        """Génère le template Wiki pour une exoplanète donnée."""
        pl_name: str = exoplanet.pl_name
        template = "{{Système planétaire\n"
        template += f"| exoplanète = [[{pl_name}]]\n"

        # Masse
        mass_str = self._format_field_with_uncertainty(exoplanet.pl_mass)
        template += f"| masse = {mass_str}\n"

        # Rayon
        radius_str = self._format_field_with_uncertainty(exoplanet.pl_radius)
        template += f"| rayon = {radius_str}\n"

        # Demi-grand axe
        axis_str = self._format_field_with_uncertainty(exoplanet.pl_semi_major_axis)
        template += f"| demi grand axe = {axis_str}\n"

        # Période
        period_str = ""
        if exoplanet.pl_orbital_period and exoplanet.pl_orbital_period.value is not None:
            try:
                period = float(exoplanet.pl_orbital_period.value)
                if period.is_integer():
                    period_str = f"{int(period)}"
                else:
                    period_str = f"{period:.2f}"
            except (ValueError, TypeError):
                pass
        template += f"| période = {period_str}\n"

        # Excentricité
        ecc_str = ""
        if exoplanet.pl_eccentricity and exoplanet.pl_eccentricity.value is not None:
            try:
                ecc = float(exoplanet.pl_eccentricity.value)
                ecc_str = f"{ecc:.3f}"
            except (ValueError, TypeError):
                pass
        template += f"| excentricité = {ecc_str}\n"

        # Inclinaison
        incl_str = self._format_field_with_uncertainty(exoplanet.pl_inclination)
        template += f"| inclinaison = {incl_str}\n"

        template += "}}\n"
        return template

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
            section += self._generate_planet_template(exoplanet)

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
