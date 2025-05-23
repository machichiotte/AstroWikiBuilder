from src.models.exoplanet import Exoplanet

class PlanetTypeUtils:
    """
    Classe utilitaire pour la classification des planètes selon les définitions Wikipédia
    """
    # Constantes de classification des planètes (en masses terrestres)
    MASS_THRESHOLDS = {
        'SUPER_JUPITER': 317.8,  # 1 masse jovienne = 317.8 masses terrestres
        'GAS_GIANT': 317.8,      # 1 masse jovienne
        'MEGA_EARTH': 10.0,      # Plus de 10 masses terrestres
        'SUPER_EARTH': 10.0,     # Entre 1 et 10 masses terrestres
        'EARTH_LIKE': 1.0,       # Entre 0.5 et 1 masse terrestre
        'SUB_EARTH': 0.5         # Moins de 0.5 masse terrestre
    }
    
    # Constantes de classification des planètes (en rayons terrestres)
    RADIUS_THRESHOLDS = {
        'SUPER_PUFF': 3.9,       # Plus grand que Neptune (3.9 R_E)
        'SUPER_EARTH': 1.25,     # Plus de 1.25 rayons terrestres
        'EARTH_LIKE': 0.8,       # Entre 0.8 et 1.25 rayons terrestres
        'SUB_EARTH': 0.8         # Moins de 0.8 rayons terrestres
    }
    
    # Constantes de classification des planètes (en kelvins)
    TEMPERATURE_THRESHOLDS = {
        'ULTRA_HOT': 2200,       # Plus de 2200 K
        'HOT': 1000,             # Entre 1000 et 2200 K
        'WARM': 500,             # Entre 500 et 1000 K
        'COLD': 500              # Moins de 500 K
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

    def _get_gas_giant_type(self, mass_value: float, temp_value: float, uspp_suffix: str) -> str:
        """Détermine le type de géante gazeuse en fonction de sa masse et température"""
        # Vérifier si c'est une super-Jupiter
        if mass_value > self.MASS_THRESHOLDS['SUPER_JUPITER']:
            return f"Super-Jupiter{uspp_suffix}"
            
        # Classification par température
        if temp_value >= self.TEMPERATURE_THRESHOLDS['ULTRA_HOT']:
            return f"Jupiter ultra-chaud{uspp_suffix}"
        elif temp_value >= self.TEMPERATURE_THRESHOLDS['HOT']:
            return f"Jupiter chaud{uspp_suffix}"
        elif temp_value >= self.TEMPERATURE_THRESHOLDS['WARM']:
            return f"Jupiter tiède{uspp_suffix}"
        else:
            return f"Jupiter froid{uspp_suffix}"

    def _get_ice_giant_type(self, mass_value: float, temp_value: float, uspp_suffix: str) -> str:
        """Détermine le type de géante de glaces en fonction de sa masse et température"""
        # Vérifier si c'est une mini-Neptune
        if mass_value < 10:  # Moins de 10 masses terrestres
            return f"Mini-Neptune{uspp_suffix}"
            
        # Classification par température
        if temp_value >= self.TEMPERATURE_THRESHOLDS['HOT']:
            return f"Neptune chaud{uspp_suffix}"
        elif temp_value >= self.TEMPERATURE_THRESHOLDS['WARM']:
            return f"Neptune tiède{uspp_suffix}"
        else:
            return f"Neptune froid{uspp_suffix}"

    def _get_terrestrial_type(self, mass_value: float, radius_value: float, uspp_suffix: str) -> str:
        """Détermine le type de planète tellurique en fonction de sa masse et rayon"""
        # Vérifier si c'est une méga-Terre
        if mass_value > self.MASS_THRESHOLDS['MEGA_EARTH']:
            return f"Méga-Terre{uspp_suffix}"
            
        # Vérifier si c'est une super-Terre
        if mass_value > self.MASS_THRESHOLDS['EARTH_LIKE'] or radius_value > self.RADIUS_THRESHOLDS['EARTH_LIKE']:
            return f"Super-Terre{uspp_suffix}"
            
        # Vérifier si c'est une sous-Terre
        if mass_value < self.MASS_THRESHOLDS['SUB_EARTH'] or radius_value < self.RADIUS_THRESHOLDS['SUB_EARTH']:
            return f"Sous-Terre{uspp_suffix}"
            
        # Sinon c'est une planète de dimensions terrestres
        return f"Planète de dimensions terrestres{uspp_suffix}"

    def get_planet_type(self, exoplanet: Exoplanet) -> str:
        """
        Détermine le type de planète en fonction de ses caractéristiques physiques.
        
        Classification basée sur :
        - Masse (M_E) : > 317.8 = super-Jupiter, > 10 = méga-Terre, > 1 = super-Terre, < 0.5 = sous-Terre
        - Rayon (R_E) : > 3.9 = super-puff, > 1.25 = super-Terre, < 0.8 = sous-Terre
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

        # Convertir la masse en masses terrestres si elle est en masses joviennes
        if mass_value and exoplanet.mass.unit == "M_J":
            mass_value *= 317.8  # 1 M_J = 317.8 M_E

        # Convertir le rayon en rayons terrestres si il est en rayons joviens
        if radius_value and exoplanet.radius.unit == "R_J":
            radius_value *= 11.2  # 1 R_J = 11.2 R_E

        # Vérifier si c'est une planète super-enflée
        if radius_value and radius_value > self.RADIUS_THRESHOLDS['SUPER_PUFF']:
            return f"Planète super-enflée{uspp_suffix}"

        # Classification des planètes gazeuses
        if mass_value and mass_value >= self.MASS_THRESHOLDS['GAS_GIANT']:
            if temp_value:
                return self._get_gas_giant_type(mass_value, temp_value, uspp_suffix)
            return f"Géante gazeuse{uspp_suffix}"

        # Classification des planètes de glace
        elif mass_value and 10 <= mass_value < self.MASS_THRESHOLDS['GAS_GIANT']:
            if temp_value:
                return self._get_ice_giant_type(mass_value, temp_value, uspp_suffix)
            return f"Géante de glaces{uspp_suffix}"

        # Classification des planètes telluriques
        elif mass_value and mass_value < self.MASS_THRESHOLDS['MEGA_EARTH']:
            if radius_value:
                return self._get_terrestrial_type(mass_value, radius_value, uspp_suffix)
            return f"Planète tellurique{uspp_suffix}"

        # Par défaut, on considère que c'est une planète tellurique
        return f"Planète tellurique{uspp_suffix}" 