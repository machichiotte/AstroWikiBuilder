# src/utils/astro/classification/exoplanet_type_util.py

import math

from src.models.entities.exoplanet_entity import Exoplanet


# ============================================================================
# DÉCLARATION DE LA CLASSE ExoplanetTypeUtil
# ============================================================================
class ExoplanetTypeUtil:
    # ============================================================================
    # CONSTANTES ET LIMITES DE CLASSIFICATION
    # ============================================================================
    # Définitions basées sur les standards scientifiques :
    # - Valencia et al. (2007) : Super-Terre = 1-10 M⊕ (masse)
    # - Kepler : classification par rayon (voir ci-dessous)
    # - Distinction Super-Terre vs Mini-Neptune par densité
    CLASSIFICATION_LIMITS = {
        "mass": {
            "sub_earth_max": 0.5,  # < 0.5 M⊕
            "earth_min": 0.5,  # 0.5-2 M⊕
            "earth_max": 2.0,
            "super_earth_min": 1.0,  # Valencia et al. : 1-10 M⊕
            "super_earth_max": 10.0,
            "mini_neptune_max": 10.0,  # Masse similaire à Super-Terre
            "ice_giant_min": 10.0,  # Neptune froid : 10-30 M⊕
            "ice_giant_max": 30.0,  # Neptune/Uranus : ~17 M⊕
            "gas_giant_min": 10.0,
            "jupiter": 317.8,  # 1 M_J = 317.8 M⊕
            "super_jupiter_min": 635.6,  # > 2 M_J (définition haute)
        },
        "radius": {
            # Classification Kepler (en rayons terrestres R⊕)
            "sub_earth_max": 0.8,  # < 0.8 R⊕
            "earth_size_max": 1.25,  # Kepler : R < 1.25 R⊕
            "super_earth_min": 1.25,  # Kepler : 1.25-2 R⊕
            "super_earth_max": 2.0,
            "sub_neptune_max": 3.0,  # Sous-Neptune : < 3 R⊕
            "neptune_size_min": 2.0,  # Kepler : 2-6 R⊕
            "neptune_size_max": 6.0,
            "neptune_radius": 3.88,  # Rayon de Neptune : 3.88 R⊕
            "jupiter_size_min": 6.0,  # Kepler : 6-15 R⊕
            "jupiter_size_max": 15.0,
            "jupiter_radius": 11.2,  # Rayon de Jupiter : 11.2 R⊕
            "very_large_min": 15.0,  # Kepler : 15-22.4 R⊕
            "very_large_max": 22.4,
            "super_puff_min": 4.0,  # Planètes super-enflées : R > Neptune
        },
        "temperature": {
            "ultra_hot": 2200,  # > 2200 K
            "hot": 1000,  # 1000-2200 K
            "warm": 500,  # 500-1000 K
            "neptune_warm_min": 200,  # Neptune tiède : 200-1000 K
            "neptune_warm_max": 1000,
        },
        "insolation": {
            "high": 100,  # Flux élevé (> 100× Terre)
            "neptune_hot": 20,  # Seuil Neptune chaud (> 20× Terre)
        },
        "eccentricity": {
            "eccentric_min": 0.1,  # Jupiter excentrique : e > 0.1
        },
        "density": {
            # Distinction Super-Terre (rocheuse) vs Mini-Neptune (gazeuse)
            "rocky_min": 3.0,  # ≥ 3.0 g/cm³ → rocheuse/tellurique
            "ice_giant_max": 2.5,  # ≤ 2.5 g/cm³ → géante de glaces
            "mini_neptune_max": 3.0,  # < 3.0 g/cm³ → atmosphère épaisse
            "puffy_max": 0.7,  # Saturne chaud / Planète enflée : ρ ≤ 0.7 g/cm³
            "super_puff_max": 0.3,  # Planète super-enflée : ρ très faible
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
        # ========================================================================
        # CAS 1 : Petite masse ET petit rayon (< 10 M⊕ ET < 4 R⊕)
        # → Probablement terrestre, Super-Terre ou Mini-Neptune
        # ========================================================================
        if (
            m <= self.CLASSIFICATION_LIMITS["mass"]["super_earth_max"]
            and r <= self.CLASSIFICATION_LIMITS["radius"]["super_puff_min"]
        ):
            # Classification par RAYON selon Kepler :
            # - R < 1.25 R⊕ → Taille terrestre
            # - 1.25 R⊕ < R < 2 R⊕ → Super-Terre (si densité élevée) ou Mini-Neptune (si densité faible)
            # - 2 R⊕ < R < 6 R⊕ → Taille neptunienne (Mini-Neptune)

            # Taille neptunienne (2-6 R⊕)
            if (
                self.CLASSIFICATION_LIMITS["radius"]["neptune_size_min"]
                <= r
                < self.CLASSIFICATION_LIMITS["radius"]["neptune_size_max"]
            ):
                # Vérifier la densité pour distinguer Super-Terre dense vs Mini-Neptune
                if d and d >= self.CLASSIFICATION_LIMITS["density"]["rocky_min"]:
                    return "Super-Terre"  # Planète rocheuse dense malgré le rayon
                return self.classify_giant_planet_by_temperature_or_insolation(m, p, insolation, d)

            # Taille Super-Terre (1.25-2 R⊕) - DISTINCTION CRITIQUE
            if (
                self.CLASSIFICATION_LIMITS["radius"]["super_earth_min"]
                <= r
                < self.CLASSIFICATION_LIMITS["radius"]["super_earth_max"]
            ):
                # DISTINCTION Super-Terre vs Mini-Neptune par DENSITÉ
                if d:
                    if d >= self.CLASSIFICATION_LIMITS["density"]["rocky_min"]:
                        return "Super-Terre"  # Rocheuse, densité ≥ 3.0 g/cm³
                    elif d < self.CLASSIFICATION_LIMITS["density"]["mini_neptune_max"]:
                        return "Mini-Neptune"  # Gazeuse, densité < 3.0 g/cm³
                # Sans densité, utiliser masse et rayon
                return self.classify_terrestrial_type_by_mass_and_radius(m, r)

            # Taille terrestre (< 1.25 R⊕)
            return self.classify_terrestrial_type_by_mass_and_radius(m, r)

        # ========================================================================
        # CAS 2 : Grande masse OU grand rayon (≥ 10 M⊕ OU ≥ 4 R⊕)
        # → Probablement géante (Jupiter, Neptune, etc.)
        # ========================================================================
        if (
            m >= self.CLASSIFICATION_LIMITS["mass"]["gas_giant_min"]
            or r >= self.CLASSIFICATION_LIMITS["radius"]["super_puff_min"]
        ):
            return self.classify_giant_planet_by_temperature_or_insolation(m, p, insolation, d)

        # ========================================================================
        # CAS 3 : Masse modérée mais faible densité
        # → Tendance gazeuse (Mini-Neptune ou géante)
        # ========================================================================
        if d is not None and d < 2.0 and r > 1.5:
            return self.classify_giant_planet_by_temperature_or_insolation(m, p, insolation, d)

        # Masse modérée et densité moyenne ou élevée → tendance terrestre
        return self.classify_terrestrial_type_by_mass_and_radius(m, r)

    def _classify_jupiter_type(
        self,
        temperature: float | None,
        insolation: float | None,
        semi_major_axis: float | None,
        mass: float | None = None,
        density: float | None = None,
        eccentricity: float | None = None,
    ) -> str:
        """Classifie un Jupiter par température/insolation/masse/densité/excentricité."""

        # Super-Jupiter : masse > 2 M_J (définition haute)
        if mass and mass >= self.CLASSIFICATION_LIMITS["mass"]["super_jupiter_min"]:
            # Classifier comme Super-Jupiter avec qualificatif thermique
            if insolation and insolation >= self.CLASSIFICATION_LIMITS["insolation"]["high"]:
                return "Super-Jupiter ultra-chaud"
            if temperature:
                if temperature >= self.CLASSIFICATION_LIMITS["temperature"]["ultra_hot"]:
                    return "Super-Jupiter ultra-chaud"
                if temperature >= self.CLASSIFICATION_LIMITS["temperature"]["hot"]:
                    return "Super-Jupiter chaud"
            return "Super-Jupiter"

        # Saturne chaud / Planète enflée : densité très faible (≤ 0.7 g/cm³)
        if density and density <= self.CLASSIFICATION_LIMITS["density"]["puffy_max"]:
            if insolation and insolation >= self.CLASSIFICATION_LIMITS["insolation"]["neptune_hot"]:
                return "Saturne chaud"
            if temperature and temperature >= self.CLASSIFICATION_LIMITS["temperature"]["hot"]:
                return "Saturne chaud"

        # Jupiter excentrique : excentricité > 0.1
        if (
            eccentricity
            and eccentricity > self.CLASSIFICATION_LIMITS["eccentricity"]["eccentric_min"]
        ):
            # Combiner avec classification thermique si disponible
            if temperature and temperature >= self.CLASSIFICATION_LIMITS["temperature"]["hot"]:
                return "Jupiter chaud excentrique"
            return "Jupiter excentrique"

        # Classification thermique standard
        if insolation and insolation >= self.CLASSIFICATION_LIMITS["insolation"]["high"]:
            return "Jupiter ultra-chaud"

        if temperature:
            if temperature >= self.CLASSIFICATION_LIMITS["temperature"]["ultra_hot"]:
                return "Jupiter ultra-chaud"
            if temperature >= self.CLASSIFICATION_LIMITS["temperature"]["hot"]:
                return "Jupiter chaud"
            if temperature >= self.CLASSIFICATION_LIMITS["temperature"]["warm"]:
                return "Jupiter tiède"

        if semi_major_axis and semi_major_axis >= 1.0:
            return "Jupiter froid"

        return "Planète géante gazeuse"

    def _classify_neptune_type(
        self,
        insolation: float | None,
        semi_major_axis: float | None,
        temperature: float | None,
    ) -> str:
        """Classifie un Neptune par insolation/distance/température."""
        # Neptune chaud: insolation > 20 ou semi_major_axis < 1.0 UA
        if insolation is not None and not math.isnan(insolation):
            if insolation > self.CLASSIFICATION_LIMITS["insolation"]["neptune_hot"]:
                return "Neptune chaud"

        if semi_major_axis and semi_major_axis < 1.0:
            return "Neptune chaud"

        # Neptune tiède: température entre 200K et 1000K, proche de l'étoile mais pas trop
        if temperature:
            if (
                self.CLASSIFICATION_LIMITS["temperature"]["neptune_warm_min"]
                <= temperature
                < self.CLASSIFICATION_LIMITS["temperature"]["neptune_warm_max"]
            ):
                # Vérifier qu'on n'est pas dans la zone "Neptune chaud"
                if (
                    insolation
                    and insolation <= self.CLASSIFICATION_LIMITS["insolation"]["neptune_hot"]
                ):
                    return "Neptune tiède"

        # Neptune froid: distance > 1.0 UA ou température basse
        if semi_major_axis and semi_major_axis >= 1.0:
            return "Neptune froid"

        return "Planète géante de glaces"

    def classify_giant_planet_by_temperature_or_insolation(
        self, m: float, p: Exoplanet, insolation: float | None, density: float | None = None
    ) -> str:
        t: float | None = float(p.pl_temperature.value) if p.pl_temperature else None
        a: float | None = (
            float(p.pl_semi_major_axis.value)
            if p.pl_semi_major_axis and p.pl_semi_major_axis.value
            else None
        )

        # Jupiter-mass planets (≥ 317.8 M⊕ ≈ 1 M_J)
        if m >= self.CLASSIFICATION_LIMITS["mass"]["jupiter"]:
            return self._classify_jupiter_type(t, insolation, a)

        # Neptune-mass planets (≤ 30 M⊕ ≈ 0.09 M_J)
        # IMPORTANT : Vérifier la densité pour distinguer :
        # - Super-Terre dense (densité ≥ 3.0 g/cm³) → rocheuse
        # - Mini-Neptune (densité < 3.0 g/cm³) → atmosphère épaisse
        # - Neptune (géante de glaces classique)
        if m <= self.CLASSIFICATION_LIMITS["mass"]["ice_giant_max"]:
            # Si densité élevée (≥ 3.0 g/cm³) → Super-Terre rocheuse
            if density and density >= self.CLASSIFICATION_LIMITS["density"]["rocky_min"]:
                return "Super-Terre"

            # Si densité faible (< 3.0 g/cm³) → Mini-Neptune ou Neptune
            # Distinction par température/insolation
            if density and density < self.CLASSIFICATION_LIMITS["density"]["mini_neptune_max"]:
                # Petite masse (< 10 M⊕) → Mini-Neptune
                if m <= self.CLASSIFICATION_LIMITS["mass"]["mini_neptune_max"]:
                    return self._classify_mini_neptune_type(insolation, a, t)

            # Masse Neptune classique (10-30 M⊕)
            return self._classify_neptune_type(insolation, a, t)

        # Intermediate mass planets (between Neptune and Jupiter: 30-318 M⊕)
        return self._classify_jupiter_type(t, insolation, a)

    def _classify_mini_neptune_type(
        self,
        insolation: float | None,
        semi_major_axis: float | None,
        temperature: float | None,
    ) -> str:
        """Classifie un Mini-Neptune par insolation/distance/température."""
        # Mini-Neptune chaud : insolation > 20 ou semi_major_axis < 1.0 UA
        if insolation is not None and not math.isnan(insolation):
            if insolation > self.CLASSIFICATION_LIMITS["insolation"]["neptune_hot"]:
                return "Mini-Neptune"  # Proche de l'étoile

        if semi_major_axis and semi_major_axis < 1.0:
            return "Mini-Neptune"

        # Mini-Neptune tiède : température entre 200K et 1000K
        if temperature:
            if (
                self.CLASSIFICATION_LIMITS["temperature"]["neptune_warm_min"]
                <= temperature
                < self.CLASSIFICATION_LIMITS["temperature"]["neptune_warm_max"]
            ):
                return "Mini-Neptune"

        # Par défaut
        return "Mini-Neptune"

    def classify_terrestrial_type_by_mass_and_radius(self, m: float, r: float) -> str:
        if (
            m <= self.CLASSIFICATION_LIMITS["mass"]["sub_earth_max"]
            or r <= self.CLASSIFICATION_LIMITS["radius"]["sub_earth_max"]
        ):
            return "Sous-Terre"
        if (
            m <= self.CLASSIFICATION_LIMITS["mass"]["earth_max"]
            and r <= self.CLASSIFICATION_LIMITS["radius"]["earth_size_max"]
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
        if r <= self.CLASSIFICATION_LIMITS["radius"]["earth_size_max"]:
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
