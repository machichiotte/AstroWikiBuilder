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
    """
    Modèle de données pour une exoplanète.

    Cette classe représente toutes les données connues d'une exoplanète,
    incluant ses caractéristiques physiques, orbitales, et les informations
    sur sa découverte.

    Attributes:
        pl_name (str): Nom principal de l'exoplanète (ex: "HD 209458 b").
        pl_altname (List[str]): Noms alternatifs de l'exoplanète.
        image (str): Chemin ou URL de l'image représentant l'exoplanète.
        caption (str): Légende de l'image.
        sy_constellation (str): Constellation dans laquelle se trouve le système.

        st_name (str): Nom de l'étoile hôte.
        st_epoch (float): Époque de référence pour les coordonnées stellaires (JD).
        st_right_ascension (float): Ascension droite de l'étoile (degrés).
        st_declination (float): Déclinaison de l'étoile (degrés).
        st_distance (ValueWithUncertainty): Distance à l'étoile (parsecs).
        st_spectral_type (str): Type spectral de l'étoile (ex: "G0V").
        st_apparent_magnitude (float): Magnitude apparente de l'étoile.
        st_luminosity (ValueWithUncertainty): Luminosité de l'étoile (L☉).
        st_mass (ValueWithUncertainty): Masse de l'étoile (M☉).
        st_radius (ValueWithUncertainty): Rayon de l'étoile (R☉).
        st_variability (ValueWithUncertainty): Variabilité de l'étoile.
        st_metallicity (ValueWithUncertainty): Métallicité de l'étoile [Fe/H].

        pl_semi_major_axis (ValueWithUncertainty): Demi-grand axe orbital (UA).
        pl_periastron (float): Distance au périastre (UA).
        pl_apoastron (float): Distance à l'apoastre (UA).
        pl_eccentricity (ValueWithUncertainty): Excentricité orbitale (sans unité).
        pl_orbital_period (ValueWithUncertainty): Période orbitale (jours).
        pl_angular_distance (float): Distance angulaire (secondes d'arc).
        pl_periastron_time (float): Temps de passage au périastre (JD).
        pl_inclination (ValueWithUncertainty): Inclinaison orbitale (degrés).
        pl_argument_of_periastron (float): Argument du périastre (degrés).
        pl_epoch (float): Époque de référence pour les éléments orbitaux (JD).

        pl_mass (ValueWithUncertainty): Masse de l'exoplanète (M_Jupiter).
        pl_minimum_mass (ValueWithUncertainty): Masse minimale (M_Jupiter).
        pl_radius (ValueWithUncertainty): Rayon de l'exoplanète (R_Jupiter).
        pl_density (ValueWithUncertainty): Densité moyenne (g/cm³).
        pl_gravity (float): Gravité de surface (log10(cm/s²)).
        pl_rotation_period (float): Période de rotation (jours).
        pl_temperature (ValueWithUncertainty): Température d'équilibre (K).
        pl_albedo_bond (float): Albédo de Bond (sans unité).

        pl_pressure (float): Pression atmosphérique (bar).
        pl_composition (str): Composition atmosphérique.
        pl_wind_speed (float): Vitesse des vents (m/s).

        disc_by (str): Découvreur(s) de l'exoplanète.
        disc_program (str): Programme de découverte.
        disc_method (str): Méthode de découverte (Transit, Radial Velocity, etc.).
        disc_year (int): Année de découverte.
        disc_facility (str): Installation ayant permis la découverte.
        pre_discovery (str): Informations sur une éventuelle pré-découverte.
        detection_type (str): Type de détection.
        status (str): Statut de confirmation de l'exoplanète.

        reference (Reference): Référence bibliographique de la source des données.
    """

    # Identifiants
    pl_name: str = None
    pl_altname: Optional[List[str]] = field(default_factory=list)
    image: Optional[str] = None
    caption: Optional[str] = None
    sy_constellation: Optional[str] = None

    # Étoile hôte
    st_name: str = None
    st_epoch: Optional[float] = None
    st_right_ascension: Optional[float] = None
    st_declination: Optional[float] = None
    st_distance: Optional[ValueWithUncertainty] = None
    st_spectral_type: Optional[str] = None
    st_apparent_magnitude: Optional[float] = None
    st_luminosity: Optional[ValueWithUncertainty] = None

    # Caractéristiques orbitales
    pl_semi_major_axis: Optional[ValueWithUncertainty] = None
    pl_periastron: Optional[float] = None
    pl_apoastron: Optional[float] = None
    pl_eccentricity: Optional[ValueWithUncertainty] = None
    pl_orbital_period: Optional[ValueWithUncertainty] = None
    pl_angular_distance: Optional[float] = None
    pl_periastron_time: Optional[float] = None
    pl_inclination: Optional[ValueWithUncertainty] = None
    pl_argument_of_periastron: Optional[float] = None
    pl_epoch: Optional[float] = None

    # Caractéristiques physiques
    pl_mass: Optional[ValueWithUncertainty] = None
    pl_minimum_mass: Optional[ValueWithUncertainty] = None
    pl_radius: Optional[ValueWithUncertainty] = None
    pl_density: Optional[ValueWithUncertainty] = None
    pl_gravity: Optional[float] = None
    pl_rotation_period: Optional[float] = None
    pl_temperature: Optional[ValueWithUncertainty] = None
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

    st_mass: Optional[ValueWithUncertainty] = None
    st_radius: Optional[ValueWithUncertainty] = None
    st_variability: Optional[ValueWithUncertainty] = None
    st_metallicity: Optional[ValueWithUncertainty] = None
