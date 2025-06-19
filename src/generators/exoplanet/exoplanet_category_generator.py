# src/generators/exoplanet/exoplanet_category_generator.py
from typing import List, Optional, Callable
from src.models.entities.exoplanet import Exoplanet
from src.utils.astro.classification.exoplanet_type_utils import ExoplanetTypeUtils
from src.generators.base_category_generator import BaseCategoryGenerator


class ExoplanetCategoryGenerator(BaseCategoryGenerator):
    """
    Classe pour générer les catégories des articles d'exoplanètes.
    Utilise un générateur de règles centralisé.
    """

    DISCOVERY_FACILITY_CATEGORY_MAPPING: dict[str, str] = {
        "Kepler": "[[Catégorie:Exoplanète découverte grâce à Kepler]]",
        "Transiting Exoplanet Survey Satellite (TESS)": "[[Catégorie:Exoplanète découverte grâce au Transiting Exoplanet Survey Satellite]]",
        "TESS": "[[Catégorie:Exoplanète découverte grâce au Transiting Exoplanet Survey Satellite]]",
        "CoRoT": "[[Catégorie:Exoplanète découverte grâce au télescope spatial CoRoT]]",
        "Very Large Telescope": "[[Catégorie:Exoplanète découverte grâce au Very Large Telescope (VLT)]]",
        "Paranal Observatory": "[[Catégorie:Exoplanète découverte grâce au Very Large Telescope (VLT)]]",
        "VLT": "[[Catégorie:Exoplanète découverte grâce au Very Large Telescope (VLT)]]",
        "Hubble Space Telescope": "[[Catégorie:Exoplanète découverte grâce au télescope spatial Hubble]]",
        "HST": "[[Catégorie:Exoplanète découverte grâce au télescope spatial Hubble]]",
        "HARPS": "[[Catégorie:Exoplanète découverte grâce à HARPS]]",
        "La Silla Observatory": "[[Catégorie:Exoplanète découverte grâce à HARPS]]",
        "James Webb Space Telescope (JWST)": "[[Catégorie:Exoplanète découverte grâce au télescope spatial James Webb]]",
        "James Webb Space Telescope": "[[Catégorie:Exoplanète découverte grâce au télescope spatial James Webb]]",
        "JWST": "[[Catégorie:Exoplanète découverte grâce au télescope spatial James Webb]]",
        "Spitzer Space Telescope": "[[Catégorie:Exoplanète découverte grâce au télescope spatial Spitzer]]",
        "Spitzer": "[[Catégorie:Exoplanète découverte grâce au télescope spatial Spitzer]]",
        "Gaia": "[[Catégorie:Exoplanète découverte grâce au télescope spatial Gaia]]",
        "European Space Agency (ESA) Gaia Satellite": "[[Catégorie:Exoplanète découverte grâce au télescope spatial Gaia]]",
        "W. M. Keck Observatory": "[[Catégorie:Exoplanète découverte grâce au W. M. Keck Observatory]]",
        "Keck": "[[Catégorie:Exoplanète découverte grâce au W. M. Keck Observatory]]",
        "Gemini Observatory": "[[Catégorie:Exoplanète découverte grâce au Gemini Observatory]]",
        "CHEOPS": "[[Catégorie:Exoplanète découverte grâce au télescope spatial CHEOPS]]",
        "CHaracterising ExOPlanets Satellite (CHEOPS)": "[[Catégorie:Exoplanète découverte grâce au télescope spatial CHEOPS]]",
        # Les autres facilités n'ont pas de catégorie dédiée sur Wikipédia FR à ce jour,
        # mais sont conservées pour une éventuelle création future de catégorie :
        "OGLE": "",
        "HATNet": "",
        "Haute-Provence Observatory": "",
        "Okayama Astrophysical Observatory": "",
        "K2": "",
        "Bohyunsan Optical Astronomical Observatory": "",
        "Multiple Observatories": "",
        "Multiple Facilities": "",
        "Calar Alto Observatory": "",
        "Qatar": "",
        "SuperWASP-South": "",
        "SuperWASP": "",
        "Thueringer Landessternwarte Tautenburg": "",
        "Lick Observatory": "",
        "KMTNet": "",
        "Leoncito Astronomical Complex": "",
        "HATSouth": "",
        "Roque de los Muchachos Observatory": "",
        "MOA": "",
        "McDonald Observatory": "",
        "Anglo-Australian Telescope": "",
        "University of Canterbury Mt John Observatory": "",
        "United Kingdom Infrared Telescope": "",
        "European Southern Observatory": "",
        "Next-Generation Transit Survey (NGTS)": "",
        "Las Campanas Observatory": "",
        "NASA Infrared Telescope Facility (IRTF)": "",
        "KELT-North": "",
        "SPECULOOS Southern Observatory": "",
        "Lowell Observatory": "",
        "Fred Lawrence Whipple Observatory": "",
        "MEarth Project": "",
        "Large Binocular Telescope Observatory": "",
        "KELT-South": "",
        "XO": "",
        "WASP-South": "",
        "KELT": "",
        "Cerro Tololo Inter-American Observatory": "",
        "SuperWASP-North": "",
        "Subaru Telescope": "",
        "Mauna Kea Observatory": "",
        "South African Radio Astronomy Observatory (SARAO)": "",
        "TrES": "",
        "Winer Observatory": "",
        "Very Long Baseline Array": "",
        "Arecibo Observatory": "",
        "Apache Point Observatory": "",
        "KOINet": "",
        "Yunnan Astronomical Observatory": "",
        "Atacama Large Millimeter Array (ALMA)": "",
        "Palomar Observatory": "",
        "Acton Sky Portal Observatory": "",
        "Haleakala Observatory": "",
        "Zwicky Transient Facility": "",
        "Xinglong Station": "",
        "Kitt Peak National Observatory": "",
        "Parkes Observatory": "",
        "Infrared Survey Facility": "",
        "Teide Observatory": "",
        "Wide-field Infrared Survey Explorer (WISE) Satellite Mission": "",
    }

    def __init__(self, rules_filepath: str = "src/constants/categories_rules.yaml"):
        super().__init__(rules_filepath)
        self.planet_type_utils = ExoplanetTypeUtils()

    def get_object_type(self) -> str:
        return "exoplanet"

    def list_category_rules(self) -> List[Callable]:
        return [
            self._get_planet_type_category,
            self._get_constellation_category,
        ]

    def _get_planet_type_category(self, exoplanet: Exoplanet) -> Optional[str]:
        """
        Règle personnalisée pour déterminer la catégorie de type de planète.
        """
        try:
            planet_type: str = (
                self.planet_type_utils.determine_exoplanet_classification(exoplanet)
            )
            if planet_type:
                mapping = (
                    self.generator.rules.get("exoplanet", {})
                    .get("mapped", {})
                    .get("planet_type", {})
                )
                if planet_type in mapping:
                    return mapping[planet_type]
        except Exception:
            pass
        return None

    def _get_constellation_category(self, exoplanet: Exoplanet) -> Optional[str]:
        """
        Règle personnalisée pour déterminer la catégorie de constellation.
        """
        if exoplanet.st_constellation:
            constellation: str = exoplanet.st_constellation
            mapping = (
                self.generator.rules.get("exoplanet", {})
                .get("mapped", {})
                .get("constellation", {})
            )
            if constellation in mapping:
                return mapping[constellation]
        return None

    def _get_discovered_by_category(self, exoplanet: Exoplanet) -> Optional[str]:
        """
        Règle personnalisée pour déterminer la catégorie 'découverte grâce à'
        en utilisant le champ 'discovery_program' de l'exoplanète et le mapping.
        """
        discovered_by_program: str | None = (
            exoplanet.disc_program.value if exoplanet.disc_program else None
        )
        if discovered_by_program:
            # Check for exact matches first
            if discovered_by_program in self.DISCOVERY_FACILITY_CATEGORY_MAPPING:
                return self.DISCOVERY_FACILITY_CATEGORY_MAPPING[discovered_by_program]
            # If no exact match, check for partial matches (case-insensitive for robustness)
            for key, cat in self.DISCOVERY_FACILITY_CATEGORY_MAPPING.items():
                if key.lower() in discovered_by_program.lower():
                    return cat
        return None  # Returns None if no match is found, or if disc_program is None.

    def generate_categories(self, exoplanet: Exoplanet) -> List[str]:
        """
        Génère les catégories pour une exoplanète en déléguant au générateur de règles
        et en ajoutant des règles personnalisées.
        """
        custom_rules = [
            self._get_planet_type_category,
            self._get_discovered_by_category,
            self._get_constellation_category,
        ]

        # The CategoryGenerator.generate method should be responsible for filtering out
        # empty strings or None values returned by custom rules.
        return self.generator.generate(
            exoplanet, "exoplanet", custom_rules=custom_rules
        )
