# Rapport d'Utilisation des Paramètres NEA dans AstroWikiBuilder

Ce document recense l'utilisation actuelle des paramètres de la NASA Exoplanet Archive (NEA) dans la génération des articles d'exoplanètes et d'étoiles. Il met également en évidence les données disponibles mais non exploitées pour guider les futures améliorations.

## 1. Paramètres Utilisés par Section (Exoplanète)

Les attributs listés ci-dessous sont ceux accédés via l'objet `exoplanet` dans les générateurs de section.

| Section                        | Attributs de l'Entité Exoplanet Utilisés                                                                                                                                                                             | Correspondance NEA (Probable)                                                                                                                                              |
| :----------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Introduction**               | `pl_name`, `st_name`, `sy_snum`, `cb_flag`, `st_distance`, `sy_constellation`                                                                                                                                        | `pl_name`, `hostname`, `sy_snum`, `cb_flag`, `sy_dist`, `sy_constellation` (dérivé)                                                                                        |
| **Infobox**                    | `pl_name`, `pl_mass`, `pl_radius`, `pl_orbital_period`, `pl_semi_major_axis`, `pl_eccentricity`, `pl_inclination`, `st_name`, `st_spectral_type`, `st_apparent_magnitude`, `st_distance`, `disc_method`, `disc_year` | `pl_name`, `pl_bmassj`, `pl_radj`, `pl_orbper`, `pl_orbsmax`, `pl_orbeccen`, `pl_orbincl`, `hostname`, `st_spectype`, `sy_vmag`, `sy_dist`, `discoverymethod`, `disc_year` |
| **Caractéristiques Physiques** | `pl_mass`, `pl_radius`, `pl_density`, `pl_temperature`, `pl_insolation_flux`                                                                                                                                         | `pl_bmassj`, `pl_radj`, `pl_dens`, `pl_eqt`, `pl_insol`                                                                                                                    |
| **Orbite**                     | `pl_orbital_period`, `pl_semi_major_axis`, `pl_eccentricity`, `pl_inclination`, `pl_projobliq`, `pl_trueobliq`, `pl_ratdor`, `pl_ratror`, `pl_imppar`, `pl_transit_depth`                                            | `pl_orbper`, `pl_orbsmax`, `pl_orbeccen`, `pl_orbincl`, `pl_projobliq`, `pl_trueobliq`, `pl_ratdor`, `pl_ratror`, `pl_imppar`, `pl_trandep`                                |
| **Étoile Hôte**                | `st_name`, `st_mass`, `st_metallicity`, `st_age`, `st_spectral_type`, `st_apparent_magnitude`, `st_distance`                                                                                                         | `hostname`, `st_mass`, `st_met`, `st_age`, `st_spectype`, `sy_vmag`, `sy_dist`                                                                                             |
| **Découverte**                 | `disc_method`, `disc_year`, `disc_facility`, `disc_telescope`, `disc_instrument`, `disc_pubdate`, `disc_program`                                                                                                     | `discoverymethod`, `disc_year`, `disc_facility`, `disc_telescope`, `disc_instrument`, `disc_pubdate`, `disc_program` (dérivé)                                              |
| **Système**                    | `sy_planet_count`, `sy_snum`, `cb_flag`                                                                                                                                                                              | `sy_pnum`, `sy_snum`, `cb_flag`                                                                                                                                            |
| **Identification**             | `pl_altname`, `hd_name`, `hip_name`, `gaia_id`, `tic_id`                                                                                                                                                             | `pl_altname`, `hd_name`, `hip_name`, `gaia_id`, `tic_id`                                                                                                                   |
| **Spectroscopie**              | `pl_nespec`, `pl_ntranspec`, `pl_ndispec`                                                                                                                                                                            | `pl_nespec`, `pl_ntranspec`, `pl_ndispec`                                                                                                                                  |

## 2. Paramètres Utilisés par Section (Étoile)

Les attributs listés ci-dessous sont ceux accédés via l'objet `star` dans les générateurs de section.

| Section                        | Attributs de l'Entité Star Utilisés                                                                                                                                                          | Correspondance NEA (Probable)                                                                                              |
| :----------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------- |
| **Introduction**               | `st_name`, `st_spectral_type`, `sy_constellation`, `st_distance`, `sy_star_count`                                                                                                            | `hostname`, `st_spectype`, `sy_constellation` (dérivé), `sy_dist`, `sy_snum`                                               |
| **Infobox**                    | `st_name`, `sy_constellation`, `st_right_ascension`, `st_declination`, `st_apparent_magnitude`, `st_distance`, `st_spectral_type`, `st_mass`, `st_radius`, `st_temperature`, `st_luminosity` | `hostname`, `sy_constellation`, `ra`, `dec`, `sy_vmag`, `sy_dist`, `st_spectype`, `st_mass`, `st_rad`, `st_teff`, `st_lum` |
| **Astrométrie**                | `st_parallax`, `st_proper_motion_ra`, `st_proper_motion_dec`, `st_radial_velocity`, `glon`, `glat`                                                                                           | `sy_plx`, `sy_pmra`, `sy_pmdec`, `st_radv`, `glon`, `glat`                                                                 |
| **Photométrie**                | `st_mag_u`, `st_mag_b`, `st_mag_v`, `st_mag_g`, `st_mag_r`, `st_mag_i`, `st_mag_j`, `st_mag_h`, `st_mag_k`                                                                                   | `sy_umag`, `sy_bmag`, `sy_vmag`, `sy_gmag`, `sy_rmag`, `sy_imag`, `sy_jmag`, `sy_hmag`, `sy_kmag`                          |
| **Caractéristiques Physiques** | `st_mass`, `st_radius`, `st_density`, `st_luminosity`, `st_temperature`, `st_rotation`, `st_vsin`                                                                                            | `st_mass`, `st_rad`, `st_dens`, `st_lum`, `st_teff`, `st_rotp`, `st_vsin`                                                  |
| **Système**                    | `sy_star_count`, `st_altname`                                                                                                                                                                | `sy_snum`, `pl_altname` (ou source externe)                                                                                |

## 3. Paramètres NEA Inutilisés et Opportunités

Voici une liste de paramètres présents dans le fichier JSON NEA mais qui ne semblent pas être exploités actuellement dans le code (ou très peu), offrant des opportunités pour enrichir les articles.

### 3.1. Caractéristiques de l'Étoile

- **`st_logg` (Gravité de surface)** : Disponible dans l'entité `Star` (`st_surface_gravity`) mais **non utilisé** dans les sections `star`.
  - _Opportunité_ : Ajouter à la section "Caractéristiques physiques" de l'étoile.
- **`st_met` (Métallicité)** : Utilisé dans l'article Exoplanète (section Étoile Hôte) mais **non utilisé** dans l'article Étoile (section Caractéristiques physiques).
  - _Opportunité_ : Ajouter à la section "Caractéristiques physiques" de l'étoile (indique la richesse en éléments lourds).
- **`st_age` (Âge)** : Utilisé dans l'article Exoplanète mais **non utilisé** dans l'article Étoile.
  - _Opportunité_ : Ajouter une section "Évolution" ou compléter "Caractéristiques physiques".
- **`st_log_rhk` (Indice d'activité chromosphérique)** : Non utilisé.
  - _Opportunité_ : Créer une section "Activité stellaire" ou "Magnétisme".
- **Magnitudes étendues** : `sy_zmag`, `sy_w1mag`, `sy_w2mag`, `sy_w3mag`, `sy_w4mag` (WISE), `sy_gaiamag` (Gaia), `sy_tmag` (TESS), `sy_kepmag` (Kepler).
  - _Opportunité_ : Compléter la section "Photométrie" ou créer un tableau détaillé des magnitudes.

### 3.2. Caractéristiques de l'Exoplanète

- **`pl_orbtper` (Date du passage au périastre)** : Non utilisé.
  - _Opportunité_ : Ajouter aux détails orbitaux (éphémérides).
- **`pl_orblper` (Argument du périastre)** : Non utilisé (semble absent des `grep`).
  - _Opportunité_ : Préciser l'orientation de l'orbite.
- **`pl_occdep` (Profondeur d'occultation)** : Non utilisé.
  - _Opportunité_ : Ajouter aux détails sur les transits/occultations.
- **`pl_msinij` / `pl_msinie` (Masse minimale)** : L'attribut `pl_minimum_mass` existe dans l'entité mais n'apparaît pas dans les `grep` d'utilisation (seul `pl_mass` est utilisé).
  - _Opportunité_ : Pour les planètes détectées par vitesses radiales, afficher explicitement "Masse minimale" au lieu de juste "Masse".
- **`pl_pubdate` (Date de publication)** : Non utilisé.
  - _Opportunité_ : Préciser la date exacte de l'annonce dans la section "Découverte".

### 3.3. Système

- **`sy_mnum` (Nombre de lunes)** : Non utilisé.
  - _Opportunité_ : Mentionner si le système contient des lunes connues (rare mais possible).
- **`sy_pm` (Mouvement propre total)** : Non utilisé (seuls RA/Dec sont utilisés).
  - _Opportunité_ : Afficher la vitesse totale de déplacement sur le ciel.
- **`elonsymerr`, `elat`, etc. (Coordonnées écliptiques)** : Non utilisées.
  - _Opportunité_ : Peut-être moins pertinent pour le grand public, mais disponible.

## 4. Recommandations d'Action

### ✅ Implémenté (Commit 6ff0f82)

1.  **Enrichir l'article Étoile** : ✅ **FAIT**

    - Intégration de `st_age`, `st_met` (métallicité) et `st_logg` (gravité) dans la section "Caractéristiques physiques".
    - Ces paramètres fondamentaux sont maintenant affichés lorsqu'ils sont disponibles.

2.  **Préciser les Masses** : ✅ **FAIT**

    - Distinction automatique entre "masse" et "masse minimale" selon la méthode de détection.
    - Pour les exoplanètes détectées par vitesse radiale, le terme "masse minimale" est utilisé.

3.  **Section Activité** : ✅ **FAIT**

    - Utilisation de `st_log_rhk` (indice d'activité chromosphérique) dans la section "Rotation et activité".
    - Combiné avec `st_rotp` (période de rotation) déjà présent.

4.  **Photométrie complète** : ✅ **FAIT**
    - Ajout des magnitudes WISE (W1, W2, W3, W4), Gaia (G), TESS (T) et Kepler (Kp).
    - Le tableau de photométrie des étoiles est maintenant complet avec tous les systèmes standards modernes.

### 🔄 Améliorations Futures Possibles

5.  **Éphémérides Orbitales** :

    - Ajouter `pl_orbtper` (date du passage au périastre) et `pl_orblper` (argument du périastre) aux détails orbitaux.
    - Créer une sous-section "Éléments orbitaux" plus détaillée.

6.  **Profondeur d'Occultation** :

    - Utiliser `pl_occdep` pour enrichir la section sur les transits/occultations.

7.  **Dates de Publication** :

    - Afficher `pl_pubdate` (date de publication) dans la section "Découverte" pour plus de précision.

8.  **Système Planétaire** :

    - Mentionner `sy_mnum` (nombre de lunes) si des lunes sont connues dans le système.
    - Afficher `sy_pm` (mouvement propre total) en complément des composantes RA/Dec.

9.  **Coordonnées Écliptiques** :
    - Optionnel : Ajouter les coordonnées écliptiques (`elat`, `elon`) pour les utilisateurs avancés.

## 5. Détails Techniques de l'Implémentation

### Modifications du Modèle de Données

**Entité `Star`** :

- Ajout de `st_log_rhk: ValueWithUncertainty | None`
- Ajout de `st_mag_w1`, `st_mag_w2`, `st_mag_w3`, `st_mag_w4` (WISE)
- Ajout de `st_mag_gaia` (Gaia DR2/DR3)
- Ajout de `st_mag_t` (TESS)
- Ajout de `st_mag_kep` (Kepler)

**Mapping NEA** :

- `st_log_rhk` → `st_log_rhk`
- `sy_w1mag` → `st_mag_w1`, `sy_w2mag` → `st_mag_w2`, etc.
- `sy_gaiamag` → `st_mag_gaia`
- `sy_tmag` → `st_mag_t`
- `sy_kepmag` → `st_mag_kep`

### Sections Modifiées

1.  **`PhysicalCharacteristicsSection` (Star)** :

    - Ajout de `_add_metallicity()`, `_add_surface_gravity()`, `_add_age()`
    - Correction de la gestion des valeurs nulles (`.value is not None` au lieu de `.value`)

2.  **`PhysicalCharacteristicsSection` (Exoplanet)** :

    - Modification de `_format_mass_description()` pour accepter l'objet `Exoplanet` complet
    - Détection automatique de la méthode de découverte pour afficher "masse minimale"

3.  **`RotationActivitySection` (Star)** :

    - Ajout de l'affichage de `st_log_rhk`
    - Mise à jour de la condition `any()` pour inclure `st_log_rhk`

4.  **`PhotometrySection` (Star)** :
    - Ajout de `_collect_wise_magnitudes()`
    - Ajout de `_collect_gaia_magnitudes()`
    - Ajout de `_collect_tess_magnitudes()`
    - Ajout de `_collect_kepler_magnitudes()`

### Tests Unitaires Créés

- `test_physical_characteristics_section_v2.py` (Star)
- `test_physical_characteristics_section_mass.py` (Exoplanet)
- `test_rotation_activity_section_v2.py` (Star)
- `test_photometry_section_v2.py` (Star)

**Couverture** : Tous les tests passent avec succès ✅
