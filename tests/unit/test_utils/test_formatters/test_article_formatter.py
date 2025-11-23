import locale
import unittest
from unittest.mock import patch

from src.models.entities.exoplanet_entity import ValueWithUncertainty
from src.utils.formatters.article_formatter import ArticleFormatter


class TestArticleFormatter(unittest.TestCase):
    def setUp(self):
        self.formatter = ArticleFormatter()

    def test_init_locale_fallback(self):
        """Test that __init__ tries multiple locales."""
        with patch("locale.setlocale") as mock_setlocale:
            # Make setlocale fail for the first few calls, then succeed
            mock_setlocale.side_effect = [locale.Error, locale.Error, None]

            ArticleFormatter()

            # Should have called setlocale at least 3 times (or until success)
            self.assertGreaterEqual(mock_setlocale.call_count, 3)

    def test_format_number_as_french_string_none(self):
        self.assertEqual(self.formatter.format_number_as_french_string(None), "")

    def test_format_number_as_french_string_integer(self):
        self.assertEqual(self.formatter.format_number_as_french_string(10.0), "10")
        self.assertEqual(self.formatter.format_number_as_french_string(10), "10")

    def test_format_number_as_french_string_float(self):
        # Assuming the locale is set correctly to French or handled by replace
        # We might need to mock locale.format_string if the system locale isn't reliable in tests
        with patch("locale.format_string") as mock_format:
            mock_format.return_value = "12,34"
            self.assertEqual(self.formatter.format_number_as_french_string(12.34), "12,34")

    def test_format_number_as_french_string_fallback_replace(self):
        """Test the fallback where dot is replaced by comma if locale fails to do so."""
        with patch("locale.format_string") as mock_format:
            # Simulate a locale that returns dot
            mock_format.return_value = "12.34"
            self.assertEqual(self.formatter.format_number_as_french_string(12.34), "12,34")

    def test_format_number_as_french_string_exception(self):
        """Test handling of non-numeric values."""
        self.assertEqual(self.formatter.format_number_as_french_string("invalid"), "invalid")

    def test_format_year_without_decimals_none(self):
        self.assertEqual(self.formatter.format_year_without_decimals(None), "")

    def test_format_year_without_decimals_integer(self):
        self.assertEqual(self.formatter.format_year_without_decimals(2023.0), "2023")
        self.assertEqual(self.formatter.format_year_without_decimals(2023), "2023")

    def test_format_year_without_decimals_non_integer(self):
        self.assertEqual(self.formatter.format_year_without_decimals(2023.5), "2023.5")
        self.assertEqual(self.formatter.format_year_without_decimals("approx 2023"), "approx 2023")

    def test_convert_parsecs_to_lightyears(self):
        self.assertAlmostEqual(self.formatter.convert_parsecs_to_lightyears(10), 32.6156)

    def test_format_uncertain_value_empty(self):
        self.assertEqual(self.formatter.format_uncertain_value_for_article(None), "")
        self.assertEqual(
            self.formatter.format_uncertain_value_for_article(ValueWithUncertainty(value=None)), ""
        )

    def test_format_uncertain_value_simple(self):
        val = ValueWithUncertainty(value=10.5)
        # Mocking format_number_as_french_string to ensure consistent output
        with patch.object(self.formatter, "format_number_as_french_string", return_value="10,5"):
            self.assertEqual(self.formatter.format_uncertain_value_for_article(val), "10,5")

    def test_format_uncertain_value_non_numeric(self):
        val = ValueWithUncertainty(value="unknown")
        self.assertEqual(self.formatter.format_uncertain_value_for_article(val), "unknown")

    def test_format_uncertain_value_with_errors(self):
        val = ValueWithUncertainty(value=10.0, error_positive=0.5, error_negative=0.3)
        with patch.object(self.formatter, "format_number_as_french_string") as mock_fmt:
            mock_fmt.side_effect = ["10", "0,5", "0,3"]
            self.assertEqual(self.formatter.format_uncertain_value_for_article(val), "10 +0,5-0,3")

    def test_format_uncertain_value_with_sign(self):
        val = ValueWithUncertainty(value=10.0, sign="~")
        with patch.object(self.formatter, "format_number_as_french_string", return_value="10"):
            self.assertEqual(self.formatter.format_uncertain_value_for_article(val), "~10")


if __name__ == "__main__":
    unittest.main()
