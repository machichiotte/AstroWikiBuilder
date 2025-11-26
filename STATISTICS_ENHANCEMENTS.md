# Améliorations Statistiques avec les Nouvelles Données NEA

## Nouvelles Statistiques Possibles

### 1. Statistiques sur les Éphémérides Orbitales (Exoplanètes)

**Argument du Périastre** (`pl_argument_of_periastron`):

- Distribution des arguments de périastre
- Permet d'analyser l'orientation des orbites

**Temps de Passage au Périastre** (`pl_periastron_time`):

- Nombre d'exoplanètes avec éphémérides précises
- Utile pour planifier les observations

```python
"periastron_data_availability": {
    "with_periastron_time": 0,
    "with_argument_of_periastron": 0,
    "with_both": 0,
    "with_neither": 0
}
```

### 2. Statistiques sur les Occultations (Exoplanètes)

**Profondeur d'Occultation** (`pl_occultation_depth`):

- Nombre d'exoplanètes avec occultation mesurée
- Distribution des profondeurs d'occultation

```python
"occultation_stats": {
    "with_occultation_depth": 0,
    "occultation_depth_ranges": {
        "< 0.001": 0,  # Très faible
        "0.001-0.01": 0,  # Faible
        "0.01-0.1": 0,  # Modéré
        "> 0.1": 0  # Élevé
    }
}
```

### 3. Statistiques sur les Systèmes avec Lunes (Exoplanètes)

**Nombre de Lunes** (`sy_mnum`):

- Systèmes avec lunes connues
- Distribution du nombre de lunes

```python
"moon_statistics": {
    "systems_with_moons": 0,
    "total_moons": 0,
    "moon_count_distribution": {
        "1": 0,
        "2-3": 0,
        "4+": 0
    }
}
```

### 4. Statistiques Astrométriques Avancées (Étoiles)

**Mouvement Propre Total** (`sy_pm`):

- Distribution du mouvement propre
- Étoiles à mouvement propre élevé

```python
"proper_motion_stats": {
    "with_total_pm": 0,
    "pm_ranges": {
        "< 10 mas/an": 0,  # Faible
        "10-50 mas/an": 0,  # Modéré
        "50-100 mas/an": 0,  # Élevé
        "> 100 mas/an": 0  # Très élevé (étoiles proches)
    }
}
```

**Coordonnées Écliptiques** (`elon`, `elat`):

- Disponibilité des coordonnées écliptiques
- Distribution par latitude écliptique (proximité du plan écliptique)

```python
"ecliptic_coordinates_stats": {
    "with_ecliptic_coords": 0,
    "ecliptic_latitude_ranges": {
        "< 10°": 0,  # Proche du plan écliptique
        "10-30°": 0,
        "30-60°": 0,
        "> 60°": 0  # Proche des pôles écliptiques
    }
}
```

### 5. Statistiques sur l'Âge Stellaire (Étoiles)

**Âge des Étoiles** (`st_age`):

- Distribution des âges stellaires
- Corrélation âge/métallicité

```python
"star_age_stats": {
    "with_age_data": 0,
    "age_ranges": {
        "< 1 Gyr": 0,  # Jeunes
        "1-5 Gyr": 0,  # Intermédiaires
        "5-10 Gyr": 0,  # Matures
        "> 10 Gyr": 0  # Anciennes
    }
}
```

### 6. Statistiques sur l'Activité Stellaire (Étoiles)

**Indice d'Activité Chromosphérique** (`st_log_rhk`):

- Étoiles actives vs calmes
- Corrélation avec l'âge

```python
"stellar_activity_stats": {
    "with_activity_data": 0,
    "activity_levels": {
        "très active": 0,  # log R'HK > -4.5
        "active": 0,  # -4.5 à -4.75
        "modérée": 0,  # -4.75 à -5.0
        "calme": 0  # < -5.0
    }
}
```

### 7. Statistiques sur les Systèmes Multiples (Étoiles)

**Nombre d'Étoiles** (`sy_star_count`):

- Déjà partiellement implémenté, peut être enrichi

```python
"stellar_multiplicity_stats": {
    "single_stars": 0,
    "binary_systems": 0,
    "triple_systems": 0,
    "higher_order_systems": 0
}
```

## Recommandations d'Implémentation

### Priorité 1 (Impact Élevé)

1. **Statistiques sur l'âge stellaire** - Très utile scientifiquement
2. **Statistiques sur l'activité stellaire** - Important pour l'habitabilité
3. **Statistiques sur les lunes** - Rare mais intéressant

### Priorité 2 (Impact Modéré)

4. **Mouvement propre total** - Complète les données astrométriques
5. **Profondeur d'occultation** - Utile pour les observations

### Priorité 3 (Données Avancées)

6. **Coordonnées écliptiques** - Pour utilisateurs avancés
7. **Éphémérides orbitales** - Données techniques

## Exemple de Code

```python
def _update_star_age_stats(self, value: float, ranges_dict: dict[str, int]) -> None:
    """Catégorise l'âge stellaire (en milliards d'années)"""
    if value < 1:
        ranges_dict["< 1 Gyr"] += 1
    elif value < 5:
        ranges_dict["1-5 Gyr"] += 1
    elif value < 10:
        ranges_dict["5-10 Gyr"] += 1
    else:
        ranges_dict["> 10 Gyr"] += 1

def _update_stellar_activity_stats(self, value: float, levels_dict: dict[str, int]) -> None:
    """Catégorise l'activité chromosphérique (log R'HK)"""
    if value > -4.5:
        levels_dict["très active"] += 1
    elif value > -4.75:
        levels_dict["active"] += 1
    elif value > -5.0:
        levels_dict["modérée"] += 1
    else:
        levels_dict["calme"] += 1
```

## Impact sur les Statistiques Existantes

Les nouvelles données n'entrent **pas en conflit** avec les statistiques existantes. Elles les **complètent** :

- Les statistiques de métallicité peuvent maintenant être corrélées avec l'âge
- Les statistiques de distance peuvent être enrichies avec le mouvement propre
- Les statistiques de système peuvent inclure les lunes

## Conclusion

Oui, les statistiques peuvent être **significativement enrichies** avec nos nouvelles données ! Je recommande d'implémenter au minimum les statistiques de **Priorité 1** qui apportent le plus de valeur scientifique.
