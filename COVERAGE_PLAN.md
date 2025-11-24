# Plan d'Amélioration de la Couverture de Tests

**Date de création**: 2025-11-24
**Couverture globale actuelle**: ~92%
**Objectif**: Atteindre 100% de couverture pour tous les fichiers

## Priorités d'Amélioration

### 🔴 PRIORITÉ 1: Fichiers < 80% de couverture

#### 1. `src/generators/articles/exoplanet/sections/formation_mechanism_section.py` - **75%**

- **Lignes manquantes**: 66, 72-73, 76, 79, 84
- **Fonctions non testées**:
  - `_is_super_earth_or_mini_neptune()` (0%)
  - `_has_eccentric_orbit()` (0%)
- **Actions**:
  - [ ] Créer tests pour `_is_super_earth_or_mini_neptune()`
  - [ ] Créer tests pour `_has_eccentric_orbit()`
  - [ ] Tester le cas où `_is_red_dwarf_system()` retourne True
  - [ ] Tester le cas où `generate()` retourne None

---

### 🟡 PRIORITÉ 2: Fichiers 80-85% de couverture

#### 1. `src/generators/articles/star/sections/category_section.py` - **84%**

- **Lignes manquantes**: 60, 62, 64, 66-67, 69, 75, 91-92, 111, 128, 163-164
- **Fonctions à améliorer**:
  - `extract_key()` dans `map_catalog_prefix_to_category` (33%)
  - `process_name()` (89%)
  - `map_spectral_type_to_category()` (86%)
  - `map_luminosity_class_to_category()` (86%)
  - `map_star_type_to_category()` (83%)
- **Actions**:
  - [ ] Tester tous les cas de `extract_key()` (patterns HD, HIP, TYC, etc.)
  - [ ] Tester les cas limites de `process_name()`
  - [ ] Tester les cas manquants pour les types spectraux
  - [ ] Tester les classes de luminosité manquantes

#### 2. `src/generators/articles/exoplanet/sections/physical_characteristics_section.py` - **85%**

- **Lignes manquantes**: 20, 28-29, 47-48, 65, 67, 71-72, 77, 80
- **Fonctions à améliorer**:
  - `_get_value_or_none_if_nan()` (83%)
  - `_format_mass_description()` (83%)
  - `_format_radius_description()` (83%)
  - `_format_temperature_description()` (65%)
- **Actions**:
  - [ ] Tester le cas où `isnan()` retourne True
  - [ ] Tester les cas de masse < 0.1 et > 13
  - [ ] Tester les cas de rayon < 0.5 et > 2.5
  - [ ] Tester tous les cas de température (< 200K, 200-400K, 400-1000K, > 1000K)

#### 3. `src/generators/articles/star/sections/planetary_system_section.py` - **85%**

- **Lignes manquantes**: 35-36, 94-95, 121, 123-124, 126-127
- **Fonctions à améliorer**:
  - `sort_key()` (67%)
  - `_format_field_with_uncertainty()` (71%)
  - `_format_uncertainty()` (64%)
- **Actions**:
  - [ ] Tester le cas où `semi_major_axis` est None
  - [ ] Tester le cas où `value` est None dans `_format_field_with_uncertainty()`
  - [ ] Tester tous les cas de `_format_uncertainty()` (None, < 0.01, 0.01-0.1, > 0.1)

#### 4. `src/generators/articles/exoplanet/sections/system_architecture_section.py` - **83%**

- **Lignes manquantes**: 24, 27-28, 35, 39, 51, 71-72
- **Fonctions à améliorer**:
  - `generate()` (74%)
  - `sort_key()` (67%)
  - `_generate_with_siblings()` (92%)
- **Actions**:
  - [ ] Tester le cas où il n'y a pas de siblings
  - [ ] Tester le cas où `semi_major_axis` est None dans `sort_key()`
  - [ ] Tester les cas de comparaison de types de planètes

---

### 🟢 PRIORITÉ 3: Fichiers 85-90% de couverture

#### 1. `src/generators/articles/exoplanet/sections/habitability_section.py` - **87%**

- **Lignes manquantes**: 18, 34-36
- **Actions**:
  - [ ] Tester le cas où `isnan()` retourne True
  - [ ] Tester le cas où la planète est potentiellement habitable

#### 2. `src/generators/articles/exoplanet/sections/infobox_section.py` - **88%**

- **Lignes manquantes**: 47, 54
- **Actions**:
  - [ ] Tester le cas où `field_mapping` est None
  - [ ] Tester `default_field_mapping()`

#### 3. `src/generators/articles/exoplanet/sections/discovery_section.py` - **88%**

- **Lignes manquantes**: 49, 52
- **Actions**:
  - [ ] Tester les cas où `disc_year` ou `disc_method` sont None

---

### 🔵 PRIORITÉ 4: Fichiers 90-95% de couverture

#### 1. `src/generators/articles/star/sections/infobox_section.py` - **92%**

- **Lignes manquantes**: 43, 50
- **Actions**:
  - [ ] Tester le cas où `field_mapping` est None
  - [ ] Tester `default_field_mapping()`

#### 2. `src/generators/articles/exoplanet/sections/infobox_section.py` - **93%**

- **Lignes manquantes**: 47, 54
- **Actions**:
  - [ ] Tester les cas limites de génération d'infobox

#### 3. `src/generators/articles/star/sections/introduction_section.py` - **91%**

- **Lignes manquantes**: 23, 44-45
- **Actions**:
  - [ ] Tester le cas où `star_type` est None
  - [ ] Tester le cas où `distance` est None

#### 4. `src/generators/base/base_wikipedia_article_generator.py` - **93%**

- **Lignes manquantes**: 50-51
- **Actions**:
  - [ ] Tester `build_category_section()` (méthode abstraite)

#### 5. `src/collectors/base_collector.py` - **94%**

- **Lignes manquantes**: 35, 40, 45, 50, 55, 60, 65, 185
- **Fonctions non testées**: Toutes les méthodes abstraites (0%)
- **Actions**:
  - [ ] Tester les méthodes abstraites via les implémentations concrètes
  - [ ] Tester le cas d'erreur dans `collect_entities_from_source()`

#### 6. `src/generators/articles/exoplanet/exoplanet_article_generator.py` - **95%**

- **Lignes manquantes**: 38-39, 148
- **Actions**:
  - [ ] Tester le cas où `self.planet_type_util` est None
  - [ ] Tester le cas où `replace_first_reference_with_full()` ne trouve pas de match

#### 7. `src/generators/base/category_rules_manager.py` - **96%**

- **Lignes manquantes**: 23, 63
- **Actions**:
  - [ ] Tester le cas où `getattr()` lève une exception
  - [ ] Tester le cas où `generator_function()` lève une exception

#### 8. `src/mappers/nasa_exoplanet_archive_mapper.py` - **97%**

- **Lignes manquantes**: 165-166, 179-180, 292-293
- **Actions**:
  - [ ] Tester le cas où `ra_str` est None dans `_set_right_ascension()`
  - [ ] Tester le cas où `dec_str` est None dans `_set_declination()`
  - [ ] Tester le cas où `match` est None dans `_parse_html_value()`

#### 9. `src/generators/articles/star/star_article_generator.py` - **97%**

- **Lignes manquantes**: 49-50
- **Actions**:
  - [ ] Tester le cas où `self.star_type_util` est None

#### 10. `src/generators/articles/exoplanet/sections/introduction_section.py` - **97%**

- **Lignes manquantes**: 64, 76
- **Actions**:
  - [ ] Tester le cas où `distance` est None dans `_compose_distance_phrase()`
  - [ ] Tester le cas où `constellation` est None dans `_compose_constellation_phrase()`

#### 11. `src/generators/articles/exoplanet/sections/observation_potential_section.py` - **97%**

- **Lignes manquantes**: 23
- **Actions**:
  - [ ] Tester le cas où `_extract_apparent_magnitude()` retourne None

#### 12. `src/generators/articles/exoplanet/sections/category_section.py` - **98%**

- **Lignes manquantes**: 49
- **Actions**:
  - [ ] Tester le cas où `planet_type` est "Terrestrial"

#### 13. `src/generators/articles/exoplanet/sections/see_also_section.py` - **98%**

- **Lignes manquantes**: 64
- **Actions**:
  - [ ] Tester le cas où `nasa_link` est None

#### 14. `src/models/references/reference.py` - **98%**

- **Lignes manquantes**: 71
- **Actions**:
  - [ ] Tester le cas où `self.url` est None dans `to_url()`

---

### ⚪ PRIORITÉ 5: Fichiers 95-100% de couverture

Ces fichiers ont déjà une excellente couverture (≥95%). Les améliorer est optionnel mais recommandé pour atteindre 100%.

#### Fichiers à 100%

- ✅ `src/collectors/implementations/exoplanet_eu_collector.py`
- ✅ `src/collectors/implementations/nasa_exoplanet_archive_collector.py`
- ✅ `src/collectors/implementations/open_exoplanet_catalogue_collector.py`
- ✅ `src/constants/wikipedia_field_config.py`
- ✅ `src/core/config.py`
- ✅ `src/generators/articles/exoplanet/sections/__init__.py`
- ✅ `src/generators/articles/exoplanet/sections/composition_section.py`
- ✅ `src/generators/articles/exoplanet/sections/host_star_section.py`
- ✅ `src/generators/articles/exoplanet/sections/insolation_section.py`
- ✅ `src/generators/articles/exoplanet/sections/orbit_section.py`
- ✅ `src/generators/articles/exoplanet/sections/tidal_locking_section.py`
- ✅ `src/generators/articles/star/sections/environment_section.py`
- ✅ `src/generators/articles/star/sections/history_section.py`
- ✅ `src/generators/articles/star/sections/observation_section.py`
- ✅ `src/generators/articles/star/sections/physical_characteristics_section.py`
- ✅ `src/models/entities/exoplanet_entity.py`
- ✅ `src/models/entities/nea_entity.py`
- ✅ `src/models/entities/star_entity.py`
- ✅ `src/models/infobox_fields.py`

---

## Stratégie d'Exécution

### Phase 1: Fichiers < 80% (CRITIQUE)

1. `formation_mechanism_section.py` (75%)

### Phase 2: Fichiers 80-85% (HAUTE PRIORITÉ)

1. `star/sections/category_section.py` (84%)
2. `exoplanet/sections/physical_characteristics_section.py` (85%)
3. `star/sections/planetary_system_section.py` (85%)
4. `exoplanet/sections/system_architecture_section.py` (83%)

### Phase 3: Fichiers 85-90% (MOYENNE PRIORITÉ)

1. `habitability_section.py` (87%)
2. `exoplanet/sections/infobox_section.py` (88%)
3. `discovery_section.py` (88%)

### Phase 4: Fichiers 90-95% (BASSE PRIORITÉ)

1. Tous les fichiers entre 90% et 95%

### Phase 5: Fichiers 95-100% (OPTIONNEL)

1. Peaufinage des fichiers déjà bien couverts

---

## Commandes Utiles

```bash
# Exécuter les tests avec couverture
make cov

# Exécuter les tests pour un fichier spécifique
pytest tests/unit/test_generators/test_sections/test_formation_mechanism_section.py -v

# Voir le rapport de couverture HTML
coverage html
start htmlcov/index.html

# Vérifier la couverture d'un fichier spécifique
coverage report --include="src/generators/articles/exoplanet/sections/formation_mechanism_section.py"
```

---

## Notes

- **Priorité absolue**: Se concentrer d'abord sur les fichiers < 80%
- **Approche incrémentale**: Traiter un fichier à la fois, commit après chaque amélioration significative
- **Tests de qualité**: Privilégier des tests significatifs plutôt que juste augmenter les chiffres
- **Cas limites**: Bien tester les cas None, valeurs extrêmes, exceptions
- **Documentation**: Documenter les cas de test complexes

---

## Suivi de Progression

| Priorité     | Fichiers Total | Fichiers Complétés | Progression |
| ------------ | -------------- | ------------------ | ----------- |
| P1 (<80%)    | 1              | 0                  | 0%          |
| P2 (80-85%)  | 4              | 0                  | 0%          |
| P3 (85-90%)  | 3              | 0                  | 0%          |
| P4 (90-95%)  | 14             | 0                  | 0%          |
| P5 (95-100%) | 19             | 19                 | 100%        |
| **TOTAL**    | **41**         | **19**             | **46%**     |
