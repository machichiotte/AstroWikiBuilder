import unittest

from src.models.star import Star, DataPoint
from src.utils.star_infobox_generator import StarInfoboxGenerator
from src.utils.wikipedia_star_generator import WikipediaStarGenerator

class TestStarModel(unittest.TestCase):
    def test_star_creation(self):
        star = Star(
            name=DataPoint("Test Star"),
            spectral_type=DataPoint("G2V"),
            distance=DataPoint(1.0, "pc")
        )
        self.assertEqual(star.name.value, "Test Star")
        self.assertEqual(star.spectral_type.value, "G2V")
        self.assertEqual(star.distance.value, 1.0)
        self.assertEqual(star.distance.unit, "pc")
        self.assertIsNone(star.mass) # Test that unassigned attributes are None

    def test_star_designations_processing(self):
        # Test with comma-separated string
        star1 = Star(name=DataPoint("Star1"), designations=DataPoint("Des1, Des2, Des3"))
        self.assertIsInstance(star1.designations.value, list)
        self.assertEqual(star1.designations.value, ["Des1", "Des2", "Des3"])

        # Test with already a list
        star2 = Star(name=DataPoint("Star2"), designations=DataPoint(["DesA", "DesB"]))
        self.assertIsInstance(star2.designations.value, list)
        self.assertEqual(star2.designations.value, ["DesA", "DesB"])

        # Test with a single string value (not comma-separated)
        star3 = Star(name=DataPoint("Star3"), designations=DataPoint("SingleDes"))
        self.assertIsInstance(star3.designations.value, list)
        self.assertEqual(star3.designations.value, ["SingleDes"])
        
        # Test with None
        star4 = Star(name=DataPoint("Star4"), designations=None)
        self.assertIsNone(star4.designations)

        # Test with DataPoint having None value
        star5 = Star(name=DataPoint("Star5"), designations=DataPoint(None))
        self.assertIsNone(star5.designations.value)


class TestStarInfoboxGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = StarInfoboxGenerator()
        self.maxDiff = None # To see full diffs on error

    def test_generate_infobox_minimal(self):
        star = Star(name=DataPoint("Minimal Star"))
        infobox = self.generator.generate_star_infobox(star)
        self.assertIn("{{Infobox Étoile", infobox)
        self.assertIn("| nom = Minimal Star", infobox)
        self.assertIn("}}", infobox)

    def test_generate_infobox_full_data(self):
        star_data = {
            "name": DataPoint("Alpha Centauri A"),
            "image": DataPoint("Alpha_Cen_A.jpg"),
            "caption": DataPoint("Artwork of Alpha Centauri A"),
            "epoch": DataPoint("J2000.0"),
            "right_ascension": DataPoint("14h 39m 36.49400s"),
            "declination": DataPoint("−60° 50′ 02.3737″"),
            "constellation": DataPoint("Centaure"),
            "apparent_magnitude": DataPoint("0.01"),
            "spectral_type": DataPoint("G2V"),
            "distance": DataPoint(value=1.347, unit="pc"),
            "mass": DataPoint(value=1.100, unit="M☉"),
            "radius": DataPoint(value=1.227, unit="R☉"),
            "temperature": DataPoint(value=5790, unit="K"),
            "age": DataPoint(value="4.85", unit="Gyr"), # Gigayears
            "designations": DataPoint(["Rigil Kentaurus", "Toliman", "α Cen A"])
        }
        star = Star(**star_data)
        infobox = self.generator.generate_star_infobox(star)

        self.assertIn("{{Infobox Étoile", infobox)
        self.assertIn("| nom = Alpha Centauri A", infobox)
        self.assertIn("| image = Alpha_Cen_A.jpg", infobox)
        self.assertIn("| légende = Artwork of Alpha Centauri A", infobox)
        self.assertIn("| époque = J2000.0", infobox)
        self.assertIn("| ascension droite = 14h 39m 36.49400s", infobox)
        self.assertIn("| déclinaison = −60° 50′ 02.3737″", infobox)
        self.assertIn("| constellation = Centaure", infobox)
        self.assertIn("| magnitude apparente = 0.01", infobox)
        self.assertIn("| type spectral = G2V", infobox)
        self.assertIn("| distance = {{Parsec|1.347|pc}}", infobox)
        self.assertIn("| masse = 1.1", infobox) # Note: _add_field might simplify float output
        self.assertIn("| masse unité = M☉", infobox)
        self.assertIn("| rayon = 1.227", infobox)
        self.assertIn("| rayon unité = R☉", infobox)
        self.assertIn("| température = 5790", infobox)
        self.assertIn("| température unité = K", infobox)
        self.assertIn("| âge = 4.85", infobox)
        self.assertIn("| âge unité = Gyr", infobox)
        self.assertIn("| désignations = Rigil Kentaurus, Toliman, α Cen A", infobox)
        self.assertIn("}}", infobox)

    def test_generate_infobox_distance_formats(self):
        # Test with pc
        star_pc = Star(name=DataPoint("StarPC"), distance=DataPoint(10, "pc"))
        infobox_pc = self.generator.generate_star_infobox(star_pc)
        self.assertIn("| distance = {{Parsec|10|pc}}", infobox_pc)

        # Test with al
        star_al = Star(name=DataPoint("StarAL"), distance=DataPoint(32.6, "al"))
        infobox_al = self.generator.generate_star_infobox(star_al)
        self.assertIn("| distance al = 32.6", infobox_al) # Check specific field for 'al'
        self.assertNotIn("| distance = 32.6 al", infobox_al) # Ensure it doesn't use the generic distance field with unit

        # Test with other unit (km) - fallback
        star_km = Star(name=DataPoint("StarKM"), distance=DataPoint(9.461e12, "km"))
        infobox_km = self.generator.generate_star_infobox(star_km)
        self.assertIn("| distance = 9.461e+12 km", infobox_km)

        # Test with no unit
        star_nounit = Star(name=DataPoint("StarNoUnit"), distance=DataPoint(5))
        infobox_nounit = self.generator.generate_star_infobox(star_nounit)
        self.assertIn("| distance = 5", infobox_nounit)
        self.assertNotIn("| distance unité =", infobox_nounit)

    def test_generate_infobox_no_attributes(self):
        star = Star() # All attributes are None by default if not provided
        infobox = self.generator.generate_star_infobox(star)
        self.assertIn("{{Infobox Étoile", infobox)
        self.assertIn("}}", infobox)
        # Check that no data lines are present (except potentially name if it defaults)
        self.assertNotIn("| nom =", infobox) # Since name is None
        self.assertNotIn("| époque =", infobox)
        self.assertNotIn("| distance =", infobox)
        self.assertNotIn("| masse =", infobox)

class TestWikipediaStarGenerator(unittest.TestCase):
    def setUp(self):
        self.wiki_generator = WikipediaStarGenerator()
        self.infobox_generator = StarInfoboxGenerator() # For comparison

    def test_generate_article_content_calls_infobox_generator(self):
        star_data = {
            "name": DataPoint("Test Star for Wiki Gen"),
            "spectral_type": DataPoint("M0V"),
            "distance": DataPoint(value=10, unit="pc")
        }
        star = Star(**star_data)

        # Generate content using WikipediaStarGenerator
        article_content = self.wiki_generator.generate_article_content(star)

        # Generate content directly using StarInfoboxGenerator
        expected_infobox_content = self.infobox_generator.generate_star_infobox(star)

        # Assert that the article content is the same as the infobox content
        self.assertEqual(article_content, expected_infobox_content)
        self.assertIn("{{Infobox Étoile", article_content)
        self.assertIn("| nom = Test Star for Wiki Gen", article_content)
        self.assertIn("| type spectral = M0V", article_content)
        self.assertIn("| distance = {{Parsec|10|pc}}", article_content)


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
