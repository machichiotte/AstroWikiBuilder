# 📝 Nouvelles Informations à Ajouter dans les Sections Wikipedia

## 🎯 Objectif

Enrichir les articles Wikipedia avec les données disponibles dans NASA Exoplanet Archive mais **actuellement non utilisées**.

---

## 🪐 SECTIONS EXOPLANÈTES

### 1. Section "Découverte" - Enrichissements Possibles

#### Données Disponibles (NEA) mais Non Utilisées

- `disc_locale` - Lieu de découverte (Ground/Space)
- `disc_telescope` - Nom du télescope
- `disc_instrument` - Nom de l'instrument
- `disc_pubdate` - Date de publication de la découverte

#### Phrases à Ajouter

**Exemple actuel** :

> L'exoplanète a été découverte par la méthode des transits en 2009.

**Exemple enrichi** :

> L'exoplanète a été découverte par la méthode des transits en 2009 grâce au **télescope spatial Kepler**, utilisant l'instrument **photomètre Kepler**. La découverte a été publiée le **12 août 2010**.

**Code à ajouter dans `discovery_section.py`** :

```python
# Après la phrase de base sur la méthode et l'année
if exoplanet.disc_telescope:
    section += f" grâce au télescope {exoplanet.disc_telescope}"

if exoplanet.disc_instrument:
    section += f", utilisant l'instrument {exoplanet.disc_instrument}"

if exoplanet.disc_locale:
    if exoplanet.disc_locale == "Space":
        section += " depuis l'espace"
    elif exoplanet.disc_locale == "Ground":
        section += " depuis un observatoire terrestre"

if exoplanet.disc_pubdate:
    section += f". La découverte a été publiée le {format_date(exoplanet.disc_pubdate)}"
```

---

### 2. Section "Caractéristiques Physiques" - Enrichissements Possibles

#### Données Disponibles mais Non Utilisées

- `pl_dens` - Densité planétaire (g/cm³) ✅ **Déjà dans l'entité**
- `pl_rade` - Rayon en unités terrestres
- `pl_masse` - Masse en unités terrestres

#### Phrases à Ajouter

**Exemple actuel** :

> L'exoplanète se distingue par sa masse imposante de 1,2 M_J et son rayon de 1,1 R_J.

**Exemple enrichi** :

> L'exoplanète se distingue par sa masse imposante de 1,2 M*J (\*\*380 M*⊕**) et son rayon de 1,1 R_J (**12,3 R_⊕**), ce qui lui confère une **densité de 1,2 g/cm³\*\*, similaire à celle de Jupiter.

**Code à ajouter dans `physical_characteristics_section.py`** :

```python
# Après masse et rayon
if exoplanet.pl_density and exoplanet.pl_density.value:
    density_value = format_number(exoplanet.pl_density.value)
    section += f", ce qui lui confère une densité de {density_value} g/cm³"

    # Comparaison avec planètes connues (densités : Saturne 0,69 / Jupiter 1,33 / Neptune 1,64 / Terre 5,51)
    if exoplanet.pl_density.value < 0.8:
        section += ", inférieure à celle de Saturne (0,69 g/cm³)"
    elif exoplanet.pl_density.value < 1.1:
        section += ", proche de celle de Saturne (0,69 g/cm³)"
    elif exoplanet.pl_density.value < 1.5:
        section += ", similaire à celle de Jupiter (1,33 g/cm³)"
    elif exoplanet.pl_density.value < 2.0:
        section += ", proche de celle de Neptune (1,64 g/cm³)"
    elif exoplanet.pl_density.value < 3.5:
        section += ", intermédiaire entre Neptune et la Terre"
    elif exoplanet.pl_density.value < 6.0:
        section += ", proche de celle de la Terre (5,51 g/cm³)"
    else:
        section += ", supérieure à celle de la Terre, suggérant une composition riche en fer"
```

---

### 3. Section "Orbite" - Enrichissements Possibles

#### Données Disponibles mais Non Utilisées

- `pl_projobliq` - Obliquité projetée (angle spin-orbite)
- `pl_trueobliq` - Obliquité vraie
- `pl_angsep` - Séparation angulaire (arcsec)
- `pl_imppar` - Paramètre d'impact du transit
- `pl_ratdor` - Ratio distance/rayon stellaire (a/R\*)
- `pl_ratror` - Ratio rayon planétaire/rayon stellaire (Rp/R\*)

#### Phrases à Ajouter

**Exemple actuel** :

> L'exoplanète orbite son étoile en 3,5 jours avec une excentricité de 0,02.

**Exemple enrichi** :

> L'exoplanète orbite son étoile en 3,5 jours avec une excentricité de 0,02. L'orbite présente une **obliquité projetée de 12°**, indiquant un alignement spin-orbite relativement bon. Lors des transits, le **paramètre d'impact est de 0,3**, suggérant un passage proche du centre du disque stellaire. La planète se situe à une distance de **8,5 rayons stellaires** de son étoile.

**Code à ajouter dans `orbit_section.py`** :

```python
# Après période et excentricité
if exoplanet.pl_projobliq and exoplanet.pl_projobliq.value:
    obliq = exoplanet.pl_projobliq.value
    section += f" L'orbite présente une obliquité projetée de {obliq}°"
    if obliq < 10:
        section += ", indiquant un excellent alignement spin-orbite"
    elif obliq < 30:
        section += ", indiquant un alignement spin-orbite relativement bon"
    else:
        section += ", suggérant une possible migration planétaire"

if exoplanet.pl_imppar and exoplanet.pl_imppar.value:
    impact = exoplanet.pl_imppar.value
    section += f". Lors des transits, le paramètre d'impact est de {impact}"
    if impact < 0.3:
        section += ", suggérant un passage proche du centre du disque stellaire"
    elif impact < 0.7:
        section += ", indiquant un transit central"
    else:
        section += ", correspondant à un transit rasant"

if exoplanet.pl_ratdor and exoplanet.pl_ratdor.value:
    ratio = exoplanet.pl_ratdor.value
    section += f". La planète se situe à une distance de {ratio} rayons stellaires de son étoile"
```

---

### 4. NOUVELLE Section "Observations et Spectroscopie"

#### Données Disponibles

- `pl_ntranspec` - Nombre de spectres de transmission
- `pl_nespec` - Nombre de spectres d'éclipse
- `pl_ndispec` - Nombre de spectres d'imagerie directe
- `tran_flag` - Flag transit (1 si détecté par transit)
- `rv_flag` - Flag vitesse radiale
- `ima_flag` - Flag imagerie directe
- `ttv_flag` - Flag variations temporelles de transit

#### Exemple de Section Complète

```
== Observations ==

L'exoplanète a été détectée par plusieurs méthodes complémentaires : **transits** et **vitesses radiales**.

=== Spectroscopie ===
Des observations spectroscopiques ont permis d'étudier l'atmosphère de la planète. **12 spectres de transmission** ont été obtenus lors des transits, révélant la présence de vapeur d'eau et de sodium. **5 spectres d'éclipse secondaire** ont également été acquis, permettant d'estimer la température du côté jour de la planète.

=== Variations temporelles ===
Des **variations temporelles de transit (TTV)** ont été détectées, suggérant la présence d'une planète compagne perturbant l'orbite.
```

---

## ⭐ SECTIONS ÉTOILES

### 5. Section "Caractéristiques Physiques" (Étoiles) - Enrichissements

#### Données Disponibles mais Non Utilisées

- `st_lum` - Luminosité stellaire (L☉) ✅ **Déjà dans NEA**
- `st_dens` - Densité stellaire (g/cm³) ✅ **Déjà dans NEA**
- `st_age` - Âge stellaire (Ga) ✅ **Déjà dans l'entité**
- `st_logg` - Gravité de surface (log g)

#### Phrases à Ajouter

**Exemple enrichi** :

> L'étoile est une naine jaune de type spectral G2V, avec une masse de 1,05 M☉ et un rayon de 1,02 R☉. Sa **luminosité est de 1,1 L☉**, légèrement supérieure à celle du Soleil. L'étoile a un **âge estimé à 4,6 milliards d'années**, similaire à celui du Soleil, et présente une **densité de 1,4 g/cm³**.

---

### 6. NOUVELLE Section "Rotation et Activité" (Étoiles)

#### Données Disponibles

- `st_rotp` - Période de rotation (jours)
- `st_vsin` - Vitesse de rotation projetée (km/s)
- `st_radv` - Vitesse radiale systémique (km/s)
- `st_log_rhk` - Indice d'activité chromosphérique

#### Exemple de Section Complète

```
== Rotation et activité ==

L'étoile présente une **période de rotation de 25 jours**, similaire à celle du Soleil (25-35 jours). La **vitesse de rotation projetée** (v sin i) est de **2,1 km/s**, indiquant une rotation lente caractéristique des étoiles de type solaire âgées.

La **vitesse radiale systémique** de l'étoile est de **-12,3 km/s** par rapport au Soleil, indiquant son mouvement dans la Galaxie.

L'**indice d'activité chromosphérique** log(R'HK) de **-4,9** suggère une étoile peu active, cohérent avec son âge avancé.
```

---

## 📊 Résumé des Améliorations Possibles

### Par Section

| Section                        | Données Disponibles                   | Phrases à Ajouter | Impact       |
| ------------------------------ | ------------------------------------- | ----------------- | ------------ |
| **Découverte**                 | télescope, instrument, lieu, date pub | 2-3 phrases       | ⭐⭐⭐ Haute |
| **Caractéristiques Physiques** | densité, comparaisons                 | 1-2 phrases       | ⭐⭐⭐ Haute |
| **Orbite**                     | obliquité, paramètre impact, ratios   | 2-4 phrases       | ⭐⭐ Moyenne |
| **Observations** (NOUVEAU)     | spectres, flags détection, TTV        | Section complète  | ⭐⭐⭐ Haute |
| **Rotation Étoile** (NOUVEAU)  | rotation, v sin i, vitesse radiale    | Section complète  | ⭐⭐ Moyenne |

### Priorités d'Implémentation

1. **Priorité 1** (Impact immédiat) :

   - Enrichir section "Découverte" avec télescope/instrument
   - Ajouter densité dans "Caractéristiques Physiques"
   - Créer section "Observations et Spectroscopie"

2. **Priorité 2** (Bon complément) :
   - Enrichir section "Orbite" avec obliquité et paramètres
   - Créer section "Rotation et Activité" pour étoiles

---

## 🚀 Prochaines Étapes

1. **Immédiat** : Enrichir `discovery_section.py` avec télescope/instrument
2. **Cette semaine** : Ajouter densité dans `physical_characteristics_section.py`
3. **Semaine prochaine** : Créer `observations_section.py`

---

**Note** : Tous ces paramètres sont **déjà disponibles** dans `nea_entity.py` ! Il suffit de les mapper et de les utiliser dans les sections.
