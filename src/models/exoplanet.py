from dataclasses import dataclass, field
from typing import Optional, Dict, List
from datetime import datetime
from .reference import DataPoint, Reference, SourceType

@dataclass
class Exoplanet:
    # Identifiants
    name: str
    other_names: List[str] = field(default_factory=list)
    
    # Étoile hôte
    host_star: DataPoint = None
    star_epoch: DataPoint = None
    right_ascension: DataPoint = None
    declination: DataPoint = None
    distance: DataPoint = None
    constellation: DataPoint = None
    spectral_type: DataPoint = None
    apparent_magnitude: DataPoint = None
    
    # Caractéristiques orbitales
    semi_major_axis: DataPoint = None
    periastron: DataPoint = None
    apoastron: DataPoint = None
    eccentricity: DataPoint = None
    orbital_period: DataPoint = None
    angular_distance: DataPoint = None
    periastron_time: DataPoint = None
    inclination: DataPoint = None
    argument_of_periastron: DataPoint = None
    epoch: DataPoint = None
    
    # Caractéristiques physiques
    mass: DataPoint = None
    minimum_mass: DataPoint = None
    radius: DataPoint = None
    density: DataPoint = None
    gravity: DataPoint = None
    rotation_period: DataPoint = None
    temperature: DataPoint = None
    bond_albedo: DataPoint = None
    
    # Atmosphère
    pressure: DataPoint = None
    composition: DataPoint = None
    wind_speed: DataPoint = None
    
    # Découverte
    discoverers: DataPoint = None
    discovery_program: DataPoint = None
    discovery_method: DataPoint = None
    discovery_date: DataPoint = None
    discovery_location: DataPoint = None
    pre_discovery: DataPoint = None
    detection_method: DataPoint = None
    status: DataPoint = None
    
    def merge_with(self, other: 'Exoplanet') -> None:
        """Fusionne les données d'une autre exoplanète en respectant la priorité des sources"""
        for field_name in self.__dataclass_fields__:
            if field_name == 'name':
                continue
                
            current_value = getattr(self, field_name)
            other_value = getattr(other, field_name)
            
            if current_value is None and other_value is not None:
                setattr(self, field_name, other_value)
            elif current_value is not None and other_value is not None:
                # Priorité : NASA > EPE > OEP
                current_source = current_value.reference.source if current_value.reference else None
                other_source = other_value.reference.source if other_value.reference else None
                
                if other_source == SourceType.NASA:
                    setattr(self, field_name, other_value)
                elif current_source != SourceType.NASA and other_source == SourceType.EPE:
                    setattr(self, field_name, other_value)
                elif current_source not in [SourceType.NASA, SourceType.EPE] and other_source == SourceType.OEP:
                    setattr(self, field_name, other_value)
    
    def to_wiki_infobox(self) -> str:
        """Génère le contenu de l'infobox Wikipédia"""
        infobox = "{{Infobox Exoplanète\n"
        
        # Nom
        infobox += f" | nom = {self.name}\n"
        
        # Étoile
        if self.host_star:
            infobox += f" | étoile = {self.host_star.to_wiki_value()}\n"
        if self.star_epoch:
            infobox += f" | époque étoile = {self.star_epoch.to_wiki_value()}\n"
        if self.right_ascension:
            infobox += f" | ascension droite = {self.right_ascension.to_wiki_value()}\n"
        if self.declination:
            infobox += f" | déclinaison = {self.declination.to_wiki_value()}\n"
        if self.distance:
            infobox += f" | distance = {self.distance.to_wiki_value()}\n"
        if self.constellation:
            infobox += f" | constellation = {self.constellation.to_wiki_value()}\n"
        if self.spectral_type:
            infobox += f" | type spectral = {self.spectral_type.to_wiki_value()}\n"
        if self.apparent_magnitude:
            infobox += f" | magnitude apparente = {self.apparent_magnitude.to_wiki_value()}\n"
        
        # Caractéristiques orbitales
        if self.semi_major_axis:
            infobox += f" | demi-grand axe = {self.semi_major_axis.to_wiki_value()}\n"
        if self.periastron:
            infobox += f" | périastre = {self.periastron.to_wiki_value()}\n"
        if self.apoastron:
            infobox += f" | apoastre = {self.apoastron.to_wiki_value()}\n"
        if self.eccentricity:
            infobox += f" | excentricité = {self.eccentricity.to_wiki_value()}\n"
        if self.orbital_period:
            infobox += f" | période = {self.orbital_period.to_wiki_value()}\n"
        if self.angular_distance:
            infobox += f" | distance angulaire = {self.angular_distance.to_wiki_value()}\n"
        if self.periastron_time:
            infobox += f" | t_peri = {self.periastron_time.to_wiki_value()}\n"
        if self.inclination:
            infobox += f" | inclinaison = {self.inclination.to_wiki_value()}\n"
        if self.argument_of_periastron:
            infobox += f" | arg_péri = {self.argument_of_periastron.to_wiki_value()}\n"
        if self.epoch:
            infobox += f" | époque = {self.epoch.to_wiki_value()}\n"
        
        # Caractéristiques physiques
        if self.mass:
            infobox += f" | masse = {self.mass.to_wiki_value()}\n"
        if self.minimum_mass:
            infobox += f" | masse minimale = {self.minimum_mass.to_wiki_value()}\n"
        if self.radius:
            infobox += f" | rayon = {self.radius.to_wiki_value()}\n"
        if self.density:
            infobox += f" | masse volumique = {self.density.to_wiki_value()}\n"
        if self.gravity:
            infobox += f" | gravité = {self.gravity.to_wiki_value()}\n"
        if self.rotation_period:
            infobox += f" | période de rotation = {self.rotation_period.to_wiki_value()}\n"
        if self.temperature:
            infobox += f" | température = {self.temperature.to_wiki_value()}\n"
        if self.bond_albedo:
            infobox += f" | albedo_bond = {self.bond_albedo.to_wiki_value()}\n"
        
        # Atmosphère
        if self.pressure:
            infobox += f" | pression = {self.pressure.to_wiki_value()}\n"
        if self.composition:
            infobox += f" | composition = {self.composition.to_wiki_value()}\n"
        if self.wind_speed:
            infobox += f" | vitesse des vents = {self.wind_speed.to_wiki_value()}\n"
        
        # Découverte
        if self.discoverers:
            infobox += f" | découvreurs = {self.discoverers.to_wiki_value()}\n"
        if self.discovery_program:
            infobox += f" | programme = {self.discovery_program.to_wiki_value()}\n"
        if self.discovery_method:
            infobox += f" | méthode = {self.discovery_method.to_wiki_value()}\n"
        if self.discovery_date:
            infobox += f" | date = {self.discovery_date.to_wiki_value()}\n"
        if self.discovery_location:
            infobox += f" | lieu = {self.discovery_location.to_wiki_value()}\n"
        if self.pre_discovery:
            infobox += f" | prédécouverte = {self.pre_discovery.to_wiki_value()}\n"
        if self.detection_method:
            infobox += f" | détection = {self.detection_method.to_wiki_value()}\n"
        if self.status:
            infobox += f" | statut = {self.status.to_wiki_value()}\n"
        
        # Autres noms
        if self.other_names:
            infobox += f" | autres noms = {', '.join(self.other_names)}\n"
        
        infobox += "}}"
        return infobox 