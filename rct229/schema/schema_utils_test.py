import pytest
from rct229.schema.config_functions import get_pint_unit_registry
from rct229.schema.schema_utils import quantitize_rmr


# Testing quantitize_rmr
# TODO: Mock the schema to eliminate the dependency on ASHRAE 229
def test__quantitize_rmr():
    ureg = get_pint_unit_registry()
    assert quantitize_rmr(
        {"transformers": [{"id": 1, "name": "tranformer_1", "capacity": 500}]}
    ) == {
        "transformers": [
            {"id": 1, "name": "tranformer_1", "capacity": 500 * ureg("ampere * volt")}
        ]
    }
