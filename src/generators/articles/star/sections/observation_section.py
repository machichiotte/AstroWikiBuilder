from src.models.entities.star_entity import Star
from src.utils.formatters.article_formatter import ArticleFormatter


class ObservationSection:
    """
    Génère la section sur l'observation de l'étoile.
    """

    def __init__(self, article_util: ArticleFormatter):
        self.article_util = article_util

    def generate(self, star: Star) -> str:
        """
        Génère le contenu de la section.
        """
        if not any(
            [star.st_apparent_magnitude, star.st_right_ascension, star.st_declination]
        ):
            return ""

        content: list[str] = ["== Observation ==\n"]

        if star.st_apparent_magnitude and star.st_apparent_magnitude.value:
            mag: str = self.article_util.format_number_as_french_string(
                star.st_apparent_magnitude.value
            )
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
