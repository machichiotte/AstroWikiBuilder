# src/models/entities/exoplanet_entity.py

from dataclasses import dataclass, field

from ..references.reference import Reference


@dataclass(frozen=True)
class ValueWithUncertainty:
    """Classe pour représenter une valeur avec ses incertitudes et son signe"""

    value: int | float | None = None
    error_positive: int | float | None = None
    error_negative: int | float | None = None
    sign: str | None = None  # Ex "<", ">", "±", etc.

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
    pl_altname: list[str] | None = field(default_factory=list)
    image: str | None = None
    caption: str | None = None
    sy_constellation: str | None = None
    sy_planet_count: int | None = None

    # Étoile hôte
    st_name: str = None
    st_epoch: float | None = None
    st_right_ascension: float | None = None
    st_declination: float | None = None
    st_distance: ValueWithUncertainty | None = None
    st_spectral_type: str | None = None
    st_apparent_magnitude: float | None = None
    st_luminosity: ValueWithUncertainty | None = None

    # Caractéristiques orbitales
    pl_semi_major_axis: ValueWithUncertainty | None = None
    pl_periastron: float | None = None
    pl_apoastron: float | None = None
    pl_eccentricity: ValueWithUncertainty | None = None
    pl_orbital_period: ValueWithUncertainty | None = None
    pl_angular_distance: float | None = None
    pl_periastron_time: float | None = None
    pl_inclination: ValueWithUncertainty | None = None
    pl_argument_of_periastron: float | None = None
    pl_epoch: float | None = None

    # Caractéristiques physiques
    pl_mass: ValueWithUncertainty | None = None
    pl_minimum_mass: ValueWithUncertainty | None = None
    pl_radius: ValueWithUncertainty | None = None
    pl_density: ValueWithUncertainty | None = None
    pl_gravity: float | None = None
    pl_rotation_period: float | None = None
    pl_temperature: ValueWithUncertainty | None = None
    pl_insolation_flux: ValueWithUncertainty | None = None
    pl_transit_depth: ValueWithUncertainty | None = None
    pl_albedo_bond: float | None = None

    # Atmosphère
    pl_pressure: float | None = None
    pl_composition: str | None = None
    pl_wind_speed: float | None = None

    # Découverte
    disc_by: str | None = None
    disc_program: str | None = None
    disc_method: str | None = None
    disc_year: int | None = None
    disc_facility: str | None = None
    pre_discovery: str | None = None
    detection_type: str | None = None
    status: str | None = None

    # Références
    reference: Reference = None

    st_mass: ValueWithUncertainty | None = None
    st_radius: ValueWithUncertainty | None = None
    st_variability: ValueWithUncertainty | None = None
    st_metallicity: ValueWithUncertainty | None = None
    st_age: ValueWithUncertainty | None = None
