from rct229.ruleset_functions.baseline_systems.baseline_hvac_test_util import (
    load_system_test_file,
)
from rct229.ruleset_functions.baseline_systems.baseline_system_util import HVAC_SYS
from rct229.ruleset_functions.baseline_systems.is_baseline_system_12 import (
    is_baseline_system_12,
)
from rct229.schema.validate import schema_validate_rmr

SYS_12_TEST_RMD = {}



def test__TEST_RMD_baseline_system_12__is_valid():
    schema_validation_result = schema_validate_rmr(SYS_12_TEST_RMD)
    assert schema_validation_result[
        "passed"
    ], f"Schema error: {schema_validation_result['error']}"