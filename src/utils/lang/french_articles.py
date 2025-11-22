# src/utils/lang/french_articles.py


def starts_with_vowel_or_silent_h(word: str) -> bool:
    return word[0].lower() in "aeiouyhéèêàâîïùü"


def guess_grammatical_gender(type_description: str) -> str:
    """
    Essaie de deviner le genre grammatical d'un type d'étoile.
    """
    feminine_keywords = ["naine", "étoile", "géante", "brune"]
    masculine_keywords = ["nain", "géant", "sous-nain", "subdwarf"]

    for f in feminine_keywords:
        if f in type_description:
            return "f"
    for m in masculine_keywords:
        if m in type_description:
            return "m"
    return "?"  # inconnu


def _get_indefinite_article(gender: str) -> str:
    if gender == "f":
        return "une"
    elif gender == "m":
        return "un"
    return "un(e)"


def _get_preposition_de_article(gender: str, elision: bool) -> str:
    if elision:
        return "de l'"
    elif gender == "f":
        return "de la"
    elif gender == "m":
        return "du"
    return "de"


def _get_preposition_dans_article(gender: str, elision: bool) -> str:
    if elision:
        return "dans l'"
    elif gender == "f":
        return "dans la"
    elif gender == "m":
        return "dans le"
    return "dans la"


def get_french_article(
    gender: str,
    definite: bool = True,
    preposition: str | None = "de",
    noun: str | None = None,
) -> str:
    """
    Retourne juste l'article correct (ex : "de la", "du", "de l'", etc.)
    Si noun est fourni, gère l'élision.
    """
    elision = False
    if noun:
        noun = noun.strip()
        elision = starts_with_vowel_or_silent_h(noun)

    if not definite:
        return _get_indefinite_article(gender)

    if preposition == "de":
        return _get_preposition_de_article(gender, elision)

    if preposition == "dans":
        return _get_preposition_dans_article(gender, elision)

    return f"{preposition}"


def format_noun(noun: str, with_brackets: bool = False) -> str:
    noun = noun.strip()
    if with_brackets:
        return f"[[{noun}]]"
    return noun


def get_french_article_noun(
    noun: str,
    gender: str,
    definite: bool = True,
    preposition: str | None = "de",
    with_brackets: bool = False,
) -> str:
    """
    Combine l'article et le nom, avec ou sans crochets.
    Exemples :
    - de la [[géante rouge]]
    - du [[Soleil]]
    - de l'étoile
    - dans la constellation de la Lyre
    """
    article = get_french_article(gender, definite, preposition, noun)
    noun_formatted = format_noun(noun, with_brackets)
    # Gère l'élision (pas d'espace après l')
    if article.endswith("'"):
        return f"{article}{noun_formatted}"
    else:
        return f"{article} {noun_formatted}"
