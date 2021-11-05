import pytest

from rct229.schema.config_functions import get_pint_unit_registry
from rct229.schema.schema_utils import clean_schema_units, quantify_rmr

# Testing clean_schema_units()
def test__clean_schema_units__with_dash_in_numerator():
    assert clean_schema_units("hr-m2/W") == "(hr*m2)/W"


def test__clean_schema_units__with_dash_in_denominator():
    assert clean_schema_units("W/hr-m2") == "W/(hr*m2)"


def test__clean_schema_units__with_K_units():
    assert clean_schema_units("K") == "delta_degK"


def test__clean_schema_units__with_R_units():
    assert clean_schema_units("R") == "delta_degR"


def test__clean_schema_units__with_Kblah_units():
    assert clean_schema_units("Kblah") == "Kblah"


def test__clean_schema_units__with_blahK_units():
    assert clean_schema_units("blahK") == "blahK"


def test__clean_schema_units__with_C_units():
    assert clean_schema_units("C") == "degC"


def test__clean_schema_units__with_K_units():
    assert clean_schema_units("F") == "degF"


def test__clean_schema_units__with_Cblah_units():
    assert clean_schema_units("Cblah") == "Cblah"


def test__clean_schema_units__with_blahC_units():
    assert clean_schema_units("blahC") == "blahC"


# Testing quantify_rmr()
# TODO: Mock the schema to eliminate the dependency on ASHRAE 229
def test__quantify_rmr():
    ureg = get_pint_unit_registry()
    assert quantify_rmr(
        {"transformers": [{"id": 1, "name": "tranformer_1", "capacity": 500}]}
    ) == {
        "transformers": [
            {"id": 1, "name": "tranformer_1", "capacity": 500 * ureg("ampere * volt")}
        ]
    }
