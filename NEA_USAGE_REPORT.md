# Rapport d'Utilisation des Paramètres NEA dans AstroWikiBuilder

Ce document recense l'utilisation actuelle des paramètres de la NASA Exoplanet Archive (NEA) dans la génération des articles d'exoplanètes et d'étoiles. Il met également en évidence les données disponibles mais non exploitées pour guider les futures améliorations.

## 1. Paramètres Utilisés par Section (Exoplanète)

Les attributs listés ci-dessous sont ceux accédés via l'objet `exoplanet` dans les générateurs de section.

| Section                        | Attributs de l'Entité Exoplanet Utilisés                                                                                                                                                                             | Correspondance NEA (Probable)                                                                                                                                              |
| :----------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Introduction**               | `pl_name`, `st_name`, `sy_snum`, `cb_flag`, `st_distance`, `sy_constellation`, `sy_mnum`                                                                                                                             | `pl_name`, `hostname`, `sy_snum`, `cb_flag`, `sy_dist`, `sy_constellation` (dérivé), `sy_mnum`                                                                             |
| **Infobox**                    | `pl_name`, `pl_mass`, `pl_radius`, `pl_orbital_period`, `pl_semi_major_axis`, `pl_eccentricity`, `pl_inclination`, `st_name`, `st_spectral_type`, `st_apparent_magnitude`, `st_distance`, `disc_method`, `disc_year` | `pl_name`, `pl_bmassj`, `pl_radj`, `pl_orbper`, `pl_orbsmax`, `pl_orbeccen`, `pl_orbincl`, `hostname`, `st_spectype`, `sy_vmag`, `sy_dist`, `discoverymethod`, `disc_year` |
| **Caractéristiques Physiques** | `pl_mass`, `pl_radius`, `pl_density`, `pl_temperature`, `pl_insolation_flux`                                                                                                                                         | `pl_bmassj`, `pl_radj`, `pl_dens`, `pl_eqt`, `pl_insol`                                                                                                                    |
| **Orbite**                     | `pl_orbital_period`, `pl_semi_major_axis`, `pl_eccentricity`, `pl_inclination`, `pl_projobliq`, `pl_trueobliq`, `pl_ratdor`, `pl_ratror`, `pl_imppar`                                                                | `pl_orbper`, `pl_orbsmax`, `pl_orbeccen`, `pl_orbincl`, `pl_projobliq`, `pl_trueobliq`, `pl_ratdor`, `pl_ratror`, `pl_imppar`                                              |
| **Étoile Hôte**                | `st_name`, `st_mass`, `st_metallicity`, `st_age`, `st_spectral_type`, `st_apparent_magnitude`, `st_distance`                                                                                                         | `hostname`, `st_mass`, `st_met`, `st_age`, `st_spectype`, `sy_vmag`, `sy_dist`                                                                                             |
| **Découverte**                 | `disc_method`, `disc_year`, `disc_facility`, `disc_telescope`, `disc_instrument`, `disc_pubdate`, `disc_program`                                                                                                     | `discoverymethod`, `disc_year`, `disc_facility`, `disc_telescope`, `disc_instrument`, `disc_pubdate`, `disc_program` (dérivé)                                              |
| **Détection et Observations**  | `pl_occultation_depth`, `disc_facility`                                                                                                                                                                              | `pl_occdep`, `disc_facility`                                                                                                                                               |
| **Potentiel d'Observation**    | `pl_transit_depth`                                                                                                                                                                                                   | `pl_trandep`                                                                                                                                                               |
| **Système**                    | `sy_planet_count`, `sy_snum`, `cb_flag`                                                                                                                                                                              | `sy_pnum`, `sy_snum`, `cb_flag`                                                                                                                                            |
| **Identification**             | `pl_altname`, `hd_name`, `hip_name`, `gaia_id`, `tic_id`                                                                                                                                                             | `pl_altname`, `hd_name`, `hip_name`, `gaia_id`, `tic_id`                                                                                                                   |
| **Spectroscopie**              | `pl_nespec`, `pl_ntranspec`, `pl_ndispec`                                                                                                                                                                            | `pl_nespec`, `pl_ntranspec`, `pl_ndispec`                                                                                                                                  |

## 2. Paramètres Utilisés par Section (Étoile)

Les attributs listés ci-dessous sont ceux accédés via l'objet `star` dans les générateurs de section.

| Section                        | Attributs de l'Entité Star Utilisés                                                                                                                                                          | Correspondance NEA (Probable)                                                                                              |
| :----------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------- |
| **Introduction**               | `st_name`, `st_spectral_type`, `sy_constellation`, `st_distance`, `sy_star_count`                                                                                                            | `hostname`, `st_spectype`, `sy_constellation` (dérivé), `sy_dist`, `sy_snum`                                               |
| **Infobox**                    | `st_name`, `sy_constellation`, `st_right_ascension`, `st_declination`, `st_apparent_magnitude`, `st_distance`, `st_spectral_type`, `st_mass`, `st_radius`, `st_temperature`, `st_luminosity` | `hostname`, `sy_constellation`, `ra`, `dec`, `sy_vmag`, `sy_dist`, `st_spectype`, `st_mass`, `st_rad`, `st_teff`, `st_lum` |
| **Astrométrie**                | `st_parallax`, `st_proper_motion_ra`, `st_proper_motion_dec`, `st_radial_velocity`, `glon`, `glat`, `sy_pm`                                                                                  | `sy_plx`, `sy_pmra`, `sy_pmdec`, `st_radv`, `glon`, `glat`, `sy_pm`                                                        |
| **Photométrie**                | `st_mag_u`, `st_mag_b`, `st_mag_v`, `st_mag_g`, `st_mag_r`, `st_mag_i`, `st_mag_j`, `st_mag_h`, `st_mag_k`, `st_mag_w1-4`, `st_mag_gaia`, `st_mag_t`, `st_mag_kep`                           | `sy_umag`, `sy_bmag`, `sy_vmag`, `sy_gmag`, `sy_rmag`, `sy_imag`, `sy_jmag`, `sy_hmag`, `sy_kmag`, etc.                    |
| **Caractéristiques Physiques** | `st_mass`, `st_radius`, `st_density`, `st_luminosity`, `st_temperature`, `st_rotation`, `st_vsin`, `st_age`, `st_metallicity`, `st_surface_gravity`                                          | `st_mass`, `st_rad`, `st_dens`, `st_lum`, `st_teff`, `st_rotp`, `st_vsin`, `st_age`, `st_met`, `st_logg`                   |
| **Rotation et Activité**       | `st_rotation`, `st_vsin`, `st_radial_velocity`, `st_log_rhk`                                                                                                                                 | `st_rotp`, `st_vsin`, `st_radv`, `st_log_rhk`                                                                              |
| **Système**                    | `sy_star_count`, `st_altname`, `sy_mnum`                                                                                                                                                     | `sy_snum`, `pl_altname`, `sy_mnum`                                                                                         |

## 3. Paramètres NEA Inutilisés et Opportunités

Voici une liste mise à jour des paramètres présents dans le fichier JSON NEA mais qui ne sont **pas exploités** dans le code actuel.

### 3.1. Caractéristiques de l'Exoplanète (Transit & Orbite)

- **`pl_trandur` (Durée de transit)** : Donnée fondamentale pour les transits.
  - _Opportunité_ : Ajouter à la section "Orbite" ou "Caractéristiques physiques".
- **`pl_tranmid` (Temps central du transit)** : Éphéméride de transit.
  - _Opportunité_ : Ajouter aux détails orbitaux (éphémérides).
- **`pl_orbtper` (Date du passage au périastre)** : Éphéméride orbitale.
  - _Opportunité_ : Ajouter aux détails orbitaux.
- **`pl_orblper` (Argument du périastre)** : Paramètre orbital définissant l'orientation de l'ellipse.
  - _Opportunité_ : Compléter les paramètres orbitaux (avec excentricité et inclinaison).
- **`pl_rvamp` (Amplitude de vitesse radiale)** : Amplitude du signal RV induit par la planète.
  - _Opportunité_ : Ajouter à la section "Orbite" ou "Détection" pour les planètes RV.

### 3.2. Métadonnées et Références

- **`pl_pubdate` (Date de publication des paramètres)** : Date de la mise à jour des paramètres planétaires (différent de `disc_pubdate`).
  - _Opportunité_ : Indiquer la fraîcheur des données ("Données mises à jour en ...").
- **`pl_tsystemref` (Référence temporelle)** : Système de temps utilisé (ex: BJD_TDB).
  - _Opportunité_ : Précision technique pour les éphémérides.

### 3.3. Système et Environnement

- **`sy_dist` (Distance)** : Bien que mappé (`st_distance`), il est parfois utilisé uniquement pour l'étoile.
  - _Opportunité_ : Vérifier que la distance est bien mentionnée dans l'intro de l'exoplanète (c'est le cas actuellement).
- **`elonsymerr`, `elat`, etc. (Coordonnées écliptiques)** : Non utilisées.
  - _Opportunité_ : Faible priorité, mais disponible.

## 4. Recommandations d'Action Prioritaires

1.  **Ajouter la Durée de Transit (`pl_trandur`)** : C'est une donnée physique simple et parlante ("Le transit dure environ 2 heures...").
2.  **Compléter les Paramètres Orbitaux** : Ajouter l'argument du périastre (`pl_orblper`) et l'amplitude RV (`pl_rvamp`) pour avoir un set complet de paramètres orbitaux kepleriens.
3.  **Éphémérides** : Créer une sous-section ou une note avec les temps de passage (`pl_tranmid`, `pl_orbtper`) pour les observateurs amateurs/professionnels.

## 5. État des Lieux (Mise à jour)

### ✅ Paramètres correctement intégrés (contrairement aux versions précédentes du rapport)

- `sy_pm` (Mouvement propre) : Utilisé dans la section Astrométrie.
- `sy_mnum` (Lunes) : Utilisé dans l'introduction et la section Système.
- `pl_occdep` (Profondeur d'occultation) : Utilisé dans la section Détection.
- `pl_transit_depth` (`pl_trandep`) : Utilisé dans la section Potentiel d'Observation.
