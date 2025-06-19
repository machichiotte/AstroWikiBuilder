# src/models/entities/exoplanet.py

from dataclasses import dataclass, field
from typing import Optional, List

from ..references.reference import Reference


@dataclass(frozen=True)
class ValueWithUncertainty:
    """Classe pour représenter une valeur avec ses incertitudes et son signe"""

    value: Optional[int | float] = None
    error_positive: Optional[int | float] = None
    error_negative: Optional[int | float] = None
    sign: Optional[str] = None  # Ex "<", ">", "±", etc.

    def __hash__(self) -> int:
        """Permet d'utiliser la classe comme clé dans un dictionnaire"""
        return hash((self.value, self.error_positive, self.error_negative, self.sign))

    def __eq__(self, other: object) -> bool:
        """Permet de comparer deux instances de ValueWithUncertainty"""
        if not isinstance(other, ValueWithUncertainty):
            return NotImplemented
        return (
            self.value == other.value
            and self.error_positive == other.error_positive
            and self.error_negative == other.error_negative
            and self.sign == other.sign
        )


@dataclass
class Exoplanet:
    """Classe de base pour les entités d'exoplanètes"""

    # Identifiants
    pl_name: str = None
    pl_altname: Optional[List[str]] = field(default_factory=list)
    image: Optional[str] = None
    caption: Optional[str] = None

    # Étoile hôte
    st_name: str = None
    st_epoch: Optional[float] = None
    st_right_ascension: Optional[float] = None
    st_declination: Optional[float] = None
    st_distance: Optional[ValueWithUncertainty] = None  # Distance avec incertitude
    st_constellation: Optional[str] = None
    st_spectral_type: Optional[str] = None
    st_apparent_magnitude: Optional[float] = None
    st_luminosity: Optional[ValueWithUncertainty] = None

    # Caractéristiques orbitales
    pl_semi_major_axis: Optional[ValueWithUncertainty] = (
        None  # Axe semi-major avec incertitude
    )
    pl_periastron: Optional[float] = None
    pl_apoastron: Optional[float] = None
    pl_eccentricity: Optional[ValueWithUncertainty] = (
        None  # Excentricité avec incertitude
    )
    pl_orbital_period: Optional[ValueWithUncertainty] = (
        None  # Période orbitale avec incertitude
    )
    pl_angular_distance: Optional[float] = None
    pl_periastron_time: Optional[float] = None
    pl_inclination: Optional[ValueWithUncertainty] = (
        None  # Inclinaison avec incertitude
    )
    pl_argument_of_periastron: Optional[float] = None
    pl_epoch: Optional[float] = None

    # Caractéristiques physiques
    pl_mass: Optional[ValueWithUncertainty] = None  # Masse avec incertitude
    pl_minimum_mass: Optional[ValueWithUncertainty] = (
        None  # Masse minimale avec incertitude
    )
    pl_radius: Optional[ValueWithUncertainty] = None  # Rayon avec incertitude
    pl_density: Optional[ValueWithUncertainty] = None  # Densité avec incertitude
    pl_gravity: Optional[float] = None
    pl_rotation_period: Optional[float] = None
    pl_temperature: Optional[ValueWithUncertainty] = (
        None  # Température avec incertitude
    )
    pl_albedo_bond: Optional[float] = None

    # Atmosphère
    pl_pressure: Optional[float] = None
    pl_composition: Optional[str] = None
    pl_wind_speed: Optional[float] = None

    # Découverte
    disc_by: Optional[str] = None
    disc_program: Optional[str] = None
    disc_method: Optional[str] = None
    disc_year: Optional[int] = None
    disc_facility: Optional[str] = None
    pre_discovery: Optional[str] = None
    detection_type: Optional[str] = None
    status: Optional[str] = None

    # Références
    reference: Reference = None
