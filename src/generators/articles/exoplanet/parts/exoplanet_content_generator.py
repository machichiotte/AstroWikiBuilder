# src/generators/articles/exoplanet/parts/exoplanet_content_generator.py

# ============================================================================
# IMPORTS
# ============================================================================
import math

from src.models.entities.exoplanet_entity import Exoplanet
from src.utils.formatters.article_formatter import ArticleFormatter


# ============================================================================
# DÉCLARATION DE LA CLASSE ExoplanetContentGenerator
# ============================================================================
class ExoplanetContentGenerator:
    """
    Générateur de contenu pour les articles d'exoplanetes.
    Responsable de la génération des différentes sections de l'article.
    """

    # ============================================================================
    # INITIALISATION
    # ============================================================================
    def __init__(self):
        self.article_util = ArticleFormatter()

    # ============================================================================
    # MÉTHODE PRINCIPALE
    # ============================================================================
    def compose_exoplanet_content(self, exoplanet: Exoplanet) -> str:
        """
        Génère l'ensemble du contenu de l'article pour une étoile.
        """
        sections: list[str] = [
            self.build_nomenclature_section(exoplanet),
            self.build_host_star_section(exoplanet),
            self.build_physical_characteristics_section(exoplanet),
            self.build_composition_section(exoplanet),
            self.build_orbit_section(exoplanet),
            self.build_tidal_locking_section(exoplanet),
            self.build_system_architecture_section(exoplanet),
            self.build_insolation_section(exoplanet),
            self.build_observation_potential_section(exoplanet),
            self.build_formation_mechanism_section(exoplanet),
            self.build_discovery_section(exoplanet),
            self.build_habitability_section(exoplanet),
        ]

        # Filtrer les sections vides et les combiner
        return "\n\n".join(filter(None, sections))

    # ============================================================================
    # GÉNÉRATION DES SECTIONS DE CONTENU
    # ============================================================================

    # --- CARACTÉRISTIQUES PHYSIQUES ---
    def build_orbit_section(self, exoplanet: Exoplanet) -> str:
        """Génère la section sur l'orbite de l'exoplanète."""
        if not any(
            [
                exoplanet.pl_semi_major_axis,
                exoplanet.pl_eccentricity,
                exoplanet.pl_orbital_period,
                exoplanet.pl_inclination,
            ]
        ):
            return ""

        content: list[str] = ["== Orbite ==\n"]

        if exoplanet.pl_semi_major_axis:
            semi_major_axis_str = self.article_util.format_uncertain_value_for_article(
                exoplanet.pl_semi_major_axis
            )
            if semi_major_axis_str:
                content.append(
                    f"L'exoplanète orbite à une distance de {semi_major_axis_str} [[unité astronomique|UA]] de son étoile."
                )

        if exoplanet.pl_eccentricity:
            eccentricity_str: str = self.article_util.format_uncertain_value_for_article(
                exoplanet.pl_eccentricity
            )
            if eccentricity_str:
                content.append(f"L'orbite a une excentricité de {eccentricity_str}.")

        if exoplanet.pl_orbital_period:
            period_str: str = self.article_util.format_uncertain_value_for_article(
                exoplanet.pl_orbital_period
            )
            if period_str:
                content.append(f"La période orbitale est de {period_str} [[jour|jours]].")

        if exoplanet.pl_inclination:
            inclination_str: str = self.article_util.format_uncertain_value_for_article(
                exoplanet.pl_inclination
            )
            if inclination_str:
                content.append(
                    f"L'inclinaison de l'orbite est de {inclination_str} [[degré (angle)|degrés]]."
                )

        return "\n".join(content)

    def build_discovery_section(self, exoplanet: Exoplanet) -> str:
        """Génère la section de découverte."""
        if not exoplanet.disc_year:
            return ""

        section = "== Découverte ==\n"

        # Traduction des méthodes de découverte
        method_translations: dict[str, str] = {
            "Transit": "des transits",
            "Radial Velocity": "des vitesses radiales",
            "Imaging": "de l'imagerie directe",
            "Microlensing": "de la microlentille gravitationnelle",
            "Timing": "du chronométrage",
            "Astrometry": "de l'astrométrie",
            "Orbital Brightness Modulation": "de la modulation de luminosité orbitale",
            "Eclipse Timing Variations": "des variations temporelles d'éclipses",
            "Pulsar Timing": "du chronométrage de pulsar",
            "Pulsation Timing Variations": "des variations temporelles de pulsation",
            "Disk Kinematics": "de la cinématique du disque",
            "Transit Timing Variations": "des variations temporelles de transit",
        }

        method_raw = (
            exoplanet.disc_method.value
            if exoplanet.disc_method and hasattr(exoplanet.disc_method, "value")
            else ""
        )
        disc_method: str | None = method_translations.get(method_raw, None)

        # Gestion robuste de la date
        date_value = exoplanet.disc_year
        if hasattr(date_value, "value"):
            date_value = date_value.value

        if hasattr(date_value, "year"):
            date_str: str = f"en {self.article_util.format_year_without_decimals(date_value.year)}"
        else:
            date_str: str = f"en {str(self.article_util.format_year_without_decimals(date_value))}"

        if disc_method:
            section += f"L'exoplanète a été découverte par la méthode {disc_method} {date_str}.\n"
        else:
            section += f"L'exoplanète a été découverte {date_str}.\n"

        return section

    def _get_value_or_none_if_nan(self, data_point) -> float | int | None:
        """Extrait la valeur d'un data point ou retourne None si NaN."""
        if data_point and hasattr(data_point, "value") and data_point.value is not None:
            value = data_point.value
            if isinstance(value, str) and value.lower() == "nan":
                return None
            return value
        return None

    def _format_mass_description(self, mass: float | int) -> str | None:
        """Formate la description de la masse."""
        try:
            mass_f = float(mass)
        except Exception:
            return None

        precision = 3 if mass_f < 0.1 else (2 if mass_f < 1 else 1)
        mass_value = self.article_util.format_number_as_french_string(mass, precision=precision)

        if mass_f < 0.1:
            label = "faible"
        elif mass_f < 1:
            label = "modérée"
        else:
            label = "imposante"

        return f"sa masse {label} de {mass_value} [[Masse_jovienne|''M''{{{{ind|J}}}}]]"

    def _format_radius_description(self, radius: float | int) -> str | None:
        """Formate la description du rayon."""
        try:
            radius_f = float(radius)
        except Exception:
            return None

        precision = 3 if radius_f < 0.1 else (2 if radius_f < 1 else 1)
        radius_value = self.article_util.format_number_as_french_string(radius, precision=precision)

        if radius_f < 0.5:
            label = "compact"
        elif radius_f < 1.5:
            label = None
        else:
            label = "étendu"

        return f"son rayon{' ' + label if label else ''} de {radius_value} [[Rayon_jovien|''R''{{{{ind|J}}}}]]"

    def _format_temperature_description(self, temp: float | int) -> str | None:
        """Formate la description de la température."""
        if isinstance(temp, str) and temp.lower() == "nan":
            return None
        if isinstance(temp, float) and math.isnan(temp):
            return None

        try:
            temp_f = float(temp)
        except Exception:
            return None

        if isinstance(temp, (int, float)):
            temp_value = f"{float(temp):.5f}".rstrip("0").rstrip(".")
        else:
            temp_value = str(temp)

        if temp_f < 500:
            label = ""
        elif temp_f < 1000:
            label = "élevée "
        else:
            label = "extrême "

        return f"sa température {label}de {temp_value} [[Kelvin|K]]"

    def build_physical_characteristics_section(self, exoplanet: Exoplanet) -> str:
        """Génère la section des caractéristiques physiques."""
        mass = self._get_value_or_none_if_nan(exoplanet.pl_mass)
        radius = self._get_value_or_none_if_nan(exoplanet.pl_radius)
        temp = self._get_value_or_none_if_nan(exoplanet.pl_temperature)

        if not any([mass is not None, radius is not None, temp is not None]):
            return ""

        section = "== Caractéristiques physiques ==\n"
        desc_parts = []

        if mass is not None:
            mass_desc = self._format_mass_description(mass)
            if mass_desc:
                desc_parts.append(mass_desc)

        if radius is not None:
            radius_desc = self._format_radius_description(radius)
            if radius_desc:
                desc_parts.append(radius_desc)

        if temp is not None:
            temp_desc = self._format_temperature_description(temp)
            if temp_desc:
                desc_parts.append(temp_desc)

        if desc_parts:
            if len(desc_parts) == 1:
                section += f"L'exoplanète se distingue par {desc_parts[0]}.\n"
            else:
                section += f"L'exoplanète se distingue par {', '.join(desc_parts[:-1])} et {desc_parts[-1]}.\n"

        return section

    def build_habitability_section(self, exoplanet: Exoplanet) -> str:
        """
        Génère la section sur l'habitabilité de l'exoplanète en se basant sur la température d'équilibre.
        """
        section = "== Habitabilité ==\n"

        temp = self._get_value_or_none_if_nan(exoplanet.pl_temperature)

        if temp is None:
            section += "Les conditions d'habitabilité de cette exoplanète ne sont pas déterminées ou ne sont pas connues.\n"
            return section

        try:
            temp_val = float(temp)
        except (ValueError, TypeError):
            section += "Les conditions d'habitabilité de cette exoplanète ne sont pas déterminées ou ne sont pas connues.\n"
            return section

        # Estimation basique basée sur la température d'équilibre
        # Zone habitable approximative (très simplifiée) : 180K - 395K
        # Note: C'est une estimation purement thermique sans tenir compte de l'atmosphère

        temp_str = self.article_util.format_uncertain_value_for_article(exoplanet.pl_temperature)

        if temp_val > 395:
            section += (
                f"Avec une température d'équilibre estimée à {temp_str} [[Kelvin|K]], "
                "cette exoplanète est considérée comme trop chaude pour abriter de l'eau liquide en surface.\n"
            )
        elif temp_val < 180:
            section += (
                f"Avec une température d'équilibre estimée à {temp_str} [[Kelvin|K]], "
                "cette exoplanète est considérée comme trop froide pour abriter de l'eau liquide en surface.\n"
            )
        else:
            section += (
                f"Avec une température d'équilibre estimée à {temp_str} [[Kelvin|K]], "
                "cette exoplanète se situe théoriquement dans la zone habitable de son étoile, "
                "permettant potentiellement la présence d'eau liquide en surface sous réserve d'une atmosphère adéquate.\n"
            )

        return section

    def build_nomenclature_section(self, exoplanet: Exoplanet) -> str:
        """
        Génère un paragraphe standard expliquant la convention de nommage.
        """
        if not exoplanet.pl_name:
            return ""

        content = "== Nomenclature ==\n"
        content += (
            "La convention de l'[[Union astronomique internationale]] (UAI) pour la désignation des exoplanètes "
            "consiste à ajouter une lettre minuscule à la suite du nom de l'étoile hôte, en commençant par la lettre « b » "
            "pour la première planète découverte dans le système (la lettre « a » désignant l'étoile elle-même). "
            "Les planètes suivantes reçoivent les lettres « c », « d », etc., dans l'ordre de leur découverte.\n"
        )

        return content

    def build_host_star_section(self, exoplanet: Exoplanet) -> str:
        """
        Génère la section résumant les caractéristiques de l'étoile hôte.
        """
        if not exoplanet.st_name:
            return ""

        content = "== Étoile hôte ==\n"

        # Introduction avec le nom de l'étoile
        content += f"L'exoplanète orbite autour de [[{exoplanet.st_name}]], "

        characteristics = []

        # Type spectral
        if exoplanet.st_spectral_type:
            characteristics.append(f"une étoile de type spectral {exoplanet.st_spectral_type}")

        # Masse
        if exoplanet.st_mass and exoplanet.st_mass.value:
            mass_str = self.article_util.format_uncertain_value_for_article(exoplanet.st_mass)
            if mass_str:
                characteristics.append(
                    f"d'une masse de {mass_str} [[Masse solaire|''M''{{{{ind|☉}}}}]]"
                )

        # Métallicité
        if exoplanet.st_metallicity and exoplanet.st_metallicity.value:
            met_str = self.article_util.format_uncertain_value_for_article(exoplanet.st_metallicity)
            if met_str:
                characteristics.append(f"d'une métallicité de {met_str} [Fe/H]")

        # Âge
        if exoplanet.st_age and exoplanet.st_age.value:
            age_str = self.article_util.format_uncertain_value_for_article(exoplanet.st_age)
            if age_str:
                characteristics.append(f"âgée de {age_str} [[milliard]]s d'années")

        if not characteristics:
            # Si on a juste le nom mais aucune info, on fait une phrase simple
            content = f"== Étoile hôte ==\nL'exoplanète orbite autour de l'étoile [[{exoplanet.st_name}]].\n"
            return content

        # Assemblage de la phrase
        if len(characteristics) == 1:
            content += f"{characteristics[0]}.\n"
        else:
            content += f"{', '.join(characteristics[:-1])} et {characteristics[-1]}.\n"

        return content

    def build_insolation_section(self, exoplanet: Exoplanet) -> str:
        """Génère la section sur le flux d'insolation reçu par rapport à la Terre. Seuils basés sur Mars:0.43, Terre:1.0, Venus:1.9."""
        if not exoplanet.pl_insolation_flux or not exoplanet.pl_insolation_flux.value:
            return ""
        try:
            flux_value = float(exoplanet.pl_insolation_flux.value)
        except (ValueError, TypeError):
            return ""
        section = "== Flux d'insolation ==\n"
        flux_str = self.article_util.format_uncertain_value_for_article(
            exoplanet.pl_insolation_flux
        )
        if flux_value < 0.1:
            section += f"La planète reçoit environ {flux_str} fois le flux lumineux que la [[Terre]] reçoit du [[Soleil]], ce qui la place dans une zone très froide et sombre, similaire aux planètes externes du système solaire comme [[Jupiter (planète)|Jupiter]] ou [[Saturne (planète)|Saturne]].\n"
        elif flux_value < 0.4:
            section += f"La planète reçoit {flux_str} fois le flux lumineux que la Terre reçoit du Soleil, soit un niveau d'insolation inférieur à celui de [[Mars (planète)|Mars]]. Elle se trouve dans la zone externe du système planétaire.\n"
        elif flux_value < 0.8:
            section += f"La planète reçoit {flux_str} fois le flux lumineux que la Terre reçoit du Soleil, la plaçant dans la limite externe de la [[zone habitable]], où l'eau liquide pourrait théoriquement exister avec une atmosphère à effet de serre appropriée.\n"
        elif flux_value < 1.3:
            section += f"La planète reçoit {flux_str} fois le flux lumineux que la Terre reçoit du Soleil, soit un niveau d'insolation relativement comparable. Ces conditions sont favorables au maintien d'eau liquide en surface.\n"
        elif flux_value < 1.9:
            section += f"La planète reçoit {flux_str} fois le flux lumineux que la Terre reçoit du Soleil, la plaçant dans la limite interne de la zone habitable, proche des conditions de [[Vénus (planète)|Vénus]]. Le risque d'un effet de serre incontrôlé est élevé.\n"
        elif flux_value < 4:
            section += f"La planète reçoit {flux_str} fois le flux lumineux que la Terre reçoit du Soleil. Ce flux élevé indique une proximité importante avec son étoile hôte, susceptible d'entraîner une température de surface très élevée et l'évaporation de toute eau liquide.\n"
        else:
            section += f"La planète reçoit {flux_str} fois le flux lumineux que la Terre reçoit du Soleil. Ce flux extrêmement élevé, supérieur à celui de [[Mercure (planète)|Mercure]], indique une très grande proximité avec son étoile hôte. De telles conditions entraînent des températures de surface extrêmes et peuvent provoquer l'évaporation massive de l'atmosphère.\n"
        return section

    def build_composition_section(self, exoplanet: Exoplanet) -> str:
        """Génère la section sur la composition théorique basée sur la densité."""
        if not exoplanet.pl_density or not exoplanet.pl_density.value:
            return ""
        try:
            density_value = float(exoplanet.pl_density.value)
        except (ValueError, TypeError):
            return ""
        section = "== Composition ==\n"
        density_str = self.article_util.format_uncertain_value_for_article(exoplanet.pl_density)
        if density_value > 5.0:
            section += f"Avec une densité de {density_str} g/cm³, cette exoplanète présente une composition probablement [[Planète tellurique|tellurique]].\n"
        elif density_value > 3.0:
            section += f"Avec une densité de {density_str} g/cm³, cette exoplanète pourrait avoir une composition [[Planète tellurique|tellurique]].\n"
        elif density_value > 2.0:
            section += f"Avec une densité de {density_str} g/cm³, cette exoplanète pourrait être une [[mini-Neptune]].\n"
        else:
            section += f"Avec une faible densité de {density_str} g/cm³, cette exoplanète est probablement une [[géante gazeuse]].\n"
        return section

    def build_tidal_locking_section(self, exoplanet: Exoplanet) -> str:
        """Génère la section sur le verrouillage gravitationnel potentiel."""
        if not exoplanet.pl_orbital_period or not exoplanet.pl_orbital_period.value:
            return ""
        try:
            period_value = float(exoplanet.pl_orbital_period.value)
        except (ValueError, TypeError):
            return ""
        eccentricity_value = 0.0
        if exoplanet.pl_eccentricity and exoplanet.pl_eccentricity.value:
            try:
                eccentricity_value = float(exoplanet.pl_eccentricity.value)
            except (ValueError, TypeError):
                pass
        is_likely_locked = period_value < 15 and eccentricity_value < 0.1
        if not is_likely_locked:
            return ""
        section = "== Rotation et verrouillage gravitationnel ==\n"
        section += "En raison de sa proximité avec son étoile hôte, il est très probable que cette exoplanète subisse un [[verrouillage gravitationnel|verrouillage par effet de marée]].\n"
        return section

    def build_observation_potential_section(self, exoplanet: Exoplanet) -> str:
        """Génère la section sur le potentiel d'observation pour la spectroscopie."""
        if not exoplanet.st_apparent_magnitude:
            return ""
        try:
            if hasattr(exoplanet.st_apparent_magnitude, "value"):
                mag_value = float(exoplanet.st_apparent_magnitude.value)
            else:
                mag_value = float(exoplanet.st_apparent_magnitude)
        except (ValueError, TypeError, AttributeError):
            return ""
        if mag_value > 12:
            return ""
        section = "== Potentiel d'observation ==\n"
        is_transiting = exoplanet.disc_method and "Transit" in str(exoplanet.disc_method)
        has_transit_depth = exoplanet.pl_transit_depth and exoplanet.pl_transit_depth.value
        if is_transiting and has_transit_depth and mag_value < 10:
            section += f"Grâce à la brillance de son étoile hôte (magnitude apparente de {mag_value:.1f}) et à sa méthode de détection par transit, cette exoplanète constitue une cible prometteuse pour la caractérisation atmosphérique par [[spectroscopie de transmission]]. De telles observations peuvent révéler la composition chimique de son atmosphère, notamment avec des instruments comme ceux du [[Télescope spatial James-Webb|JWST]].\n"
        elif mag_value < 10:
            section += f"Son étoile hôte possède une magnitude apparente de {mag_value:.1f}, ce qui en fait une cible relativement brillante accessible aux télescopes modernes pour des observations photométriques ou spectroscopiques.\n"
        elif mag_value < 12:
            section += f"Avec une magnitude apparente de {mag_value:.1f}, l'étoile hôte est observable avec des télescopes de taille moyenne, permettant des études de suivi.\n"
        return section

    def build_system_architecture_section(self, exoplanet: Exoplanet) -> str:
        """Génère la section sur l'architecture du système planétaire."""
        if not exoplanet.sy_planet_count:
            return ""
        try:
            if hasattr(exoplanet.sy_planet_count, "value"):
                planet_count = int(exoplanet.sy_planet_count.value)
            else:
                planet_count = int(exoplanet.sy_planet_count)
        except (ValueError, TypeError, AttributeError):
            return ""
        if planet_count <= 1:
            return ""
        section = "== Architecture du système ==\n"
        if planet_count == 2:
            section += f"Cette planète fait partie d'un système binaire planétaire orbitant autour de [[{exoplanet.st_name}]]. L'existence de multiples planètes dans un même système permet d'étudier la formation et l'évolution planétaire de manière comparative.\n"
        elif planet_count >= 3 and planet_count <= 5:
            section += f"Cette planète fait partie d'un système de {planet_count} planètes connues orbitant autour de [[{exoplanet.st_name}]]. L'étude de systèmes multi-planétaires fournit des informations précieuses sur les mécanismes de formation et de migration planétaire.\n"
        else:
            section += f"Cette planète fait partie d'un système planétaire remarquable contenant {planet_count} planètes connues autour de [[{exoplanet.st_name}]]. Un tel système dense offre une opportunité unique d'étudier les interactions gravitationnelles entre planètes et la stabilité dynamique à long terme.\n"
        return section

    def _is_hot_jupiter(self, exoplanet: Exoplanet) -> bool:
        """Détermine si c'est un Hot Jupiter."""
        is_massive = False
        if exoplanet.pl_mass and exoplanet.pl_mass.value:
            try:
                mass_earth = float(exoplanet.pl_mass.value) * 318
                is_massive = mass_earth > 30
            except (ValueError, TypeError):
                pass
        is_large = False
        if exoplanet.pl_radius and exoplanet.pl_radius.value:
            try:
                is_large = float(exoplanet.pl_radius.value) > 0.8
            except (ValueError, TypeError):
                pass
        is_close = False
        if exoplanet.pl_orbital_period and exoplanet.pl_orbital_period.value:
            try:
                is_close = float(exoplanet.pl_orbital_period.value) < 10
            except (ValueError, TypeError):
                pass
        return (is_massive or is_large) and is_close

    def _is_red_dwarf_system(self, exoplanet: Exoplanet) -> bool:
        """Détermine si l'étoile est une naine rouge."""
        if exoplanet.st_spectral_type and exoplanet.st_spectral_type.startswith("M"):
            return True
        if exoplanet.st_mass and hasattr(exoplanet.st_mass, "value"):
            try:
                return float(exoplanet.st_mass.value) < 0.5
            except (ValueError, TypeError):
                pass
        return False

    def _is_super_earth_or_mini_neptune(self, exoplanet: Exoplanet) -> bool:
        """Détermine si c'est une super-Terre ou mini-Neptune."""
        if not exoplanet.pl_radius or not exoplanet.pl_radius.value:
            return False
        try:
            radius_earth = float(exoplanet.pl_radius.value)
            return 1.5 < radius_earth < 4.0
        except (ValueError, TypeError):
            return False

    def _has_eccentric_orbit(self, exoplanet: Exoplanet) -> bool:
        """Détermine si l'orbite est fortement excentrique."""
        if not exoplanet.pl_eccentricity or not exoplanet.pl_eccentricity.value:
            return False
        try:
            return float(exoplanet.pl_eccentricity.value) > 0.3
        except (ValueError, TypeError):
            return False

    def build_formation_mechanism_section(self, exoplanet: Exoplanet) -> str:
        """Génère une section sur les mécanismes de formation (spéculatif)."""
        is_hot_jupiter = self._is_hot_jupiter(exoplanet)
        is_red_dwarf = self._is_red_dwarf_system(exoplanet)
        is_super_earth = self._is_super_earth_or_mini_neptune(exoplanet)
        is_eccentric = self._has_eccentric_orbit(exoplanet)
        if not any([is_hot_jupiter, is_red_dwarf, is_super_earth, is_eccentric]):
            return ""
        section = "== Mécanismes de formation ==\n"
        if is_hot_jupiter:
            section += "Les modèles de formation planétaire suggèrent que cette exoplanète, de par sa nature gazeuse et sa proximité extrême avec son étoile, ne s'est probablement pas formée à sa position actuelle. Les théories de [[migration planétaire]] proposent qu'elle se soit formée dans les régions externes du système, où les températures permettent l'accumulation de gaz, avant de migrer vers l'intérieur par interaction gravitationnelle avec le [[Disque protoplanétaire|disque protoplanétaire]].\n"
        elif is_red_dwarf:
            section += f"L'évolution de cette planète autour de [[{exoplanet.st_name}]], une [[naine rouge]], présente des défis particuliers. L'[[activité stellaire]] intense des naines rouges, notamment les [[éruption stellaire|éruptions]] fréquentes, peut éroder l'atmosphère planétaire primitive. De plus, la [[zone habitable]] très proche de ces étoiles implique un fort [[verrouillage gravitationnel]], avec des conséquences importantes sur la circulation atmosphérique et le climat.\n"
        elif is_eccentric:
            section += "L'excentricité orbitale élevée de cette planète suggère qu'elle a subi des perturbations gravitationnelles importantes. De telles orbites excentriques peuvent résulter d'interactions dynamiques avec d'autres planètes du système, d'une migration induite par le disque, ou de rencontres stellaires dans l'environnement de formation.\n"
        elif is_super_earth:
            section += "La nature exacte de cette planète, située dans la catégorie des [[super-Terre]]s ou [[mini-Neptune]]s, reste débattue. Cette classe d'exoplanètes, rare dans notre Système solaire, soulève des questions sur les processus de formation. Il pourrait s'agir soit d'un noyau rocheux massif avec une atmosphère épaisse, soit d'une planète majoritairement composée de volatils.\n"
        return section
