# CI/CD Pipeline - Guide

## 📋 Vue d'ensemble

Le projet AstroWikiBuilder utilise **GitHub Actions** pour automatiser la vérification de la qualité du code, les tests, et l'analyse de sécurité à chaque push ou pull request.

## 🔧 Fichiers de configuration

### 1. `.github/workflows/tests.yml`
C'est le **fichier principal** du CI/CD. Il définit deux jobs :

#### Job 1 : `quality-checks` (Vérifications de qualité)
- ✅ **Ruff** : Linter Python (vérifie le style et le formatage)
- ✅ **Bandit** : Audit de sécurité (détecte les vulnérabilités)
- ✅ **Radon** : Analyse de complexité (complexité cyclomatique et maintenabilité)

#### Job 2 : `test` (Tests)
- ✅ Lance tous les tests avec **pytest**
- ✅ Génère un rapport de couverture
- ✅ Upload les résultats vers **Codecov** (optionnel)
- ✅ Commente la couverture sur les Pull Requests

### 2. `.pre-commit-config.yaml`
Hooks Git qui s'exécutent **avant chaque commit** :
- Ruff (linting et formatting)
- Bandit (security)
- MyPy (type checking - désactivé pour l'instant)

### 3. `pyproject.toml`
Configuration centralisée pour tous les outils :
- Poetry (dépendances)
- Ruff, Bandit, MyPy, Pytest

### 4. `Makefile`
Commandes simplifiées pour le développement local

## 🚀 Workflow de développement

### Avant de committer
```bash
make format    # Formate le code automatiquement
make lint      # Vérifie style + sécurité
make test      # Lance les tests
```

Ou en une seule commande :
```bash
make check     # Fait tout d'un coup
```

### Lors du commit
Les **pre-commit hooks** s'exécutent automatiquement et bloquent le commit si :
- Le code n'est pas formaté (Ruff)
- Il y a des erreurs de linting (Ruff)
- Des failles de sécurité sont détectées (Bandit)

### Lors du push
GitHub Actions s'exécute automatiquement et :
1. Vérifie la qualité du code
2. Lance tous les tests
3. Génère un rapport de couverture
4. Commente sur la PR (si applicable)

## 📊 Badges dans le README

Les badges affichent l'état du projet :
- **CI/CD Pipeline** : ✅ Passing / ❌ Failing
- **Python Version** : 3.13
- **Code Coverage** : 86%
- **Code Quality** : A (Radon)
- **Security** : Passing (Bandit)

## 🔐 Secrets GitHub (optionnel)

Pour activer Codecov, ajoute ce secret dans GitHub :
1. Va sur https://codecov.io et connecte ton repo
2. Copie le token
3. Dans GitHub : Settings → Secrets → New repository secret
4. Nom : `CODECOV_TOKEN`
5. Valeur : ton token

## 🛠️ Personnalisation

### Modifier les seuils de couverture
Dans `.github/workflows/tests.yml` :
```yaml
MINIMUM_GREEN: 80   # Couverture "verte"
MINIMUM_ORANGE: 70  # Couverture "orange"
```

### Ajouter des vérifications
Édite `.github/workflows/tests.yml` et ajoute des steps dans le job `quality-checks`.

### Désactiver un outil
Commente la ligne correspondante dans :
- `Makefile` (pour le développement local)
- `.github/workflows/tests.yml` (pour la CI)
- `.pre-commit-config.yaml` (pour les hooks Git)

## 📈 Analyse de complexité

Radon génère deux métriques :

### Complexité cyclomatique (CC)
- **A** : Simple (CC 1-5)
- **B** : Peu complexe (CC 6-10)
- **C** : Modérément complexe (CC 11-20)
- **D** : Complexe (CC 21-30)
- **E** : Très complexe (CC 31-40)
- **F** : Extrêmement complexe (CC 41+)

**Objectif** : Garder toutes les fonctions en A ou B

### Indice de maintenabilité (MI)
- **A** : 20-100 (Très maintenable)
- **B** : 10-19 (Maintenable)
- **C** : 0-9 (Difficile à maintenir)

**Objectif** : Tous les fichiers en A

## 🎯 Résumé

Quand tu push sur GitHub :
1. ✅ Le code est vérifié (Ruff)
2. ✅ La sécurité est auditée (Bandit)
3. ✅ La complexité est analysée (Radon)
4. ✅ Les tests sont lancés (Pytest)
5. ✅ La couverture est calculée
6. ✅ Les résultats sont commentés sur la PR

**Tout est automatique !** 🎉
