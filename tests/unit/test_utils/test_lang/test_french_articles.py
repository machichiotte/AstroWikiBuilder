from src.utils.lang.french_articles import (
    format_noun,
    get_french_article,
    get_french_article_noun,
    guess_grammatical_gender,
    starts_with_vowel_or_silent_h,
)


class TestFrenchArticles:
    def test_starts_with_vowel_or_silent_h(self):
        # Voyelles
        assert starts_with_vowel_or_silent_h("avion") is True
        assert starts_with_vowel_or_silent_h("Etoile") is True
        assert starts_with_vowel_or_silent_h("image") is True
        assert starts_with_vowel_or_silent_h("orange") is True
        assert starts_with_vowel_or_silent_h("univers") is True
        assert starts_with_vowel_or_silent_h("yack") is True

        # H muet / aspiré (simplification dans le code actuel : tout h est considéré muet)
        assert starts_with_vowel_or_silent_h("homme") is True
        assert starts_with_vowel_or_silent_h("Hôpital") is True

        # Voyelles accentuées
        assert starts_with_vowel_or_silent_h("étoile") is True
        assert starts_with_vowel_or_silent_h("âme") is True
        assert starts_with_vowel_or_silent_h("île") is True

        # Consonnes
        assert starts_with_vowel_or_silent_h("banane") is False
        assert starts_with_vowel_or_silent_h("Soleil") is False
        assert starts_with_vowel_or_silent_h("planète") is False

    def test_guess_grammatical_gender(self):
        # Féminin
        assert guess_grammatical_gender("naine rouge") == "f"
        assert guess_grammatical_gender("étoile binaire") == "f"
        assert guess_grammatical_gender("géante bleue") == "f"
        assert guess_grammatical_gender("naine brune") == "f"

        # Masculin
        assert guess_grammatical_gender("nain blanc") == "m"  # Si ça existait
        assert guess_grammatical_gender("géant rouge") == "m"
        assert guess_grammatical_gender("sous-nain") == "m"
        assert guess_grammatical_gender("hot subdwarf") == "m"

        # Inconnu
        assert guess_grammatical_gender("trou noir") == "?"
        assert guess_grammatical_gender("pulsar") == "?"
        assert guess_grammatical_gender("") == "?"

    def test_get_french_article_indefinite(self):
        # Indéfini (un/une)
        assert get_french_article("m", definite=False) == "un"
        assert get_french_article("f", definite=False) == "une"
        assert get_french_article("?", definite=False) == "un(e)"

    def test_get_french_article_definite_preposition_de(self):
        # Préposition "de" (du/de la/de l')

        # Masculin
        assert get_french_article("m", definite=True, preposition="de", noun="Soleil") == "du"
        assert get_french_article("m", definite=True, preposition="de", noun="Centaure") == "du"

        # Féminin
        assert get_french_article("f", definite=True, preposition="de", noun="Lune") == "de la"
        assert get_french_article("f", definite=True, preposition="de", noun="Terre") == "de la"

        # Élision (voyelle ou h)
        assert get_french_article("m", definite=True, preposition="de", noun="Océan") == "de l'"
        assert get_french_article("f", definite=True, preposition="de", noun="Étoile") == "de l'"
        assert get_french_article("m", definite=True, preposition="de", noun="Homme") == "de l'"

        # Cas sans nom fourni (pas d'élision possible)
        assert get_french_article("m", definite=True, preposition="de") == "du"
        assert get_french_article("f", definite=True, preposition="de") == "de la"
        assert get_french_article("?", definite=True, preposition="de") == "de"

    def test_get_french_article_definite_preposition_dans(self):
        # Préposition "dans" (dans le/dans la/dans l')

        # Masculin
        assert get_french_article("m", definite=True, preposition="dans", noun="Ciel") == "dans le"

        # Féminin
        assert (
            get_french_article("f", definite=True, preposition="dans", noun="Constellation")
            == "dans la"
        )

        # Élision
        assert (
            get_french_article("m", definite=True, preposition="dans", noun="Espace") == "dans l'"
        )
        assert (
            get_french_article("f", definite=True, preposition="dans", noun="Atmosphère")
            == "dans l'"
        )

        # Cas par défaut / inconnu
        assert get_french_article("?", definite=True, preposition="dans") == "dans la"

    def test_get_french_article_other_preposition(self):
        # Autre préposition (retourne la préposition telle quelle)
        assert get_french_article("m", definite=True, preposition="sur") == "sur"
        assert get_french_article("f", definite=True, preposition="avec") == "avec"
        assert get_french_article("m", definite=True, preposition=None) == "None"

    def test_format_noun(self):
        assert format_noun("Soleil") == "Soleil"
        assert format_noun("  Lune  ") == "Lune"
        assert format_noun("Soleil", with_brackets=True) == "[[Soleil]]"
        assert format_noun("Lune", with_brackets=False) == "Lune"

    def test_get_french_article_noun(self):
        # Combinaison article + nom

        # Masculin
        assert get_french_article_noun("Soleil", "m", preposition="de") == "du Soleil"
        assert (
            get_french_article_noun("Soleil", "m", preposition="de", with_brackets=True)
            == "du [[Soleil]]"
        )

        # Féminin
        assert get_french_article_noun("Lune", "f", preposition="de") == "de la Lune"
        assert (
            get_french_article_noun("Lune", "f", preposition="de", with_brackets=True)
            == "de la [[Lune]]"
        )

        # Élision
        assert get_french_article_noun("Étoile", "f", preposition="de") == "de l'Étoile"
        assert (
            get_french_article_noun("Étoile", "f", preposition="de", with_brackets=True)
            == "de l'[[Étoile]]"
        )

        # Indéfini
        assert get_french_article_noun("planète", "f", definite=False) == "une planète"
        assert get_french_article_noun("monde", "m", definite=False) == "un monde"

        # Dans
        assert (
            get_french_article_noun("constellation", "f", preposition="dans")
            == "dans la constellation"
        )
        assert get_french_article_noun("univers", "m", preposition="dans") == "dans l'univers"
