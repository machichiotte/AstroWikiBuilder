# src/utils/astro/classification/exoplanet_type_utils.py
from typing import Optional
from src.models.data_sources.exoplanet_source import DataSourceExoplanet


class ExoplanetTypeUtils:
    SUB_EARTH_MAX = 0.5
    EARTH_MAX = 2.0
    SUPER_EARTH_MAX = 10.0
    ICE_GIANT_MAX = 30.0
    GAS_GIANT_MIN = 10.0
    JUPITER_MASS = 317.8

    SUB_EARTH_RADIUS_MAX = 0.8
    EARTH_RADIUS_MAX = 1.25
    SUPER_PUFF_RADIUS_MIN = 4.0

    ULTRA_HOT_MIN = 2200
    HOT_MIN = 1000
    WARM_MIN = 500
    HIGH_INSOLATION_MIN = 100

    def get_exoplanet_planet_type(self, exoplanet: DataSourceExoplanet) -> str:
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

        m = self._mass_in_earth(exoplanet)
        r = self._radius_in_earth(exoplanet)
        d = self._density(exoplanet)
        insolation = self._stellar_insolation(exoplanet)

        if m is not None and r is not None:
            return self._classify_combined(m, r, d, exoplanet, insolation)

        if m is not None:
            return self._classify_by_mass(m)

        if r is not None:
            return self._classify_by_radius(r)

        return "Exoplanète"  # Type par défaut

    def _classify_combined(
        self,
        m: float,
        r: float,
        d: Optional[float],
        p: DataSourceExoplanet,
        insolation: Optional[float],
    ) -> str:
        # Petite masse et petit rayon → probablement terrestre
        if m <= self.SUPER_EARTH_MAX and r <= self.SUPER_PUFF_RADIUS_MIN:
            return self._classify_terrestrial(m, r)

        # Grande masse ou grand rayon → probablement géante
        if m >= self.GAS_GIANT_MIN or r >= self.SUPER_PUFF_RADIUS_MIN:
            return self._classify_giant(m, p, insolation)

        # Masse modérée mais faible densité → tendance gazeuse
        if d is not None and d < 2.0 and r > 1.5:
            return self._classify_giant(m, p, insolation)

        # Masse modérée et densité moyenne ou élevée → tendance terrestre
        return self._classify_terrestrial(m, r)

    def _classify_giant(
        self, m: float, p: DataSourceExoplanet, insolation: Optional[float]
    ) -> str:
        t = (
            float(p.pl_temperature.value)
            if p.pl_temperature and p.pl_temperature.value
            else None
        )
        a = (
            float(p.pl_semi_major_axis.value)
            if p.pl_semi_major_axis and p.pl_semi_major_axis.value
            else None
        )

        if m >= self.JUPITER_MASS:
            if insolation and insolation >= self.HIGH_INSOLATION_MIN:
                return "Jupiter ultra-chaud"
            if t:
                if t >= self.ULTRA_HOT_MIN:
                    return "Jupiter ultra-chaud"
                if t >= self.HOT_MIN:
                    return "Jupiter chaud"
                if t >= self.WARM_MIN:
                    return "Jupiter tiède"
            if a and a >= 1.0:
                return "Jupiter froid"
            return "Planète géante gazeuse"

        if m <= self.ICE_GIANT_MAX:
            if insolation:
                return "Neptune chaud" if insolation > 20 else "Neptune froid"
            if a:
                return "Neptune chaud" if a < 1.0 else "Neptune froid"
            return "Planète géante de glaces"

        if t:
            if t >= self.HOT_MIN:
                return "Jupiter chaud"
            if t >= self.WARM_MIN:
                return "Jupiter tiède"
        if a and a >= 1.0:
            return "Jupiter froid"
        return "Planète géante gazeuse"

    def _classify_terrestrial(self, m: float, r: float) -> str:
        if m <= self.SUB_EARTH_MAX or r <= self.SUB_EARTH_RADIUS_MAX:
            return "Sous-Terre"
        if m <= self.EARTH_MAX and r <= self.EARTH_RADIUS_MAX:
            return "Planète de dimensions terrestres"
        if m <= self.SUPER_EARTH_MAX:
            return "Super-Terre"
        return "Méga-Terre"

    def _mass_in_earth(self, p: DataSourceExoplanet) -> Optional[float]:
        if not p.pl_mass or p.pl_mass.value is None:
            return None
        try:
            value = float(p.pl_mass.value)
        except (TypeError, ValueError):
            return None
        return value * (self.JUPITER_MASS if p.pl_mass.unit == "M_J" else 1)

    def _radius_in_earth(self, p: DataSourceExoplanet) -> Optional[float]:
        if not p.pl_radius or p.pl_radius.value is None:
            return None
        try:
            value = float(p.pl_radius.value)
        except (TypeError, ValueError):
            return None
        return value * (11.2 if p.pl_radius.unit == "R_J" else 1)

    def _density(self, p: DataSourceExoplanet) -> Optional[float]:
        m = self._mass_in_earth(p)
        r = self._radius_in_earth(p)
        if m is None or r is None:
            return None
        mass_g = m * 5.972e27
        vol_cm3 = 4 / 3 * 3.1416 * (r * 6.371e8) ** 3
        return mass_g / vol_cm3

    def _stellar_insolation(self, p: DataSourceExoplanet) -> float:
        # Rendre robuste l'accès à st_name et pl_semi_major_axis
        st_name = p.st_name.value if hasattr(p.st_name, "value") else p.st_name
        semi_major_axis = (
            p.pl_semi_major_axis.value
            if (hasattr(p.pl_semi_major_axis, "value"))
            else p.pl_semi_major_axis
        )
        if (
            not st_name
            or st_name is None
            or not semi_major_axis
            or semi_major_axis is None
        ):
            return float("nan")
        try:
            L = float(st_name)
            a = float(semi_major_axis)
        except (TypeError, ValueError):
            return float("nan")
        if a <= 0:
            return float("nan")
        return L / (a**2)

    def _classify_by_mass(self, m: float) -> str:
        if m <= self.SUPER_EARTH_MAX:
            return (
                "Super-Terre"
                if m > self.EARTH_MAX
                else "Planète de dimensions terrestres"
            )
        return "Planète géante de masse élevée"

    def _classify_by_radius(self, r: float) -> str:
        if r <= self.EARTH_RADIUS_MAX:
            return "Planète de dimensions terrestres"
        if r >= self.SUPER_PUFF_RADIUS_MIN:
            return "Planète super-enflée"
        return "Planète géante de rayon modéré"
