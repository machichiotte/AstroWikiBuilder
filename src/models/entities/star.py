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
    st_declination: Optional[DataPoint] = None
    st_radial_velocity: Optional[DataPoint] = None
    st_proper_motion_ra: Optional[DataPoint] = None
    st_proper_motion_dec: Optional[DataPoint] = None
    st_parallax: Optional[DataPoint] = None
    st_distance: Optional[DataPoint] = None

    # Caractéristiques spectroscopiques
    st_spectral_type: Optional[DataPoint] = None

    # Magnitudes
    st_mag_u: Optional[DataPoint] = None
    st_mag_b: Optional[DataPoint] = None
    st_mag_v: Optional[DataPoint] = None
    st_mag_g: Optional[DataPoint] = None
    st_mag_r: Optional[DataPoint] = None
    st_mag_i: Optional[DataPoint] = None
    st_mag_j: Optional[DataPoint] = None
    st_mag_h: Optional[DataPoint] = None
    st_mag_k: Optional[DataPoint] = None

    # Indices de couleur
    st_u_b_color: Optional[DataPoint] = None
    st_b_v_color: Optional[DataPoint] = None
    st_v_r_color: Optional[DataPoint] = None
    st_r_i_color: Optional[DataPoint] = None
    st_j_k_color: Optional[DataPoint] = None
    st_j_h_color: Optional[DataPoint] = None

    # Caractéristiques physiques
    st_mass: Optional[DataPoint] = None
    st_radius: Optional[DataPoint] = None
    st_density: Optional[DataPoint] = None
    st_luminosity: Optional[DataPoint] = None
    st_surface_gravity: Optional[DataPoint] = None
    st_temperature: Optional[DataPoint] = None
    st_metallicity: Optional[DataPoint] = None
    st_rotation: Optional[DataPoint] = None
    st_age: Optional[DataPoint] = None
    st_evolutionary_stage: Optional[DataPoint] = None

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

    def add_reference(self, reference: Reference) -> None:
        """Ajoute une référence à l'étoile"""
        self.references[reference.source.value] = reference

    def get_reference(self, source: str) -> Optional[Reference]:
        """Récupère une référence par sa source"""
        return self.references.get(source)
