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
│   ├── utils/              # Utilitaires
│   └── main.py            # Point d'entrée principal
├── data/                   # Données téléchargées (ex: exoplanet_eu.csv)
├── output/                 # Données consolidées exportées
└── requirements.txt        # Dépendances Python
```

## Utilisation

1. Placez votre fichier CSV d'Exoplanet.eu dans le dossier `data/` (nommé `exoplanet_eu.csv`)

2. Exécutez le script principal :

```bash
python src/main.py
```

Le script va :

- Collecter les données des trois sources (NASA Exoplanet Archive, Exoplanet.eu, Open Exoplanet Catalogue)
- Consolider les données en gérant les doublons
- Exporter les données consolidées en CSV et JSON dans le dossier `output/`
- Afficher des statistiques sur les données collectées

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
