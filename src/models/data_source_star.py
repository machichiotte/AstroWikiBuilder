# src/models/data_source_star.py
from dataclasses import dataclass
from typing import Optional
from .reference import DataPoint


@dataclass
class DataSourceStar:
    # Identifiants
    st_name: Optional[DataPoint] = None
    st_image: Optional[DataPoint] = None
    st_caption: Optional[DataPoint] = None
    st_coord_title: Optional[DataPoint] = None  # Added based on the template
    st_upright: Optional[DataPoint] = None  # Added based on the template
    st_iau_map: Optional[DataPoint] = None  # Added based on the template
    st_altname: Optional[DataPoint] = None

    # Astrometry
    st_epoch: Optional[DataPoint] = None
    st_right_ascension: Optional[DataPoint] = None
    st_right_ascension_2: Optional[DataPoint] = None
    st_declination: Optional[DataPoint] = None
    st_declination_2: Optional[DataPoint] = None
    st_constellation: Optional[DataPoint] = None
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
    st_distance_light_years: Optional[DataPoint] = None  # distance al
    st_distance_light_years_2: Optional[DataPoint] = None
    st_distance: Optional[DataPoint] = None  # distance
    st_distance_2: Optional[DataPoint] = None

    # Photometry
    st_apparent_magnitude: Optional[DataPoint] = None
    st_mag_2: Optional[DataPoint] = None
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

    # Physical Characteristics
    st_evolutionary_stage: Optional[DataPoint] = None
    st_evolutionary_stage_2: Optional[DataPoint] = None
    st_spectral_type: Optional[DataPoint] = None
    st_spectral_type_2: Optional[DataPoint] = None
    st_variability: Optional[DataPoint] = None
    st_variability_2: Optional[DataPoint] = None
    st_mass: Optional[DataPoint] = None
    st_mass_2: Optional[DataPoint] = None
    st_radius: Optional[DataPoint] = None
    st_radius_2: Optional[DataPoint] = None
    st_density: Optional[DataPoint] = None
    st_density_2: Optional[DataPoint] = None
    st_surface_gravity: Optional[DataPoint] = None
    st_surface_gravity_2: Optional[DataPoint] = None
    st_luminosity: Optional[DataPoint] = None
    st_luminosity_2: Optional[DataPoint] = None
    st_temperature: Optional[DataPoint] = None
    st_temperature_2: Optional[DataPoint] = None
    st_metallicity: Optional[DataPoint] = None
    st_metallicity_2: Optional[DataPoint] = None
    st_rotation: Optional[DataPoint] = None
    st_rotation_2: Optional[DataPoint] = None
    st_age: Optional[DataPoint] = None
    st_age_2: Optional[DataPoint] = None

    # System Components
    st_stellar_components: Optional[DataPoint] = None
    st_planets: Optional[DataPoint] = None
    st_companion: Optional[DataPoint] = None

    # Caractéristiques système binaire
    st_semi_amplitude_1: Optional[DataPoint] = None
    st_semi_amplitude_2: Optional[DataPoint] = None
    st_argument_of_periapsis_2: Optional[DataPoint] = (
        None  # Assuming this refers to the second component's argument of periapsis
    )
    st_epoch_binary: Optional[DataPoint] = None
