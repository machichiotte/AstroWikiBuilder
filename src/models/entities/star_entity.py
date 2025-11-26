# src/models/entities/star_entity.py
from dataclasses import dataclass, field

from ..references.reference import Reference
from .exoplanet_entity import ValueWithUncertainty


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

    sy_constellation: str | None = None

    # Identifiants
    st_name: str = None
    st_altname: list[str] | None = field(default_factory=list)
    st_image: str | None = None
    st_upright: str | None = None
    st_caption: str | None = None
    st_coord_title: str | None = None

    # Système stellaire
    sy_star_count: int | None = None
    sy_mnum: int | None = None
    sy_pm: ValueWithUncertainty | None = None

    # Données d'observation
    apparent_magnitude: ValueWithUncertainty | None = None
    st_epoch: ValueWithUncertainty | None = None
    st_right_ascension: str | None = None
    st_right_ascension_2: str | None = None
    st_declination: str | None = None
    st_declination_2: str | None = None
    st_radial_velocity: ValueWithUncertainty | None = None
    st_radial_velocity_2: ValueWithUncertainty | None = None
    st_proper_motion_ra: ValueWithUncertainty | None = None
    st_proper_motion_ra_2: ValueWithUncertainty | None = None
    st_proper_motion_dec: ValueWithUncertainty | None = None
    st_proper_motion_dec_2: ValueWithUncertainty | None = None
    st_parallax: ValueWithUncertainty | None = None
    st_parallax_2: ValueWithUncertainty | None = None
    st_distance_pc: ValueWithUncertainty | None = None
    st_distance_pc_2: ValueWithUncertainty | None = None
    st_distance_light_years: ValueWithUncertainty | None = None
    st_distance_light_years_2: ValueWithUncertainty | None = None
    st_distance: ValueWithUncertainty | None = None
    st_distance_2: ValueWithUncertainty | None = None
    glon: ValueWithUncertainty | None = None
    glat: ValueWithUncertainty | None = None
    elon: ValueWithUncertainty | None = None
    elat: ValueWithUncertainty | None = None

    # Caractéristiques spectroscopiques
    st_spectral_type: str | None = None
    st_spectral_type_2: str | None = None

    # Magnitudes
    st_apparent_magnitude: ValueWithUncertainty | None = None
    st_apparent_magnitude_2: ValueWithUncertainty | None = None
    st_mag_u: ValueWithUncertainty | None = None
    st_mag_u_2: ValueWithUncertainty | None = None
    st_mag_b: ValueWithUncertainty | None = None
    st_mag_b_2: ValueWithUncertainty | None = None
    st_mag_v: ValueWithUncertainty | None = None
    st_mag_v_2: ValueWithUncertainty | None = None
    st_mag_g: ValueWithUncertainty | None = None
    st_mag_g_2: ValueWithUncertainty | None = None
    st_mag_r: ValueWithUncertainty | None = None
    st_mag_r_2: ValueWithUncertainty | None = None
    st_mag_i: ValueWithUncertainty | None = None
    st_mag_i_2: ValueWithUncertainty | None = None
    st_mag_j: ValueWithUncertainty | None = None
    st_mag_j_2: ValueWithUncertainty | None = None
    st_mag_h: ValueWithUncertainty | None = None
    st_mag_h_2: ValueWithUncertainty | None = None
    st_mag_k: ValueWithUncertainty | None = None
    st_mag_k_2: ValueWithUncertainty | None = None
    st_mag_w1: ValueWithUncertainty | None = None
    st_mag_w2: ValueWithUncertainty | None = None
    st_mag_w3: ValueWithUncertainty | None = None
    st_mag_w4: ValueWithUncertainty | None = None
    st_mag_gaia: ValueWithUncertainty | None = None
    st_mag_t: ValueWithUncertainty | None = None
    st_mag_kep: ValueWithUncertainty | None = None

    # Indices de couleur
    st_u_b_color: ValueWithUncertainty | None = None
    st_u_b_color_2: ValueWithUncertainty | None = None
    st_b_v_color: ValueWithUncertainty | None = None
    st_b_v_color_2: ValueWithUncertainty | None = None
    st_v_r_color: ValueWithUncertainty | None = None
    st_v_r_color_2: ValueWithUncertainty | None = None
    st_r_i_color: ValueWithUncertainty | None = None
    st_r_i_color_2: ValueWithUncertainty | None = None
    st_j_k_color: ValueWithUncertainty | None = None
    st_j_k_color_2: ValueWithUncertainty | None = None
    st_j_h_color: ValueWithUncertainty | None = None
    st_j_h_color_2: ValueWithUncertainty | None = None
    st_absolute_magnitude: ValueWithUncertainty | None = None
    st_absolute_magnitude_2: ValueWithUncertainty | None = None

    # Caractéristiques physiques
    mass: ValueWithUncertainty | None = None
    radius: ValueWithUncertainty | None = None
    density: ValueWithUncertainty | None = None
    luminosity: ValueWithUncertainty | None = None
    surface_gravity: ValueWithUncertainty | None = None
    temperature: ValueWithUncertainty | None = None
    metallicity: ValueWithUncertainty | None = None
    rotation: ValueWithUncertainty | None = None
    age: ValueWithUncertainty | None = None
    st_mass: ValueWithUncertainty | None = None
    st_mass_2: ValueWithUncertainty | None = None
    st_radius: ValueWithUncertainty | None = None
    st_radius_2: ValueWithUncertainty | None = None
    st_density: ValueWithUncertainty | None = None
    st_density_2: ValueWithUncertainty | None = None
    st_luminosity: ValueWithUncertainty | None = None
    st_luminosity_2: ValueWithUncertainty | None = None
    st_surface_gravity: ValueWithUncertainty | None = None
    st_surface_gravity_2: ValueWithUncertainty | None = None
    st_temperature: ValueWithUncertainty | None = None
    st_temperature_2: ValueWithUncertainty | None = None
    st_metallicity: ValueWithUncertainty | None = None
    st_metallicity_2: ValueWithUncertainty | None = None
    st_rotation: ValueWithUncertainty | None = None
    st_rotation_2: ValueWithUncertainty | None = None
    st_vsin: ValueWithUncertainty | None = None
    st_vsin_2: ValueWithUncertainty | None = None
    st_log_rhk: ValueWithUncertainty | None = None
    st_age: ValueWithUncertainty | None = None
    st_age_2: ValueWithUncertainty | None = None
    st_evolutionary_stage: str | None = None
    st_evolutionary_stage_2: str | None = None
    st_variability: str | None = None
    st_variability_2: str | None = None

    # Système stellaire
    st_stellar_components: list[str] | None = None
    st_companion: str | None = None
    st_planets: list[str] | None = None

    # Éléments orbitaux binaires
    st_semi_major_axis: ValueWithUncertainty | None = None
    st_eccentricity: ValueWithUncertainty | None = None
    st_period: ValueWithUncertainty | None = None
    st_inclination: ValueWithUncertainty | None = None
    st_argument_of_periapsis: ValueWithUncertainty | None = None
    st_epoch_binary: ValueWithUncertainty | None = None
    st_semi_amplitude: ValueWithUncertainty | None = None

    # Référence unique
    reference: Reference = None
