from rct229.data.schema_enums import schema_enums
from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.ruleset_functions.baseline_systems.baseline_system_util import HVAC_SYS
from rct229.ruleset_functions.get_baseline_system_types import get_baseline_system_types
from rct229.ruleset_functions.get_hw_loop_zone_list_w_area_dict import get_hw_loop_zone_list_w_area
from rct229.ruleset_functions.get_zone_conditioning_category_dict import (get_zone_conditioning_category_dict, ZoneConditioningCategory as ZCC)
from rct229.schema.config import ureg
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all, find_exactly_one_with_field_value
from rct229.utils.pint_utils import ZERO, pint_sum

APPLICABLE_SYS_TYPES = [
    HVAC_SYS.SYS_1,
    HVAC_SYS.SYS_5,
    HVAC_SYS.SYS_7,
    HVAC_SYS.SYS_11_2,
    HVAC_SYS.SYS_12,
    HVAC_SYS.SYS_1A,
    HVAC_SYS.SYS_7A,
    HVAC_SYS.SYS_11_2A,
    HVAC_SYS.SYS_12A
]

FLUID_LOOP = schema_enums["FluidLoopOptions"]
HEATING_LOOP_CONDITIONED_AREA_THRESHOLD = 15000 * ureg("ft2")


class Section21Rule5(RuleDefinitionListIndexedBase):
    """Rule 5 of ASHRAE 90.1-2019 Appendix G Section 21 (Hot water loop)"""
    def __init__(self):
        super(Section21Rule5, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            each_rule=Section21Rule5.RulesetModelInstanceRule(),
            index_rmr="baseline",
            id="21-5",
            description="The baseline building design boiler plant shall be modeled as having a single boiler if the baseline building design plant serves a conditioned floor area of 15,000sq.ft. or less, and as having two equally sized boilers for plants serving more than 15,000sq.ft.",
            list_path="ruleset_model_instances[*]",
            data_items={"climate_zone": ("baseline", "weather/climate_zone")},
        )

    class RulesetModelInstanceRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section21Rule5.RulesetModelInstanceRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
                each_rule=Section21Rule5.RulesetModelInstanceRule.BoilerLoop(),
                index_rmr="baseline",
                list_path="$fluid_loops[*]",
            )

        def is_applicable(self, context, data=None):
            rmi_b = context.baseline
            baseline_system_types_dict = get_baseline_system_types(rmi_b)
            # create a list contains all HVAC systems that are modeled in the rmi_b
            available_type_lists = [
                hvac_type
                for hvac_type in baseline_system_types_dict.keys()
                if len(baseline_system_types_dict[hvac_type]) > 0
            ]
            return any(
                [
                    available_type in APPLICABLE_SYS_TYPES
                    for available_type in available_type_lists
                ]
            )

        def create_data(self, context, data):
            rmi_b = context.baseline
            climate_zone = data["climate_zone"]
            # join multiple dicts as temp solution. zone_cond_cat function may upgrade to rmi level
            zone_conditioning_category_dict = {}
            for bldg in find_all("$buildings[*]", rmi_b):
                zone_conditioning_category_dict = {**zone_conditioning_category_dict, **get_zone_conditioning_category_dict(climate_zone, bldg)}
            loop_zone_list_w_area_dict = get_hw_loop_zone_list_w_area(rmi_b)
            # boiler to loop dict
            loop_attach_boiler_dict = {}
            for boiler in find_all("$boilers[*]", rmi_b):
                loop_id = getattr_(boiler, "boiler", "loop")
                if loop_id not in loop_attach_boiler_dict.keys():
                    loop_attach_boiler_dict[loop_id] = list()
                loop_attach_boiler_dict[loop_id].append(boiler["id"])
            # boiler capacity dict
            boiler_capacity_dict = {
                boiler["id"]: getattr_(boiler, "boiler", "rated_capacity")
                for boiler in find_all("$boilers[*]", rmi_b)
            }
            # calculate zone area map based on the zone's conditioning category
            zone_area_dict = {
                zone_id: pint_sum(find_all("$..floor_area", find_exactly_one_with_field_value("$..zones[*]", "id", zone_id, rmi_b)), ZERO.AREA)
                for zone_id in zone_conditioning_category_dict.keys()
                if zone_conditioning_category_dict[zone_id] in [ZCC.CONDITIONED_MIXED, ZCC.CONDITIONED_RESIDENTIAL, ZCC.CONDITIONED_NON_RESIDENTIAL]
            }
            return {
                **data,
                "zone_conditioning_category_dict": zone_conditioning_category_dict,
                "loop_zone_list_w_area_dict": loop_zone_list_w_area_dict,
                "loop_attach_boiler_dict": loop_attach_boiler_dict,
                "boiler_capacity_dict": boiler_capacity_dict,
                "zone_area_dict": zone_area_dict
            }

        def list_filter(self, context_item, data):
            fluid_loop = context_item.baseline
            loop_attach_boiler_dict = data["loop_attach_boiler_dict"]
            # Only applies to heating loop with boilers
            return getattr_(fluid_loop, "fluid_loop", "type") == FLUID_LOOP.HEATING and fluid_loop["id"] in loop_attach_boiler_dict.keys()

        class BoilerLoop(RuleDefinitionBase):
            def __init__(self):
                super(
                    Section21Rule5.RulesetModelInstanceRule.BoilerLoop,
                    self,
                ).__init__(
                    rmrs_used=UserBaselineProposedVals(False, True, False),
                )

            def get_calc_vals(self, context, data=None):
                boiler_loop = context.baseline
                boiler_loop_id = boiler_loop["id"]
                zone_conditioning_category_dict = data["zone_conditioning_category_dict"]
                loop_zone_list_w_area_dict = data["loop_zone_list_w_area_dict"]
                loop_attach_boiler_dict = data["loop_attach_boiler_dict"]
                boiler_capacity_dict = data["boiler_capacity_dict"]
                zone_area_dict = data["zone_area_dict"]

                loop_zone_list = loop_zone_list_w_area_dict[boiler_loop_id]["zone_list"]
                heating_loop_conditioned_zone_area = loop_zone_list_w_area_dict[boiler_loop_id]["zone_list"]

                # check indirectly conditioned zones, add them to the total area
                for zone_id in zone_conditioning_category_dict.keys():
                    if zone_conditioning_category_dict[zone_id] in [ZCC.CONDITIONED_MIXED, ZCC.CONDITIONED_RESIDENTIAL, ZCC.CONDITIONED_NON_RESIDENTIAL] and zone_id not in loop_zone_list:
                        heating_loop_conditioned_zone_area += zone_area_dict[zone_id]

                # check number of boilers attach to this loop
                num_boilers = len(loop_attach_boiler_dict[boiler_loop_id])
                boiler_capacity_list = [boiler_capacity_dict[boiler_id] for boiler_id in boiler_capacity_dict.keys() if boiler_id in loop_attach_boiler_dict[boiler_loop_id]]

                return {
                    "heating_loop_conditioned_zone_area": heating_loop_conditioned_zone_area,
                    "num_boilers": num_boilers,
                    "boiler_capacity_list": boiler_capacity_list
                }

            def rule_check(self, context, calc_vals=None, data=None):
                heating_loop_conditioned_zone_area = calc_vals["heating_loop_conditioned_zone_area"]
                num_boilers = calc_vals["num_boilers"]
                boiler_capacity_list = calc_vals["boiler_capacity_list"]
                return{
                    heating_loop_conditioned_zone_area <= HEATING_LOOP_CONDITIONED_AREA_THRESHOLD and num_boilers == 1
                    or
                    num_boilers == 2 and len(boiler_capacity_list) == 2 and boiler_capacity_list[0] == boiler_capacity_list[1]
                }
