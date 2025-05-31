# src/mappers/nasa_to_star_mapper.py
from typing import Dict, Any, Optional
from src.models.star import Star, DataPoint


class NasaToStarMapper:
    """Mapper pour convertir les données NASA Exoplanet Archive vers le modèle Star"""

    # Mapping des colonnes NASA vers les attributs Star
    NASA_TO_STAR_MAPPING = {
        # Identifiants
        "hostname": "name",
        # Coordonnées
        "ra": "right_ascension",
        "dec": "declination",
        "sy_pmra": "proper_motion_ra",
        "sy_pmdec": "proper_motion_dec",
        "sy_plx": "parallax",
        "sy_dist": "distance_general",
        # Magnitudes
        "sy_bmag": "apparent_magnitude_b_band",
        "sy_vmag": "apparent_magnitude_v_band",
        "sy_jmag": "apparent_magnitude_j_band",
        "sy_hmag": "apparent_magnitude_h_band",
        "sy_kmag": "apparent_magnitude_k_band",
        "sy_gmag": "apparent_magnitude_g_band",
        "sy_rmag": "apparent_magnitude_r_band",
        "sy_imag": "apparent_magnitude_i_band",
        "sy_umag": "apparent_magnitude_u_band",
        "sy_zmag": "apparent_magnitude_z_band",
        "sy_w1mag": "apparent_magnitude_w1_band",
        "sy_w2mag": "apparent_magnitude_w2_band",
        "sy_w3mag": "apparent_magnitude_w3_band",
        "sy_w4mag": "apparent_magnitude_w4_band",
        "sy_gaiamag": "apparent_magnitude_gaia_band",
        "sy_tmag": "apparent_magnitude_t_band",
        "sy_kepmag": "apparent_magnitude_kep_band",
        # Propriétés stellaires
        "st_teff": "temperature",
        "st_mass": "mass",
        "st_rad": "radius",
        "st_met": "metallicity",
        "st_logg": "surface_gravity",
        "st_lum": "luminosity",
        "st_dens": "density",
        "st_age": "age",
        "st_spectype": "spectral_type",
        "st_radv": "radial_velocity",
        "st_rotp": "rotation",
        "st_vsin": "rotation",  # v*sin(i) - peut être mappé sur rotation
    }

    # Unités par défaut pour certains champs NASA
    DEFAULT_UNITS = {
        "ra": "deg",
        "dec": "deg",
        "sy_pmra": "mas/yr",
        "sy_pmdec": "mas/yr",
        "sy_plx": "mas",
        "sy_dist": "pc",
        "st_teff": "K",
        "st_mass": "M☉",
        "st_rad": "R☉",
        "st_met": "dex",
        "st_logg": "log(cm/s²)",
        "st_lum": "L☉",
        "st_dens": "g/cm³",
        "st_age": "Gyr",
        "st_radv": "km/s",
        "st_rotp": "days",
        "st_vsin": "km/s",
    }

    def map_nasa_data_to_star(self, nasa_data: Dict[str, Any]) -> Star:
        """Convertit un dictionnaire de données NASA vers un objet Star"""
        star = Star()

        for nasa_field, star_attribute in self.NASA_TO_STAR_MAPPING.items():
            if nasa_field in nasa_data:
                value = nasa_data[nasa_field]

                # Créer un DataPoint avec la valeur et l'unité par défaut
                if value is not None and str(value).strip():
                    unit = self.DEFAULT_UNITS.get(nasa_field)
                    datapoint = DataPoint(value=value, unit=unit)
                    setattr(star, star_attribute, datapoint)

        # Traitement spécial pour les désignations
        designations = self._extract_designations(nasa_data)
        if designations:
            star.designations = DataPoint(value=designations)

        return star

    def _extract_designations(self, nasa_data: Dict[str, Any]) -> Optional[list]:
        """Extrait les différentes désignations d'une étoile"""
        designation_fields = ["hostname", "hd_name", "hip_name", "tic_id"]
        designations = []

        for field in designation_fields:
            if field in nasa_data and nasa_data[field]:
                value = str(nasa_data[field]).strip()
                if value and value not in designations:
                    designations.append(value)

        return designations if designations else None
