# Classification des Exoplanètes

Ce document décrit le système de classification des exoplanètes utilisé par AstroWikiBuilder, basé sur les standards scientifiques.

## Sources Scientifiques

### Super-Terre

- **Valencia et al. (2007)** : Définit une Super-Terre comme une planète rocheuse ayant une masse comprise entre **1 et 10 masses terrestres** (M⊕)
- **Fortney et al. (2007)** : Propose une fourchette comprise entre **5 et 10 M⊕**
- **Kepler** : Définit une Super-Terre par son rayon : **1,25 R⊕ < R < 2 R⊕**

### Distinction Super-Terre vs Mini-Neptune

Une distinction critique est faite entre :

- **Super-Terre** : Planète tellurique avec un sol bien défini, **densité ≥ 3.0 g/cm³**
- **Mini-Neptune** : Planète de taille et masse comparables, mais couverte d'une épaisse atmosphère gazeuse, **densité < 3.0 g/cm³**

### Neptune Chaud

Une exoplanète de type Neptune chaud est en orbite près de son étoile parente (< 1 UA), avec :

- Masse comparable à celle d'Uranus ou Neptune (**10-30 M⊕**)
- **Insolation > 20× celle de la Terre**
- Température élevée due à la proximité stellaire

### Neptune Tiède

Une Neptune tiède est une planète géante de glaces qui :

- Reste suffisamment éloignée pour ne pas devenir un Neptune chaud
- **Température comprise entre 200 K et 1000 K**
- Moins massive que les Jupiters mais plus massive que les planètes rocheuses

### Jupiter Chaud

Un Jupiter chaud est une planète géante gazeuse avec :

- **Masse ≥ Jupiter (≈ 318 M⊕)**
- **Température > 1000 K**
- **Jupiter ultra-chaud** : température > 2200 K

## Classification Kepler (par rayon)

| Catégorie          | Rayon (R⊕)      |
| ------------------ | --------------- |
| Taille terrestre   | R < 1.25        |
| Super-Terre        | 1.25 < R < 2.0  |
| Taille neptunienne | 2.0 < R < 6.0   |
| Taille jovienne    | 6.0 < R < 15.0  |
| Très grande taille | 15.0 < R < 22.4 |

## Limites de Classification Implémentées

### Masse (en M⊕)

- **Sous-Terre** : < 0.5
- **Terre** : 0.5 - 2.0
- **Super-Terre** : 1.0 - 10.0
- **Mini-Neptune** : < 10.0 (avec densité < 3.0 g/cm³)
- **Neptune** : 10.0 - 30.0
- **Jupiter** : ≥ 317.8

### Rayon (en R⊕)

- **Sous-Terre** : < 0.8
- **Taille terrestre** : < 1.25
- **Super-Terre** : 1.25 - 2.0
- **Taille neptunienne** : 2.0 - 6.0
- **Taille jovienne** : 6.0 - 15.0
- **Très grande** : 15.0 - 22.4

### Densité (en g/cm³)

- **Rocheuse/tellurique** : ≥ 3.0
- **Géante de glaces** : ≤ 2.5
- **Mini-Neptune** : < 3.0

### Température (en K)

- **Ultra-chaud** : > 2200
- **Chaud** : 1000 - 2200
- **Tiède** : 500 - 1000
- **Neptune tiède** : 200 - 1000

### Insolation (× Terre)

- **Flux élevé** : > 100
- **Neptune chaud** : > 20

## Algorithme de Classification

### 1. Vérification masse + rayon + densité

Si les trois paramètres sont disponibles :

#### Cas 1 : Petite masse (< 10 M⊕) ET petit rayon (< 4 R⊕)

- **Rayon 2-6 R⊕** :
  - Densité ≥ 3.0 → **Super-Terre** (rocheuse dense)
  - Densité < 3.0 → **Mini-Neptune** ou **Neptune chaud/tiède/froid**
- **Rayon 1.25-2 R⊕** :
  - Densité ≥ 3.0 → **Super-Terre** (rocheuse)
  - Densité < 3.0 → **Mini-Neptune** (gazeuse)
- **Rayon < 1.25 R⊕** :
  - Classification terrestre standard (Sous-Terre, Terre, Super-Terre)

#### Cas 2 : Grande masse (≥ 10 M⊕) OU grand rayon (≥ 4 R⊕)

- Classification comme géante (Jupiter, Neptune, etc.)
- Vérification de la densité pour cas particuliers

### 2. Classification des géantes

- **Masse ≥ 318 M⊕** → Jupiter (chaud/tiède/froid selon température)
- **Masse 10-30 M⊕** :
  - Densité ≥ 3.0 → **Super-Terre** (cas rare mais possible)
  - Densité < 3.0 :
    - Masse < 10 M⊕ → **Mini-Neptune**
    - Masse ≥ 10 M⊕ → **Neptune** (chaud/tiède/froid)

### 3. Classification thermique

- **Insolation > 20** → Chaud
- **200 K < T < 1000 K** → Tiède
- **Distance > 1 UA** → Froid

## Exemple : Kepler-81 b

**Données** :

- Masse : 0.05 M_J ≈ 16 M⊕
- Rayon : 0.22 R_J ≈ 2.5 R⊕
- Densité : 6.67 g/cm³
- Température : 635 K
- Insolation : 39.95× Terre

**Classification** :

1. Masse < 10 M⊕ ? **Non** (16 M⊕)
2. Rayon 2-6 R⊕ ? **Oui** (2.5 R⊕) → Taille neptunienne
3. Densité ≥ 3.0 ? **Oui** (6.67 g/cm³) → **Rocheuse**
4. **Résultat : Super-Terre** (planète rocheuse dense malgré le rayon neptunien)

**Ancienne classification incorrecte** : Neptune chaud (ignorait la densité)
**Nouvelle classification correcte** : Super-Terre (prend en compte la densité)
