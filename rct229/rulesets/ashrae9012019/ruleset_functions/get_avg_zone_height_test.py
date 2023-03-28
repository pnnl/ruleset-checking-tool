from rct229.rulesets.ashrae9012019.ruleset_functions.get_avg_zone_height import (
    get_avg_zone_height,
)
from rct229.schema.config import ureg

# Constants
M = ureg("m")
M2 = M * M
M3 = M * M * M

TEST_ZONE = {
    "id": "zone_1",
    "spaces": [
        {"id": "surf_1", "floor_area": 10 * M2},
        {"id": "surf_2"},
    ],
    "volume": 50 * M3,
}


def test__get_avg_zone_height():
    assert get_avg_zone_height(TEST_ZONE) == 5 * M
