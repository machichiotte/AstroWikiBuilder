# src/utils/formatters/infobox_fields.py
from typing import List, Optional, Callable, Any, Union
from dataclasses import dataclass
from enum import Enum

from src.models.data_source_exoplanet import DataSourceExoplanet
from src.models.data_source_star import DataSourceStar


class FieldType(Enum):
    """Types de champs pour déterminer le formatage approprié"""

    SIMPLE = "simple"  # Valeur simple avec unité optionnelle
    SEPARATE_UNIT = "separate_unit"  # Champs nécessitant une ligne séparée pour l'unité
    CONSTELLATION = "constellation"  # Champ constellation calculé
    CARTE_UAI = "carte_uai"  # Carte UAI calculée

@dataclass
class FieldMapping:
    """Configuration pour mapper un champ de source de données vers l'infobox"""

    source_attribute: str  # Attribut de DataSourceExoplanet ou DataSourceStar
    infobox_field: str
    field_type: FieldType = FieldType.SIMPLE
    default_unit: Optional[str] = None # Unité par défaut pour ce champ
    unit_override: Optional[str] = None  # Pour remplacer l'unité par défaut
    formatter: Optional[Callable[[Any], str]] = (
        None  # Fonction de formatage personnalisée
    )
    condition: Optional[Callable[[Union[DataSourceExoplanet, DataSourceStar]], bool]] = (
        None  # Condition pour inclure le champ
    )


class InfoboxMapper:
    """Configuration centralisée des mappings de sources de données -> Infobox"""

    @classmethod
    def get_exoplanet_field_mappings(cls) -> List[FieldMapping]:
        """Retourne la liste complète des mappings de champs pour les exoplanètes"""
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
            FieldMapping("semi_major_axis", "demi-grand axe", FieldType.SEPARATE_UNIT, default_unit="unités astronomiques"),
            FieldMapping(
                "argument_of_periastron", "périastre", FieldType.SEPARATE_UNIT, default_unit="unités astronomiques"
            ),
            FieldMapping("apoastron", "apoastre", FieldType.SEPARATE_UNIT, default_unit="unités astronomiques"),
            FieldMapping("eccentricity", "excentricité"),
            FieldMapping("period", "période", FieldType.SEPARATE_UNIT, default_unit="jours"),
            FieldMapping("angular_distance", "distance angulaire"),
            FieldMapping("periastron_time", "t_peri"),
            FieldMapping("inclination", "inclinaison", FieldType.SEPARATE_UNIT), # Pas d'unité par défaut spécifiée dans les notes pour inclinaison
            FieldMapping(
                "longitude_of_periastron", "arg_péri", FieldType.SEPARATE_UNIT # Pas d'unité par défaut spécifiée dans les notes pour arg_péri
            ),
            FieldMapping("epoch", "époque"),
            # Caractéristiques physiques
            FieldMapping("mass", "masse", FieldType.SEPARATE_UNIT, default_unit="masses joviennes"),
            FieldMapping("minimum_mass", "masse minimale", FieldType.SEPARATE_UNIT, default_unit="masses joviennes"),
            FieldMapping("radius", "rayon", FieldType.SEPARATE_UNIT, default_unit="rayons joviens"),
            FieldMapping("density", "masse volumique", FieldType.SEPARATE_UNIT, default_unit="kilogrammes par mètre cube"),
            FieldMapping("surface_gravity", "gravité", FieldType.SEPARATE_UNIT, default_unit="mètres par seconde carrée"),
            FieldMapping(
                "rotation_period", "période de rotation", FieldType.SEPARATE_UNIT, default_unit="heures"
            ),
            FieldMapping("temperature", "température", FieldType.SEPARATE_UNIT, default_unit="kelvins"),
            FieldMapping("albedo_bond", "albedo_bond"),
            # Atmosphère
            FieldMapping("pression", "pression"),
            FieldMapping("composition", "composition"),
            FieldMapping("wind_speed", "vitesse des vents"),
            # Découverte
            FieldMapping("discoverers", "découvreurs"),
            FieldMapping("program", "programme"),
            FieldMapping("discovery_method", "méthode"),
            FieldMapping("discovery_date", "date"),
            FieldMapping("discovery_site", "lieu"),
            FieldMapping("pre_discovery", "prédécouverte"),
            FieldMapping("detection_type", "détection"),
            FieldMapping("status", "statut"),
            # Informations supplémentaires
            FieldMapping("other_names", "autres noms"),
        ]

    @classmethod
    def get_star_field_mappings(cls) -> List[FieldMapping]:
        """Retourne la liste complète des mappings de champs pour les étoiles"""
        return [
            # Identifiants
            FieldMapping("name", "nom"),
            FieldMapping("image", "image"),
            FieldMapping("upright", "upright"),
            FieldMapping("caption", "légende"),
            FieldMapping("coord_title", "coord titre"),
            FieldMapping("designations", "désignations"),
            # Champs calculés
            FieldMapping("constellation", "constellation", FieldType.CONSTELLATION),
            FieldMapping("carte_uai", "carte UAI", FieldType.CARTE_UAI),
            # Données d'observation
            FieldMapping("epoch", "époque"),
            FieldMapping("right_ascension", "ascension droite"),
            FieldMapping("right_ascension_2", "ascension droite 2"),
            FieldMapping("declination", "déclinaison"),
            FieldMapping("declination_2", "déclinaison 2"),
            FieldMapping("radial_velocity", "vitesse radiale", FieldType.SEPARATE_UNIT),
            FieldMapping(
                "radial_velocity_2", "vitesse radiale 2", FieldType.SEPARATE_UNIT
            ),
            FieldMapping(
                "proper_motion_ra", "mouvement propre ad", FieldType.SEPARATE_UNIT
            ),
            FieldMapping(
                "proper_motion_ra_2", "mouvement propre ad 2", FieldType.SEPARATE_UNIT
            ),
            FieldMapping(
                "proper_motion_dec", "mouvement propre déc", FieldType.SEPARATE_UNIT
            ),
            FieldMapping(
                "proper_motion_dec_2", "mouvement propre déc 2", FieldType.SEPARATE_UNIT
            ),
            FieldMapping("parallax", "parallaxe", FieldType.SEPARATE_UNIT),
            FieldMapping("parallax_2", "parallaxe 2", FieldType.SEPARATE_UNIT),
            FieldMapping("distance_general", "distance"),
            FieldMapping("distance_general_2", "distance 2"),
            # Caractéristiques spectroscopiques et photométriques
            FieldMapping("spectral_type", "type spectral"),
            FieldMapping("spectral_type_2", "type spectral 2"),
            # Magnitudes apparentes
            FieldMapping("apparent_magnitude_u_band", "magnitude apparente bande U"),
            FieldMapping(
                "apparent_magnitude_u_band_2", "magnitude apparente bande U 2"
            ),
            FieldMapping("apparent_magnitude_b_band", "magnitude apparente bande B"),
            FieldMapping(
                "apparent_magnitude_b_band_2", "magnitude apparente bande B 2"
            ),
            FieldMapping("apparent_magnitude_v_band", "magnitude apparente bande V"),
            FieldMapping(
                "apparent_magnitude_v_band_2", "magnitude apparente bande V 2"
            ),
            FieldMapping("apparent_magnitude_g_band", "magnitude apparente bande G"),
            FieldMapping(
                "apparent_magnitude_g_band_2", "magnitude apparente bande G 2"
            ),
            FieldMapping("apparent_magnitude_r_band", "magnitude apparente bande R"),
            FieldMapping(
                "apparent_magnitude_r_band_2", "magnitude apparente bande R 2"
            ),
            FieldMapping("apparent_magnitude_i_band", "magnitude apparente bande I"),
            FieldMapping(
                "apparent_magnitude_i_band_2", "magnitude apparente bande I 2"
            ),
            FieldMapping("apparent_magnitude_j_band", "magnitude apparente bande J"),
            FieldMapping(
                "apparent_magnitude_j_band_2", "magnitude apparente bande J 2"
            ),
            FieldMapping("apparent_magnitude_h_band", "magnitude apparente bande H"),
            FieldMapping(
                "apparent_magnitude_h_band_2", "magnitude apparente bande H 2"
            ),
            FieldMapping("apparent_magnitude_k_band", "magnitude apparente bande K"),
            FieldMapping(
                "apparent_magnitude_k_band_2", "magnitude apparente bande K 2"
            ),
            # Indices de couleur
            FieldMapping("u_b_color", "u-b"),
            FieldMapping("u_b_color_2", "u-b 2"),
            FieldMapping("b_v_color", "b-v"),
            FieldMapping("b_v_color_2", "b-v 2"),
            FieldMapping("v_r_color", "v-r"),
            FieldMapping("v_r_color_2", "v-r 2"),
            FieldMapping("r_i_color", "r-i"),
            FieldMapping("r_i_color_2", "r-i 2"),
            FieldMapping("j_k_color", "j-k"),
            FieldMapping("j_k_color_2", "j-k 2"),
            FieldMapping("j_h_color", "j-h"),
            FieldMapping("j_h_color_2", "j-h 2"),
            FieldMapping("absolute_magnitude", "magnitude absolue"),
            FieldMapping("absolute_magnitude_2", "magnitude absolue 2"),
            FieldMapping("variability", "variabilité"),
            FieldMapping("variability_2", "variabilité 2"),
            # Caractéristiques physiques
            FieldMapping("mass", "masse", FieldType.SEPARATE_UNIT),
            FieldMapping("mass_2", "masse 2", FieldType.SEPARATE_UNIT),
            FieldMapping("radius", "rayon", FieldType.SEPARATE_UNIT),
            FieldMapping("radius_2", "rayon 2", FieldType.SEPARATE_UNIT),
            FieldMapping("density", "masse volumique", FieldType.SEPARATE_UNIT),
            FieldMapping("density_2", "masse volumique 2", FieldType.SEPARATE_UNIT),
            FieldMapping("luminosity", "luminosité", FieldType.SEPARATE_UNIT),
            FieldMapping("luminosity_2", "luminosité 2", FieldType.SEPARATE_UNIT),
            FieldMapping("surface_gravity", "gravité", FieldType.SEPARATE_UNIT),
            FieldMapping("surface_gravity_2", "gravité 2", FieldType.SEPARATE_UNIT),
            FieldMapping("temperature", "température", FieldType.SEPARATE_UNIT),
            FieldMapping("temperature_2", "température 2", FieldType.SEPARATE_UNIT),
            FieldMapping("metallicity", "métallicité"),
            FieldMapping("metallicity_2", "métallicité 2"),
            FieldMapping("rotation", "rotation", FieldType.SEPARATE_UNIT),
            FieldMapping("rotation_2", "rotation 2", FieldType.SEPARATE_UNIT),
            FieldMapping("age", "âge"),
            FieldMapping("age_2", "âge 2"),
            FieldMapping("evolutionary_stage", "stade évolutif"),
            FieldMapping("evolutionary_stage_2", "stade évolutif 2"),
            # Système stellaire
            FieldMapping("stellar_components", "composantes stellaires"),
            FieldMapping("companion", "compagnon"),
            FieldMapping("planets", "planètes"),
            # Éléments orbitaux binaires
            FieldMapping("semi_major_axis", "demi-grand axe", FieldType.SEPARATE_UNIT),
            FieldMapping("eccentricity", "excentricité"),
            FieldMapping("period", "période", FieldType.SEPARATE_UNIT),
            FieldMapping("inclination", "inclinaison", FieldType.SEPARATE_UNIT),
            FieldMapping("argument_of_periapsis", "argument", FieldType.SEPARATE_UNIT),
            FieldMapping(
                "argument_of_periapsis_2", "argument 2", FieldType.SEPARATE_UNIT
            ),
            FieldMapping(
                "longitude_of_ascending_node", "nœud", FieldType.SEPARATE_UNIT
            ),
            FieldMapping("epoch_binary", "époque binaire"),
            FieldMapping("semi_amplitude_1", "demi-amplitude"),
            FieldMapping("semi_amplitude_2", "demi-amplitude 2"),
        ]