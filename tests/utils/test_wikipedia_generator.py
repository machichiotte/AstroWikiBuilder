import unittest
from src.utils.wikipedia_generator import WikipediaGenerator # The class to test
from typing import Optional, List, Dict # For type hints in mocks
import math # For checking light-year conversion

# --- Mock Data Structures ---
# Simplified SourceType Enum for testing
class MockSourceType:
    NEA = "NEA"
    EPE = "EPE"
    OEC = "OEC"
    ARTICLE = "Article"
    OUVRAGE = "Ouvrage"
    CUSTOM = "CustomRef" 
    NOTE_REF = "NoteRef"


class MockReference:
    def __init__(self, source_type_val: str, content_template: str, name_override: Optional[str] = None, group: Optional[str] = None):
        self.source = type('EnumMock', (), {'value': source_type_val})() 
        self.content_template = content_template 
        self._name_override = name_override
        self.group = group

    def to_wiki_ref(self) -> str:
        ref_name = self._name_override if self._name_override else self.source.value
        group_attr = f' group="{self.group}"' if self.group else ''
        # Ensure no space before group attribute if name is not present, though name usually is.
        # For this test, we assume named references. If anonymous, ref_name part would be empty.
        return f'<ref name="{ref_name}"{group_attr}>{self.content_template}</ref>'


class MockDataPoint:
    def __init__(self, value: any, unit: Optional[str] = None, reference: Optional[MockReference] = None):
        self.value = value
        self.unit = unit
        self.reference = reference

class MockExoplanet:
    def __init__(self, name: str):
        self.name = name
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
        self.__dataclass_fields__ = [ # Simplified for testing get_used_references if needed
            f for f in self.__dict__ if not f.startswith('_')
        ]

# --- Test Class ---
class TestWikipediaGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = WikipediaGenerator()
        self.generator._used_refs = set()
        self.generator._has_grouped_notes = False


    def test_date_formatting_in_article(self):
        exoplanet = MockExoplanet(name="TestDatePlanet")
        exoplanet.discovery_date = MockDataPoint(value=2011.0) # Test float year
        article_output = self.generator.generate_article_content(exoplanet)
        self.assertIn("découverte en 2011 par la méthode", article_output)

        exoplanet.discovery_date = MockDataPoint(value="2012") # Test string year
        article_output = self.generator.generate_article_content(exoplanet)
        self.assertIn("découverte en 2012 par la méthode", article_output)
        
        exoplanet.discovery_date = MockDataPoint(value="2013-05-20") # Test full date string
        article_output = self.generator.generate_article_content(exoplanet)
        self.assertIn("découverte en 2013-05-20 par la méthode", article_output)


    def test_infobox_default_units(self):
        exoplanet = MockExoplanet(name="TestUnitPlanet")
        # Case 1: Unit is the default
        exoplanet.mass = MockDataPoint(value="1", unit="M_J") # M_J is default for "masse"
        exoplanet.radius = MockDataPoint(value="1", unit="R_J") # R_J is default for "rayon"
        
        # Case 2: Unit is different from default
        exoplanet.temperature = MockDataPoint(value="1200", unit="°C") # Default for "température" is K
        
        # Case 3: Data has no unit (should not print unit line)
        exoplanet.distance = MockDataPoint(value="50") # Default for "distance" is "pc"

        # Case 4: Field with no predefined default unit in FIELD_DEFAULT_UNITS
        exoplanet.eccentricity = MockDataPoint(value="0.1", unit="n/a") # Eccentricity has no default in map

        infobox = self.generator.generate_infobox_exoplanet(exoplanet)

        self.assertNotIn("| masse unité = M_J", infobox)
        self.assertNotIn("| rayon unité = R_J", infobox)
        self.assertIn("| température unité = °C", infobox)
        self.assertNotIn("| distance unité =", infobox) # No unit in data, so no unit line
        self.assertIn("| eccentricité unité = n/a", infobox) # No default, so unit is shown


    def test_first_reference_formatting_globally(self):
        exoplanet = MockExoplanet(name="TestGlobalRefPlanet")
        
        ref_nasa_content = "{{Lien web | titre=NASA1 | url=http://nasa.gov/1 }}"
        mock_ref_nasa = MockReference(source_type_val=MockSourceType.NEA, content_template=ref_nasa_content)
        
        ref_epe_content = "{{Lien web | titre=EPE1 | url=http://epe.eu/1 }}"
        mock_ref_epe = MockReference(source_type_val=MockSourceType.EPE, content_template=ref_epe_content)

        # Setup: Mass (NASA ref) for infobox, Period (EPE ref) for body
        exoplanet.mass = MockDataPoint(value="1", unit="M_J", reference=mock_ref_nasa)
        exoplanet.orbital_period = MockDataPoint(value="365", unit="j", reference=mock_ref_epe)
        # For a second use of NASA ref in body, let's use radius.
        exoplanet.radius = MockDataPoint(value="1", unit="R_J", reference=mock_ref_nasa)

        article = self.generator.generate_article_content(exoplanet)

        # NASA ref: First used in infobox (mass), should be full.
        # Then used in body (radius), should be short.
        expected_nasa_full = f'<ref name="{MockSourceType.NEA}">{ref_nasa_content}</ref>'
        expected_nasa_short = f'<ref name="{MockSourceType.NEA}" />'
        
        self.assertEqual(article.count(expected_nasa_full), 1, "NASA full ref should appear once")
        self.assertTrue(article.count(expected_nasa_short) >= 1, "NASA short ref should appear at least once")
        
        # EPE ref: First used in body (orbital_period), should be full.
        expected_epe_full = f'<ref name="{MockSourceType.EPE}">{ref_epe_content}</ref>'
        self.assertIn(expected_epe_full, article)
        # Ensure it's not later shortened if not used again, or correctly shortened if it were.
        # For this test, its first use is its only use in the provided setup for orbital_period.
        self.assertEqual(article.count(expected_epe_full), 1, "EPE full ref should appear once")


    def test_conditional_notes_subsection(self):
        exoplanet = MockExoplanet(name="TestNotesPlanet")
        
        # Scenario 1: No grouped notes
        ref_regular_content = "{{Lien web | titre=Regular | url=http://example.com/regular }}"
        mock_ref_regular = MockReference(source_type_val=MockSourceType.CUSTOM, content_template=ref_regular_content)
        exoplanet.temperature = MockDataPoint(value="300", unit="K", reference=mock_ref_regular)
        
        article_no_notes = self.generator.generate_article_content(exoplanet)
        self.assertNotIn("=== Notes ===", article_no_notes)
        self.assertNotIn("{{références|groupe=\"note\"}}", article_no_notes)
        self.assertIn("=== Références ===", article_no_notes) # Main refs should still be there

        # Scenario 2: With a grouped note
        self.generator._used_refs = set() # Reset for next generation
        self.generator._has_grouped_notes = False

        ref_note_content_str = "{{Note | texte=Ceci est une note. }}"
        # MockReference.to_wiki_ref needs to produce the group="note" part.
        # The check in _add_reference is on ref_content, which is the output of to_wiki_ref().
        # So, the content_template itself doesn't need group="note", but the to_wiki_ref() output should.
        mock_ref_grouped_note = MockReference(
            source_type_val=MockSourceType.NOTE_REF, 
            content_template=ref_note_content_str, 
            name_override="testnote1", # Grouped notes usually have names
            group="note" # This tells MockReference to add group="note" in its to_wiki_ref()
        )
        exoplanet.eccentricity = MockDataPoint(value="0.1", reference=mock_ref_grouped_note)

        article_with_notes = self.generator.generate_article_content(exoplanet)
        self.assertIn("=== Notes ===", article_with_notes)
        self.assertIn("{{références|groupe=\"note\"}}", article_with_notes)
        self.assertIn(mock_ref_grouped_note.to_wiki_ref(), article_with_notes) # Ensure the note itself is in the article

    def test_distance_formatting_lightyears_parsecs(self):
        exoplanet = MockExoplanet(name="TestDistancePlanet")
        
        pc_val = 103.08
        ref_dist_content = "{{Lien web | titre=DistRef | url=http://example.com/dist }}"
        mock_ref_dist = MockReference(source_type_val=MockSourceType.NEA, content_template=ref_dist_content)
        exoplanet.distance = MockDataPoint(value=pc_val, unit="pc", reference=mock_ref_dist)

        article = self.generator.generate_article_content(exoplanet)
        
        ly_val_expected = math.floor(pc_val * 3.26156) # Using floor to match precision=0 for positive numbers
        # The _format_numeric_value uses locale.format_string("%.0f", ...) which rounds.
        # For 336.2601968, %.0f gives "336".
        # For 336.7, it would give "337".
        # Let's use the generator's own formatting for expected value.
        expected_ly_str = self.generator._format_numeric_value(pc_val * 3.26156, precision=0)
        
        # Formatted PC value (number only, from _format_numeric_value)
        expected_pc_num_str = self.generator._format_numeric_value(pc_val, precision=2) # Default precision for pc
        
        # Full PC ref string as generated by _format_datapoint (number + ref tag)
        expected_pc_val_and_ref = f"{expected_pc_num_str} {mock_ref_dist.to_wiki_ref()}"
        
        expected_distance_string = f"située à {expected_ly_str} [[année-lumière|années-lumière]] ({expected_pc_val_and_ref} [[parsec|pc]]) de la [[Terre]]"
        self.assertIn(expected_distance_string, article)

if __name__ == '__main__':
    unittest.main()
