from src.models.entities.star_entity import Star
from src.utils.formatters.article_formatter import ArticleFormatter


class PhysicalCharacteristicsSection:
    """
    Génère la section des caractéristiques physiques de l'étoile.
    """

    def __init__(self, article_util: ArticleFormatter):
        self.article_util = article_util

    def generate(self, star: Star) -> str:
        """
        Génère le contenu de la section.
        """
        if not any(
            [
                star.st_spectral_type,
                star.st_temperature,
                star.st_mass,
                star.st_radius,
                star.st_luminosity,
                star.st_density,
            ]
        ):
            return ""

        content: list[str] = ["== Caractéristiques physiques ==\n"]

        # Vérifier si c'est un système multiple
        is_multiple_system = star.sy_star_count and star.sy_star_count > 1

        if is_multiple_system:
            # Pour les systèmes multiples, format liste
            content.append("Les étoiles composant ce système sont :\n")
            self._add_component_description(star, "A", content)

            # Si des données pour la composante B existent
            if self._has_component_b_data(star):
                self._add_component_description(star, "B", content)
        else:
            # Pour les étoiles simples, format classique
            self._add_spectral_type(star, content)
            self._add_temperature(star, content)
            self._add_mass(star, content)
            self._add_radius(star, content)
            self._add_density(star, content)
            self._add_luminosity(star, content)
            self._add_metallicity(star, content)
            self._add_surface_gravity(star, content)
            self._add_age(star, content)

        return "\n".join(content)

    def _add_spectral_type(self, star: Star, content: list[str]) -> None:
        if star.st_spectral_type:
            content.append(f"Cette étoile est de type spectral {star.st_spectral_type}.")

    def _add_temperature(self, star: Star, content: list[str]) -> None:
        if star.st_temperature and star.st_temperature.value is not None:
            temp: str = self.article_util.format_number_as_french_string(star.st_temperature.value)
            content.append(f"Sa température effective est d'environ {temp} [[kelvin|K]].")

    def _add_mass(self, star: Star, content: list[str]) -> None:
        if star.st_mass and star.st_mass.value is not None:
            mass: str = self.article_util.format_number_as_french_string(star.st_mass.value)
            content.append(f"Sa masse est estimée à {mass} fois celle du [[Soleil]].")

    def _add_radius(self, star: Star, content: list[str]) -> None:
        if star.st_radius and star.st_radius.value is not None:
            radius: str = self.article_util.format_number_as_french_string(star.st_radius.value)
            content.append(f"Son rayon est d'environ {radius} fois celui du Soleil.")

    def _add_density(self, star: Star, content: list[str]) -> None:
        if star.st_density and star.st_density.value is not None:
            density: str = self.article_util.format_number_as_french_string(star.st_density.value)
            content.append(f"Sa densité moyenne est d'environ {density} g/cm³.")

    def _add_luminosity(self, star: Star, content: list[str]) -> None:
        if star.st_luminosity and star.st_luminosity.value is not None:
            lum: str = self.article_util.format_number_as_french_string(star.st_luminosity.value)
            content.append(f"Sa luminosité est d'environ {lum} fois celle du Soleil.")

    def _add_metallicity(self, star: Star, content: list[str]) -> None:
        if star.st_metallicity and star.st_metallicity.value is not None:
            met: str = self.article_util.format_number_as_french_string(star.st_metallicity.value)
            content.append(f"Sa métallicité est estimée à [Fe/H] = {met}.")

    def _add_surface_gravity(self, star: Star, content: list[str]) -> None:
        if star.st_surface_gravity and star.st_surface_gravity.value is not None:
            logg: str = self.article_util.format_number_as_french_string(
                star.st_surface_gravity.value
            )
            content.append(f"Sa gravité de surface (log g) est de {logg}.")

    def _add_age(self, star: Star, content: list[str]) -> None:
        if star.st_age and star.st_age.value is not None:
            age: str = self.article_util.format_number_as_french_string(star.st_age.value)
            content.append(f"L'âge de l'étoile est estimé à environ {age} milliards d'années.")

    def _has_component_b_data(self, star: Star) -> bool:
        """Vérifie si des données existent pour la composante B."""
        return any(
            [star.st_mass_2, star.st_radius_2, star.st_temperature_2, star.st_spectral_type_2]
        )

    def _add_component_description(self, star: Star, component: str, content: list[str]) -> None:
        """Génère la description d'une composante stellaire."""
        star_name = star.st_name if star.st_name else "L'étoile"

        # Déterminer le type d'étoile
        star_type = self._get_star_type_description(star, component)

        # Construire la description
        desc_parts = []

        if component == "A":
            if star.st_mass and star.st_mass.value is not None:
                mass = self.article_util.format_number_as_french_string(star.st_mass.value)
                desc_parts.append(f"{{{{unité|{mass}|[[masse solaire]]}}}}")

            if star.st_radius and star.st_radius.value is not None:
                radius = self.article_util.format_number_as_french_string(star.st_radius.value)
                desc_parts.append(f"{{{{unité|{radius}|[[rayon solaire]]}}}}")

        elif component == "B":
            if star.st_mass_2 and star.st_mass_2.value is not None:
                mass = self.article_util.format_number_as_french_string(star.st_mass_2.value)
                desc_parts.append(f"{{{{unité|{mass}|masse solaire}}}}")

            if star.st_radius_2 and star.st_radius_2.value is not None:
                radius = self.article_util.format_number_as_french_string(star.st_radius_2.value)
                desc_parts.append(f"{{{{unité|{radius}|rayon solaire}}}}")

        # Assembler la description
        if desc_parts:
            desc_text = " et ".join(desc_parts)
            content.append(
                f"* '''{{{{nobr|{star_name} {component}}}}}''', {star_type} d'environ {desc_text} ;"
            )
        else:
            content.append(f"* '''{{{{nobr|{star_name} {component}}}}}''', {star_type} ;")

    def _get_star_type_description(self, star: Star, component: str) -> str:
        """Retourne une description du type d'étoile."""
        if component == "A":
            spectral = star.st_spectral_type
        else:
            spectral = star.st_spectral_type_2

        if not spectral:
            return "étoile"

        # Déterminer le type basé sur la classe spectrale
        spectral_str = str(spectral).upper()

        if spectral_str.startswith("O") or spectral_str.startswith("B"):
            return "étoile chaude"
        elif spectral_str.startswith("A") or spectral_str.startswith("F"):
            return "étoile blanche"
        elif spectral_str.startswith("G"):
            return "[[naine jaune]]"
        elif spectral_str.startswith("K"):
            return "[[naine orange]]"
        elif spectral_str.startswith("M"):
            return "[[naine rouge]]"
        else:
            return "étoile"
