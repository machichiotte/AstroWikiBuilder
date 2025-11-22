from src.models.entities.star_entity import Star


class HistorySection:
    """
    Génère la section historique de l'étoile.
    """

    def generate(self, star: Star) -> str:
        """
        Génère le contenu de la section.
        """
        if not star.st_name:
            return ""

        content = ["== Histoire ==\n"]
        content.append(
            f"L'étoile {star.st_name} a été découverte et cataloguée dans le cadre des observations astronomiques modernes."
        )

        return "\n".join(content)
