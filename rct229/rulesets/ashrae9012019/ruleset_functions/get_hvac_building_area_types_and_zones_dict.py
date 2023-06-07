from rct229.utils.assertions import getattr_, assert_
from rct229.utils.jsonpath_utils import find_all, find_one
from rct229.utils.pint_utils import ZERO


class ClassificationSource:
    BUILDING_SEGMENT_HVAC_BAT = "BUILDING_SEGMENT_HVAC_BAT"
    BUILDING_SEGMENT_LIGHTING = "BUILDING-SEGMENT_LIGHTING"
    SPACE_LIGHTING = "SPACE_LIGHTING"


def get_hvac_building_area_types_and_zones_dict(rmi):
    building_area_types_with_total_area_and_zones_dict = {}
    for building_segment in find_all("$.buildings[*].building_segments[*]", rmi):
        if building_segment.get("area_type_heating_ventilating_air_conditioning_system"):
            building_segment_hvac_bat = building_segment["area_type_heating_ventilating_air_conditioning_system"]
            classification_source = ClassificationSource.BUILDING_SEGMENT_HVAC_BAT
        elif building_segment.get("lighting_building_area_type"):
            building_segment_hvac_bat = building_segment["lighting_building_area_type"]
            classification_source = ClassificationSource.BUILDING_SEGMENT_LIGHTING
        else:
            building_segment_space_types_areas_dict = {}
            for space in find_all("$.zones[*].spaces[*]", building_segment):
                space_hvac_bat = space.get("lighting_space_type")
                if space_hvac_bat:
                    building_segment_space_types_areas_dict[space_hvac_bat] = building_area_types_with_total_area_and_zones_dict.get(space_hvac_bat, ZERO.AREA) + space.get("floor_area", ZERO.AREA)
            # Raise assertion if no space type matched from data.
            assert_(building_segment_space_types_areas_dict, f"Building segment: {building_segment['id']} is missing one of the three data: area_type_heating_ventilating_air_conditioning_system, lighting_building_area_type and the lighting_space_type in the spaces.")
            building_segment_hvac_bat = max(building_segment_space_types_areas_dict,
                                            key=building_segment_space_types_areas_dict.get)
            classification_source = ClassificationSource.SPACE_LIGHTING

        if building_segment_hvac_bat not in building_area_types_with_total_area_and_zones_dict:
            building_area_types_with_total_area_and_zones_dict[building_segment_hvac_bat] = {"zone_id": [], "floor_area": ZERO.AREA, classification_source: classification_source}


