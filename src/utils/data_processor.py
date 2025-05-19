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
                if field == 'name':
                    continue
                value = getattr(exoplanet, field)
                if value and value.reference:
                    source = value.reference.source.value
                    stats['sources'][source] = stats['sources'].get(source, 0) + 1
            
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
        # Récupérer tous les noms d'exoplanètes
        exoplanet_names = list(self.exoplanets.keys())
        
        # Vérifier l'existence des articles par lots de 50
        batch_size = 50
        results = {}
        
        for i in range(0, len(exoplanet_names), batch_size):
            batch = exoplanet_names[i:i + batch_size]
            batch_results = self.wikipedia_checker.check_multiple_articles(batch, delay=1.0)
            results.update(batch_results)
        
        # Filtrer les exoplanètes qui n'ont pas d'article
        exoplanets_without_articles = []
        for name, exists in results.items():
            if not exists:
                exoplanet = self.exoplanets.get(name)
                if exoplanet:
                    exoplanets_without_articles.append(exoplanet)
        
        return exoplanets_without_articles
    
    def _exoplanet_to_dict(self, exoplanet: Exoplanet) -> Dict:
        """Convertit une exoplanète en dictionnaire pour l'export"""
        data = {
            'name': exoplanet.name,
            'other_names': {name: ref.to_wiki_value() for name, ref in exoplanet.other_names.items()}
        }
        
        # Fonction helper pour ajouter un champ avec sa référence
        def add_field(field_name: str, data_point: DataPoint):
            if data_point:
                data[field_name] = data_point.to_wiki_value()
        
        # Étoile hôte
        add_field('host_star', exoplanet.host_star)
        add_field('star_epoch', exoplanet.star_epoch)
        add_field('right_ascension', exoplanet.right_ascension)
        add_field('declination', exoplanet.declination)
        add_field('distance', exoplanet.distance)
        add_field('constellation', exoplanet.constellation)
        add_field('spectral_type', exoplanet.spectral_type)
        add_field('apparent_magnitude', exoplanet.apparent_magnitude)
        
        # Caractéristiques orbitales
        add_field('semi_major_axis', exoplanet.semi_major_axis)
        add_field('periastron', exoplanet.periastron)
        add_field('apoastron', exoplanet.apoastron)
        add_field('eccentricity', exoplanet.eccentricity)
        add_field('orbital_period', exoplanet.orbital_period)
        add_field('angular_distance', exoplanet.angular_distance)
        add_field('periastron_time', exoplanet.periastron_time)
        add_field('inclination', exoplanet.inclination)
        add_field('argument_of_periastron', exoplanet.argument_of_periastron)
        add_field('epoch', exoplanet.epoch)
        
        # Caractéristiques physiques
        add_field('mass', exoplanet.mass)
        add_field('minimum_mass', exoplanet.minimum_mass)
        add_field('radius', exoplanet.radius)
        add_field('density', exoplanet.density)
        add_field('gravity', exoplanet.gravity)
        add_field('rotation_period', exoplanet.rotation_period)
        add_field('temperature', exoplanet.temperature)
        add_field('bond_albedo', exoplanet.bond_albedo)
        
        # Atmosphère
        add_field('pressure', exoplanet.pressure)
        add_field('composition', exoplanet.composition)
        add_field('wind_speed', exoplanet.wind_speed)
        
        # Découverte
        add_field('discoverers', exoplanet.discoverers)
        add_field('discovery_program', exoplanet.discovery_program)
        add_field('discovery_method', exoplanet.discovery_method)
        add_field('discovery_date', exoplanet.discovery_date)
        add_field('discovery_location', exoplanet.discovery_location)
        add_field('pre_discovery', exoplanet.pre_discovery)
        add_field('detection_method', exoplanet.detection_method)
        add_field('status', exoplanet.status)
        
        return data
    
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