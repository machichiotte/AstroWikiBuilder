from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime

@dataclass
class Exoplanet:
    name: str
    host_star: str
    discovery_year: int
    discovery_method: str
    mass: Optional[float] = None
    mass_error_min: Optional[float] = None
    mass_error_max: Optional[float] = None
    radius: Optional[float] = None
    radius_error_min: Optional[float] = None
    radius_error_max: Optional[float] = None
    orbital_period: Optional[float] = None
    orbital_period_error_min: Optional[float] = None
    orbital_period_error_max: Optional[float] = None
    semi_major_axis: Optional[float] = None
    semi_major_axis_error_min: Optional[float] = None
    semi_major_axis_error_max: Optional[float] = None
    eccentricity: Optional[float] = None
    eccentricity_error_min: Optional[float] = None
    eccentricity_error_max: Optional[float] = None
    inclination: Optional[float] = None
    inclination_error_min: Optional[float] = None
    inclination_error_max: Optional[float] = None
    equilibrium_temperature: Optional[float] = None
    equilibrium_temperature_error_min: Optional[float] = None
    equilibrium_temperature_error_max: Optional[float] = None
    source: str = "unknown"
    last_updated: datetime = datetime.now()

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "host_star": self.host_star,
            "discovery_year": self.discovery_year,
            "discovery_method": self.discovery_method,
            "mass": self.mass,
            "mass_error_min": self.mass_error_min,
            "mass_error_max": self.mass_error_max,
            "radius": self.radius,
            "radius_error_min": self.radius_error_min,
            "radius_error_max": self.radius_error_max,
            "orbital_period": self.orbital_period,
            "orbital_period_error_min": self.orbital_period_error_min,
            "orbital_period_error_max": self.orbital_period_error_max,
            "semi_major_axis": self.semi_major_axis,
            "semi_major_axis_error_min": self.semi_major_axis_error_min,
            "semi_major_axis_error_max": self.semi_major_axis_error_max,
            "eccentricity": self.eccentricity,
            "eccentricity_error_min": self.eccentricity_error_min,
            "eccentricity_error_max": self.eccentricity_error_max,
            "inclination": self.inclination,
            "inclination_error_min": self.inclination_error_min,
            "inclination_error_max": self.inclination_error_max,
            "equilibrium_temperature": self.equilibrium_temperature,
            "equilibrium_temperature_error_min": self.equilibrium_temperature_error_min,
            "equilibrium_temperature_error_max": self.equilibrium_temperature_error_max,
            "source": self.source,
            "last_updated": self.last_updated.isoformat()
        } 