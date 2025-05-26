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
├── data/                  # Données téléchargées et mises en cache, et mock data (ex: data/exoplanet_eu_downloaded.csv)
├── output/               # Données consolidées et exports (configurable via --output-dir)
├── drafts/              # Projets d'articles générés (configurable via --drafts-dir)
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
- Mise en cache locale des données téléchargées pour éviter les téléchargements répétitifs.
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

Le script principal `src/main.py` est utilisé pour toutes les opérations. Voici les options de base :

```bash
python src/main.py --sources <source1> [<source2>...] [--use-mock <source1> [<source2>...]] [--skip-wikipedia-check] [--output-dir CHEMIN] [--drafts-dir CHEMIN]
```

**Arguments principaux :**

-   `--sources`: Spécifie les sources de données à utiliser. Choix possibles : `nasa`, `exoplanet_eu`, `open_exoplanet`. Par défaut : `nasa`.
    Exemple : `python src/main.py --sources nasa exoplanet_eu`
-   `--use-mock`: Utilise les données mockées pour les sources spécifiées au lieu de les télécharger. Les fichiers mock doivent être présents dans le répertoire `data/` (par exemple, `data/nasa_mock_data_complete.csv`, `data/exoplanet_eu_mock.csv`).
    Exemple : `python src/main.py --sources exoplanet_eu --use-mock exoplanet_eu`
-   `--skip-wikipedia-check`: Ignore l'étape de vérification des articles Wikipedia existants et la génération de brouillons. Utile si vous souhaitez uniquement collecter et consolider les données.

**Exemples de commandes :**

1.  Collecter et consolider les données de toutes les sources disponibles :
    ```bash
    python src/main.py --sources nasa exoplanet_eu open_exoplanet
    ```
    Les données téléchargées seront mises en cache dans le répertoire `data/`. Les données consolidées et les statistiques seront sauvegardées dans le répertoire `output/` (par défaut).

2.  Générer des brouillons d'articles pour les données collectées (implique la collecte si non faite) :
    ```bash
    python src/main.py --sources nasa exoplanet_eu open_exoplanet
    ```
    (Note : Actuellement, il n'y a pas d'argument distinct comme `--generate`. La génération de brouillons est un processus qui suit la collecte de données si `--skip-wikipedia-check` n'est pas utilisé.)

3.  Utiliser des données mockées pour une source spécifique et spécifier des répertoires de sortie personnalisés :
    ```bash
    python src/main.py --sources nasa --use-mock nasa --output-dir my_custom_output --drafts-dir my_custom_drafts
    ```

**Options supplémentaires :**

-   `--output-dir CHEMIN`: Spécifie le répertoire de sortie principal pour les données consolidées, les logs, etc. (défaut: `output`).
-   `--drafts-dir CHEMIN`: Spécifie le répertoire pour les brouillons d'articles Wikipedia générés (défaut: `drafts`).

## Configuration

### User-Agent Wikipedia

Pour les requêtes à l'API Wikipedia, il est recommandé de définir un User-Agent personnalisé. Vous pouvez le faire en définissant la variable d'environnement `WIKI_USER_AGENT`.

**Objectif :** Permet à Wikipedia d'identifier votre script/bot. Il est important de fournir un moyen de vous contacter si votre script cause des problèmes.

**Comment définir :**
Sur Linux/macOS :
```bash
export WIKI_USER_AGENT="MonBotAstroWiki/1.0 (monemail@example.com ou https://github.com/monprofil/AstroWikiBuilder)"
```
Sur Windows (Command Prompt) :
```bash
set WIKI_USER_AGENT=MonBotAstroWiki/1.0 (monemail@example.com ou https://github.com/monprofil/AstroWikiBuilder)
```
Ou dans PowerShell :
```bash
$env:WIKI_USER_AGENT="MonBotAstroWiki/1.0 (monemail@example.com ou https://github.com/monprofil/AstroWikiBuilder)"
```

**Valeur par défaut :** Si cette variable n'est pas définie, le script utilisera la valeur par défaut : `'AstroWikiBuilder/1.1 (bot; machichiotte@gmail.com or your_project_contact_page)'`. Il est fortement recommandé de la personnaliser.

## Sources de Données

1.  **NASA Exoplanet Archive** (https://exoplanetarchive.ipac.caltech.edu/)
    -   Accès via API TAP (Table Access Protocol).
    -   Données sur les exoplanètes confirmées et leurs étoiles hôtes.
    -   Les données mockées peuvent être utilisées avec `--use-mock nasa` (ex: `data/nasa_mock_data_complete.csv`).

2.  **The Extrasolar Planets Encyclopaedia** (http://exoplanet.eu/)
    -   Données via un fichier CSV téléchargé depuis le site exoplanet.eu et mis en cache localement (par ex., dans `data/exoplanet_eu_downloaded.csv`).
    -   Fournit des informations complémentaires sur les exoplanètes.
    -   Les données mockées peuvent être utilisées avec `--use-mock exoplanet_eu` (ex: `data/exoplanet_eu_mock.csv`).

3.  **Open Exoplanet Catalogue** (http://www.openexoplanetcatalogue.com/)
    -   Données via un fichier texte (CSV-like) téléchargé depuis le dépôt GitHub du catalogue (OpenExoplanetCatalogue/oec_tables) et mis en cache localement (par ex., dans `data/open_exoplanet_downloaded.txt`).
    -   Catalogue open source d'exoplanètes.
    -   Les données mockées peuvent être utilisées avec `--use-mock open_exoplanet` (ex: `data/open_exoplanet_mock.csv`).

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :

1. Fork le projet
2. Créer une branche pour votre fonctionnalité
3. Commiter vos changements
4. Pousser vers la branche
5. Ouvrir une Pull Request

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.
