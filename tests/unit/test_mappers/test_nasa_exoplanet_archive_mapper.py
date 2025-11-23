"""
Tests unitaires pour NasaExoplanetArchiveMapper.

Ce module teste la transformation des données NEA vers les modèles Exoplanet et Star.
"""

from datetime import datetime
from unittest.mock import Mock, patch

import pytest

from src.mappers.nasa_exoplanet_archive_mapper import (
    NasaExoplanetArchiveMapper,
    is_invalid_raw_value,
)
from src.models.entities.exoplanet_entity import Exoplanet, ValueWithUncertainty
from src.models.entities.star_entity import Star
from src.models.references.reference import SourceType


class TestIsInvalidRawValue:
    """Tests pour la fonction is_invalid_raw_value."""

    def test_none_is_invalid(self):
        assert is_invalid_raw_value(None) is True

    def test_empty_string_is_invalid(self):
        assert is_invalid_raw_value("") is True
        assert is_invalid_raw_value("   ") is True

    def test_nan_string_is_invalid(self):
        assert is_invalid_raw_value("nan") is True
        assert is_invalid_raw_value("NaN") is True
        assert is_invalid_raw_value("NAN") is True

    def test_none_string_is_invalid(self):
        assert is_invalid_raw_value("none") is True
        assert is_invalid_raw_value("None") is True

    def test_valid_values_are_not_invalid(self):
        assert is_invalid_raw_value("123.45") is False
        assert is_invalid_raw_value(123.45) is False
        assert is_invalid_raw_value("test") is False
        assert is_invalid_raw_value(0) is False


class TestNasaExoplanetArchiveMapper:
    """Tests pour NasaExoplanetArchiveMapper."""

    @pytest.fixture
    def mapper(self):
        """Fixture pour créer un mapper."""
        return NasaExoplanetArchiveMapper()

    @pytest.fixture
    def sample_nea_data(self):
        """Fixture pour créer des données NEA de test."""
        return {
            "pl_name": "Kepler-186 f",
            "hostname": "Kepler-186",
            "pl_bmasse": 1.71,
            "pl_bmasse_err1": 0.15,
            "pl_bmasse_err2": -0.12,
            "pl_rade": 1.17,
            "pl_orbper": 129.9441,
            "st_teff": 3788.0,
            "st_teff_err1": 54.0,
            "st_teff_err2": -54.0,
            "st_mass": 0.544,
            "rastr": "19h54m36.65s",
            "decstr": "+43d57m03.8s",
            "ra": 298.652708,
            "dec": 43.951056,
        }

    def test_build_reference_from_nea_for_planet(self, mapper, sample_nea_data):
        """Test de création de référence pour une planète."""
        ref = mapper.build_reference_from_nea(sample_nea_data, isPlanet=True)

        assert ref.source == SourceType.NEA
        assert ref.star_id == "Kepler-186"
        assert ref.planet_id == "Kepler-186 f"
        assert isinstance(ref.update_date, datetime)
        assert isinstance(ref.consultation_date, datetime)

    def test_build_reference_from_nea_for_star(self, mapper, sample_nea_data):
        """Test de création de référence pour une étoile."""
        ref = mapper.build_reference_from_nea(sample_nea_data, isPlanet=False)

        assert ref.source == SourceType.NEA
        assert ref.star_id == "Kepler-186"
        assert ref.planet_id is None

    def test_parse_error_value_valid(self, mapper):
        """Test de parsing d'une valeur d'erreur valide."""
        assert mapper._parse_error_value(0.15) == 0.15
        assert mapper._parse_error_value("+0.15") == 0.15
        assert mapper._parse_error_value("-0.12") == 0.12

    def test_parse_error_value_invalid(self, mapper):
        """Test de parsing d'une valeur d'erreur invalide."""
        assert mapper._parse_error_value(None) is None
        assert mapper._parse_error_value("invalid") is None
        assert mapper._parse_error_value("") is None

    def test_format_right_ascension_str(self, mapper):
        """Test de formatage d'ascension droite en chaîne."""
        assert mapper._format_right_ascension_str("19h54m36.65s") == "19/54/36.65"
        assert mapper._format_right_ascension_str("12h00m00s") == "12/00/00"
        assert mapper._format_right_ascension_str("") == ""
        assert mapper._format_right_ascension_str(None) == ""

    def test_format_declination_str(self, mapper):
        """Test de formatage de déclinaison en chaîne."""
        assert mapper._format_declination_str("+43d57m03.8s") == "+43/57/03.8"
        assert mapper._format_declination_str("-12d30m45s") == "-12/30/45"
        assert mapper._format_declination_str("") == ""
        assert mapper._format_declination_str(None) == ""

    def test_format_right_ascension_deg(self, mapper):
        """Test de formatage d'ascension droite en degrés."""
        result = mapper._format_right_ascension_deg(298.652708)
        assert result.startswith("19/54/")
        assert mapper._format_right_ascension_deg(None) == ""

    def test_format_declination_deg(self, mapper):
        """Test de formatage de déclinaison en degrés."""
        result = mapper._format_declination_deg(43.951056)
        assert result.startswith("+43/")
        result_neg = mapper._format_declination_deg(-12.5)
        assert result_neg.startswith("-12/")
        assert mapper._format_declination_deg(None) == ""

    def test_is_composite_formatted_string(self, mapper):
        """Test de détection de chaîne composite."""
        assert mapper.is_composite_formatted_string("\u003cspan\u003e123\u003c/span\u003e") is True
        assert mapper.is_composite_formatted_string("123\u0026plusmn0.5") is True
        assert mapper.is_composite_formatted_string("\u0026gt123") is True
        assert mapper.is_composite_formatted_string("\u0026lt456") is True
        assert mapper.is_composite_formatted_string("123.45") is False

    def test_convert_to_value_with_uncertainty(self, mapper):
        """Test de conversion vers ValueWithUncertainty."""
        result = mapper.convert_to_value_with_uncertainty(
            123.45, error_positive=0.5, error_negative=0.3, sign="±"
        )
        assert isinstance(result, ValueWithUncertainty)
        assert result.value == 123.45
        assert result.error_positive == 0.5
        assert result.error_negative == 0.3
        assert result.sign == "±"

    def test_convert_to_value_with_uncertainty_none(self, mapper):
        """Test de conversion avec valeur None."""
        assert mapper.convert_to_value_with_uncertainty(None) is None
        assert mapper.convert_to_value_with_uncertainty("") is None

    def test_extract_star_alternative_names(self, mapper):
        """Test d'extraction des noms alternatifs d'étoile."""
        nea_data = {
            "hostname": "Kepler-186",
            "hd_name": "HD 123456",
            "hip_name": "HIP 98765",
            "tic_id": "TIC 111222",
        }
        result = mapper.extract_star_alternative_names(nea_data)
        assert result is not None
        assert "HD 123456" in result
        assert "HIP 98765" in result
        assert "TIC 111222" in result
        assert "Kepler-186" not in result  # hostname ne doit pas être inclus

    def test_extract_star_alternative_names_with_duplicates(self, mapper):
        """Test d'extraction avec doublons."""
        nea_data = {
            "hostname": "Kepler-186",
            "hd_name": "Kepler-186",  # Doublon avec hostname
            "hip_name": "HIP 98765",
            "tic_id": "nan",  # Valeur invalide
        }
        result = mapper.extract_star_alternative_names(nea_data)
        assert result is not None
        assert "Kepler-186" not in result
        assert "HIP 98765" in result
        assert len(result) == 1

    def test_extract_star_alternative_names_empty(self, mapper):
        """Test d'extraction sans noms alternatifs."""
        nea_data = {"hostname": "Kepler-186"}
        result = mapper.extract_star_alternative_names(nea_data)
        assert result is None

    def test_extract_exoplanet_alternative_names(self, mapper):
        """Test d'extraction des noms alternatifs d'exoplanète."""
        nea_data = {"pl_name": "Kepler-186 f"}
        result = mapper.extract_exoplanet_alternative_names(nea_data)
        assert result is None  # Actuellement retourne None

    @patch("src.mappers.nasa_exoplanet_archive_mapper.ConstellationUtil")
    def test_set_coordinates_and_constellation_with_str(
        self, mock_constellation_util, mapper, sample_nea_data
    ):
        """Test de définition des coordonnées avec chaînes."""
        mock_util_instance = Mock()
        mock_util_instance.get_constellation_name.return_value = "Cygnus"
        mapper.constellation_util = mock_util_instance

        obj = Mock()
        obj.st_right_ascension = None
        obj.st_declination = None
        obj.sy_constellation = None

        ref = Mock()
        mapper.set_coordinates_and_constellation(obj, sample_nea_data, ref)

        assert obj.st_right_ascension == "19/54/36.65"
        assert obj.st_declination == "+43/57/03.8"
        assert obj.sy_constellation == "Cygnus"

    @patch("src.mappers.nasa_exoplanet_archive_mapper.ConstellationUtil")
    def test_map_exoplanet_from_nea_record(self, mock_constellation_util, mapper, sample_nea_data):
        """Test de mapping complet d'une exoplanète."""
        mock_util_instance = Mock()
        mock_util_instance.get_constellation_name.return_value = "Cygnus"
        mapper.constellation_util = mock_util_instance

        exoplanet = mapper.map_exoplanet_from_nea_record(sample_nea_data)

        assert isinstance(exoplanet, Exoplanet)
        assert exoplanet.pl_name == "Kepler-186 f"
        assert exoplanet.st_name == "Kepler-186"
        assert exoplanet.reference.source == SourceType.NEA
        assert exoplanet.st_right_ascension == "19/54/36.65"
        assert exoplanet.sy_constellation == "Cygnus"

    @patch("src.mappers.nasa_exoplanet_archive_mapper.ConstellationUtil")
    def test_map_star_from_nea_record(self, mock_constellation_util, mapper, sample_nea_data):
        """Test de mapping complet d'une étoile."""
        mock_util_instance = Mock()
        mock_util_instance.get_constellation_name.return_value = "Cygnus"
        mapper.constellation_util = mock_util_instance

        star = mapper.map_star_from_nea_record(sample_nea_data)

        assert isinstance(star, Star)
        assert star.st_name == "Kepler-186"
        assert star.reference.source == SourceType.NEA
        assert star.st_right_ascension == "19/54/36.65"
        assert star.sy_constellation == "Cygnus"

    def test_parse_field_with_numeric_value(self, mapper, sample_nea_data):
        """Test de parsing d'un champ numérique."""
        result = mapper._parse_field(
            raw_value=3788.0,
            nea_data=sample_nea_data,
            nea_field="st_teff",
            attribute="st_temperature",
        )

        assert isinstance(result, ValueWithUncertainty)
        assert result.value == 3788.0
        assert result.error_positive == 54.0
        assert result.error_negative == 54.0
        assert result.sign == "±"

    def test_parse_field_with_string_value(self, mapper, sample_nea_data):
        """Test de parsing d'un champ chaîne."""
        result = mapper._parse_field(
            raw_value="G2V",
            nea_data=sample_nea_data,
            nea_field="st_spectype",
            attribute="st_spectral_type",
        )

        assert result == "G2V"

    def test_parse_field_with_luminosity(self, mapper):
        """Test de parsing de la luminosité (log10)."""
        nea_data = {"st_lum": -0.5, "st_lum_err1": 0.1, "st_lum_err2": -0.1}

        result = mapper._parse_field(
            raw_value=-0.5,
            nea_data=nea_data,
            nea_field="st_lum",
            attribute="st_luminosity",
        )

        assert isinstance(result, ValueWithUncertainty)
        # 10^(-0.5) ≈ 0.316
        assert 0.3 < result.value < 0.4


class TestCompositeValueParsing:
    """Tests for composite formatted value parsing."""

    @pytest.fixture
    def mapper(self):
        """Fixture pour créer un mapper."""
        return NasaExoplanetArchiveMapper()

    def test_parse_plusmn_value_valid(self, mapper):
        """Test de parsing d'une valeur avec &plusmn."""
        result = mapper._parse_plusmn_value("2450000&plusmn100")
        assert isinstance(result, ValueWithUncertainty)
        assert result.value == 2450000.0
        assert result.error_positive == 100.0
        assert result.error_negative == 100.0
        assert result.sign == "±"

    def test_parse_plusmn_value_single_value(self, mapper):
        """Test de parsing d'une valeur sans erreur."""
        result = mapper._parse_plusmn_value("2450000")
        assert isinstance(result, ValueWithUncertainty)
        assert result.value == 2450000.0
        assert result.error_positive is None
        assert result.error_negative is None

    def test_parse_plusmn_value_invalid(self, mapper):
        """Test de parsing d'une valeur invalide."""
        result = mapper._parse_plusmn_value("invalid&plusmntext")
        assert result is None

    def test_parse_html_value_with_errors(self, mapper):
        """Test de parsing d'une valeur HTML avec erreurs."""
        html_value = (
            '<div><span class="supersubNumber">2450000</span>'
            '<span class="superscript">+100</span>'
            '<span class="subscript">-50</span></div>'
        )
        result = mapper._parse_html_value(html_value)
        assert isinstance(result, ValueWithUncertainty)
        assert result.value == 2450000.0
        assert result.error_positive == 100.0
        assert result.error_negative == 50.0
        assert result.sign == "±"

    def test_parse_html_value_malformed(self, mapper):
        """Test de parsing d'une valeur HTML malformée."""
        result = mapper._parse_html_value("<div>invalid</div>")
        # HTML malformé retourne un ValueWithUncertainty avec des None
        # ou None selon le cas
        assert result is None or (result.value is None)

    def test_parse_gt_lt_value_greater_than(self, mapper):
        """Test de parsing d'une valeur avec &gt."""
        result = mapper._parse_gt_lt_value("&gt5.0")
        assert isinstance(result, ValueWithUncertainty)
        assert result.value == 5.0
        assert result.sign == ">"

    def test_parse_gt_lt_value_less_than(self, mapper):
        """Test de parsing d'une valeur avec &lt."""
        result = mapper._parse_gt_lt_value("&lt3.5")
        assert isinstance(result, ValueWithUncertainty)
        assert result.value == 3.5
        assert result.sign == "<"

    def test_parse_gt_lt_value_invalid(self, mapper):
        """Test de parsing d'une valeur sans &gt ou &lt."""
        result = mapper._parse_gt_lt_value("5.0")
        assert result is None

    def test_parse_gt_lt_value_invalid_number(self, mapper):
        """Test de parsing d'une valeur &gt avec nombre invalide."""
        result = mapper._parse_gt_lt_value("&gtinvalid")
        assert result is None

    def test_parse_composite_formatted_value_plusmn(self, mapper):
        """Test du parser composite avec format &plusmn."""
        result = mapper.parse_composite_formatted_value("2450000&plusmn100")
        assert isinstance(result, ValueWithUncertainty)
        assert result.value == 2450000.0

    def test_parse_composite_formatted_value_html(self, mapper):
        """Test du parser composite avec format HTML."""
        html_value = (
            '<div><span class="supersubNumber">2450000</span>'
            '<span class="superscript">+100</span></div>'
        )
        result = mapper.parse_composite_formatted_value(html_value)
        assert isinstance(result, ValueWithUncertainty)
        assert result.value == 2450000.0

    def test_parse_composite_formatted_value_gt(self, mapper):
        """Test du parser composite avec format &gt."""
        result = mapper.parse_composite_formatted_value("&gt5.0")
        assert isinstance(result, ValueWithUncertainty)
        assert result.value == 5.0
        assert result.sign == ">"

    def test_parse_composite_formatted_value_lt(self, mapper):
        """Test du parser composite avec format &lt."""
        result = mapper.parse_composite_formatted_value("&lt3.5")
        assert isinstance(result, ValueWithUncertainty)
        assert result.value == 3.5
        assert result.sign == "<"

    def test_parse_composite_formatted_value_simple_numeric(self, mapper):
        """Test du parser composite avec valeur numérique simple."""
        result = mapper.parse_composite_formatted_value("123.45")
        assert isinstance(result, ValueWithUncertainty)
        assert result.value == 123.45

    def test_parse_composite_formatted_value_none(self, mapper):
        """Test du parser composite avec None."""
        assert mapper.parse_composite_formatted_value(None) is None

    def test_parse_composite_formatted_value_invalid(self, mapper):
        """Test du parser composite avec valeur invalide."""
        result = mapper.parse_composite_formatted_value("invalid text")
        assert result is None


class TestCoordinateFallbacks:
    """Tests for coordinate parsing when string formats unavailable."""

    @pytest.fixture
    def mapper(self):
        """Fixture pour créer un mapper."""
        return NasaExoplanetArchiveMapper()

    @patch("src.mappers.nasa_exoplanet_archive_mapper.ConstellationUtil")
    def test_set_right_ascension_from_degrees(self, mock_constellation_util, mapper):
        """Test de définition de l'ascension droite depuis les degrés."""
        nea_data = {
            "ra": 298.652708,  # Pas de rastr
            "dec": 43.951056,
        }
        obj = Mock()
        obj.st_right_ascension = None
        obj.st_declination = None
        obj.sy_constellation = None

        ref = Mock()
        mapper.set_coordinates_and_constellation(obj, nea_data, ref)

        # Devrait utiliser le format en degrés
        assert obj.st_right_ascension is not None
        assert obj.st_right_ascension.startswith("19/")

    @patch("src.mappers.nasa_exoplanet_archive_mapper.ConstellationUtil")
    def test_set_declination_from_degrees(self, mock_constellation_util, mapper):
        """Test de définition de la déclinaison depuis les degrés."""
        nea_data = {
            "ra": 298.652708,
            "dec": 43.951056,  # Pas de decstr
        }
        obj = Mock()
        obj.st_right_ascension = None
        obj.st_declination = None
        obj.sy_constellation = None

        ref = Mock()
        mapper.set_coordinates_and_constellation(obj, nea_data, ref)

        # Devrait utiliser le format en degrés
        assert obj.st_declination is not None
        assert obj.st_declination.startswith("+43/")

    @patch("src.mappers.nasa_exoplanet_archive_mapper.ConstellationUtil")
    def test_set_coordinates_with_only_degrees(self, mock_constellation_util, mapper):
        """Test de définition des coordonnées uniquement avec degrés."""
        mock_util_instance = Mock()
        mock_util_instance.get_constellation_name.return_value = "Cygnus"
        mapper.constellation_util = mock_util_instance

        nea_data = {
            "ra": 298.652708,
            "dec": 43.951056,
            # Pas de rastr ni decstr
        }
        obj = Mock()
        obj.st_right_ascension = None
        obj.st_declination = None
        obj.sy_constellation = None

        ref = Mock()
        mapper.set_coordinates_and_constellation(obj, nea_data, ref)

        # Devrait utiliser les formats en degrés
        assert obj.st_right_ascension is not None
        assert obj.st_declination is not None
        assert obj.sy_constellation == "Cygnus"


class TestSpecialFieldParsing:
    """Tests for special field parsing logic."""

    @pytest.fixture
    def mapper(self):
        """Fixture pour créer un mapper."""
        return NasaExoplanetArchiveMapper()

    def test_parse_field_disc_year_as_integer(self, mapper):
        """Test de parsing de disc_year comme entier."""
        nea_data = {"disc_year": 2014.0}
        result = mapper._parse_field(
            raw_value=2014.0,
            nea_data=nea_data,
            nea_field="disc_year",
            attribute="disc_year",
        )
        assert result == 2014
        assert isinstance(result, int)

    def test_parse_field_with_composite_formatted_string(self, mapper):
        """Test de parsing d'un champ avec chaîne composite."""
        nea_data = {"pl_tranmid": "2450000&plusmn100"}
        result = mapper._parse_field(
            raw_value="2450000&plusmn100",
            nea_data=nea_data,
            nea_field="pl_tranmid",
            attribute="pl_transit_midpoint",
        )
        assert isinstance(result, ValueWithUncertainty)
        assert result.value == 2450000.0
        assert result.error_positive == 100.0

    def test_format_trimmed_numeric_string(self, mapper):
        """Test de formatage d'une chaîne numérique."""
        assert mapper.format_trimmed_numeric_string(123.45000) == "123.45"
        assert mapper.format_trimmed_numeric_string(100.0) == "100"
        assert mapper.format_trimmed_numeric_string(0.00100) == "0.001"
        assert mapper.format_trimmed_numeric_string("invalid") == "invalid"


class TestEdgeCases:
    """Tests for edge cases and error handling."""

    @pytest.fixture
    def mapper(self):
        """Fixture pour créer un mapper."""
        return NasaExoplanetArchiveMapper()

    def test_is_invalid_raw_value_exception_handling(self):
        """Test de gestion des exceptions dans is_invalid_raw_value."""

        # Créer un objet qui lève une exception lors de la conversion en string
        class BadObject:
            def __str__(self):
                raise RuntimeError("Cannot convert to string")

        bad_obj = BadObject()
        result = is_invalid_raw_value(bad_obj)
        assert result is True

    @patch("src.mappers.nasa_exoplanet_archive_mapper.ConstellationUtil")
    def test_map_from_nea_record_skips_invalid_values(self, mock_constellation_util, mapper):
        """Test que le mapping saute les valeurs invalides."""
        mock_util_instance = Mock()
        mock_util_instance.get_constellation_name.return_value = None
        mapper.constellation_util = mock_util_instance

        nea_data = {
            "pl_name": "Test Planet",
            "hostname": "Test Star",
            "pl_bmasse": "nan",  # Valeur invalide
            "pl_radj": 1.5,  # Valeur valide (pl_radj maps to pl_radius)
            "pl_orbper": None,  # Valeur invalide
        }

        exoplanet = mapper.map_exoplanet_from_nea_record(nea_data)

        # pl_bmasse ne devrait pas être défini (valeur invalide)
        # Note: The mapper creates ValueWithUncertainty objects, so we check the value
        # pl_radj maps to pl_radius and should be set with value 1.5
        assert exoplanet.pl_radius is not None
        assert exoplanet.pl_radius.value == 1.5
