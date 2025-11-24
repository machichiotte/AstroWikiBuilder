from src.models.entities.exoplanet_entity import Exoplanet, ValueWithUncertainty
from src.models.entities.star_entity import Star
from src.utils.astro.classification.star_type_util import StarTypeUtil


class TestStarTypeUtil:
    def test_extract_spectral_components_simple(self):
        result = StarTypeUtil.extract_spectral_components_from_string("G2V")
        assert result.spectral_class == "G"
        assert result.subtype == "2"
        assert result.luminosity_class == "V"

    def test_extract_spectral_components_with_noise(self):
        result = StarTypeUtil.extract_spectral_components_from_string("K5Vvar")
        assert result.spectral_class == "K"
        assert result.subtype == "5"
        assert result.luminosity_class == "V"

    def test_extract_spectral_components_invalid(self):
        result = StarTypeUtil.extract_spectral_components_from_string("Invalid")
        assert result.spectral_class is None
        assert result.subtype is None
        assert result.luminosity_class is None

    def test_extract_luminosity_class_from_star(self):
        star = Star(st_name="Test Star", st_spectral_type="G2V")
        result = StarTypeUtil.extract_luminosity_class_from_star(star)
        assert result == "V"

    def test_extract_luminosity_class_from_star_no_spectral_type(self):
        star = Star(st_name="Test Star")
        result = StarTypeUtil.extract_luminosity_class_from_star(star)
        assert result is None

    def test_extract_spectral_class_from_star(self):
        star = Star(st_name="Test Star", st_spectral_type="K5III")
        result = StarTypeUtil.extract_spectral_class_from_star(star)
        assert result == "K"

    def test_get_temperature_range_for_spectral_class(self):
        result = StarTypeUtil.get_temperature_range_for_spectral_class("G")
        assert result == (5200, 6000)

    def test_get_temperature_range_for_unknown_class(self):
        result = StarTypeUtil.get_temperature_range_for_spectral_class("X")
        assert result == (0, 0)

    def test_determine_star_types_from_properties_no_spectral_type(self):
        exoplanet = Exoplanet(pl_name="Test", st_spectral_type=None)
        result = StarTypeUtil.determine_star_types_from_properties(exoplanet)
        assert result == []

    def test_determine_star_types_from_properties_basic(self):
        exoplanet = Exoplanet(pl_name="Test", st_spectral_type="G2V")
        result = StarTypeUtil.determine_star_types_from_properties(exoplanet)
        assert len(result) > 0
        assert any("G" in r for r in result)

    def test_get_neutron_star_type(self):
        exoplanet = Exoplanet(pl_name="Test")
        exoplanet.st_mass = ValueWithUncertainty(value=2.0)
        exoplanet.st_radius = ValueWithUncertainty(value=0.005)
        result = StarTypeUtil._get_neutron_star_type(exoplanet)
        assert result == ["Étoile à neutrons"]

    def test_get_neutron_star_type_invalid_values(self):
        exoplanet = Exoplanet(pl_name="Test")
        exoplanet.st_mass = ValueWithUncertainty(value="invalid")
        exoplanet.st_radius = ValueWithUncertainty(value=0.005)
        result = StarTypeUtil._get_neutron_star_type(exoplanet)
        assert result == []

    def test_get_variability_type(self):
        exoplanet = Exoplanet(pl_name="Test")
        exoplanet.st_variability = ValueWithUncertainty(value="Cepheid")
        result = StarTypeUtil._get_variability_type(exoplanet)
        assert result == ["Étoile variable de type Cepheid"]

    def test_get_metallicity_type_poor(self):
        exoplanet = Exoplanet(pl_name="Test")
        exoplanet.st_metallicity = ValueWithUncertainty(value=-1.5)
        result = StarTypeUtil._get_metallicity_type(exoplanet)
        assert result == ["Étoile pauvre en métaux"]

    def test_get_metallicity_type_rich(self):
        exoplanet = Exoplanet(pl_name="Test")
        exoplanet.st_metallicity = ValueWithUncertainty(value=0.6)
        result = StarTypeUtil._get_metallicity_type(exoplanet)
        assert result == ["Étoile riche en métaux"]

    def test_get_metallicity_type_invalid(self):
        exoplanet = Exoplanet(pl_name="Test")
        exoplanet.st_metallicity = ValueWithUncertainty(value="invalid")
        result = StarTypeUtil._get_metallicity_type(exoplanet)
        assert result == []

    def test_get_raw_spectral_type_full(self):
        result = StarTypeUtil._get_raw_spectral_type("G", "2", "V")
        assert result == ["Étoile de type spectral G2V"]

    def test_get_raw_spectral_type_no_subtype(self):
        result = StarTypeUtil._get_raw_spectral_type("K", None, "III")
        assert result == ["Étoile de type spectral KIII"]

    def test_infer_evolutionary_stage_from_spectral_data_no_luminosity(self):
        result = StarTypeUtil.infer_evolutionary_stage_from_spectral_data("G", None)
        assert result is None

    def test_infer_evolutionary_stage_from_spectral_data_white_dwarf(self):
        result = StarTypeUtil.infer_evolutionary_stage_from_spectral_data("DA", "VII")
        assert result is not None

    def test_infer_evolutionary_stage_from_spectral_class_white_dwarf(self):
        result = StarTypeUtil.infer_evolutionary_stage_from_spectral_class("DA")
        assert result == "Naine blanche"

    def test_infer_evolutionary_stage_from_spectral_class_brown_dwarf(self):
        result = StarTypeUtil.infer_evolutionary_stage_from_spectral_class("L5")
        assert result == "Naine brune"

    def test_infer_evolutionary_stage_from_spectral_class_wolf_rayet(self):
        result = StarTypeUtil.infer_evolutionary_stage_from_spectral_class("WN")
        assert result == "Étoile Wolf-Rayet"

    def test_infer_evolutionary_stage_from_spectral_class_s_type(self):
        result = StarTypeUtil.infer_evolutionary_stage_from_spectral_class("S5")
        assert result == "Étoile de type spectral S"

    def test_infer_evolutionary_stage_from_spectral_class_c_type(self):
        result = StarTypeUtil.infer_evolutionary_stage_from_spectral_class("C5")
        assert result == "Étoile de type spectral C"
