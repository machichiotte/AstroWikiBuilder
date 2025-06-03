# src/mappers/exoplanet_mapping.py
from typing import List, Optional, Callable, Any
from dataclasses import dataclass
from enum import Enum

from src.models.data_source_exoplanet import DataSourceExoplanet


class FieldType(Enum):
    """Types de champs pour déterminer le formatage approprié"""

    SIMPLE = "simple"  # Valeur simple avec unité optionnelle
    SEPARATE_UNIT = "separate_unit"  # Champs nécessitant une ligne séparée pour l'unité
    CONSTELLATION = "constellation"  # Champ constellation calculé
    CARTE_UAI = "carte_uai"  # Carte UAI calculée


@dataclass
class FieldMapping:
    """Configuration pour mapper un champ Star vers l'infobox"""

    star_attribute: str
    infobox_field: str
    field_type: FieldType = FieldType.SIMPLE
    unit_override: Optional[str] = None  # Pour remplacer l'unité par défaut
    formatter: Optional[Callable[[Any], str]] = (
        None  # Fonction de formatage personnalisée
    )
    condition: Optional[Callable[[DataSourceExoplanet], bool]] = (
        None  # Condition pour inclure le champ
    )


class ExoplanetMappingConfig:
    """Configuration centralisée des mappings Exoplanets -> Infobox"""

    @classmethod
    def get_field_mappings(cls) -> List[FieldMapping]:
        """Retourne la liste complète des mappings de champs"""
        return [
            # Identifiants
            FieldMapping("name", "nom"),
            FieldMapping("image", "image"),
            FieldMapping("caption", "légende"),
            # ÉTOILE
            FieldMapping("star_name", "étoile"),
            FieldMapping("epoch_star", "époque étoile"),
            FieldMapping("right_ascension", "ascension droite"),
            FieldMapping("declination", "déclinaison"),
            FieldMapping("distance_general", "distance"),
            FieldMapping("constellation", "constellation", FieldType.CONSTELLATION),
            FieldMapping("carte_uai", "carte UAI", FieldType.CARTE_UAI),
            FieldMapping("spectral_type", "type spectral"),
            FieldMapping("apparent_magnitude", "magnitude apparente"),
            # PLANÈTE
            # Type
            FieldMapping("type", "type"),
            # Caractéristiques orbitales
            FieldMapping("semi_major_axis", "demi-grand axe", FieldType.SEPARATE_UNIT),
            FieldMapping(
                "argument_of_periastron", "périastre", FieldType.SEPARATE_UNIT
            ),
            FieldMapping("apoastron", "apoastre", FieldType.SEPARATE_UNIT),
            FieldMapping("eccentricity", "excentricité"),
            FieldMapping("period", "période", FieldType.SEPARATE_UNIT),
            FieldMapping("angular_distance", "distance angulaire"),
            FieldMapping("periastron_time", "t_peri"),
            FieldMapping("inclination", "inclinaison", FieldType.SEPARATE_UNIT),
            FieldMapping(
                "longitude_of_periastron", "arg_péri", FieldType.SEPARATE_UNIT
            ),
            FieldMapping("epoch", "époque"),
            # Caractéristiques physiques
            FieldMapping("mass", "masse", FieldType.SEPARATE_UNIT),
            FieldMapping("minimum_mass", "masse minimale", FieldType.SEPARATE_UNIT),
            FieldMapping("radius", "rayon", FieldType.SEPARATE_UNIT),
            FieldMapping("density", "masse volumique", FieldType.SEPARATE_UNIT),
            FieldMapping("surface_gravity", "gravité", FieldType.SEPARATE_UNIT),
            FieldMapping(
                "rotation_period", "période de rotation", FieldType.SEPARATE_UNIT
            ),
            FieldMapping("temperature", "température", FieldType.SEPARATE_UNIT),
            FieldMapping("albedo_bond", "albedo_bond"),
            # Atmosphère
            FieldMapping("pression", "pression"),
            FieldMapping("composition", "composition"),
            FieldMapping("wind_speed", "vitesse des vents"),
            # Découverte
            FieldMapping("discoverers", "découvreurs"),
            FieldMapping("program", "programme"),
            FieldMapping("method", "méthode"),
            FieldMapping("discovery_date", "date"),
            FieldMapping("discovery_site", "lieu"),
            FieldMapping("pre_discovery", "prédécouverte"),
            FieldMapping("detection_type", "détection"),
            FieldMapping("status", "statut"),
            # Informations supplémentaires
            FieldMapping("other_names", "autres noms"),
        ]
