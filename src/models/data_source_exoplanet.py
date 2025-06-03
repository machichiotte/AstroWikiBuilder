# src/models/data_source_exoplanet.py
from dataclasses import dataclass, field
from typing import Optional, List
from .reference import DataPoint


@dataclass
class DataSourceExoplanet:
    # Identifiants
    name: Optional[DataPoint] = None
    other_names: Optional[List[str]] = field(default_factory=list)

    # Étoile hôte
    host_star: Optional[DataPoint] = None
    star_epoch: Optional[DataPoint] = None
    right_ascension: Optional[DataPoint] = None
    declination: Optional[DataPoint] = None
    distance: Optional[DataPoint] = None
    constellation: Optional[DataPoint] = None
    spectral_type: Optional[DataPoint] = None
    apparent_magnitude: Optional[DataPoint] = None

    # Caractéristiques orbitales
    semi_major_axis: Optional[DataPoint] = None
    periastron: Optional[DataPoint] = None
    apoastron: Optional[DataPoint] = None
    eccentricity: Optional[DataPoint] = None
    orbital_period: Optional[DataPoint] = None
    angular_distance: Optional[DataPoint] = None
    periastron_time: Optional[DataPoint] = None
    inclination: Optional[DataPoint] = None
    argument_of_periastron: Optional[DataPoint] = None
    epoch: Optional[DataPoint] = None

    # Caractéristiques physiques
    mass: Optional[DataPoint] = None
    minimum_mass: Optional[DataPoint] = None
    radius: Optional[DataPoint] = None
    density: Optional[DataPoint] = None
    gravity: Optional[DataPoint] = None
    rotation_period: Optional[DataPoint] = None
    temperature: Optional[DataPoint] = None
    bond_albedo: Optional[DataPoint] = None

    # Atmosphère
    pressure: Optional[DataPoint] = None
    composition: Optional[DataPoint] = None
    wind_speed: Optional[DataPoint] = None

    # Découverte
    discoverers: Optional[DataPoint] = None
    discovery_program: Optional[DataPoint] = None
    discovery_method: Optional[DataPoint] = None
    discovery_date: Optional[DataPoint] = None
    discovery_location: Optional[DataPoint] = None
    pre_discovery: Optional[DataPoint] = None
    detection_method: Optional[DataPoint] = None
    status: Optional[DataPoint] = None
