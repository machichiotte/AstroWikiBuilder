from src.models.exoplanet import Exoplanet

class PlanetTypeUtils:
    """
    Classe utilitaire pour la classification des planètes
    """
    # Constantes de classification des planètes
    MASS_THRESHOLDS = {
        'GAS_GIANT': 1.0,  # Masse en M_J
        'TERRESTRIAL': 1.0  # Masse en M_J
    }
    
    RADIUS_THRESHOLDS = {
        'ICE_GIANT': 0.8,   # Rayon en R_J
        'SUPER_EARTH': 1.5, # Rayon en R_J
        'EARTH_LIKE': 0.8   # Rayon en R_J
    }
    
    TEMPERATURE_THRESHOLDS = {
        'ULTRA_HOT': 2200,  # Température en K
        'HOT': 1000,        # Température en K
        'WARM': 500         # Température en K
    }

    def is_ultra_short_period_planet(self, exoplanet: Exoplanet) -> bool:
        """
        Détermine si une planète est une planète à période de révolution ultra-courte (USPP)
        Une USPP a une période orbitale inférieure à 1 jour terrestre et orbite autour d'une étoile
        dont la masse n'excède pas 0.88 fois celle du Soleil.
        """
        if not exoplanet.orbital_period or not exoplanet.orbital_period.value:
            return False
            
        # Vérifier si la période est inférieure à 1 jour
        if exoplanet.orbital_period.value >= 1:
            return False
            
        # Vérifier la masse de l'étoile hôte
        if not exoplanet.star_mass or not exoplanet.star_mass.value:
            return False
            
        # La masse de l'étoile doit être inférieure ou égale à 0.88 masses solaires
        return exoplanet.star_mass.value <= 0.88

    def _get_gas_giant_type(self, temp_value: float, uspp_suffix: str) -> str:
        """Détermine le type de géante gazeuse en fonction de sa température"""
        if temp_value >= self.TEMPERATURE_THRESHOLDS['ULTRA_HOT']:
            return f"Jupiter ultra-chaud{uspp_suffix}"
        elif temp_value >= self.TEMPERATURE_THRESHOLDS['HOT']:
            return f"Jupiter chaud{uspp_suffix}"
        elif temp_value >= self.TEMPERATURE_THRESHOLDS['WARM']:
            return f"Jupiter tiède{uspp_suffix}"
        else:
            return f"Jupiter froid{uspp_suffix}"

    def _get_ice_giant_type(self, temp_value: float, uspp_suffix: str) -> str:
        """Détermine le type de géante de glaces en fonction de sa température"""
        if temp_value >= self.TEMPERATURE_THRESHOLDS['HOT']:
            return f"Neptune chaud{uspp_suffix}"
        elif temp_value >= self.TEMPERATURE_THRESHOLDS['WARM']:
            return f"Neptune tiède{uspp_suffix}"
        else:
            return f"Neptune froid{uspp_suffix}"

    def _get_terrestrial_type(self, radius_value: float, uspp_suffix: str) -> str:
        """Détermine le type de planète tellurique en fonction de son rayon"""
        if radius_value >= self.RADIUS_THRESHOLDS['SUPER_EARTH']:
            return f"Super-Terre{uspp_suffix}"
        elif radius_value >= self.RADIUS_THRESHOLDS['EARTH_LIKE']:
            return f"Planète de dimensions terrestres{uspp_suffix}"
        else:
            return f"Sous-Terre{uspp_suffix}"

    def get_planet_type(self, exoplanet: Exoplanet) -> str:
        """
        Détermine le type de planète en fonction de ses caractéristiques physiques.
        
        Classification basée sur :
        - Masse (M_J) : > 1.0 = géante gazeuse, < 1.0 = tellurique
        - Rayon (R_J) : > 0.8 = géante de glaces, > 1.5 = Super-Terre
        - Température (K) : > 2200 = ultra-chaud, > 1000 = chaud, > 500 = tiède
        
        Args:
            exoplanet: L'objet Exoplanet à classifier
            
        Returns:
            str: Le type de planète avec le suffixe USPP si applicable
        """
        # Vérifier si c'est une planète à période ultra-courte
        is_uspp = self.is_ultra_short_period_planet(exoplanet)
        uspp_suffix = " à période de révolution ultra-courte" if is_uspp else ""

        # Extraire les valeurs des caractéristiques
        mass_value = exoplanet.mass.value if exoplanet.mass and exoplanet.mass.value else None
        radius_value = exoplanet.radius.value if exoplanet.radius and exoplanet.radius.value else None
        temp_value = exoplanet.temperature.value if exoplanet.temperature and exoplanet.temperature.value else None

        # Classification des planètes gazeuses
        if mass_value and mass_value >= self.MASS_THRESHOLDS['GAS_GIANT']:
            if temp_value:
                return self._get_gas_giant_type(temp_value, uspp_suffix)
            return f"Géante gazeuse{uspp_suffix}"

        # Classification des planètes de glace
        elif radius_value and radius_value >= self.RADIUS_THRESHOLDS['ICE_GIANT']:
            if temp_value:
                return self._get_ice_giant_type(temp_value, uspp_suffix)
            return f"Géante de glaces{uspp_suffix}"

        # Classification des planètes telluriques
        elif mass_value and mass_value < self.MASS_THRESHOLDS['TERRESTRIAL']:
            if radius_value:
                return self._get_terrestrial_type(radius_value, uspp_suffix)
            return f"Planète tellurique{uspp_suffix}"

        # Par défaut, on considère que c'est une planète tellurique
        return f"Planète tellurique{uspp_suffix}" 