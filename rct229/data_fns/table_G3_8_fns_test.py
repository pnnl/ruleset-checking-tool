import pytest
from numpy.testing import assert_approx_equal
from rct229.data_fns.table_G3_8_fns import (
    lighting_space_enumeration_to_lpd_space_type_map ,
)
from rct229.utils.json_utils import load_json

osstd_prm_interior_lighting_list = load_json(
    "../data/ashrae_90_1_prm_2019.prm_interior_lighting.json"
)


#def test__table_8_4_4_in_range__with_single_phase_low_value():
    #assert table_8_4_4_in_range(phase=SINGLE_PHASE, kVA=14) == False

def test_table_G3_8_lpd_automotive_facility():
    assert table_G3_8_lpd("automotive facility - whole building") == 0.9

def test_table_G3_8_lpd_convention_center():
    assert table_G3_8_lpd("convention center - whole building") == 1.20

def test_table_G3_8_lpd_courthouse():
    assert table_G3_8_lpd("courthouse - whole building") == 1.20

def test_table_G3_8_lpd_workshop():
    assert table_G3_8_lpd("workshop") == 1.40

def test_table_G3_8_lpd_warehouse():
    assert table_G3_8_lpd("warehouse - whole building") == 0.80

def test_table_G3_8_lpd_courthouse():
    assert table_G3_8_lpd("courthouse - whole building") == 1.20