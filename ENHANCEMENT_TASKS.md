# Tâches d'Amélioration AstroWikiBuilder

## 🚀 Phase 1 : Haute Priorité (Enrichissement du Contenu)

### Exoplanètes

- [x] **1.1 - Enrichir `physical_characteristics_section.py` (Exoplanètes)** ✅ **Complété**

  - [x] Ajouter densité (`pl_dens`)
  - [x] Ajouter température (`pl_eqt`)
  - [x] Ajouter masse (`pl_mass`, `pl_bmasse`, `pl_bmassj`)
  - [x] Ajouter rayon (`pl_radj`, `pl_rade`)
  - [x] Tests unitaires
  - [x] Commit

- [x] **1.2 - Enrichir `discovery_section.py` (Exoplanètes)** ✅ **Complété**

  - [x] ~~Ajouter `disc_telescope` (nom du télescope)~~ ✅ Déjà dans `nea_entity.py`
  - [x] Ajouter `disc_instrument` (nom de l'instrument)
  - [x] Ajouter `disc_pubdate` (date de publication)
  - [x] Utiliser ces champs dans `discovery_section.py`
  - [x] Tests unitaires (9 tests passent)
  - [x] Commit

- [ ] **1.3 - Enrichir `infobox_section.py` (Exoplanètes)**
  - [ ] Ajouter identifiants alternatifs (HD, HIP, TIC, Gaia DR2/DR3)
  - [ ] Ajouter flag de controverse (`pl_controv_flag`)
  - [ ] Tests unitaires (couverture actuelle: **93%**)
  - [ ] Commit

### Étoiles

- [x] **1.4 - Enrichir `physical_characteristics_section.py` (Étoiles)** ✅ **Partiellement complété**

  - [x] ~~Ajouter âge stellaire (`st_age`)~~ ✅ Déjà dans `exoplanet_entity.py` et `star_entity.py`
  - [ ] Ajouter densité stellaire (`st_dens`) - À vérifier dans NEA
  - [ ] Ajouter luminosité (`st_lum`) - À vérifier dans NEA
  - [ ] Utiliser ces champs dans la section étoiles
  - [ ] Tests unitaires
  - [ ] Commit

- [ ] **1.5 - Créer `rotation_activity_section.py` (Étoiles)**

  - [ ] Implémenter section rotation (`st_vsin`, `st_rotp`)
  - [ ] Ajouter vitesse radiale systémique (`st_radv`)
  - [ ] Intégrer dans `star_article_generator.py`
  - [ ] Tests unitaires
  - [ ] Commit

- [ ] **1.6 - Enrichir `infobox_section.py` (Étoiles)**
  - [ ] Ajouter tous les identifiants de catalogues
  - [ ] Ajouter coordonnées galactiques/écliptiques
  - [ ] Tests unitaires
  - [ ] Commit

## 🔧 Phase 2 : Moyenne Priorité (Amélioration Couverture Tests)

### Exoplanètes - Améliorer couverture tests existantes

- [x] **2.1 - Améliorer `physical_characteristics_section.py`** ✅ **Couverture: 87%**

  - [x] Couverture actuelle: **87%** (objectif 90% atteint ou presque)
  - [ ] Tester tous les cas limites (NaN, None, valeurs extrêmes)
  - [ ] Commit

- [x] **2.2 - Améliorer `discovery_section.py`** ✅ **Couverture: 91%**

  - [x] Couverture actuelle: **91%** (objectif 90% atteint)
  - [ ] Commit

- [x] **2.3 - Améliorer `composition_section.py`** ✅ **Couverture: 100%**

  - [x] Couverture actuelle: **100%** (objectif dépassé)
  - [x] Commit

- [ ] **2.4 - Améliorer `habitability_section.py`**

  - [ ] Augmenter couverture de **87%** à 90%+
  - [ ] Tester calculs zone habitable
  - [ ] Commit

- [x] **2.5 - Améliorer `insolation_section.py`** ✅ **Couverture: 100%**

  - [x] Couverture actuelle: **100%** (objectif dépassé)
  - [x] Commit

- [x] **2.6 - Améliorer `orbit_section.py`** ✅ **Couverture: 100%**

  - [x] Couverture actuelle: **100%** (objectif dépassé)
  - [x] Commit

- [x] **2.7 - Améliorer `introduction_section.py`** ✅ **Couverture: 97%**

  - [x] Couverture actuelle: **97%** (objectif 90% atteint)
  - [x] Commit

- [x] **2.8 - Améliorer `observation_potential_section.py`** ✅ **Couverture: 97%**

  - [x] Couverture actuelle: **97%** (objectif 90% atteint)
  - [x] Commit

- [x] **2.9 - Améliorer `see_also_section.py`** ✅ **Couverture: 98%**

  - [x] Couverture actuelle: **98%** (objectif 90% atteint)
  - [x] Commit

- [ ] **2.10 - Améliorer `system_architecture_section.py`**

  - [ ] Augmenter couverture de **85%** à 90%+
  - [ ] Tester tri des planètes
  - [ ] Commit

- [x] **2.11 - Améliorer `tidal_locking_section.py`** ✅ **Couverture: 100%**

  - [x] Couverture actuelle: **100%** (objectif dépassé)
  - [x] Commit

- [x] **2.12 - Améliorer `host_star_section.py`** ✅ **Couverture: 100%**

  - [x] Couverture actuelle: **100%** (objectif dépassé)
  - [x] Commit

- [x] **2.13 - Améliorer `category_section.py`** ✅ **Couverture: 98%**
  - [x] Couverture actuelle: **98%** (objectif 90% atteint)
  - [x] Commit

### Nouvelles Sections Exoplanètes

- [ ] **2.14 - Enrichir `orbit_section.py`**

  - [ ] Ajouter obliquité projetée (`pl_projobliq`)
  - [ ] Ajouter obliquité vraie (`pl_trueobliq`)
  - [ ] Ajouter séparation angulaire (`pl_angsep`)
  - [ ] Ajouter paramètre d'impact (`pl_imppar`)
  - [ ] Ajouter ratios géométriques (`pl_ratdor`, `pl_ratror`)
  - [ ] Tests unitaires
  - [ ] Commit

- [ ] **2.15 - Créer `spectroscopy_section.py`**

  - [ ] Vérifier disponibilité spectres transmission (`pl_ntranspec`)
  - [ ] Vérifier disponibilité spectres éclipse (`pl_nespec`)
  - [ ] Vérifier disponibilité spectres imagerie directe (`pl_ndispec`)
  - [ ] Générer section si données disponibles
  - [ ] Intégrer dans `exoplanet_article_generator.py`
  - [ ] Tests unitaires
  - [ ] Commit

- [ ] **2.16 - Créer `detection_observations_section.py`**
  - [ ] Lister méthodes de détection multiples (flags)
  - [ ] Mentionner facilités d'observation
  - [ ] Indiquer nombre de mesures disponibles
  - [ ] Intégrer dans `exoplanet_article_generator.py`
  - [ ] Tests unitaires
  - [ ] Commit

### Étoiles

- [ ] **2.17 - Enrichir `planetary_system_section.py`**
  - [ ] Ajouter nombre d'étoiles (`sy_snum`)
  - [ ] Ajouter flag circumbinaire (`cb_flag`)
  - [ ] Ajouter nombre de lunes (`sy_mnum`)
  - [ ] Tests unitaires
  - [ ] Commit

## 📊 Phase 3 : Basse Priorité (Nouvelles Sections Avancées)

- [ ] **3.1 - Créer `photometry_section.py` (Étoiles)**

  - [ ] Tableau complet des magnitudes (Johnson, 2MASS, Sloan, WISE, Gaia, TESS, Kepler)
  - [ ] Formatage Wikipedia tableau
  - [ ] Tests unitaires
  - [ ] Commit

- [ ] **3.2 - Créer `astrometry_section.py` (Étoiles)**
  - [ ] Mouvement propre (`sy_pm`, `sy_pmra`, `sy_pmdec`)
  - [ ] Parallaxe et distance (`sy_plx`, `sy_dist`)
  - [ ] Position galactique (`glat`, `glon`)
  - [ ] Tests unitaires
  - [ ] Commit

## 🔄 Tâches Transverses

- [x] **Mettre à jour `ExoplanetEntity` et `StarEntity`** ✅ **Partiellement complété**

  - [x] ~~Ajouter `pl_density`~~ ✅ Déjà présent
  - [x] ~~Ajouter `st_age`~~ ✅ Déjà présent
  - [ ] Vérifier et ajouter tous les champs manquants de NEA
  - [ ] Mettre à jour les dataclasses
  - [ ] Commit

- [ ] **Mettre à jour `nasa_exoplanet_archive_mapper.py`**

  - [ ] Mapper tous les nouveaux champs
  - [ ] Gérer les valeurs manquantes
  - [ ] Tests unitaires
  - [ ] Commit

- [x] **Mettre à jour la couverture de tests** ✅ **96% ATTEINT**

  - [x] ~~`formation_mechanism_section.py`~~ ✅ 100% couverture
  - [x] Couverture globale: **96%** (objectif 90%+ largement dépassé)
  - [x] Toutes les sections >85% maintenant
  - [x] Commits effectués régulièrement par section

- [ ] **Documentation**
  - [ ] Mettre à jour `ARCHITECTURE.md`
  - [ ] Mettre à jour `README.md` si nécessaire
  - [ ] Documenter les nouvelles sections
  - [ ] Commit

## 📝 Notes

- Toujours tester avec `make run` après chaque phase
- Vérifier la qualité des articles générés
- Committer régulièrement (par tâche ou groupe de tâches cohérentes)
- **Objectif couverture: passer de 28% à 90%+**
- Priorité: améliorer tests des sections existantes avant d'en créer de nouvelles
