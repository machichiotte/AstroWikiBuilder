# src/services/export_service.py
import logging
import pandas as pd
import json
from typing import List, Dict, Any, Optional
from src.models.data_source_exoplanet import DataSourceExoplanet, DataPoint

logger = logging.getLogger(__name__)

class ExportService:
    def __init__(self):
        logger.info("ExportService initialized.")

    def _exoplanet_to_dict_flat(self, exoplanet: DataSourceExoplanet) -> Dict[str, Any]:
        """
        Convertit un objet Exoplanet en dictionnaire avec des valeurs 'plates' (pas d'objets DataPoint).
        Utilise la valeur de DataPoint, et ajoute la source si disponible.
        """
        data = {'name': exoplanet.pl_name}
        
        pl_altname_str = ", ".join(exoplanet.pl_altname) if exoplanet.pl_altname else None
        if pl_altname_str: # Only add if there are other names
             data['pl_altname'] = pl_altname_str

        for field_name in exoplanet.__dataclass_fields__:
            if field_name in ['name', 'pl_altname']:
                continue
            
            attr_value = getattr(exoplanet, field_name)
            if isinstance(attr_value, DataPoint):
                if attr_value.value is not None:
                    data[field_name] = attr_value.value
                    if attr_value.reference and attr_value.reference.source:
                        data[f"{field_name}_source"] = attr_value.reference.source.value
                    if attr_value.reference and attr_value.reference.update_date:
                         data[f"{field_name}_ref_date"] = attr_value.reference.update_date.isoformat()
            elif attr_value is not None: # For any direct attributes not DataPoint (if any added later)
                data[field_name] = attr_value
        
        return data # No need to filter Nones here, pandas handles it gracefully in to_csv. For JSON, it might be desired.

    def export_exoplanets_to_csv(self, filename: str, exoplanets: List[DataSourceExoplanet]) -> None:
        logger.info(f"Exporting {len(exoplanets)} exoplanets to CSV: {filename}")
        if not exoplanets:
            logger.warning("No exoplanets to export to CSV.")
            # Create empty CSV with headers if that's desired, or just return
            # For now, just creating an empty file might be misleading.
            # df = pd.DataFrame([]) 
            # df.to_csv(filename, index=False, encoding='utf-8')
            return

        data_for_df = [self._exoplanet_to_dict_flat(exoplanet) for exoplanet in exoplanets]
        df = pd.DataFrame(data_for_df)
        
        try:
            df.to_csv(filename, index=False, encoding='utf-8')
            logger.info(f"Successfully exported exoplanets to {filename}")
        except Exception as e:
            logger.error(f"Error exporting exoplanets to CSV {filename}: {e}")
            raise # Re-raise the exception to notify the caller

    def export_exoplanets_to_json(self, filename: str, exoplanets: List[DataSourceExoplanet]) -> None:
        logger.info(f"Exporting {len(exoplanets)} exoplanets to JSON: {filename}")
        if not exoplanets:
            logger.warning("No exoplanets to export to JSON.")
            # with open(filename, 'w', encoding='utf-8') as f:
            #    json.dump([], f, ensure_ascii=False, indent=2)
            return
            
        # For JSON, we might want a slightly different structure or to keep DataPoint objects
        # The original _exoplanet_to_dict called .to_wiki_value() which includes HTML-like refs.
        # For a data JSON, flat values or structured DataPoints are usually better.
        # Using the same flat structure as CSV for consistency here.
        data_to_export = [self._exoplanet_to_dict_flat(exoplanet) for exoplanet in exoplanets]
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data_to_export, f, ensure_ascii=False, indent=2)
            logger.info(f"Successfully exported exoplanets to {filename}")
        except Exception as e:
            logger.error(f"Error exporting exoplanets to JSON {filename}: {e}")
            raise

    def export_generic_list_of_dicts_to_csv(self, filename: str, data: List[Dict[str, Any]], headers: Optional[List[str]] = None) -> None:
        logger.info(f"Exporting {len(data)} records to CSV: {filename}")
        if not data:
            logger.warning(f"No data to export to CSV: {filename}")
            return

        df = pd.DataFrame(data)
        if headers: # Ensure specified header order and inclusion
            df = df.reindex(columns=headers)

        try:
            df.to_csv(filename, index=False, encoding='utf-8')
            logger.info(f"Successfully exported data to {filename}")
        except Exception as e:
            logger.error(f"Error exporting data to CSV {filename}: {e}")
            raise

    def export_generic_list_of_dicts_to_json(self, filename: str, data: List[Dict[str, Any]]) -> None:
        logger.info(f"Exporting {len(data)} records to JSON: {filename}")
        if not data:
            logger.warning(f"No data to export to JSON: {filename}")
            return
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info(f"Successfully exported data to {filename}")
        except Exception as e:
            logger.error(f"Error exporting data to JSON {filename}: {e}")
            raise