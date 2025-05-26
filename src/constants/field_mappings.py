# astro_wiki/constants/field_mappings.py

# Unités par défaut associées aux champs physiques
FIELD_DEFAULT_UNITS: dict[str, str] = {
    "masse": "M_J", 
    "rayon": "R_J", 
    "température": "K", 
    "distance": "pc",
    "demi-grand axe": 
    "ua", "période": "j", 
    "inclinaison": "°", 
    "périastre": "ua",
    "apoastre": "ua", 
    "masse minimale": "M_J", 
    "masse volumique": "kg/m³",
    "gravité": "m/s²", 
    "période de rotation": "h", 
    "arg_péri": "°",
}

# Champs pour lesquels un lien direct vers un article Wikipédia doit être généré
WIKILINK_FIELDS_DIRECT: list[str] = [
     "étoile", 
     "constellation", 
     "programme", 
     "lieu"
        # Ex: "programme": "Programme Kepler" -> [[Programme Kepler]]
        # Ex: "lieu": "Observatoire de La Silla" -> [[Observatoire de La Silla]]
]

# Dictionnaire pour traduire les méthodes de découverte et lier vers l'article FR
# Les clés sont les valeurs attendues de la source de données (en anglais, normalisées en minuscules)
METHOD_NAME_MAPPING: dict[str, str] = {
    "transit": {
            "display": "Transits",
            "article": "Méthode des transits"
        },
        "radial velocity": {
            "display": "Vitesses radiales",
            "article": "Méthode des vitesses radiales"
        },
        "imaging": {
            "display": "Imagerie directe",
            "article": "Imagerie directe des exoplanètes" # ou "Imagerie directe" si plus générique
        },
        "microlensing": {
            "display": "Microlentille gravitationnelle",
            "article": "Microlentille gravitationnelle"
        },
        "gravitational microlensing": { # Au cas où la source utiliserait ce terme plus long
            "display": "Microlentille gravitationnelle",
            "article": "Microlentille gravitationnelle"
        },
        "timing": { # Terme générique, peut nécessiter plus de spécificité
            "display": "Variations de chronométrage",
            "article": "Chronométrage (astronomie)" # Exemple, à vérifier pour la pertinence
        },
        "pulsar timing": {
            "display": "Chronométrage de pulsar",
            "article": "Détection des exoplanètes par chronométrage de pulsar" # Titre d'article possible
        },
        "transit timing variations": {
            "display": "Variations du moment de transit",
            "article": "Mesure des variations de temps de transit" # TTV
        },
        "ttv": { # Acronyme commun pour Transit Timing Variations
            "display": "Variations du moment de transit (TTV)",
            "article": "Mesure des variations de temps de transit"
        },
        "astrometry": {
            "display": "Astrométrie",
            "article": "Astrométrie"
        },
        # Ajoutez d'autres méthodes ici au besoin
        # "primary transit": { # Si vos données ont des variantes
        # "display": "Transits (primaire)",
        # "article": "Méthode des transits"
        # }
}
