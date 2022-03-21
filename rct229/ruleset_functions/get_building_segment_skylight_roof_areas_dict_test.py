import pytest

from rct229.ruleset_functions.get_building_segment_skylight_roof_areas_dict import (
    get_building_segment_skylight_roof_areas_dict,
)
from rct229.ruleset_functions.get_zone_conditioning_category_dict_test import (
    CLIMATE_ZONE,
    TEST_BUILDING,
)


def test__get_building_segment_skylight_roof_areas_dict():
    assert (
        get_building_segment_skylight_roof_areas_dict(CLIMATE_ZONE, TEST_BUILDING) == {}
    )


get_building_segment_skylight_roof_areas_dict(CLIMATE_ZONE, TEST_BUILDING)
