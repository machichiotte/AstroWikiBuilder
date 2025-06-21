#!/usr/bin/env python3
"""
Script de test pour vérifier le post-traitement des références.
"""

import sys
import os
import traceback

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime
from src.models.entities.star import Star
from src.models.entities.exoplanet import Exoplanet
from src.models.references.reference import Reference, SourceType
from src.models.entities.nea_entity import ValueWithUncertainty
from src.generators.star.article_star_generator import ArticleStarGenerator
from src.generators.exoplanet.article_exoplanet_generator import (
    ArticleExoplanetGenerator,
)


def create_test_star() -> Star:
    """Crée une étoile de test avec une référence."""
    print("Création d'une étoile de test...")
    reference = Reference(
        source=SourceType.NEA,
        update_date=datetime.now(),
        consultation_date=datetime.now(),
        star_id="HD 209458",
    )

    star = Star(
        st_name="HD 209458",
        st_spectral_type="G0V",
        sy_constellation="Pégase",
        st_distance=ValueWithUncertainty(
            value=47.1, error_positive=0.5, error_negative=0.5
        ),
        reference=reference,
    )
    print(f"Étoile créée: {star.st_name}")
    return star


def create_test_exoplanet() -> Exoplanet:
    """Crée une exoplanète de test avec une référence."""
    print("Création d'une exoplanète de test...")
    reference = Reference(
        source=SourceType.NEA,
        update_date=datetime.now(),
        consultation_date=datetime.now(),
        star_id="HD 209458",
        planet_id="HD 209458 b",
    )

    exoplanet = Exoplanet(
        pl_name="HD 209458 b",
        pl_mass=ValueWithUncertainty(
            value=0.69, error_positive=0.05, error_negative=0.05
        ),
        pl_radius=ValueWithUncertainty(
            value=1.35, error_positive=0.05, error_negative=0.05
        ),
        pl_orbital_period=ValueWithUncertainty(
            value=3.5247, error_positive=0.0001, error_negative=0.0001
        ),
        reference=reference,
    )
    print(f"Exoplanète créée: {exoplanet.pl_name}")
    return exoplanet


def test_star_references():
    """Teste le post-traitement des références pour les étoiles."""
    print("=== Test des références pour les étoiles ===")

    try:
        star = create_test_star()
        generator = ArticleStarGenerator()

        # Générer l'article
        print("Génération de l'article...")
        content = generator.compose_article_content(star)
        print(f"Article généré, longueur: {len(content)} caractères")

        # Vérifier que la première référence est complète
        if '<ref name="NEA">' in content and "{{Lien web" in content:
            print("✅ Première référence complète trouvée")
        else:
            print("❌ Première référence complète non trouvée")

        # Vérifier qu'il n'y a pas de références simples restantes
        if '<ref name="NEA" />' in content:
            print(
                "❌ Références simples trouvées (ne devrait pas y en avoir pour une seule référence)"
            )
        else:
            print("✅ Aucune référence simple trouvée (correct)")

        print(f"Nombre total de références NEA: {content.count('NEA')}")

        # Afficher un extrait du contenu pour debug
        print("Extrait du contenu (premiers 500 caractères):")
        print(content[:500])
        print()

    except Exception as e:
        print(f"❌ Erreur lors du test des étoiles: {e}")
        traceback.print_exc()


def test_exoplanet_references():
    """Teste le post-traitement des références pour les exoplanètes."""
    print("=== Test des références pour les exoplanètes ===")

    try:
        exoplanet = create_test_exoplanet()
        generator = ArticleExoplanetGenerator()

        # Générer l'article
        print("Génération de l'article...")
        content = generator.compose_exoplanet_article(exoplanet)
        print(f"Article généré, longueur: {len(content)} caractères")

        # Vérifier que la première référence est complète
        if '<ref name="NEA">' in content and "{{Lien web" in content:
            print("✅ Première référence complète trouvée")
        else:
            print("❌ Première référence complète non trouvée")

        # Vérifier qu'il n'y a pas de références simples restantes
        if '<ref name="NEA" />' in content:
            print(
                "❌ Références simples trouvées (ne devrait pas y en avoir pour une seule référence)"
            )
        else:
            print("✅ Aucune référence simple trouvée (correct)")

        print(f"Nombre total de références NEA: {content.count('NEA')}")

        # Afficher un extrait du contenu pour debug
        print("Extrait du contenu (premiers 500 caractères):")
        print(content[:500])
        print()

    except Exception as e:
        print(f"❌ Erreur lors du test des exoplanètes: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    print("Démarrage des tests...")
    test_star_references()
    test_exoplanet_references()
    print("Tests terminés !")
