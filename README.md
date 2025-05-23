# AstroWikiBuilder

Un outil Python pour collecter des données astronomiques (exoplanètes, étoiles) à partir de catalogues en ligne et générer des projets d'articles bien sourcés pour Wikipédia en français.

## Installation

1. Clonez le dépôt :

```bash
git clone https://github.com/votre-username/AstroWikiBuilder.git
cd AstroWikiBuilder
```

2. Créez un environnement virtuel et installez les dépendances :

```bash
python -m venv venv
source venv/bin/activate  # Sur Windows : venv\Scripts\activate
pip install -r requirements.txt
```

## Structure du Projet

```
AstroWikiBuilder/
├── src/
│   ├── data_collectors/     # Collecteurs de données pour différentes sources
│   ├── models/             # Modèles de données
│   ├── services/          # Services de gestion des données et génération
│   ├── utils/             # Utilitaires et générateurs
│   └── main.py           # Point d'entrée principal
├── data/                  # Données téléchargées et mock data
├── output/               # Données consolidées et exports
├── drafts/              # Projets d'articles générés
└── requirements.txt     # Dépendances Python
```

## Fonctionnalités

### Collecte et Consolidation des Données

- Collecte automatique depuis plusieurs sources :
  - NASA Exoplanet Archive
  - The Extrasolar Planets Encyclopaedia
  - Open Exoplanet Catalogue
- Consolidation intelligente des données
- Gestion des références et des sources
- Export des données en CSV et JSON

### Génération d'Articles Wikipedia

- Vérification automatique des articles existants
- Génération de projets d'articles complets incluant :
  - Infobox détaillée
  - Introduction
  - Caractéristiques physiques
  - Orbite
  - Découverte
  - Habitabilité
  - Notes et références
- Support multilingue (articles en français)
- Gestion automatique des références et notes
- Classification des planètes selon les standards Wikipedia

## Utilisation

1. Collecte et consolidation des données :

```bash
python src/main.py --collect
```

Le script va :

- Collecter les données des sources
- Consolider les données en gérant les doublons
- Exporter les données consolidées en CSV et JSON dans `output/`
- Afficher des statistiques sur les données collectées

2. Génération d'articles :

```bash
python src/main.py --generate
```

Le script va :

- Vérifier les articles existants sur Wikipedia
- Générer des projets d'articles pour les exoplanètes sans article
- Sauvegarder les projets dans le dossier `drafts/`
- Exporter les statistiques sur les articles existants/missing

## Sources de Données

1. NASA Exoplanet Archive (https://exoplanetarchive.ipac.caltech.edu/)

   - Accès via API TAP
   - Données sur les exoplanètes confirmées et leurs étoiles hôtes

2. The Extrasolar Planets Encyclopaedia (https://exoplanet.eu/)

   - Données via fichier CSV téléchargé
   - Informations complémentaires sur les exoplanètes

3. Open Exoplanet Catalogue (https://www.openexoplanetcatalogue.com/)
   - Données via fichier XML compressé
   - Catalogue open source d'exoplanètes

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :

1. Fork le projet
2. Créer une branche pour votre fonctionnalité
3. Commiter vos changements
4. Pousser vers la branche
5. Ouvrir une Pull Request

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.
