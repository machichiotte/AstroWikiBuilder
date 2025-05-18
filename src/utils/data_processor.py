from typing import List, Dict, Set
from src.models.exoplanet import Exoplanet
import pandas as pd
from datetime import datetime
from src.utils.wikipedia_checker import WikipediaChecker

class DataProcessor:
    def __init__(self):
        self.exoplanets: Dict[str, Exoplanet] = {}
        self.wikipedia_checker = WikipediaChecker()
    
    def add_exoplanets(self, exoplanets: List[Exoplanet], source: str):
        """
        Add exoplanets from a source to the consolidated database
        """
        for exoplanet in exoplanets:
            if exoplanet.name in self.exoplanets:
                # Update existing exoplanet with new data if it's more recent
                existing = self.exoplanets[exoplanet.name]
                if exoplanet.last_updated > existing.last_updated:
                    self.exoplanets[exoplanet.name] = exoplanet
            else:
                # Add new exoplanet
                self.exoplanets[exoplanet.name] = exoplanet
    
    def get_all_exoplanets(self) -> List[Exoplanet]:
        """
        Get all consolidated exoplanets
        """
        return list(self.exoplanets.values())
    
    def export_to_csv(self, filepath: str, exoplanets: List[Exoplanet] = None):
        """
        Export consolidated data or a liste d'exoplanètes à CSV
        """
        if exoplanets is None:
            data = [exoplanet.to_dict() for exoplanet in self.exoplanets.values()]
        else:
            data = [exoplanet.to_dict() for exoplanet in exoplanets]
        df = pd.DataFrame(data)
        df.to_csv(filepath, index=False)
    
    def export_to_json(self, filepath: str):
        """
        Export consolidated data to JSON
        """
        data = [exoplanet.to_dict() for exoplanet in self.exoplanets.values()]
        df = pd.DataFrame(data)
        df.to_json(filepath, orient='records', indent=2)
    
    def get_statistics(self) -> Dict:
        """
        Get statistics about the consolidated data
        """
        total = len(self.exoplanets)
        sources = {}
        discovery_years = {}
        discovery_methods = {}
        
        for exoplanet in self.exoplanets.values():
            # Count sources
            sources[exoplanet.source] = sources.get(exoplanet.source, 0) + 1
            
            # Count discovery years
            if exoplanet.discovery_year:
                discovery_years[exoplanet.discovery_year] = discovery_years.get(exoplanet.discovery_year, 0) + 1
            
            # Count discovery methods
            if exoplanet.discovery_method:
                discovery_methods[exoplanet.discovery_method] = discovery_methods.get(exoplanet.discovery_method, 0) + 1
        
        return {
            "total_exoplanets": total,
            "sources": sources,
            "discovery_years": discovery_years,
            "discovery_methods": discovery_methods
        }
    
    def filter_exoplanets_without_articles(self) -> List[Exoplanet]:
        """
        Filtre les exoplanètes qui n'ont pas encore d'article sur Wikipedia en français
        
        Returns:
            List[Exoplanet]: Liste des exoplanètes sans article
        """
        # Générer les titres d'articles potentiels
        titles = []
        print("\nPréparation des titres d'articles à vérifier...")
        for exoplanet in self.exoplanets.values():
            # Format standard : "Nom de l'exoplanète"
            title = f"{exoplanet.name}"
            titles.append(title)
        print(f"Nombre de titres à vérifier : {len(titles)}")
        
        # Vérifier l'existence des articles par lots de 50
        print("\nDébut de la vérification des articles sur Wikipedia...")
        article_exists = {}
        batch_size = 50
        total_batches = (len(titles) + batch_size - 1) // batch_size
        
        for i in range(0, len(titles), batch_size):
            batch = titles[i:i + batch_size]
            batch_num = (i // batch_size) + 1
            print(f"\nTraitement du lot {batch_num}/{total_batches} ({len(batch)} articles)")
            batch_results = self.wikipedia_checker.check_multiple_articles(batch)
            article_exists.update(batch_results)
        
        # Filtrer les exoplanètes sans article
        print("\nFiltrage des exoplanètes sans article...")
        exoplanets_without_articles = []
        for exoplanet in self.exoplanets.values():
            title = f"{exoplanet.name}"
            if not article_exists.get(title, False):
                exoplanets_without_articles.append(exoplanet)
                print(f"Article manquant pour : {title}")
        
        print(f"\nNombre d'exoplanètes sans article : {len(exoplanets_without_articles)}")
        return exoplanets_without_articles 