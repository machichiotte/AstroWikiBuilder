# src/models/entities/star.py
from dataclasses import dataclass, field
from typing import Optional, List

from ..references.reference import Reference
from .exoplanet_model import ValueWithUncertainty


@dataclass
class Star:
    """
    Modèle de données pour une étoile hôte.

    Cette classe représente toutes les données connues d'une étoile,
    incluant ses caractéristiques physiques, spectroscopiques, et
    astrométriques. Supporte les systèmes binaires avec attributs _2.

    Attributes:
        sy_constellation (str): Constellation dans laquelle se trouve l'étoile.

        st_name (str): Nom principal de l'étoile (ex: "HD 209458").
        st_altname (List[str]): Noms alternatifs de l'étoile.
        st_image (str): Chemin ou URL de l'image de l'étoile.
        st_upright (str): Paramètre d'orientation de l'image.
        st_caption (str): Légende de l'image.
        st_coord_title (str): Titre des coordonnées.

        apparent_magnitude (ValueWithUncertainty): Magnitude apparente.
        st_epoch (ValueWithUncertainty): Époque de référence (JD).
        st_right_ascension (str): Ascension droite (format HMS).
        st_declination (str): Déclinaison (format DMS).
        st_radial_velocity (ValueWithUncertainty): Vitesse radiale (km/s).
        st_proper_motion_ra (ValueWithUncertainty): Mouvement propre en AD (mas/an).
        st_proper_motion_dec (ValueWithUncertainty): Mouvement propre en Dec (mas/an).
        st_parallax (ValueWithUncertainty): Parallaxe (mas).
        st_distance_pc (ValueWithUncertainty): Distance (parsecs).
        st_distance_light_years (ValueWithUncertainty): Distance (années-lumière).
        st_distance (ValueWithUncertainty): Distance générique.

        st_spectral_type (str): Type spectral (ex: "G0V").

        st_apparent_magnitude (ValueWithUncertainty): Magnitude apparente.
        st_mag_u/b/v/g/r/i/j/h/k (ValueWithUncertainty): Magnitudes dans différentes bandes.

        st_u_b_color (ValueWithUncertainty): Indice de couleur U-B.
        st_b_v_color (ValueWithUncertainty): Indice de couleur B-V.
        st_v_r_color (ValueWithUncertainty): Indice de couleur V-R.
        st_r_i_color (ValueWithUncertainty): Indice de couleur R-I.
        st_j_k_color (ValueWithUncertainty): Indice de couleur J-K.
        st_j_h_color (ValueWithUncertainty): Indice de couleur J-H.
        st_absolute_magnitude (ValueWithUncertainty): Magnitude absolue.

        mass (ValueWithUncertainty): Masse (M☉).
        radius (ValueWithUncertainty): Rayon (R☉).
        density (ValueWithUncertainty): Densité (g/cm³).
        luminosity (ValueWithUncertainty): Luminosité (L☉).
        surface_gravity (ValueWithUncertainty): Gravité de surface (log g).
        temperature (ValueWithUncertainty): Température effective (K).
        metallicity (ValueWithUncertainty): Métallicité [Fe/H].
        rotation (ValueWithUncertainty): Période de rotation (jours).
        age (ValueWithUncertainty): Âge (Gyr).

        st_mass/radius/density/luminosity/surface_gravity/temperature/metallicity/rotation/age:
            Versions préfixées des attributs physiques.

        st_evolutionary_stage (str): Stade évolutif (ex: "Main Sequence").
        st_variability (str): Type de variabilité.

        st_stellar_components (List[str]): Composantes du système stellaire.
        st_companion (str): Étoile compagnon.
        st_planets (List[str]): Liste des planètes connues.

        st_semi_major_axis (ValueWithUncertainty): Demi-grand axe orbital binaire (UA).
        st_eccentricity (ValueWithUncertainty): Excentricité orbitale binaire.
        st_period (ValueWithUncertainty): Période orbitale binaire (jours).
        st_inclination (ValueWithUncertainty): Inclinaison orbitale binaire (degrés).
        st_argument_of_periapsis (ValueWithUncertainty): Argument du périastre (degrés).
        st_epoch_binary (ValueWithUncertainty): Époque de référence binaire (JD).
        st_semi_amplitude (ValueWithUncertainty): Semi-amplitude (km/s).

        reference (Reference): Référence bibliographique de la source des données.

    Note:
        Les attributs avec suffixe _2 correspondent aux valeurs pour le compagnon
        dans un système binaire.
    """

    sy_constellation: Optional[str] = None

    # Identifiants
    st_name: str = None
    st_altname: Optional[List[str]] = field(default_factory=list)
    st_image: Optional[str] = None
    st_upright: Optional[str] = None
    st_caption: Optional[str] = None
    st_coord_title: Optional[str] = None

    # Données d'observation
    apparent_magnitude: Optional[ValueWithUncertainty] = None
    st_epoch: Optional[ValueWithUncertainty] = None
    st_right_ascension: Optional[str] = None
    st_right_ascension_2: Optional[str] = None
    st_declination: Optional[str] = None
    st_declination_2: Optional[str] = None
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
