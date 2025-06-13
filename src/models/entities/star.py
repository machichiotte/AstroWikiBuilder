from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any

from .base_entity import BaseEntity
from ..references.reference import Reference
from ..references.data_point import DataPoint


@dataclass
class Star(BaseEntity):
    """Classe représentant une étoile hôte"""

    # Identifiants
    st_name: str = None
    st_altname: Optional[List[str]] = field(default_factory=list)
    st_image: Optional[DataPoint] = None
    st_upright: Optional[DataPoint] = None
    st_caption: Optional[DataPoint] = None
    st_coord_title: Optional[DataPoint] = None

    # Données d'observation
    st_epoch: Optional[DataPoint] = None
    st_right_ascension: Optional[DataPoint] = None
    st_right_ascension_2: Optional[DataPoint] = None
    st_declination: Optional[DataPoint] = None
    st_declination_2: Optional[DataPoint] = None
    st_radial_velocity: Optional[DataPoint] = None
    st_radial_velocity_2: Optional[DataPoint] = None
    st_proper_motion_ra: Optional[DataPoint] = None
    st_proper_motion_ra_2: Optional[DataPoint] = None
    st_proper_motion_dec: Optional[DataPoint] = None
    st_proper_motion_dec_2: Optional[DataPoint] = None
    st_parallax: Optional[DataPoint] = None
    st_parallax_2: Optional[DataPoint] = None
    st_distance_pc: Optional[DataPoint] = None
    st_distance_pc_2: Optional[DataPoint] = None
    st_distance_light_years: Optional[DataPoint] = None
    st_distance_light_years_2: Optional[DataPoint] = None
    st_distance: Optional[DataPoint] = None
    st_distance_2: Optional[DataPoint] = None

    # Caractéristiques spectroscopiques
    st_spectral_type: Optional[DataPoint] = None
    st_spectral_type_2: Optional[DataPoint] = None

    # Magnitudes
    st_apparent_magnitude: Optional[DataPoint] = None
    st_apparent_magnitude_2: Optional[DataPoint] = None
    st_mag_u: Optional[DataPoint] = None
    st_mag_u_2: Optional[DataPoint] = None
    st_mag_b: Optional[DataPoint] = None
    st_mag_b_2: Optional[DataPoint] = None
    st_mag_v: Optional[DataPoint] = None
    st_mag_v_2: Optional[DataPoint] = None
    st_mag_g: Optional[DataPoint] = None
    st_mag_g_2: Optional[DataPoint] = None
    st_mag_r: Optional[DataPoint] = None
    st_mag_r_2: Optional[DataPoint] = None
    st_mag_i: Optional[DataPoint] = None
    st_mag_i_2: Optional[DataPoint] = None
    st_mag_j: Optional[DataPoint] = None
    st_mag_j_2: Optional[DataPoint] = None
    st_mag_h: Optional[DataPoint] = None
    st_mag_h_2: Optional[DataPoint] = None
    st_mag_k: Optional[DataPoint] = None
    st_mag_k_2: Optional[DataPoint] = None

    # Indices de couleur
    st_u_b_color: Optional[DataPoint] = None
    st_u_b_color_2: Optional[DataPoint] = None
    st_b_v_color: Optional[DataPoint] = None
    st_b_v_color_2: Optional[DataPoint] = None
    st_v_r_color: Optional[DataPoint] = None
    st_v_r_color_2: Optional[DataPoint] = None
    st_r_i_color: Optional[DataPoint] = None
    st_r_i_color_2: Optional[DataPoint] = None
    st_j_k_color: Optional[DataPoint] = None
    st_j_k_color_2: Optional[DataPoint] = None
    st_j_h_color: Optional[DataPoint] = None
    st_j_h_color_2: Optional[DataPoint] = None
    st_absolute_magnitude: Optional[DataPoint] = None
    st_absolute_magnitude_2: Optional[DataPoint] = None

    # Caractéristiques physiques
    st_mass: Optional[DataPoint] = None
    st_mass_2: Optional[DataPoint] = None
    st_radius: Optional[DataPoint] = None
    st_radius_2: Optional[DataPoint] = None
    st_density: Optional[DataPoint] = None
    st_density_2: Optional[DataPoint] = None
    st_luminosity: Optional[DataPoint] = None
    st_luminosity_2: Optional[DataPoint] = None
    st_surface_gravity: Optional[DataPoint] = None
    st_surface_gravity_2: Optional[DataPoint] = None
    st_temperature: Optional[DataPoint] = None
    st_temperature_2: Optional[DataPoint] = None
    st_metallicity: Optional[DataPoint] = None
    st_metallicity_2: Optional[DataPoint] = None
    st_rotation: Optional[DataPoint] = None
    st_rotation_2: Optional[DataPoint] = None
    st_age: Optional[DataPoint] = None
    st_age_2: Optional[DataPoint] = None
    st_evolutionary_stage: Optional[DataPoint] = None
    st_evolutionary_stage_2: Optional[DataPoint] = None
    st_variability: Optional[DataPoint] = None
    st_variability_2: Optional[DataPoint] = None

    # Système stellaire
    st_stellar_components: Optional[List[DataPoint]] = None
    st_companion: Optional[DataPoint] = None
    st_planets: Optional[List[DataPoint]] = None

    # Éléments orbitaux binaires
    st_semi_major_axis: Optional[DataPoint] = None
    st_eccentricity: Optional[DataPoint] = None
    st_period: Optional[DataPoint] = None
    st_inclination: Optional[DataPoint] = None
    st_argument_of_periapsis: Optional[DataPoint] = None
    st_epoch_binary: Optional[DataPoint] = None
    st_semi_amplitude: Optional[DataPoint] = None

    # Références
    references: Dict[str, Reference] = field(default_factory=dict)

    # Métadonnées supplémentaires
    metadata: Dict[str, Any] = field(default_factory=dict)

    st_constellation: Optional[DataPoint] = None

    def add_reference(self, reference: Reference) -> None:
        """Ajoute une référence à l'étoile"""
        self.references[reference.source.value] = reference

    def get_reference(self, source: str) -> Optional[Reference]:
        """Récupère une référence par sa source"""
        return self.references.get(source)
