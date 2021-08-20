import os

import pytest
from numpy.testing import assert_approx_equal

from rct229.data_fns.table_G3_8_fns import (
    lighting_space_enumeration_to_lpd_space_type_map,
    table_G3_8_lpd,
)
from rct229.utils.json_utils import load_json

test_g38_path = os.path.join(
    os.path.dirname(__file__), "../data/ashrae_90_1_prm_2019.prm_interior_lighting.json"
)

osstd_prm_interior_lighting_list = load_json(test_g38_path)


def test_table_G3_8_lpd_automotive_facility():
    assert table_G3_8_lpd("AUTOMOTIVE_FACILITY") == 0.9


def test_table_G3_8_lpd_convention_center():
    assert table_G3_8_lpd("CONVENTION_CENTER") == 1.20


def test_table_G3_8_lpd_courthouse():
    assert table_G3_8_lpd("COURTHOUSE") == 1.20


def test_table_G3_8_lpd_workshop():
    assert table_G3_8_lpd("WORKSHOP") == 1.40


def test_table_G3_8_lpd_warehouse():
    assert table_G3_8_lpd("WAREHOUSE") == 0.80


def test_table_G3_8_lpd_courthouse():
    assert table_G3_8_lpd("COURTHOUSE") == 1.20
