# src/utils/formatters/infobox_fields.py
from typing import List, Optional, Callable, Any, Union
from dataclasses import dataclass
from enum import Enum

from src.models.data_sources.exoplanet_source import DataSourceExoplanet
from src.models.data_sources.star_source import DataSourceStar


class FieldType(Enum):
    """Types de champs pour déterminer le formatage approprié"""

    SIMPLE = "simple"  # Valeur simple avec unité optionnelle


@dataclass
class FieldMapping:
    """Configuration pour mapper un champ de source de données vers l'infobox"""

    source_attribute: str  # Attribut de DataSourceExoplanet ou DataSourceStar
    infobox_field: str
    field_type: FieldType = FieldType.SIMPLE
    default_unit: Optional[str] = None  # Unité par défaut pour ce champ
    unit_override: Optional[str] = None  # Pour remplacer l'unité par défaut
    formatter: Optional[Callable[[Any], str]] = (
        None  # Fonction de formatage personnalisée
    )
    condition: Optional[
        Callable[[Union[DataSourceExoplanet, DataSourceStar]], bool]
    ] = None  # Condition pour inclure le champ


class InfoboxMapper:
    """Configuration centralisée des mappings de sources de données -> Infobox"""

    @classmethod
    def get_exoplanet_field_mappings(cls) -> List[FieldMapping]:
        """Retourne la liste complète des mappings de champs pour les exoplanètes"""
        return [
            # Identifiants
            FieldMapping("name", "nom"),
            FieldMapping("pl_altname", "autres noms"),
            FieldMapping("image", "image"),
            FieldMapping("caption", "légende"),
            # Étoile hôte
            FieldMapping("st_name", "étoile"),
            FieldMapping("st_epoch", "époque étoile"),
            FieldMapping("st_right_ascension", "ascension droite"),
            FieldMapping("st_declination", "déclinaison"),
            FieldMapping("st_distance", "distance"),
            FieldMapping("st_constellation", "constellation"),
            FieldMapping("st_constellation", "carte UAI"),
            FieldMapping("st_spectral_type", "type spectral"),
            FieldMapping("st_apparent_magnitude", "magnitude apparente"),
            # Caractéristiques orbitales
            FieldMapping(
                "pl_semi_major_axis",
                "demi-grand axe",
                default_unit="unités astronomiques",
            ),
            FieldMapping(
                "pl_periastron", "périastre", default_unit="unités astronomiques"
            ),
            FieldMapping(
                "pl_apoastron", "apoastre", default_unit="unités astronomiques"
            ),
            FieldMapping("pl_eccentricity", "excentricité"),
            FieldMapping("pl_orbital_period", "période", default_unit="jours"),
            FieldMapping("pl_angular_distance", "distance angulaire"),
            FieldMapping("pl_periastron_time", "t_peri"),
            FieldMapping("pl_inclination", "inclinaison"),
            FieldMapping("pl_argument_of_periastron", "arg_péri"),
            FieldMapping("pl_epoch", "époque"),
            # Caractéristiques physiques
            FieldMapping("pl_mass", "masse", default_unit="masses joviennes"),
            FieldMapping(
                "pl_minimum_mass", "masse minimale", default_unit="masses joviennes"
            ),
            FieldMapping("pl_radius", "rayon", default_unit="rayons joviens"),
            FieldMapping(
                "pl_density",
                "masse volumique",
                default_unit="kilogrammes par mètre cube",
            ),
            FieldMapping(
                "pl_gravity", "gravité", default_unit="mètres par seconde carrée"
            ),
            FieldMapping(
                "pl_rotation_period", "période de rotation", default_unit="heures"
            ),
            FieldMapping("pl_temperature", "température", default_unit="kelvins"),
            FieldMapping("pl_albedo_bond", "albedo_bond"),
            # Atmosphère
            FieldMapping("pl_pressure", "pression"),
            FieldMapping("pl_composition", "composition"),
            FieldMapping("pl_wind_speed", "vitesse des vents"),
            # Découverte
            FieldMapping("disc_by", "découvreurs"),
            FieldMapping("disc_program", "programme"),
            FieldMapping("disc_method", "méthode"),
            FieldMapping("disc_year", "date"),
            FieldMapping("disc_facility", "lieu"),
            FieldMapping("pre_discovery", "prédécouverte"),
            FieldMapping("detection_type", "détection"),
            FieldMapping("status", "statut"),
        ]

    @classmethod
    def get_star_field_mappings(cls) -> List[FieldMapping]:
        """Retourne la liste complète des mappings de champs pour les étoiles"""
        return [
            # Identifiants
            FieldMapping("st_name", "nom"),
            FieldMapping("st_image", "image"),
            FieldMapping("st_upright", "upright"),
            FieldMapping("st_caption", "légende"),
            FieldMapping("st_coord_title", "coord titre"),
            FieldMapping("st_altname", "désignations"),
            # Champs calculés
            FieldMapping("st_constellation", "constellation"),
            FieldMapping("st_constellation", "carte UAI"),
            # Données d'observation
            FieldMapping("st_epoch", "époque"),
            FieldMapping("st_right_ascension", "ascension droite"),
            FieldMapping("st_right_ascension_2", "ascension droite 2"),
            FieldMapping("st_declination", "déclinaison"),
            FieldMapping("st_declination_2", "déclinaison 2"),
            FieldMapping("st_radial_velocity", "vitesse radiale"),
            FieldMapping("st_radial_velocity_2", "vitesse radiale 2"),
            FieldMapping("st_proper_motion_ra_2", "mouvement propre ad 2"),
            FieldMapping("st_proper_motion_dec", "mouvement propre déc"),
            FieldMapping("st_proper_motion_dec_2", "mouvement propre déc 2"),
            FieldMapping("st_parallax", "parallaxe"),
            FieldMapping("st_parallax_2", "parallaxe 2"),
            FieldMapping("st_distance", "distance"),
            FieldMapping("st_distance_2", "distance 2"),
            # Caractéristiques spectroscopiques et photométriques
            FieldMapping("st_spectral_type", "type spectral"),
            FieldMapping("st_spectral_type_2", "type spectral 2"),
            # Magnitudes apparentes
            FieldMapping("st_mag_u", "magnitude apparente bande U"),
            FieldMapping("st_mag_u_2", "magnitude apparente bande U 2"),
            FieldMapping("st_mag_b", "magnitude apparente bande B"),
            FieldMapping("st_mag_b_2", "magnitude apparente bande B 2"),
            FieldMapping("st_mag_v", "magnitude apparente bande V"),
            FieldMapping("st_mag_v_2", "magnitude apparente bande V 2"),
            FieldMapping("st_mag_g", "magnitude apparente bande G"),
            FieldMapping("st_mag_g_2", "magnitude apparente bande G 2"),
            FieldMapping("st_mag_r", "magnitude apparente bande R"),
            FieldMapping("st_mag_r_2", "magnitude apparente bande R 2"),
            FieldMapping("st_mag_i", "magnitude apparente bande I"),
            FieldMapping("st_mag_i_2", "magnitude apparente bande I 2"),
            FieldMapping("st_mag_j", "magnitude apparente bande J"),
            FieldMapping("st_mag_j_2", "magnitude apparente bande J 2"),
            FieldMapping("st_mag_h", "magnitude apparente bande H"),
            FieldMapping("st_mag_h_2", "magnitude apparente bande H 2"),
            FieldMapping("st_mag_k", "magnitude apparente bande K"),
            FieldMapping("st_mag_k_2", "magnitude apparente bande K 2"),
            # Indices de couleur
            FieldMapping("st_u_b_color", "u-b"),
            FieldMapping("st_u_b_color_2", "u-b 2"),
            FieldMapping("st_b_v_color", "b-v"),
            FieldMapping("st_b_v_color_2", "b-v 2"),
            FieldMapping("st_v_r_color", "v-r"),
            FieldMapping("st_v_r_color_2", "v-r 2"),
            FieldMapping("st_r_i_color", "r-i"),
            FieldMapping("st_r_i_color_2", "r-i 2"),
            FieldMapping("st_j_k_color", "j-k"),
            FieldMapping("st_j_k_color_2", "j-k 2"),
            FieldMapping("st_j_h_color", "j-h"),
            FieldMapping("st_j_h_color_2", "j-h 2"),
            FieldMapping("st_absolute_magnitude", "magnitude absolue"),
            FieldMapping("st_absolute_magnitude_2", "magnitude absolue 2"),
            FieldMapping("st_variability", "variabilité"),
            FieldMapping("st_variability_2", "variabilité 2"),
            # Caractéristiques physiques
            FieldMapping("st_mass", "masse"),
            FieldMapping("st_mass_2", "masse 2"),
            FieldMapping("st_radius", "rayon"),
            FieldMapping("st_radius_2", "rayon 2"),
            FieldMapping("st_density", "masse volumique"),
            FieldMapping("st_density_2", "masse volumique 2"),
            FieldMapping("st_luminosity", "luminosité"),
            FieldMapping("st_luminosity_2", "luminosité 2"),
            FieldMapping("st_surface_gravity", "gravité"),
            FieldMapping("st_surface_gravity_2", "gravité 2"),
            FieldMapping("st_temperature", "température"),
            FieldMapping("st_temperature_2", "température 2"),
            FieldMapping("st_metallicity", "métallicité"),
            FieldMapping("st_metallicity_2", "métallicité 2"),
            FieldMapping("st_rotation", "rotation"),
            FieldMapping("st_rotation_2", "rotation 2"),
            FieldMapping("st_age", "âge"),
            FieldMapping("st_age_2", "âge 2"),
            FieldMapping("st_evolutionary_stage", "stade évolutif"),
            FieldMapping("st_evolutionary_stage_2", "stade évolutif 2"),
            # Système stellaire
            FieldMapping("st_stellar_components", "composantes stellaires"),
            FieldMapping("st_companion", "compagnon"),
            FieldMapping("st_planets", "planètes"),
            # Éléments orbitaux binaires
            FieldMapping("st_semi_major_axis", "demi-grand axe"),
            FieldMapping("st_eccentricity", "excentricité"),
            FieldMapping("st_period", "période"),
            FieldMapping("st_inclination", "inclinaison"),
            FieldMapping("st_argument_of_periapsis", "argument"),
            FieldMapping("st_argument_of_periapsis_2", "argument 2"),
            FieldMapping("st_longitude_of_ascending_node", "nœud"),
            FieldMapping("st_epoch_binary", "époque binaire"),
            FieldMapping("st_semi_amplitude_1", "demi-amplitude"),
            FieldMapping("st_semi_amplitude_2", "demi-amplitude 2"),
        ]
