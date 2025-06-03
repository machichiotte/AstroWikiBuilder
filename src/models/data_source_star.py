# src/models/data_source_star.py
from dataclasses import dataclass
from typing import Optional
from .reference import DataPoint


@dataclass
class DataSourceStar:
    # Identifiants
    name: Optional[DataPoint] = None
    image: Optional[DataPoint] = None
    caption: Optional[DataPoint] = None
    coord_title: Optional[DataPoint] = None  # Added based on the template
    upright: Optional[DataPoint] = None  # Added based on the template
    iau_map: Optional[DataPoint] = None  # Added based on the template
    designations: Optional[DataPoint] = None

    # Astrometry
    epoch: Optional[DataPoint] = None
    right_ascension: Optional[DataPoint] = None
    right_ascension_2: Optional[DataPoint] = None
    declination: Optional[DataPoint] = None
    declination_2: Optional[DataPoint] = None
    constellation: Optional[DataPoint] = None
    radial_velocity: Optional[DataPoint] = None
    radial_velocity_2: Optional[DataPoint] = None
    proper_motion_ra: Optional[DataPoint] = None
    proper_motion_ra_2: Optional[DataPoint] = None
    proper_motion_dec: Optional[DataPoint] = None
    proper_motion_dec_2: Optional[DataPoint] = None
    parallax: Optional[DataPoint] = None
    parallax_2: Optional[DataPoint] = None
    distance_pc: Optional[DataPoint] = None
    distance_pc_2: Optional[DataPoint] = None
    distance_light_years: Optional[DataPoint] = None  # distance al
    distance_light_years_2: Optional[DataPoint] = None
    distance_general: Optional[DataPoint] = None  # distance
    distance_general_2: Optional[DataPoint] = None

    # Photometry
    apparent_magnitude: Optional[DataPoint] = None
    apparent_magnitude_2: Optional[DataPoint] = None
    apparent_magnitude_u_band: Optional[DataPoint] = None
    apparent_magnitude_u_band_2: Optional[DataPoint] = None
    apparent_magnitude_b_band: Optional[DataPoint] = None
    apparent_magnitude_b_band_2: Optional[DataPoint] = None
    apparent_magnitude_v_band: Optional[DataPoint] = None
    apparent_magnitude_v_band_2: Optional[DataPoint] = None
    apparent_magnitude_g_band: Optional[DataPoint] = None
    apparent_magnitude_g_band_2: Optional[DataPoint] = None
    apparent_magnitude_r_band: Optional[DataPoint] = None
    apparent_magnitude_r_band_2: Optional[DataPoint] = None
    apparent_magnitude_i_band: Optional[DataPoint] = None
    apparent_magnitude_i_band_2: Optional[DataPoint] = None
    apparent_magnitude_j_band: Optional[DataPoint] = None
    apparent_magnitude_j_band_2: Optional[DataPoint] = None
    apparent_magnitude_h_band: Optional[DataPoint] = None
    apparent_magnitude_h_band_2: Optional[DataPoint] = None
    apparent_magnitude_k_band: Optional[DataPoint] = None
    apparent_magnitude_k_band_2: Optional[DataPoint] = None
    u_b_color: Optional[DataPoint] = None
    u_b_color_2: Optional[DataPoint] = None
    b_v_color: Optional[DataPoint] = None
    b_v_color_2: Optional[DataPoint] = None
    v_r_color: Optional[DataPoint] = None
    v_r_color_2: Optional[DataPoint] = None
    r_i_color: Optional[DataPoint] = None
    r_i_color_2: Optional[DataPoint] = None
    j_k_color: Optional[DataPoint] = None
    j_k_color_2: Optional[DataPoint] = None
    j_h_color: Optional[DataPoint] = None
    j_h_color_2: Optional[DataPoint] = None
    absolute_magnitude: Optional[DataPoint] = None
    absolute_magnitude_2: Optional[DataPoint] = None

    # Physical Characteristics
    evolutionary_stage: Optional[DataPoint] = None
    evolutionary_stage_2: Optional[DataPoint] = None
    spectral_type: Optional[DataPoint] = None
    spectral_type_2: Optional[DataPoint] = None
    variability: Optional[DataPoint] = None
    variability_2: Optional[DataPoint] = None
    mass: Optional[DataPoint] = None
    mass_2: Optional[DataPoint] = None
    radius: Optional[DataPoint] = None
    radius_2: Optional[DataPoint] = None
    density: Optional[DataPoint] = None
    density_2: Optional[DataPoint] = None
    surface_gravity: Optional[DataPoint] = None
    surface_gravity_2: Optional[DataPoint] = None
    luminosity: Optional[DataPoint] = None
    luminosity_2: Optional[DataPoint] = None
    temperature: Optional[DataPoint] = None
    temperature_2: Optional[DataPoint] = None
    metallicity: Optional[DataPoint] = None
    metallicity_2: Optional[DataPoint] = None
    rotation: Optional[DataPoint] = None
    rotation_2: Optional[DataPoint] = None
    age: Optional[DataPoint] = None
    age_2: Optional[DataPoint] = None

    # System Components
    stellar_components: Optional[DataPoint] = None
    planets: Optional[DataPoint] = None
    companion: Optional[DataPoint] = None

    # Caractéristiques système binaire
    semi_amplitude_1: Optional[DataPoint] = None
    semi_amplitude_2: Optional[DataPoint] = None
    argument_of_periapsis_2: Optional[DataPoint] = (
        None  # Assuming this refers to the second component's argument of periapsis
    )
    epoch_binary: Optional[DataPoint] = None

    # Caractéristiques orbitales binaire
    semi_major_axis: Optional[DataPoint] = None
    eccentricity: Optional[DataPoint] = None
    period: Optional[DataPoint] = None
    inclination: Optional[DataPoint] = None
    argument_of_periapsis: Optional[DataPoint] = None
    longitude_of_ascending_node: Optional[DataPoint] = None
    epoch: Optional[DataPoint] = None
