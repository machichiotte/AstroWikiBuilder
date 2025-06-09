# src/models/data_source_exoplanet.py
from dataclasses import dataclass, field
from typing import Optional, List
from .reference import DataPoint


@dataclass
class DataSourceExoplanet:
    # Identifiants
    pl_name: Optional[DataPoint] = None
    pl_altname: Optional[List[str]] = field(default_factory=list)

    # Étoile hôte
    st_name: Optional[DataPoint] = None
    st_epoch: Optional[DataPoint] = None
    st_right_ascension: Optional[DataPoint] = None
    st_declination: Optional[DataPoint] = None
    st_distance: Optional[DataPoint] = None
    st_constellation: Optional[DataPoint] = None
    st_spectral_type: Optional[DataPoint] = None
    st_apparent_magnitude: Optional[DataPoint] = None

    # Caractéristiques orbitales
    pl_semi_major_axis: Optional[DataPoint] = None
    pl_periastron: Optional[DataPoint] = None
    pl_apoastron: Optional[DataPoint] = None
    pl_eccentricity: Optional[DataPoint] = None
    pl_orbital_period: Optional[DataPoint] = None
    pl_angular_distance: Optional[DataPoint] = None
    pl_periastron_time: Optional[DataPoint] = None
    pl_inclination: Optional[DataPoint] = None
    pl_argument_of_periastron: Optional[DataPoint] = None
    pl_epoch: Optional[DataPoint] = None

    # Caractéristiques physiques
    pl_mass: Optional[DataPoint] = None
    pl_minimum_mass: Optional[DataPoint] = None
    pl_radius: Optional[DataPoint] = None
    pl_density: Optional[DataPoint] = None
    pl_gravity: Optional[DataPoint] = None
    pl_rotation_period: Optional[DataPoint] = None
    pl_temperature: Optional[DataPoint] = None
    pl_bond_albedo: Optional[DataPoint] = None

    # Atmosphère
    pl_pressure: Optional[DataPoint] = None
    pl_composition: Optional[DataPoint] = None
    pl_wind_speed: Optional[DataPoint] = None

    # Découverte
    disc_by: Optional[DataPoint] = None
    disc_program: Optional[DataPoint] = None
    disc_method: Optional[DataPoint] = None
    disc_year: Optional[DataPoint] = None
    disc_location: Optional[DataPoint] = None
    pre_discovery: Optional[DataPoint] = None
    detection_method: Optional[DataPoint] = None
    status: Optional[DataPoint] = None
