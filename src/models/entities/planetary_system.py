from dataclasses import dataclass, field
from typing import Optional, List, Dict

from .base_entity import BaseEntity
from ..references.reference import Reference
from .star import Star
from .exoplanet import Exoplanet


@dataclass
class PlanetarySystem(BaseEntity):
    """Classe représentant un système planétaire"""

    # Composants du système
    star: Optional[Star] = None
    planets: List[Exoplanet] = field(default_factory=list)

    # Caractéristiques du système
    number_of_planets: Optional[int] = None
    habitable_zone: Optional[Dict[str, float]] = None

    # Références
    references: Dict[str, Reference] = field(default_factory=dict)

    def add_planet(self, planet: Exoplanet) -> None:
        """Ajoute une planète au système"""
        self.planets.append(planet)
        self.number_of_planets = len(self.planets)

    def remove_planet(self, planet_name: str) -> None:
        """Retire une planète du système par son nom"""
        self.planets = [p for p in self.planets if p.name != planet_name]
        self.number_of_planets = len(self.planets)

    def get_planet(self, planet_name: str) -> Optional[Exoplanet]:
        """Récupère une planète par son nom"""
        for planet in self.planets:
            if planet.name == planet_name:
                return planet
        return None
