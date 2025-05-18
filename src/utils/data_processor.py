from typing import List, Dict
from src.models.exoplanet import Exoplanet
import pandas as pd
from datetime import datetime

class DataProcessor:
    def __init__(self):
        self.exoplanets: Dict[str, Exoplanet] = {}
    
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
    
    def export_to_csv(self, filepath: str):
        """
        Export consolidated data to CSV
        """
        data = [exoplanet.to_dict() for exoplanet in self.exoplanets.values()]
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