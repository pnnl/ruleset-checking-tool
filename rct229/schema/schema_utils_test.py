from rct229.schema.config_functions import get_pint_unit_registry
from rct229.schema.schema_utils import clean_schema_units, quantify_rmd
from rct229.schema.validate import schema_validate_rpd


# Testing clean_schema_units()
def test__clean_schema_units__with_dash_in_numerator():
    assert clean_schema_units("hr-m2/W") == "(hr*m2)/W"


def test__clean_schema_units__with_dash_in_denominator():
    assert clean_schema_units("W/hr-m2") == "W/(hr*m2)"


TEST_RMD = {
    "id": "229-01",
    "ruleset_model_descriptions": [
        {
            "id": "user_rmd",
            "type": "Enumerations2019ASHRAE901.schema.json#/definitions/RulesetModelOptions2019ASHRAE901",
            "transformers": [
                {
                    "id": "1",
                    "capacity": 500,
                }
            ],
            "type": "BASELINE_0",
        },
    ],
}


def test__TEST_RPD__is_valid():
    schema_validation_result = schema_validate_rpd(TEST_RMD)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"


# Testing quantify_rmd()
# TODO: Mock the schema to eliminate the dependency on ASHRAE 229
def test__quantify_rmd():
    ureg = get_pint_unit_registry()
    assert quantify_rmd(TEST_RMD) == {
        "id": "229-01",
        "ruleset_model_descriptions": [
            {
                "id": "user_rmd",
                "transformers": [
                    {
                        "id": "1",
                        "capacity": 500 * ureg("ampere * volt"),
                    }
                ],
                "type": "BASELINE_0",
            },
        ],
    }
