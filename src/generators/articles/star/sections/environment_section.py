from src.models.entities.star_entity import Star
from src.utils.lang.phrase.constellation import phrase_dans_constellation


class EnvironmentSection:
    """
    Génère la section sur l'environnement stellaire.
    """

    def generate(self, star: Star) -> str:
        """
        Génère le contenu de la section.
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
