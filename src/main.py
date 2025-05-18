import os
from datetime import datetime
from src.data_collectors.nasa_exoplanet import NASAExoplanetCollector
from src.data_collectors.exoplanet_eu import ExoplanetEUCollector
from src.data_collectors.open_exoplanet import OpenExoplanetCollector
from src.utils.data_processor import DataProcessor

def main():
    # Create output directory if it doesn't exist
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialize data processor
    processor = DataProcessor()
    
    # Collect data from NASA Exoplanet Archive
    print("Collecting data from NASA Exoplanet Archive...")
    nasa_collector = NASAExoplanetCollector()
    nasa_exoplanets = nasa_collector.fetch_data()
    processor.add_exoplanets(nasa_exoplanets, "NASA Exoplanet Archive")
    print(f"Collected {len(nasa_exoplanets)} exoplanets from NASA Exoplanet Archive")
    
    # Collect data from Exoplanet.eu (if CSV file exists)
    exoplanet_eu_csv = "data/exoplanet_eu.csv"  # Update this path to your CSV file
    if os.path.exists(exoplanet_eu_csv):
        print("Collecting data from Exoplanet.eu...")
        eu_collector = ExoplanetEUCollector(exoplanet_eu_csv)
        eu_exoplanets = eu_collector.fetch_data()
        processor.add_exoplanets(eu_exoplanets, "The Extrasolar Planets Encyclopaedia")
        print(f"Collected {len(eu_exoplanets)} exoplanets from Exoplanet.eu")
    
    # Collect data from Open Exoplanet Catalogue
    print("Collecting data from Open Exoplanet Catalogue...")
    oec_collector = OpenExoplanetCollector()
    oec_exoplanets = oec_collector.fetch_data()
    processor.add_exoplanets(oec_exoplanets, "Open Exoplanet Catalogue")
    print(f"Collected {len(oec_exoplanets)} exoplanets from Open Exoplanet Catalogue")
    
    # Export consolidated data
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_path = os.path.join(output_dir, f"exoplanets_{timestamp}.csv")
    json_path = os.path.join(output_dir, f"exoplanets_{timestamp}.json")
    
    processor.export_to_csv(csv_path)
    processor.export_to_json(json_path)
    
    # Print statistics
    stats = processor.get_statistics()
    print("\nData Collection Statistics:")
    print(f"Total exoplanets: {stats['total_exoplanets']}")
    print("\nSources:")
    for source, count in stats['sources'].items():
        print(f"  {source}: {count}")
    print("\nDiscovery Methods:")
    for method, count in stats['discovery_methods'].items():
        print(f"  {method}: {count}")
    print("\nDiscovery Years:")
    for year, count in sorted(stats['discovery_years'].items()):
        print(f"  {year}: {count}")
    
    print(f"\nData exported to:")
    print(f"  CSV: {csv_path}")
    print(f"  JSON: {json_path}")

if __name__ == "__main__":
    main() 