# src/utils/astro/classification/exoplanet_type_util.py

from src.models.entities.exoplanet_entity import Exoplanet


# ============================================================================
# DÉCLARATION DE LA CLASSE ExoplanetTypeUtil
# ============================================================================
class ExoplanetTypeUtil:
    # ============================================================================
    # CONSTANTES ET LIMITES DE CLASSIFICATION
    # ============================================================================
    CLASSIFICATION_LIMITS = {
        "mass": {
            "sub_earth_max": 0.5,
            "earth_max": 2.0,
            "super_earth_max": 10.0,
            "ice_giant_max": 30.0,
            "gas_giant_min": 10.0,
            "jupiter": 317.8,
        },
        "radius": {
            "sub_earth_max": 0.8,
            "earth_max": 1.25,
            "super_puff_min": 4.0,
        },
        "temperature": {
            "ultra_hot": 2200,
            "hot": 1000,
            "warm": 500,
        },
        "insolation": {
            "high": 100,
        },
    }

    # ============================================================================
    # MÉTHODE PRINCIPALE DE CLASSIFICATION
    # ============================================================================
    def determine_exoplanet_classification(self, exoplanet: Exoplanet) -> str:
        """
        Détermine le type de planète basé sur ses caractéristiques physiques.
        """
        # Vérifier d'abord si c'est une Super-Terre
        if exoplanet.pl_mass and exoplanet.pl_radius:
            try:
                mass_jupiter = float(exoplanet.pl_mass.value)
                radius_jupiter = float(exoplanet.pl_radius.value)

                # Une Super-Terre a typiquement une masse entre 1 et 10 masses terrestres
                # et un rayon entre 1 et 2 rayons terrestres
                if 0.003 < mass_jupiter < 0.03 and 0.1 < radius_jupiter < 0.2:
                    return "Super-Terre"
            except (ValueError, TypeError):
                pass

        m: float | None = self.convert_mass_to_earth_units(exoplanet)
        r: float | None = self.convert_radius_to_earth_units(exoplanet)
        d: float | None = self.calculate_density_from_mass_and_radius(exoplanet)
        insolation: float = self.compute_stellar_insolation(exoplanet)

        if m is not None and r is not None:
            return self.classify_based_on_mass_radius_density(m, r, d, exoplanet, insolation)

        if m is not None:
            return self.classify_planet_type_by_mass_only(m)

        if r is not None:
            return self.classify_planet_type_by_radius_only(r)

        return "Exoplanète"  # Type par défaut

    # ============================================================================
    # MÉTHODES DE CLASSIFICATION (logique de classification)
    # ============================================================================
    def classify_based_on_mass_radius_density(
        self,
        m: float,
        r: float,
        d: float | None,
        p: Exoplanet,
        insolation: float | None,
    ) -> str:
        # Petite masse et petit rayon → probablement terrestre
        if (
            m <= self.CLASSIFICATION_LIMITS["mass"]["super_earth_max"]
            and r <= self.CLASSIFICATION_LIMITS["radius"]["super_puff_min"]
        ):
            return self.classify_terrestrial_type_by_mass_and_radius(m, r)

        # Grande masse ou grand rayon → probablement géante
        if (
            m >= self.CLASSIFICATION_LIMITS["mass"]["gas_giant_min"]
            or r >= self.CLASSIFICATION_LIMITS["radius"]["super_puff_min"]
        ):
            return self.classify_giant_planet_by_temperature_or_insolation(m, p, insolation)

        # Masse modérée mais faible densité → tendance gazeuse
        if d is not None and d < 2.0 and r > 1.5:
            return self.classify_giant_planet_by_temperature_or_insolation(m, p, insolation)

        # Masse modérée et densité moyenne ou élevée → tendance terrestre
        return self.classify_terrestrial_type_by_mass_and_radius(m, r)

    def classify_giant_planet_by_temperature_or_insolation(
        self, m: float, p: Exoplanet, insolation: float | None
    ) -> str:
        t: float | None = float(p.pl_temperature.value) if p.pl_temperature else None
        a: float | None = (
            float(p.pl_semi_major_axis.value)
            if p.pl_semi_major_axis and p.pl_semi_major_axis.value
            else None
        )

        if m >= self.CLASSIFICATION_LIMITS["mass"]["jupiter"]:
            if insolation and insolation >= self.CLASSIFICATION_LIMITS["insolation"]["high"]:
                return "Jupiter ultra-chaud"
            if t:
                if t >= self.CLASSIFICATION_LIMITS["temperature"]["ultra_hot"]:
                    return "Jupiter ultra-chaud"
                if t >= self.CLASSIFICATION_LIMITS["temperature"]["hot"]:
                    return "Jupiter chaud"
                if t >= self.CLASSIFICATION_LIMITS["temperature"]["warm"]:
                    return "Jupiter tiède"
            if a and a >= 1.0:
                return "Jupiter froid"
            return "Planète géante gazeuse"

        if m <= self.CLASSIFICATION_LIMITS["mass"]["ice_giant_max"]:
            if insolation:
                return "Neptune chaud" if insolation > 20 else "Neptune froid"
            if a:
                return "Neptune chaud" if a < 1.0 else "Neptune froid"
            return "Planète géante de glaces"

        if t:
            if t >= self.CLASSIFICATION_LIMITS["temperature"]["hot"]:
                return "Jupiter chaud"
            if t >= self.CLASSIFICATION_LIMITS["temperature"]["warm"]:
                return "Jupiter tiède"
        if a and a >= 1.0:
            return "Jupiter froid"
        return "Planète géante gazeuse"

    def classify_terrestrial_type_by_mass_and_radius(self, m: float, r: float) -> str:
        if (
            m <= self.CLASSIFICATION_LIMITS["mass"]["sub_earth_max"]
            or r <= self.CLASSIFICATION_LIMITS["radius"]["sub_earth_max"]
        ):
            return "Sous-Terre"
        if (
            m <= self.CLASSIFICATION_LIMITS["mass"]["earth_max"]
            and r <= self.CLASSIFICATION_LIMITS["radius"]["earth_max"]
        ):
            return "Planète de dimensions terrestres"
        if m <= self.CLASSIFICATION_LIMITS["mass"]["super_earth_max"]:
            return "Super-Terre"
        return "Méga-Terre"

    def classify_planet_type_by_mass_only(self, m: float) -> str:
        if m <= self.CLASSIFICATION_LIMITS["mass"]["super_earth_max"]:
            return (
                "Super-Terre"
                if m > self.CLASSIFICATION_LIMITS["mass"]["earth_max"]
                else "Planète de dimensions terrestres"
            )
        return "Planète géante de masse élevée"

    def classify_planet_type_by_radius_only(self, r: float) -> str:
        if r <= self.CLASSIFICATION_LIMITS["radius"]["earth_max"]:
            return "Planète de dimensions terrestres"
        if r >= self.CLASSIFICATION_LIMITS["radius"]["super_puff_min"]:
            return "Planète super-enflée"
        return "Planète géante de rayon modéré"

    # ============================================================================
    # MÉTHODES UTILITAIRES (conversion, calculs physiques)
    # ============================================================================
    def convert_mass_to_earth_units(self, p: Exoplanet) -> float | None:
        if not p.pl_mass or p.pl_mass.value is None:
            return None
        try:
            value = float(p.pl_mass.value)
            # On suppose que la masse est en masses de Jupiter
            return value * self.CLASSIFICATION_LIMITS["mass"]["jupiter"]
        except (TypeError, ValueError):
            return None

    def convert_radius_to_earth_units(self, p: Exoplanet) -> float | None:
        if not p.pl_radius or p.pl_radius.value is None:
            return None
        try:
            value = float(p.pl_radius.value)
            # On suppose que le rayon est en rayons de Jupiter
            return value * 11.2
        except (TypeError, ValueError):
            return None

    def calculate_density_from_mass_and_radius(self, p: Exoplanet) -> float | None:
        m: float | None = self.convert_mass_to_earth_units(p)
        r: float | None = self.convert_radius_to_earth_units(p)
        if m is None or r is None:
            return None
        mass_g: float = m * 5.972e27
        vol_cm3: float = 4 / 3 * 3.1416 * (r * 6.371e8) ** 3
        return mass_g / vol_cm3

    def compute_stellar_insolation(self, p: Exoplanet) -> float:
        # Vérification de la présence des attributs et de leur valeur
        if (
            p.st_luminosity is None
            or p.st_luminosity.value is None
            or p.pl_semi_major_axis is None
            or p.pl_semi_major_axis.value is None
        ):
            return float("nan")
        try:
            L = float(p.st_luminosity.value)
            a = float(p.pl_semi_major_axis.value)
        except (TypeError, ValueError):
            return float("nan")
        if a <= 0:
            return float("nan")
        return L / (a**2)
