# src/data_collectors/nasa_exoplanet_archive.py
import pandas as pd
import requests
from typing import List, Optional
from datetime import datetime
import logging
import os
from src.models.exoplanet import Exoplanet
from src.models.reference import DataPoint, Reference, SourceType
from src.utils.reference_manager import ReferenceManager

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NASAExoplanetArchiveCollector:
    BASE_URL = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+*+from+PSCompPars&format=csv"
    MOCK_DATA_PATH = "data/nasa_mock_data_complete.csv"
    
    def __init__(self, use_mock_data: bool = False):
        self.required_columns = ['pl_name', 'hostname', 'discoverymethod', 'disc_year']
        self.use_mock_data = use_mock_data
        self.reference_manager = ReferenceManager()
        self.last_update_date = datetime.now()  # Par défaut, on utilise la date actuelle
        
        # Créer le dossier data s'il n'existe pas
        os.makedirs("data", exist_ok=True)
    
    def fetch_data(self) -> List[Exoplanet]:
        """
        Fetch data from NASA Exoplanet Archive and convert to Exoplanet objects
        """
        try:
            if self.use_mock_data:
                if not os.path.exists(self.MOCK_DATA_PATH):
                    logger.error(f"Fichier de données mockées non trouvé : {self.MOCK_DATA_PATH}")
                    return []
                df = pd.read_csv(self.MOCK_DATA_PATH)
                logger.info("Utilisation des données mockées")
            else:
                # Télécharger les données
                response = requests.get(self.BASE_URL)
                response.raise_for_status()
                
                # Sauvegarder les données brutes
                with open(self.MOCK_DATA_PATH, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                
                # Lire les données avec pandas
                df = pd.read_csv(self.MOCK_DATA_PATH)
                logger.info(f"Données sauvegardées dans {self.MOCK_DATA_PATH}")
            
            logger.info(f"Colonnes trouvées dans le CSV NASA : {list(df.columns)}")
            
            # Vérification des colonnes requises
            missing_columns = [col for col in self.required_columns if col not in df.columns]
            if missing_columns:
                raise ValueError(f"Colonnes manquantes dans le CSV : {missing_columns}")
            
            exoplanets = []
            for index, row in df.iterrows():
                try:
                    exoplanet = self._convert_row_to_exoplanet(row)
                    if exoplanet:
                        exoplanets.append(exoplanet)
                except Exception as e:
                    logger.error(f"Erreur sur la ligne {index}: {str(e)}")
                    logger.debug(f"Données de la ligne : {row.to_dict()}")
            
            logger.info(f"Nombre d'exoplanètes traitées avec succès : {len(exoplanets)}")
            return exoplanets
            
        except Exception as e:
            logger.error(f"Erreur lors de la lecture du CSV NASA : {str(e)}")
            return []
    
    def _create_reference(self) -> Reference:
        """Crée une référence pour les données NASA"""
        return self.reference_manager.create_reference(
            source=SourceType.NEA,
            update_date=self.last_update_date,
            url="https://exoplanetarchive.ipac.caltech.edu/"
        )
    
    def _safe_float_conversion(self, value: any) -> Optional[float]:
        """Convertit une valeur en float de manière sécurisée"""
        if pd.isna(value):
            return None
        try:
            return float(value)
        except (ValueError, TypeError):
            return None
    
    def _convert_row_to_exoplanet(self, row: pd.Series) -> Optional[Exoplanet]:
        """
        Convert a row from NASA Exoplanet Archive to an Exoplanet object
        """
        try:
            ref = self._create_reference()
            
            # Validation des données de base
            if pd.isna(row['pl_name']) or pd.isna(row['hostname']):
                logger.warning(f"Données de base manquantes pour l'exoplanète : {row.get('pl_name', 'Unknown')}")
                return None
            
            
            # --- Right Ascension ---
            # rastr renvoie "19h16m52.13s" je veux "19/16/52.13"
            rastr_val = str(row['rastr']).strip()
            formatted_ra = rastr_val.replace('h', '/').replace('m', '/').replace('s', '')

            # --- Declination ---
            # decstr renvoie "+47d53m02.91s" je veux "+47/53/02.91"
            decstr_val = str(row['decstr']).strip()
            formatted_dec = decstr_val.replace('d', '/').replace('m', '/').replace('s', '')

            # --- Epoch ---
            # pl_tranmidstr renvoie "2454966.7001&plusmn0.0068" je veux "2454966.7001 ± 0.0068 "
            pl_tranmidstr_val = str(row['pl_tranmidstr']).strip()
            formatted_epoch = pl_tranmidstr_val.replace('&plusmn', ' ± ')

            # --- Orbital Period ---
            # pl_orbperstr renvoie "289.863876&plusmn0.000013" je veux "289.8623{{±|0.0013|0.0013}}"
            # Note: The example output "289.8623{{±|0.0013|0.0013}}" seems to have a different base value (289.8623 vs 289.863876)
            # and error (0.0013 vs 0.000013) than the input.
            # Assuming you want to use the error from the input string for both parts of {{±|error|error}}
            pl_orbperstr_val = str(row['pl_orbperstr']).strip()
            if '&plusmn' in pl_orbperstr_val:
                base_orb_period, error_orb_period = pl_orbperstr_val.split('&plusmn')
                # Using the error from the input for both parts of the template
                formatted_orbital_period = f"{base_orb_period.strip()}{{±|{error_orb_period.strip()}|{error_orb_period.strip()}}}"
            else:
                formatted_orbital_period = pl_orbperstr_val # Handle case with no error

            # --- Inclination ---
            # ici c'est particulier car jai 3 choses "pl_orbincl": 89.764,"pl_orbinclerr1": 0.025,"pl_orbinclerr2": -0.042,
            # et je veux 89.764{{±|0.025|0.042}}
            # Note: pl_orbinclerr2 is negative in the data, but positive in the desired output template.
            # We'll take the absolute value of err2 for the template.
            pl_orbincl_val = row['pl_orbincl']
            pl_orbinclerr1_val = row['pl_orbinclerr1']
            pl_orbinclerr2_val = row['pl_orbinclerr2'] # This is -0.042
            # We need the absolute value for the template, but ensure it's formatted as positive.
            # The template implies positive error values.
            formatted_inclination = f"{pl_orbincl_val}{{±|{abs(pl_orbinclerr1_val)}|{abs(pl_orbinclerr2_val)}}}"

                                
            # Création de l'objet Exoplanet avec les données de base
            exoplanet = Exoplanet(
    name=str(row['pl_name']).strip(),
    host_star=DataPoint(str(row['hostname']).strip(), ref),
    discovery_method=DataPoint(str(row['discoverymethod']).strip(), ref) if pd.notna(row['discoverymethod']) else None,
    discovery_date=DataPoint(str(row['disc_year']).strip(), ref) if pd.notna(row['disc_year']) else None,
    right_ascension=DataPoint(formatted_ra, ref) if pd.notna(row['rastr']) else None,
    declination=DataPoint(formatted_dec, ref) if pd.notna(row['decstr']) else None,
    epoch=DataPoint(formatted_epoch, ref) if pd.notna(row['pl_tranmidstr']) else None,
    orbital_period=DataPoint(formatted_orbital_period, ref) if pd.notna(row['pl_orbperstr']) else None,
    inclination=DataPoint(formatted_inclination, ref) if pd.notna(row['pl_orbincl']) and pd.notna(row['pl_orbinclerr1']) and pd.notna(row['pl_orbinclerr2']) else None
)
            
            # Caractéristiques orbitales
            for field, csv_field, unit in [
                ('semi_major_axis', 'pl_orbsmax', 'ua'),
                ('eccentricity', 'pl_orbeccen', None),  # Pas d'unité pour l'excentricité
                ('orbital_period', 'pl_orbper', 'j'),  # jours
                ('inclination', 'pl_orbincl', '°'),  # degrés
                ('argument_of_periastron', 'pl_orblper', '°'),  # degrés
                ('periastron_time', 'pl_orbtper', 'j')  # jours
            ]:
                value = self._safe_float_conversion(row.get(csv_field))
                if value is not None:
                    setattr(exoplanet, field, DataPoint(value, ref, unit))
            
            # Caractéristiques physiques
            for field, csv_field, unit in [
                ('mass', 'pl_bmassj', 'M_J'),  # masses joviennes
                ('radius', 'pl_radj', 'R_J'),  # rayons joviens
                ('temperature', 'pl_eqt', 'K')  # kelvins
            ]:
                value = self._safe_float_conversion(row.get(csv_field))
                if value is not None:
                    setattr(exoplanet, field, DataPoint(value, ref, unit))
            
            # Informations sur l'étoile
            for field, csv_field, unit in [
                ('spectral_type', 'st_spectype', None),  # Pas d'unité pour le type spectral
                ('star_temperature', 'st_teff', 'K'),  # kelvins
                ('star_radius', 'st_rad', 'R_S'),  # rayons solaires
                ('star_mass', 'st_mass', 'M_S'),  # masses solaires
                ('distance', 'sy_dist', 'pc'),  # parsecs
                ('apparent_magnitude', 'sy_vmag', None)  # Pas d'unité pour la magnitude
            ]:
                value = row.get(csv_field)
                if pd.notna(value):
                    if isinstance(value, (int, float)):
                        value = self._safe_float_conversion(value)
                    setattr(exoplanet, field, DataPoint(value, ref, unit))
            
            # Autres noms
            if pd.notna(row.get('pl_altname')):
                names = str(row['pl_altname']).split(',')
                for name in names:
                    name = name.strip()
                    if name and name != exoplanet.name:
                        exoplanet.other_names.append(name)
            
            return exoplanet
            
        except Exception as e:
            logger.error(f"Erreur lors de la conversion de la ligne en Exoplanet : {str(e)}")
            return None 