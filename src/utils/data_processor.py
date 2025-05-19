from typing import List, Dict, Set
from src.models.exoplanet import Exoplanet
from src.models.reference import SourceType, DataPoint
import pandas as pd
from datetime import datetime
from src.utils.wikipedia_checker import WikipediaChecker
import json

class DataProcessor:
    def __init__(self):
        self.exoplanets: Dict[str, Exoplanet] = {}
        self.wikipedia_checker = WikipediaChecker()
    
    def add_exoplanets(self, exoplanets: List[Exoplanet], source: str) -> None:
        """
        Ajoute ou fusionne les exoplanètes dans le dictionnaire
        """
        for exoplanet in exoplanets:
            if exoplanet.name in self.exoplanets:
                # Fusion avec l'exoplanète existante
                self.exoplanets[exoplanet.name].merge_with(exoplanet)
            else:
                # Ajout d'une nouvelle exoplanète
                self.exoplanets[exoplanet.name] = exoplanet
    
    def get_all_exoplanets(self) -> List[Exoplanet]:
        """
        Get all consolidated exoplanets
        """
        return list(self.exoplanets.values())
    
    def get_statistics(self) -> Dict:
        """
        Retourne des statistiques sur les données collectées
        """
        stats = {
            'total_exoplanets': len(self.exoplanets),
            'sources': {},
            'discovery_methods': {},
            'discovery_years': {}
        }
        
        for exoplanet in self.exoplanets.values():
            # Statistiques par source
            for field in exoplanet.__dataclass_fields__:
                if field == 'name' or field == 'other_names':
                    continue
                value = getattr(exoplanet, field)
                if value and hasattr(value, 'reference') and value.reference:
                    source = value.reference.source.value
                    stats['sources'][source] = stats['sources'].get(source, 0) + 1
            
            # Statistiques pour other_names (maintenant une liste simple)
            if exoplanet.other_names:
                stats['sources']['EPE'] = stats['sources'].get('EPE', 0) + len(exoplanet.other_names)
            
            # Statistiques par méthode de découverte
            if exoplanet.discovery_method:
                method = exoplanet.discovery_method.value
                stats['discovery_methods'][method] = stats['discovery_methods'].get(method, 0) + 1
            
            # Statistiques par année de découverte
            if exoplanet.discovery_date:
                year = exoplanet.discovery_date.value
                stats['discovery_years'][year] = stats['discovery_years'].get(year, 0) + 1
        
        return stats
    
    def filter_exoplanets_without_articles(self) -> List[Exoplanet]:
        """
        Filtre les exoplanètes qui n'ont pas d'article sur Wikipédia
        """
        exoplanets_without_articles = []
        batch_size = 50
        
        # D'abord, vérifier tous les noms principaux
        main_names = [exoplanet.name for exoplanet in self.exoplanets.values()]
        main_results = {}
        
        for i in range(0, len(main_names), batch_size):
            batch = main_names[i:i + batch_size]
            batch_results = self.wikipedia_checker.check_multiple_articles(batch, delay=0.01)
            main_results.update(batch_results)
        
        # Pour chaque exoplanète, vérifier si elle a un article sous son nom principal
        for exoplanet in self.exoplanets.values():
            if main_results.get(exoplanet.name, False):
                continue  # L'article existe déjà sous le nom principal, pas besoin de vérifier les noms alternatifs
            
            # Si pas d'article sous le nom principal, vérifier les noms alternatifs
            if exoplanet.other_names:
                alt_results = {}
                
                for i in range(0, len(exoplanet.other_names), batch_size):
                    batch = exoplanet.other_names[i:i + batch_size]
                    batch_results = self.wikipedia_checker.check_multiple_articles(batch, delay=0.01)
                    alt_results.update(batch_results)
                
                # Si aucun article n'existe sous les noms alternatifs, ajouter à la liste
                if not any(alt_results.values()):
                    exoplanets_without_articles.append(exoplanet)
            else:
                # Pas de noms alternatifs et pas d'article sous le nom principal
                exoplanets_without_articles.append(exoplanet)
        
        return exoplanets_without_articles
    
    def _exoplanet_to_dict(self, exoplanet: Exoplanet) -> dict:
        """Convertit un objet Exoplanet en dictionnaire"""
        data = {
            'name': exoplanet.name,
            'other_names': exoplanet.other_names,  # Maintenant c'est une liste simple
            'host_star': exoplanet.host_star.to_wiki_value() if exoplanet.host_star else None,
            'star_epoch': exoplanet.star_epoch.to_wiki_value() if exoplanet.star_epoch else None,
            'right_ascension': exoplanet.right_ascension.to_wiki_value() if exoplanet.right_ascension else None,
            'declination': exoplanet.declination.to_wiki_value() if exoplanet.declination else None,
            'distance': exoplanet.distance.to_wiki_value() if exoplanet.distance else None,
            'constellation': exoplanet.constellation.to_wiki_value() if exoplanet.constellation else None,
            'spectral_type': exoplanet.spectral_type.to_wiki_value() if exoplanet.spectral_type else None,
            'apparent_magnitude': exoplanet.apparent_magnitude.to_wiki_value() if exoplanet.apparent_magnitude else None,
            'semi_major_axis': exoplanet.semi_major_axis.to_wiki_value() if exoplanet.semi_major_axis else None,
            'periastron': exoplanet.periastron.to_wiki_value() if exoplanet.periastron else None,
            'apoastron': exoplanet.apoastron.to_wiki_value() if exoplanet.apoastron else None,
            'eccentricity': exoplanet.eccentricity.to_wiki_value() if exoplanet.eccentricity else None,
            'orbital_period': exoplanet.orbital_period.to_wiki_value() if exoplanet.orbital_period else None,
            'angular_distance': exoplanet.angular_distance.to_wiki_value() if exoplanet.angular_distance else None,
            'periastron_time': exoplanet.periastron_time.to_wiki_value() if exoplanet.periastron_time else None,
            'inclination': exoplanet.inclination.to_wiki_value() if exoplanet.inclination else None,
            'argument_of_periastron': exoplanet.argument_of_periastron.to_wiki_value() if exoplanet.argument_of_periastron else None,
            'epoch': exoplanet.epoch.to_wiki_value() if exoplanet.epoch else None,
            'mass': exoplanet.mass.to_wiki_value() if exoplanet.mass else None,
            'minimum_mass': exoplanet.minimum_mass.to_wiki_value() if exoplanet.minimum_mass else None,
            'radius': exoplanet.radius.to_wiki_value() if exoplanet.radius else None,
            'density': exoplanet.density.to_wiki_value() if exoplanet.density else None,
            'gravity': exoplanet.gravity.to_wiki_value() if exoplanet.gravity else None,
            'rotation_period': exoplanet.rotation_period.to_wiki_value() if exoplanet.rotation_period else None,
            'temperature': exoplanet.temperature.to_wiki_value() if exoplanet.temperature else None,
            'bond_albedo': exoplanet.bond_albedo.to_wiki_value() if exoplanet.bond_albedo else None,
            'pressure': exoplanet.pressure.to_wiki_value() if exoplanet.pressure else None,
            'composition': exoplanet.composition.to_wiki_value() if exoplanet.composition else None,
            'wind_speed': exoplanet.wind_speed.to_wiki_value() if exoplanet.wind_speed else None,
            'discoverers': exoplanet.discoverers.to_wiki_value() if exoplanet.discoverers else None,
            'discovery_program': exoplanet.discovery_program.to_wiki_value() if exoplanet.discovery_program else None,
            'discovery_method': exoplanet.discovery_method.to_wiki_value() if exoplanet.discovery_method else None,
            'discovery_date': exoplanet.discovery_date.to_wiki_value() if exoplanet.discovery_date else None,
            'discovery_location': exoplanet.discovery_location.to_wiki_value() if exoplanet.discovery_location else None,
            'pre_discovery': exoplanet.pre_discovery.to_wiki_value() if exoplanet.pre_discovery else None,
            'detection_method': exoplanet.detection_method.to_wiki_value() if exoplanet.detection_method else None,
            'status': exoplanet.status.to_wiki_value() if exoplanet.status else None
        }
        
        # Supprimer les champs vides
        return {k: v for k, v in data.items() if v is not None}
    
    def export_to_csv(self, filename: str, exoplanets: List[Exoplanet] = None) -> None:
        """
        Exporte les données en CSV
        """
        if exoplanets is None:
            exoplanets = list(self.exoplanets.values())
        
        # Convertir les exoplanètes en dictionnaires
        data = [self._exoplanet_to_dict(exoplanet) for exoplanet in exoplanets]
        
        # Créer le DataFrame
        df = pd.DataFrame(data)
        
        # Exporter en CSV
        df.to_csv(filename, index=False, encoding='utf-8')
    
    def export_to_json(self, filename: str, exoplanets: List[Exoplanet] = None) -> None:
        """
        Exporte les données en JSON
        """
        if exoplanets is None:
            exoplanets = list(self.exoplanets.values())
        
        # Convertir les exoplanètes en dictionnaires
        data = [self._exoplanet_to_dict(exoplanet) for exoplanet in exoplanets]
        
        # Exporter en JSON
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2) 