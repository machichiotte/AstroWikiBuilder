# src/utils/data_processor.py
from typing import List, Dict, Set, Tuple
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
        print(f"  Ajout de {len(exoplanets)} exoplanètes depuis {source}...")
        for exoplanet in exoplanets:
            if exoplanet.name in self.exoplanets:
                # Fusion avec l'exoplanète existante
                self.exoplanets[exoplanet.name].merge_with(exoplanet)
            else:
                # Ajout d'une nouvelle exoplanète
                self.exoplanets[exoplanet.name] = exoplanet
        print(f"  Ajout terminé. Total actuel : {len(self.exoplanets)} exoplanètes")
    
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
    
    def filter_exoplanets_without_articles(self) -> List[Tuple[Exoplanet, Dict[str, 'WikiArticleInfo']]]:
        """Filtre les exoplanètes qui n'ont pas d'article sur Wikipedia.
        
        Returns:
            List[Tuple[Exoplanet, Dict[str, WikiArticleInfo]]]: Liste des tuples (exoplanet, article_info)
            où article_info est un dictionnaire des articles existants pour cette exoplanète
        """
        exoplanets_without_articles = []
        checker = WikipediaChecker()
        
        # Vérifier les articles pour chaque exoplanète
        for exoplanet in self.exoplanets:
            # Vérifier d'abord le nom principal
            article_info = checker.check_multiple_articles([exoplanet.name])
            
            # Si pas d'article avec le nom principal, vérifier les noms alternatifs
            if not any(info.exists for info in article_info.values()):
                if exoplanet.other_names:
                    alt_articles = checker.check_multiple_articles(list(exoplanet.other_names))
                    article_info.update(alt_articles)
            
            # Si aucun article n'existe, ajouter à la liste
            if not any(info.exists for info in article_info.values()):
                exoplanets_without_articles.append((exoplanet, article_info))
        
        return exoplanets_without_articles
    
    def get_all_articles_info(self) -> List[Tuple[Exoplanet, Dict[str, 'WikiArticleInfo']]]:
        """Obtient les informations de tous les articles Wikipedia pour chaque exoplanète."""
        print("\nDébut de la vérification des articles Wikipedia...")
        all_articles_info = []
        checker = WikipediaChecker()
        exoplanets_list = list(self.exoplanets.values())
        total = len(exoplanets_list)
        step = max(1, total // 20)  # 5% du total
        
        print(f"Nombre total d'exoplanètes à vérifier : {total}")
        
        # Préparation des lots de titres à vérifier
        all_titles = []
        title_to_exoplanet = {}
        
        for exoplanet in exoplanets_list:
            # Ajouter le nom principal
            all_titles.append(exoplanet.name)
            title_to_exoplanet[exoplanet.name] = exoplanet
            
            # Ajouter les noms alternatifs
            if exoplanet.other_names:
                for alt_name in exoplanet.other_names:
                    all_titles.append(alt_name)
                    title_to_exoplanet[alt_name] = exoplanet
        
        # Traitement par lots de 50
        batch_size = 50
        total_batches = (len(all_titles) + batch_size - 1) // batch_size
        
        for batch_idx in range(total_batches):
            start_idx = batch_idx * batch_size
            end_idx = min((batch_idx + 1) * batch_size, len(all_titles))
            batch_titles = all_titles[start_idx:end_idx]
            
            percent = int((batch_idx / total_batches) * 100)
            print(f"[{percent:3d}%] Vérification du lot {batch_idx + 1}/{total_batches} ({len(batch_titles)} titres)", flush=True)
            
            # Vérifier le lot de titres
            batch_results = checker.check_multiple_articles(batch_titles)
            
            # Regrouper les résultats par exoplanète
            exoplanet_results = {}
            for title, info in batch_results.items():
                # Vérifier si le titre est dans notre dictionnaire
                if title in title_to_exoplanet:
                    exoplanet = title_to_exoplanet[title]
                    if exoplanet.name not in exoplanet_results:
                        exoplanet_results[exoplanet.name] = (exoplanet, {})
                    exoplanet_results[exoplanet.name][1][title] = info
                else:
                    print(f"  ⚠️ Titre non trouvé dans la correspondance : {title}")
            
            # Ajouter les résultats au total
            all_articles_info.extend(exoplanet_results.values())
            
            # Log détaillé pour chaque exoplanète du lot
            for exoplanet, article_info in exoplanet_results.values():
                if any(info.exists for info in article_info.values()):
                    print(f"  ✓ Article trouvé pour {exoplanet.name}")
                else:
                    print(f"  ✗ Pas d'article pour {exoplanet.name}")
        
        print("Vérification des articles Wikipedia terminée.")
        return all_articles_info

    def separate_articles_by_status(self) -> Tuple[List[Tuple[Exoplanet, Dict[str, 'WikiArticleInfo']]], List[Tuple[Exoplanet, Dict[str, 'WikiArticleInfo']]]]:
        """Sépare les articles en deux listes : existants et manquants."""
        print("\nDébut de la séparation des articles...")
        all_articles = self.get_all_articles_info()
        existing_articles = []
        missing_articles = []
        
        print("Séparation des articles en cours...")
        for exoplanet, article_info in all_articles:
            if any(info.exists for info in article_info.values()):
                existing_articles.append((exoplanet, article_info))
            else:
                missing_articles.append((exoplanet, article_info))
        
        print(f"Séparation terminée :")
        print(f"- Articles existants : {len(existing_articles)}")
        print(f"- Articles manquants : {len(missing_articles)}")
        
        return existing_articles, missing_articles
    
    def format_wiki_links_data(self, articles: List[Tuple[Exoplanet, Dict[str, 'WikiArticleInfo']]]) -> Tuple[List[dict], List[List[str]]]:
        """Formate les données des liens Wikipedia pour l'export CSV et JSON."""
        print(f"\nFormatage des données pour {len(articles)} articles...")
        json_data = []
        csv_data = []
        
        for idx, (exoplanet, article_info) in enumerate(articles, 1):
            if idx % 100 == 0:
                print(f"  Formatage de l'article {idx} sur {len(articles)}...")
                
            if article_info:
                for name, info in article_info.items():
                    # Pour les articles existants, inclure toutes les informations
                    if info.exists:
                        json_data.append({
                            'exoplanet': exoplanet.name,
                            'article_name': name,
                            'type': 'Redirection' if info.is_redirect else 'Direct',
                            'url': info.url,
                            'redirect_target': info.redirect_target if info.is_redirect else None,
                            'host_star': exoplanet.host_star.value if exoplanet.host_star else None
                        })
                        csv_data.append([
                            exoplanet.name,
                            name,
                            'Redirection' if info.is_redirect else 'Direct',
                            info.url,
                            info.redirect_target if info.is_redirect else '',
                            exoplanet.host_star.value if exoplanet.host_star else ''
                        ])
                    # Pour les articles manquants, ne garder que le nom
                    else:
                        json_data.append({
                            'exoplanet': exoplanet.name,
                            'article_name': name,
                            'host_star': exoplanet.host_star.value if exoplanet.host_star else None
                        })
                        csv_data.append([
                            exoplanet.name,
                            name,
                            exoplanet.host_star.value if exoplanet.host_star else ''
                        ])
            else:
                json_data.append({
                    'exoplanet': exoplanet.name,
                    'host_star': exoplanet.host_star.value if exoplanet.host_star else None
                })
                csv_data.append([
                    exoplanet.name,
                    exoplanet.host_star.value if exoplanet.host_star else ''
                ])
        
        print("Formatage des données terminé.")
        return json_data, csv_data
    
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