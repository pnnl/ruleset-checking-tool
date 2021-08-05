import pytest
from numpy.testing import assert_approx_equal
from rct229.data_fns.table_G3_7_fns import (
    LightingSpaceType2019ASHRAE901TG37_to_lpd_space_type_map,
)
from rct229.utils.json_utils import load_json

osstd_prm_interior_lighting_list = load_json(
    "../data/ashrae_90_1_prm_2019.prm_hvac_bldg_type.json"
)


def test__table_8_4_4_in_range__with_single_phase_low_value():
    assert table_8_4_4_in_range(phase=SINGLE_PHASE, kVA=14) == False
