# src/generators/articles/exoplanet/sections/see_also_section.py

from src.models.entities.exoplanet_entity import Exoplanet


class SeeAlsoSection:
    """Génère la section 'Voir aussi' pour les articles d'exoplanètes."""

    def generate(self, exoplanet: Exoplanet) -> str:
        """Génère le contenu de la section 'Voir aussi'."""
        parts = []

        related_articles = self._generate_related_articles(exoplanet)
        if related_articles:
            parts.append(related_articles)

        external_links = self._generate_external_links(exoplanet)
        if external_links:
            parts.append(external_links)

        if not parts:
            return ""

        return "== Voir aussi ==\n" + "\n".join(parts)

    def _generate_related_articles(self, exoplanet: Exoplanet) -> str:
        """Génère la sous-section 'Articles connexes'."""
        links = []

        if exoplanet.pl_name and exoplanet.pl_name.startswith("Kepler-"):
            links.append(
                "[[Kepler (télescope spatial)|''Kepler'' (télescope spatial)]]"
            )
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
        """Génère la sous-section 'Liens externes'."""
        links = []
        if not exoplanet.pl_name:
            return ""

        epe_link = self._generate_epe_link(exoplanet.pl_name)
        if epe_link:
            links.append(epe_link)

        nasa_link = self._generate_nasa_link(exoplanet.pl_name)
        if nasa_link:
            links.append(nasa_link)

        simbad_link = self._generate_simbad_link(exoplanet)
        if simbad_link:
            links.append(simbad_link)

        if not links:
            return ""

        content = "=== Liens externes ===\n"
        for link in links:
            content += f"* {link}\n"
        return content

    def _generate_epe_link(self, pl_name: str) -> str:
        """Génère le lien vers L'Encyclopédie des planètes extrasolaires."""
        epe_id = pl_name.lower().replace(" ", "_")
        return f"{{{{EPE|id={epe_id}|nom={pl_name}}}}}"

    def _generate_nasa_link(self, pl_name: str) -> str:
        """Génère le lien vers NASA Exoplanet Archive."""
        nea_id = pl_name.replace(" ", "+")
        return f"{{{{NEA|id={nea_id}|nom={pl_name}}}}}"

    def _generate_simbad_link(self, exoplanet: Exoplanet) -> str:
        """Génère le lien vers Simbad."""
        pl_name = exoplanet.pl_name
        pl_name_compact = pl_name.replace(" ", "")

        koi_name = None
        if exoplanet.pl_altname:
            for alt in exoplanet.pl_altname:
                if "KOI-" in alt:
                    koi_name = alt
                    break

        simbad_nom = koi_name if koi_name else pl_name
        return f"{{{{Simbad|id={pl_name_compact}|nom={simbad_nom}}}}}"
