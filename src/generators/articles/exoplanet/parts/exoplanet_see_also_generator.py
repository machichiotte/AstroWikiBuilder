from src.models.entities.exoplanet_entity import Exoplanet


class ExoplanetSeeAlsoGenerator:
    """
    Générateur pour la section 'Voir aussi' des articles d'exoplanètes.
    Inclut les sous-sections 'Articles connexes' et 'Liens externes'.
    """

    def generate(self, exoplanet: Exoplanet) -> str:
        """
        Génère le contenu de la section 'Voir aussi'.
        """
        parts = []

        # Section Articles connexes
        related_articles = self._generate_related_articles(exoplanet)
        if related_articles:
            parts.append(related_articles)

        # Section Liens externes
        external_links = self._generate_external_links(exoplanet)
        if external_links:
            parts.append(external_links)

        if not parts:
            return ""

        return "== Voir aussi ==\n" + "\n".join(parts)

    def _generate_related_articles(self, exoplanet: Exoplanet) -> str:
        """
        Génère la sous-section 'Articles connexes'.
        """
        links = []

        # Logique spécifique pour Kepler
        if exoplanet.pl_name and exoplanet.pl_name.startswith("Kepler-"):
            links.append("[[Kepler (télescope spatial)|''Kepler'' (télescope spatial)]]")
            links.append(
                "[[Liste des planètes découvertes grâce au télescope spatial Kepler|"
                "Liste des planètes découvertes grâce au télescope spatial ''Kepler'']]"
            )

        if not links:
            return ""

        content = "=== Articles connexes ===\n"
        for link in links:
            content += f"* {link}\n"
        return content

    def _generate_external_links(self, exoplanet: Exoplanet) -> str:
        """
        Génère la sous-section 'Liens externes'.
        """
        links = []
        if not exoplanet.pl_name:
            return ""

        # 1. L'Encyclopédie des planètes extrasolaires (EPE)
        epe_link = self._generate_epe_link(exoplanet.pl_name)
        if epe_link:
            links.append(epe_link)

        # 2. NASA Exoplanet Archive (NEA)
        nasa_link = self._generate_nasa_link(exoplanet.pl_name)
        if nasa_link:
            links.append(nasa_link)

        # 3. Simbad
        simbad_link = self._generate_simbad_link(exoplanet)
        if simbad_link:
            links.append(simbad_link)

        # 4. Kepler Mission (only if Kepler planet)
        # kepler_link = self._generate_kepler_link(exoplanet.pl_name)
        # if kepler_link:
        #     links.append(kepler_link)

        if not links:
            return ""

        content = "=== Liens externes ===\n"
        for link in links:
            content += f"* {link}\n"
        return content

    def _generate_epe_link(self, pl_name: str) -> str:
        """Génère le lien vers L'Encyclopédie des planètes extrasolaires."""
        # id: lowercase, spaces become underscores
        # Example: Kepler-438 b -> kepler-438_b
        epe_id = pl_name.lower().replace(" ", "_")
        return f"{{{{EPE|id={epe_id}|nom={pl_name}}}}}"

    def _generate_nasa_link(self, pl_name: str) -> str:
        """Génère le lien vers NASA Exoplanet Archive."""
        # id: spaces become +
        # Example: Kepler-438 b -> Kepler-438+b
        nea_id = pl_name.replace(" ", "+")
        return f"{{{{NEA|id={nea_id}|nom={pl_name}}}}}"

    def _generate_simbad_link(self, exoplanet: Exoplanet) -> str:
        """Génère le lien vers Simbad."""
        pl_name = exoplanet.pl_name
        # id: compact name (no spaces), nom: KOI name if exists, else pl_name
        pl_name_compact = pl_name.replace(" ", "")

        # Find KOI name in altnames
        koi_name = None
        if exoplanet.pl_altname:
            for alt in exoplanet.pl_altname:
                if "KOI-" in alt:
                    koi_name = alt
                    break

        simbad_nom = koi_name if koi_name else pl_name
        return f"{{{{Simbad|id={pl_name_compact}|nom={simbad_nom}}}}}"

    def _generate_kepler_link(self, pl_name: str) -> str | None:
        """Génère le lien vers la mission Kepler si applicable."""
        if not pl_name.startswith("Kepler-"):
            return None

        # id: lowercase, no spaces, no hyphens?
        # User example: Kepler-99b -> kepler99b
        kepler_id = pl_name.lower().replace(" ", "").replace("-", "")
        pl_name_compact = pl_name.replace(" ", "")

        return (
            f"{{{{en}}}} [http://kepler.nasa.gov/Mission/discoveries/{kepler_id}/ "
            f"{pl_name_compact}] sur le site de la [[Kepler (télescope spatial)|"
            f"mission ''Kepler'']]"
        )
