from src.constants.field_mappings import CONSTELLATION_GENDER
from src.utils.lang.french_articles import get_french_article_noun


def get_constellation_article(name: str) -> str:
    """
    Renvoie l'article défini précédé de 'de' : 'du ', 'de la ', 'de l''.
    """
    gender = CONSTELLATION_GENDER.get(name, "m")
    return get_french_article_noun(
        name, gender=gender, preposition="de", with_brackets=True
    )


def phrase_de_la_constellation(name: str) -> str:
    return get_constellation_article(name)


def phrase_dans_constellation(name: str) -> str:
    return f"dans la constellation {get_constellation_article(name)}"


def phrase_situee_dans_constellation(name: str) -> str:
    return f"située dans la constellation {get_constellation_article(name)}"
