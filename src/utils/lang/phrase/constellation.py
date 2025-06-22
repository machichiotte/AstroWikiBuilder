from src.constants.wikipedia_field_config import CONSTELLATION_GENDER_FR
from src.utils.lang.french_articles import get_french_article_noun


def get_constellation_article(name: str, with_bracket: bool = False) -> str:
    """
    Renvoie l'article défini précédé de 'de' : 'du ', 'de la ', 'de l''.
    """
    gender = CONSTELLATION_GENDER_FR.get(name, "m")
    return get_french_article_noun(
        name, gender=gender, preposition="de", with_brackets=with_bracket
    )


def phrase_de_la_constellation(name: str, with_bracket: bool = False) -> str:
    return get_constellation_article(name, with_bracket)


def phrase_dans_constellation(name: str, with_bracket: bool = False) -> str:
    return f"dans la constellation {get_constellation_article(name, with_bracket=with_bracket)}"


def phrase_situee_dans_constellation(name: str, with_bracket: bool = False) -> str:
    return f"située dans la constellation {get_constellation_article(name, with_bracket=with_bracket)}"
