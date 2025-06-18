from dataclasses import dataclass, field
from typing import Optional, List

from ..references.reference import Reference
from .exoplanet import ValueWithUncertainty


@dataclass
class Star:
    """Classe représentant une étoile hôte"""

    # Identifiants
    st_name: str = None
    st_altname: Optional[List[str]] = field(default_factory=list)
    st_image: Optional[str] = None
    st_upright: Optional[str] = None
    st_caption: Optional[str] = None
    st_coord_title: Optional[str] = None

    # Données d'observation
    st_constellation: Optional[str] = None
    apparent_magnitude: Optional[ValueWithUncertainty] = None
    st_epoch: Optional[ValueWithUncertainty] = None
    st_right_ascension: Optional[ValueWithUncertainty] = None
    st_right_ascension_2: Optional[ValueWithUncertainty] = None
    st_declination: Optional[ValueWithUncertainty] = None
    st_declination_2: Optional[ValueWithUncertainty] = None
    st_radial_velocity: Optional[ValueWithUncertainty] = None
    st_radial_velocity_2: Optional[ValueWithUncertainty] = None
    st_proper_motion_ra: Optional[ValueWithUncertainty] = None
    st_proper_motion_ra_2: Optional[ValueWithUncertainty] = None
    st_proper_motion_dec: Optional[ValueWithUncertainty] = None
    st_proper_motion_dec_2: Optional[ValueWithUncertainty] = None
    st_parallax: Optional[ValueWithUncertainty] = None
    st_parallax_2: Optional[ValueWithUncertainty] = None
    st_distance_pc: Optional[ValueWithUncertainty] = None
    st_distance_pc_2: Optional[ValueWithUncertainty] = None
    st_distance_light_years: Optional[ValueWithUncertainty] = None
    st_distance_light_years_2: Optional[ValueWithUncertainty] = None
    st_distance: Optional[ValueWithUncertainty] = None
    st_distance_2: Optional[ValueWithUncertainty] = None

    # Caractéristiques spectroscopiques
    st_spectral_type: Optional[str] = None
    st_spectral_type_2: Optional[str] = None

    # Magnitudes
    st_apparent_magnitude: Optional[ValueWithUncertainty] = None
    st_apparent_magnitude_2: Optional[ValueWithUncertainty] = None
    st_mag_u: Optional[ValueWithUncertainty] = None
    st_mag_u_2: Optional[ValueWithUncertainty] = None
    st_mag_b: Optional[ValueWithUncertainty] = None
    st_mag_b_2: Optional[ValueWithUncertainty] = None
    st_mag_v: Optional[ValueWithUncertainty] = None
    st_mag_v_2: Optional[ValueWithUncertainty] = None
    st_mag_g: Optional[ValueWithUncertainty] = None
    st_mag_g_2: Optional[ValueWithUncertainty] = None
    st_mag_r: Optional[ValueWithUncertainty] = None
    st_mag_r_2: Optional[ValueWithUncertainty] = None
    st_mag_i: Optional[ValueWithUncertainty] = None
    st_mag_i_2: Optional[ValueWithUncertainty] = None
    st_mag_j: Optional[ValueWithUncertainty] = None
    st_mag_j_2: Optional[ValueWithUncertainty] = None
    st_mag_h: Optional[ValueWithUncertainty] = None
    st_mag_h_2: Optional[ValueWithUncertainty] = None
    st_mag_k: Optional[ValueWithUncertainty] = None
    st_mag_k_2: Optional[ValueWithUncertainty] = None

    # Indices de couleur
    st_u_b_color: Optional[ValueWithUncertainty] = None
    st_u_b_color_2: Optional[ValueWithUncertainty] = None
    st_b_v_color: Optional[ValueWithUncertainty] = None
    st_b_v_color_2: Optional[ValueWithUncertainty] = None
    st_v_r_color: Optional[ValueWithUncertainty] = None
    st_v_r_color_2: Optional[ValueWithUncertainty] = None
    st_r_i_color: Optional[ValueWithUncertainty] = None
    st_r_i_color_2: Optional[ValueWithUncertainty] = None
    st_j_k_color: Optional[ValueWithUncertainty] = None
    st_j_k_color_2: Optional[ValueWithUncertainty] = None
    st_j_h_color: Optional[ValueWithUncertainty] = None
    st_j_h_color_2: Optional[ValueWithUncertainty] = None
    st_absolute_magnitude: Optional[ValueWithUncertainty] = None
    st_absolute_magnitude_2: Optional[ValueWithUncertainty] = None

    # Caractéristiques physiques
    mass: Optional[ValueWithUncertainty] = None
    radius: Optional[ValueWithUncertainty] = None
    density: Optional[ValueWithUncertainty] = None
    luminosity: Optional[ValueWithUncertainty] = None
    surface_gravity: Optional[ValueWithUncertainty] = None
    temperature: Optional[ValueWithUncertainty] = None
    metallicity: Optional[ValueWithUncertainty] = None
    rotation: Optional[ValueWithUncertainty] = None
    age: Optional[ValueWithUncertainty] = None
    st_mass: Optional[ValueWithUncertainty] = None
    st_mass_2: Optional[ValueWithUncertainty] = None
    st_radius: Optional[ValueWithUncertainty] = None
    st_radius_2: Optional[ValueWithUncertainty] = None
    st_density: Optional[ValueWithUncertainty] = None
    st_density_2: Optional[ValueWithUncertainty] = None
    st_luminosity: Optional[ValueWithUncertainty] = None
    st_luminosity_2: Optional[ValueWithUncertainty] = None
    st_surface_gravity: Optional[ValueWithUncertainty] = None
    st_surface_gravity_2: Optional[ValueWithUncertainty] = None
    st_temperature: Optional[ValueWithUncertainty] = None
    st_temperature_2: Optional[ValueWithUncertainty] = None
    st_metallicity: Optional[ValueWithUncertainty] = None
    st_metallicity_2: Optional[ValueWithUncertainty] = None
    st_rotation: Optional[ValueWithUncertainty] = None
    st_rotation_2: Optional[ValueWithUncertainty] = None
    st_age: Optional[ValueWithUncertainty] = None
    st_age_2: Optional[ValueWithUncertainty] = None
    st_evolutionary_stage: Optional[str] = None
    st_evolutionary_stage_2: Optional[str] = None
    st_variability: Optional[str] = None
    st_variability_2: Optional[str] = None

    # Système stellaire
    st_stellar_components: Optional[List[str]] = None
    st_companion: Optional[str] = None
    st_planets: Optional[List[str]] = None

    # Éléments orbitaux binaires
    st_semi_major_axis: Optional[ValueWithUncertainty] = None
    st_eccentricity: Optional[ValueWithUncertainty] = None
    st_period: Optional[ValueWithUncertainty] = None
    st_inclination: Optional[ValueWithUncertainty] = None
    st_argument_of_periapsis: Optional[ValueWithUncertainty] = None
    st_epoch_binary: Optional[ValueWithUncertainty] = None
    st_semi_amplitude: Optional[ValueWithUncertainty] = None

    # Référence unique
    reference: Reference = None
