# astro_wiki/src/constants/field_mappings.py

NOTES_FIELDS_EXOPLANET = [
    "époque étoile", "ascension droite", "déclinaison", "distance", "constellation",
    "type spectral", "magnitude apparente", "type", "demi-grand axe", "périastre",
    "apoastre", "excentricité", "période", "distance angulaire", "t_peri", "inclinaison",
    "arg_péri", "époque", "masse", "masse minimale", "rayon", "masse volumique",
    "gravité", "période de rotation", "température", "albedo_bond", "pression",
    "composition", "vitesse des vents", "découvreurs", "programme", "méthode", "date",
    "lieu", "prédécouverte", "détection", "statut"
]

NOTES_FIELDS_STAR = [
    "époque", "ascension droite", "déclinaison", "distance", "constellation", "carte UAI",
    "type spectral", "classe de luminosité", "magnitude apparente", "magnitude absolue",
    "magnitude bolométrique", "indice de couleur B-V", "indice de couleur U-B",
    "indice de couleur V-R", "indice de couleur R-I", "indice de couleur J-H",
    "indice de couleur H-K", "mouvement propre", "parallaxe", "vitesse radiale",
    "métallicité", "masse", "rayon", "luminosité", "température", "gravité", "âge",
    "rotation", "vitesse de rotation", "densité", "excentricité", "période orbitale",
    "inclinaison", "argument du périastre", "nœud ascendant", "compagne", "variabilité",
    "découverte", "désignations", "statut"
]

FIELD_DEFAULT_UNITS_STAR: dict[str, str] = {
    "mass": "M☉",                  # Masse solaire
    "radius": "R☉",                # Rayon solaire
    "luminosity": "L☉",            # Luminosité solaire
    "temperature": "K",            # Kelvin
    "gravity": "log g",            # Gravité logarithmique
    "metallicity": "[Fe/H]",       # Métallicité
    "age": "Ga",                   # Gigannées
    "rotation": "j",               # Jours
    "distance": "al",              # Années-lumière (courant sur Wiki fr)
    "parallax": "mas",             # Millisecondes d'arc
    "spectral type": "",           # Sans unité
    "apparent magnitude": "",      # Sans unité
    "absolute magnitude": "",      # Sans unité
}

FIELD_DEFAULT_UNITS_EXOPLANET: dict[str, str] = {
    "mass": "MJ",                  # Masse de Jupiter
    "minimum mass": "MJ",          # Masse de Jupiter
    "radius": "RJ",                # Rayon de Jupiter
    "semi-major axis": "ua",       # Unité astronomique
    "eccentricity": "",            # Sans unité
    "period": "j",                 # Jours
    "inclination": "°",            # Degrés
    "periastron": "ua",            # UA
    "apoastron": "ua",             # UA
    "temperature": "K",            # Kelvin
    "discovery year": "",          # Sans unité
    "detection method": "",        # Sans unité
    "rotation period": "h",        # Heures (si connue)
    "density": "g/cm³",            # g/cm³ selon les conventions fr
    "gravity": "m/s²",             # m/s²
    "argument of periastron": "°",  # Degrés
}

# Champs pour lesquels un lien direct vers un article Wikipédia doit être généré
WIKILINK_FIELDS_DIRECT: list[str] = [
    "étoile",
    "constellation",
    "programme",
    "lieu",
    # Ex: "programme": "Programme Kepler" -> [[Programme Kepler]]
    # Ex: "lieu": "Observatoire de La Silla" -> [[Observatoire de La Silla]]
]

# Dictionnaire pour traduire les méthodes de découverte et lier vers l'article FR
# Les clés sont les valeurs attendues de la source de données (en anglais, normalisées en minuscules)
METHOD_NAME_MAPPING: dict[str, str] = {
    "transit": {"display": "Transits", "article": "Méthode des transits"},
    "radial velocity": {
        "display": "Vitesses radiales",
        "article": "Méthode des vitesses radiales",
    },
    "imaging": {
        "display": "Imagerie directe",
        "article": "Imagerie directe des exoplanètes",
    },
    "microlensing": {
        "display": "Microlentille gravitationnelle",
        "article": "Microlentille gravitationnelle",
    },
    "gravitational microlensing": {
        "display": "Microlentille gravitationnelle",
        "article": "Microlentille gravitationnelle",
    },
    "timing": {
        "display": "Variations de chronométrage",
        "article": "Chronométrage (astronomie)",
    },
    "pulsar timing": {
        "display": "Chronométrage de pulsar",
        "article": "Détection des exoplanètes par chronométrage de pulsar",
    },
    "transit timing variations": {
        "display": "Variation du moment de transit",
        "article": "Variation du moment de transit",
    },
    "ttv": {
        "display": "Variation du moment de transit",
        "article": "Variation du moment de transit",
    },
    "astrometry": {"display": "Astrométrie", "article": "Astrométrie"},
    # Ajoutez d'autres méthodes ici au besoin
    # "primary transit": { # Si vos données ont des variantes
    # "display": "Transits (primaire)",
    # "article": "Méthode des transits"
    # }
}

LIEU_NAME_MAPPING = {
    "Cerro Tololo Inter-American Observatory": "Observatoire interaméricain du Cerro Tololo",
    "Keck Observatory": "Observatoire W. M. Keck",
    "La Silla Observatory": "Observatoire de La Silla",
}


CONSTELLATION_FR: dict[str, str] = {
    "Andromeda": "Andromède",
    "Antlia": "Machine pneumatique",
    "Apus": "Oiseau de paradis",
    "Aquarius": "Verseau",
    "Aquila": "Aigle",
    "Ara": "Autel",
    "Aries": "Bélier",
    "Auriga": "Cocher",
    "Boötes": "Bouvier",
    "Caelum": "Burin",
    "Camelopardalis": "Girafe",
    "Cancer": "Cancer",
    "Canes Venatici": "Chiens de chasse",
    "Canis Major": "Grand Chien",
    "Canis Minor": "Petit Chien",
    "Capricornus": "Capricorne",
    "Carina": "Carène",
    "Cassiopeia": "Cassiopée",
    "Centaurus": "Centaure",
    "Cepheus": "Céphée",
    "Cetus": "Baleine",
    "Chamaeleon": "Caméléon",
    "Chamaleon": "Caméléon",
    "Circinus": "Compas",
    "Columba": "Colombe",
    "Coma Berenices": "Chevelure de Bérénice",
    "Corona Australis": "Couronne australe",
    "Corona Borealis": "Couronne boréale",
    "Corvus": "Corbeau",
    "Crater": "Cratère",
    "Crux": "Croix du Sud",
    "Cygnus": "Cygne",
    "Delphinus": "Dauphin",
    "Dorado": "Poisson doré",
    "Draco": "Dragon",
    "Equuleus": "Petit Cheval",
    "Eridanus": "Éridan",
    "Fornax": "Fourneau",
    "Gemini": "Gémeaux",
    "Grus": "Grue",
    "Hercules": "Hercule",
    "Horologium": "Horloge",
    "Hydra": "Hydre femelle",
    "Hydrus": "Hydre mâle",
    "Indus": "Indien",
    "Lacerta": "Lézard",
    "Leo": "Lion",
    "Leo Minor": "Petit Lion",
    "Lepus": "Lièvre",
    "Libra": "Balance",
    "Lupus": "Loup",
    "Lynx": "Lynx",
    "Lyra": "Lyre",
    "Mensa": "Table",
    "Microscopium": "Microscope",
    "Monoceros": "Licorne",
    "Musca": "Mouche",
    "Norma": "Règle",
    "Octans": "Octant",
    "Ophiuchus": "Serpentaire",
    "Orion": "Orion",
    "Pavo": "Paon",
    "Pegasus": "Pégase",
    "Perseus": "Persée",
    "Phoenix": "Phénix",
    "Pictor": "Peintre",
    "Pisces": "Poissons",
    "Piscis Austrinus": "Poisson austral",
    "Puppis": "Poupe",
    "Pyxis": "Boussole",
    "Reticulum": "Réticule",
    "Sagitta": "Flèche",
    "Sagittarius": "Sagittaire",
    "Scorpius": "Scorpion",
    "Sculptor": "Sculpteur",
    "Scutum": "Écu",
    "Serpens": "Serpent",
    "Sextans": "Sextant",
    "Taurus": "Taureau",
    "Telescopium": "Télescope",
    "Triangulum": "Triangle",
    "Triangulum Australe": "Triangle austral",
    "Tucana": "Toucan",
    "Ursa Major": "Grande Ourse",
    "Ursa Minor": "Petite Ourse",
    "Vela": "Voile",
    "Virgo": "Vierge",
    "Volans": "Poisson volant",
    "Vulpecula": "Petit Renard",
}

# Mapping des genres pour chaque constellation française
CONSTELLATION_GENDER: dict[str, str] = {
    "Andromède": "f",
    "Machine pneumatique": "f",
    "Oiseau de paradis": "m",
    "Verseau": "m",
    "Aigle": "m",
    "Autel": "m",
    "Bélier": "m",
    "Cocher": "m",
    "Bouvier": "m",
    "Burin": "m",
    "Girafe": "f",
    "Cancer": "m",
    "Chiens de chasse": "m",
    "Grand Chien": "m",
    "Petit Chien": "m",
    "Capricorne": "m",
    "Carène": "f",
    "Cassiopée": "f",
    "Centaure": "m",
    "Céphée": "m",
    "Baleine": "f",
    "Caméléon": "m",
    "Compas": "m",
    "Colombe": "f",
    "Chevelure de Bérénice": "f",
    "Couronne australe": "f",
    "Couronne boréale": "f",
    "Corbeau": "m",
    "Cratère": "m",
    "Croix du Sud": "f",
    "Cygne": "m",
    "Dauphin": "m",
    "Poisson doré": "m",
    "Dragon": "m",
    "Petit Cheval": "m",
    "Éridan": "m",
    "Fourneau": "m",
    "Gémeaux": "m",
    "Grue": "f",
    "Hercule": "m",
    "Horloge": "f",
    "Hydre femelle": "f",
    "Hydre mâle": "f",
    "Indien": "m",
    "Lézard": "m",
    "Lion": "m",
    "Petit Lion": "m",
    "Lièvre": "m",
    "Balance": "f",
    "Loup": "m",
    "Lynx": "m",
    "Lyre": "f",
    "Table": "f",
    "Microscope": "m",
    "Licorne": "f",
    "Mouche": "f",
    "Règle": "f",
    "Octant": "m",
    "Serpentaire": "m",
    "Orion": "m",
    "Paon": "m",
    "Pégase": "m",
    "Persée": "m",
    "Phénix": "m",
    "Peintre": "m",
    "Poissons": "m",
    "Poisson austral": "m",
    "Poupe": "f",
    "Boussole": "f",
    "Réticule": "m",
    "Flèche": "f",
    "Sagittaire": "m",
    "Scorpion": "m",
    "Sculpteur": "m",
    "Écu": "m",
    "Serpent": "m",
    "Sextant": "m",
    "Taureau": "m",
    "Télescope": "m",
    "Triangle": "m",
    "Triangle austral": "m",
    "Toucan": "m",
    "Grande Ourse": "f",
    "Petite Ourse": "f",
    "Voile": "f",
    "Vierge": "f",
    "Poisson volant": "m",
    "Petit Renard": "m",
}

# Descriptions des types spectraux selon Morgan-Keenan
SPECTRAL_TYPE_DESCRIPTIONS: dict[str, str] = {
    "O": "étoile bleue de type O",
    "B": "étoile bleue de type B",
    "A": "étoile blanche de type A",
    "F": "étoile jaune-blanc de la séquence principale",
    "G": "naine jaune",
    "K": "naine orange",
    "M": "naine rouge",
    "L": "naine brune de type L",
    "T": "naine brune de type T",
    "Y": "naine brune de type Y",
}

# Liens Wikipédia pour chaque "type d'astre" (en français)
SPECTRAL_TYPE_LINKS: dict[str, str] = {
    "O": "https://fr.wikipedia.org/wiki/%C3%89toile_bleue_de_la_s%C3%A9quence_principale",
    "B": "https://fr.wikipedia.org/wiki/%C3%89toile_bleu-blanc_de_la_s%C3%A9quence_principale",
    "A": "https://fr.wikipedia.org/wiki/%C3%89toile_blanche_de_la_s%C3%A9quence_principale",
    "F": "https://fr.wikipedia.org/wiki/%C3%89toile_jaune-blanc_de_la_s%C3%A9quence_principale",
    "G": "https://fr.wikipedia.org/wiki/Naine_jaune",
    "K": "https://fr.wikipedia.org/wiki/%C3%89toile_orange_de_la_s%C3%A9quence_principale",
    "M": "https://fr.wikipedia.org/wiki/%C3%89toile_rouge_de_la_s%C3%A9quence_principale",
    "L": "https://fr.wikipedia.org/wiki/Naine_brunne_L",
    "T": "https://fr.wikipedia.org/wiki/Naine_brune_T",
    "Y": "https://fr.wikipedia.org/wiki/Naine_brune_Y",
}
