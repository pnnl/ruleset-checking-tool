import pytest
from rct229.utils.pint_utils import UNIT_SYSTEM, CalcQ, calcq_to_q, calcq_to_str

from rct229.schema.config import ureg

FLOOR_AREA = 1 * ureg("ft2")


def test__calcq_to_q__with_quantity():
    assert calcq_to_q(FLOOR_AREA) == FLOOR_AREA


def test__calcq_to_q__with_calcq():
    assert calcq_to_q(CalcQ("area", FLOOR_AREA)) == FLOOR_AREA


def test__calcq_to_q__with_list():
    assert calcq_to_q([CalcQ("area", FLOOR_AREA)]) == [FLOOR_AREA]


def test__calcq_to_q__with_dict():
    assert calcq_to_q({"key": CalcQ("area", FLOOR_AREA)}) == {"key": FLOOR_AREA}


def test__CalcQ__to_str():
    assert CalcQ("area", FLOOR_AREA).to_str(UNIT_SYSTEM.IP) == "1 ft2"


def test__calcq_to_str__with_non_none_q():
    assert calcq_to_str(UNIT_SYSTEM.IP, {"key": CalcQ("area", FLOOR_AREA)}) == {
        "key": "1 ft2"
    }


def test__calcq_to_str__with_none_q():
    assert calcq_to_str(UNIT_SYSTEM.IP, {"key": CalcQ("area", None)}) == {"key": None}
