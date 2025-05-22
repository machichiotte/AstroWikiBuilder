import unittest
from src.utils.wikipedia_generator import WikipediaGenerator # The class to test
from typing import Optional, List, Dict # For type hints in mocks

# --- Mock Data Structures ---
# Simplified SourceType Enum for testing
class MockSourceType:
    NASA = "NasaGov"
    EPE = "EPE"
    OEC = "OEC"
    ARTICLE = "Article"
    OUVRAGE = "Ouvrage"
    CUSTOM = "CustomRef" # For generic references

class MockReference:
    def __init__(self, source_type_val: str, content_template: str, name_override: Optional[str] = None):
        # source_type_val is the string value like "NasaGov", "EPE"
        self.source = type('EnumMock', (), {'value': source_type_val})() # Mocking an object with a .value attribute
        self.content_template = content_template # This is the {{Lien web...}} or {{Article...}} part
        self._name_override = name_override

    def to_wiki_ref(self) -> str:
        # This method is crucial. It should return the *full initial reference string*
        # that _add_reference expects for its ref_content argument.
        # e.g., <ref name="NasaGov">{{Lien web...}}</ref>
        ref_name = self._name_override if self._name_override else self.source.value
        return f'<ref name="{ref_name}">{self.content_template}</ref>'

class MockDataPoint:
    def __init__(self, value: any, unit: Optional[str] = None, reference: Optional[MockReference] = None):
        self.value = value
        self.unit = unit
        self.reference = reference

class MockExoplanet:
    def __init__(self, name: str):
        self.name = name
        # Initialize all expected attributes to None or default
        self.host_star: Optional[MockDataPoint] = None
        self.star_epoch: Optional[MockDataPoint] = None
        self.right_ascension: Optional[MockDataPoint] = None
        self.declination: Optional[MockDataPoint] = None
        self.distance: Optional[MockDataPoint] = None
        self.constellation: Optional[MockDataPoint] = None
        self.spectral_type: Optional[MockDataPoint] = None
        self.apparent_magnitude: Optional[MockDataPoint] = None
        self.semi_major_axis: Optional[MockDataPoint] = None
        self.periastron: Optional[MockDataPoint] = None
        self.apoastron: Optional[MockDataPoint] = None
        self.eccentricity: Optional[MockDataPoint] = None
        self.orbital_period: Optional[MockDataPoint] = None
        self.angular_distance: Optional[MockDataPoint] = None
        self.periastron_time: Optional[MockDataPoint] = None
        self.inclination: Optional[MockDataPoint] = None
        self.argument_of_periastron: Optional[MockDataPoint] = None
        self.epoch: Optional[MockDataPoint] = None
        self.mass: Optional[MockDataPoint] = None
        self.minimum_mass: Optional[MockDataPoint] = None
        self.radius: Optional[MockDataPoint] = None
        self.density: Optional[MockDataPoint] = None
        self.gravity: Optional[MockDataPoint] = None
        self.rotation_period: Optional[MockDataPoint] = None
        self.temperature: Optional[MockDataPoint] = None
        self.bond_albedo: Optional[MockDataPoint] = None
        self.pressure: Optional[MockDataPoint] = None
        self.composition: Optional[MockDataPoint] = None
        self.wind_speed: Optional[MockDataPoint] = None
        self.discoverers: Optional[MockDataPoint] = None
        self.discovery_program: Optional[MockDataPoint] = None
        self.discovery_method: Optional[MockDataPoint] = None
        self.discovery_date: Optional[MockDataPoint] = None
        self.discovery_location: Optional[MockDataPoint] = None
        self.pre_discovery: Optional[MockDataPoint] = None
        self.detection_method: Optional[MockDataPoint] = None
        self.status: Optional[MockDataPoint] = None
        self.other_names: Optional[List[str]] = None
        self.iau_constellation_map: Optional[str] = None

        # For _get_used_references, and general iteration if any part of generator relies on it
        self.__dataclass_fields__ = [
            'host_star', 'star_epoch', 'right_ascension', 'declination', 'distance',
            'constellation', 'spectral_type', 'apparent_magnitude', 'semi_major_axis',
            'periastron', 'apoastron', 'eccentricity', 'orbital_period', 'angular_distance',
            'periastron_time', 'inclination', 'argument_of_periastron', 'epoch', 'mass',
            'minimum_mass', 'radius', 'density', 'gravity', 'rotation_period',
            'temperature', 'bond_albedo', 'pressure', 'composition', 'wind_speed',
            'discoverers', 'discovery_program', 'discovery_method', 'discovery_date',
            'discovery_location', 'pre_discovery', 'detection_method', 'status',
            'name', 'other_names' 
        ]

# --- Test Class ---
class TestWikipediaGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = WikipediaGenerator()
        # Reset used_refs before each test for isolation
        self.generator._used_refs = set()

    def test_initialization(self):
        self.assertIsNotNone(self.generator)
        self.assertEqual(self.generator._used_refs, set())
        self.assertIn('nasa', self.generator.template_refs)
        self.assertIn('article', self.generator.template_refs)
        self.assertIn('ouvrage', self.generator.template_refs)

    def test_format_datapoint_with_references(self):
        # Test how _add_reference is used by _format_datapoint
        ref_content = "{{Lien web | titre=Test1 | url=http://example.com/1 }}"
        mock_ref = MockReference(source_type_val=MockSourceType.NASA, content_template=ref_content)
        
        dp_with_ref = MockDataPoint(value="100", unit="km", reference=mock_ref)
        
        # First call
        self.generator._used_refs = set() # Clean slate for this test sequence
        output1 = self.generator._format_datapoint(dp_with_ref)
        expected_ref_name = MockSourceType.NASA 
        self.assertIn(f'<ref name="{expected_ref_name}">{ref_content}</ref>', output1)
        self.assertIn("100", output1) 

        # Second call with the same reference name
        output2 = self.generator._format_datapoint(dp_with_ref)
        self.assertIn(f'<ref name="{expected_ref_name}" />', output2)
        self.assertNotIn(ref_content, output2)

    def test_generate_infobox_with_carte_uai_and_references(self):
        exoplanet = MockExoplanet(name="Test Planet Infobox")
        exoplanet.iau_constellation_map = "Lyra_IAU.svg"
        
        ref_content_dist = "{{Lien web | titre=DistRef | url=http://example.com/dist }}"
        mock_ref_dist = MockReference(source_type_val=MockSourceType.EPE, content_template=ref_content_dist)
        exoplanet.distance = MockDataPoint(value="50", unit="pc", reference=mock_ref_dist)
        
        ref_content_mass = "{{Lien web | titre=MassRef | url=http://example.com/mass }}"
        mock_ref_mass = MockReference(source_type_val=MockSourceType.NASA, content_template=ref_content_mass)
        exoplanet.mass = MockDataPoint(value="2", unit="Mj", reference=mock_ref_mass)

        # Add another field that uses the EPE reference again to test subsequent use within one infobox
        exoplanet.spectral_type = MockDataPoint(value="G2V", reference=mock_ref_dist) 

        # generate_infobox_exoplanet resets _used_refs internally at its start
        infobox_output = self.generator.generate_infobox_exoplanet(exoplanet)

        self.assertIn("| nom = Test Planet Infobox", infobox_output)
        self.assertIn("| carte = Lyra_IAU.svg", infobox_output)
        
        # Assuming distance is processed before spectral_type in the infobox generation logic.
        # First EPE reference (distance)
        expected_dist_ref_name = MockSourceType.EPE
        self.assertIn(f'<ref name="{expected_dist_ref_name}">{ref_content_dist}</ref>', infobox_output)
        
        # NASA reference (mass) - its first use
        expected_mass_ref_name = MockSourceType.NASA
        self.assertIn(f'<ref name="{expected_mass_ref_name}">{ref_content_mass}</ref>', infobox_output)
        
        # Second EPE reference (spectral_type) should be shortened
        self.assertIn(f'<ref name="{expected_dist_ref_name}" />', infobox_output)
        # Ensure the full content for EPE only appears once
        self.assertEqual(infobox_output.count(ref_content_dist), 1)

    def test_generate_infobox_missing_carte_uai(self):
        exoplanet = MockExoplanet(name="NoMap Planet")
        infobox_output = self.generator.generate_infobox_exoplanet(exoplanet)
        self.assertNotIn("| carte =", infobox_output)

    def test_format_references_section_structure(self):
        output = self.generator._format_references_section()
        self.assertIn("== Notes et références ==", output)
        self.assertIn("=== Notes ===", output)
        self.assertIn("{{références|groupe=\"note\"}}", output)
        self.assertIn("=== Références ===", output)
        self.assertIn("{{Références}}", output)

    def test_generate_article_content_full(self):
        exoplanet = MockExoplanet(name="Kepler-186 f")
        exoplanet.host_star = MockDataPoint(value="Kepler-186")
        exoplanet.constellation = MockDataPoint(value="Cygne")
        exoplanet.spectral_type = MockDataPoint(value="M1V") 
        
        ref_content_mass = "{{Lien web | titre=MassRef | url=http://example.com/mass }}"
        mock_ref_mass = MockReference(source_type_val=MockSourceType.NASA, content_template=ref_content_mass)
        exoplanet.mass = MockDataPoint(value="0.00472", unit="M_J", reference=mock_ref_mass) # Approx 1.5 M_Earth

        ref_content_period = "{{Lien web | titre=PeriodRef | url=http://example.com/period }}"
        mock_ref_period = MockReference(source_type_val=MockSourceType.EPE, content_template=ref_content_period)
        exoplanet.orbital_period = MockDataPoint(value="129.9", unit="j", reference=mock_ref_period)
        
        exoplanet.discovery_date = MockDataPoint(value="2014-04-17")
        exoplanet.discovery_method = MockDataPoint(value="Transit")
        
        # For planet type and another reference use
        # Using same NASA ref as mass for radius
        exoplanet.radius = MockDataPoint(value="0.104", unit="R_J", reference=mock_ref_mass) # Approx 1.17 R_Earth

        # generate_article_content resets _used_refs internally
        article_output = self.generator.generate_article_content(exoplanet)

        # Introduction
        self.assertIn("'''{{nobr|Kepler-186 f}}''' est une [[exoplanète]]", article_output)
        self.assertIn("en [[orbite]] autour de {{nobr|[[Kepler-186]]}}", article_output)
        self.assertIn("une [[étoile]] de type spectral [[M1V]]", article_output) 
        self.assertIn("dans la [[constellation]] de [[Cygne]]", article_output)

        # Infobox: Mass ref (NASA) - first use
        self.assertIn(f'<ref name="{MockSourceType.NASA}">{ref_content_mass}</ref>', article_output)
        # Infobox: Radius ref (NASA) - second use for this ref name
        self.assertIn(f'<ref name="{MockSourceType.NASA}" />', article_output)
        # Overall count of full NASA ref content
        self.assertEqual(article_output.count(ref_content_mass), 1, "Full NASA ref content should appear only once in article")
        
        # Characteristics section (orbital period - EPE ref - first use for EPE)
        self.assertIn("== Caractéristiques ==", article_output)
        self.assertIn(f'<ref name="{MockSourceType.EPE}">{ref_content_period}</ref>', article_output)
        
        # References section structure
        self.assertIn("== Notes et références ==", article_output)
        self.assertIn("{{Références}}", article_output) 

        # Categories
        # Mass 0.00472 M_J < 1 M_J. Radius 0.104 R_J < 0.8 R_J. So it's "Sous-Terre"
        self.assertIn("[[Catégorie:Sous-Terre]]", article_output)
        self.assertIn("[[Catégorie:Exoplanète découverte en 2014]]", article_output)
        self.assertIn("[[Catégorie:Exoplanète découverte par transit]]", article_output)
        self.assertIn("[[Catégorie:Exoplanète en orbite autour d'une étoile de type M]]", article_output)

    def test_generate_article_content_missing_data(self):
        exoplanet = MockExoplanet(name="Minimal Planet")
        article_output = self.generator.generate_article_content(exoplanet)

        self.assertIn("'''{{nobr|Minimal Planet}}'''", article_output)
        self.assertIn("en [[orbite]] autour de son étoile hôte", article_output) 
        self.assertNotIn("dans la [[constellation]] de", article_output) 

        self.assertIn("[[Catégorie:Planète tellurique]]", article_output) 
        self.assertNotIn("découverte en", article_output)
        self.assertNotIn("découverte par", article_output)
        self.assertNotIn("étoile de type", article_output) 
        
        self.assertIn("== Notes et références ==", article_output)
        self.assertIn("{{Références}}", article_output)

if __name__ == '__main__':
    unittest.main()
