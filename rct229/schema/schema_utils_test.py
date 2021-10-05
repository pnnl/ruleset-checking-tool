import pytest

from rct229.schema.config_functions import get_pint_unit_registry
from rct229.schema.schema_utils import quantify_rmr


# Testing quantify_rmr
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
