from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_baseline_system_types import (
    get_baseline_system_types,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_hw_loop_zone_list_w_area_dict import (
    get_hw_loop_zone_list_w_area,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_zone_conditioning_category_dict import (
    ZoneConditioningCategory as ZCC,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_zone_conditioning_category_dict import (
    get_zone_conditioning_category_dict,
)
from rct229.schema.config import ureg
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.assertions import getattr_
from rct229.utils.compare_standard_val import std_le
from rct229.utils.jsonpath_utils import find_all, find_exactly_one_with_field_value
from rct229.utils.pint_utils import ZERO, CalcQ
from rct229.utils.std_comparisons import std_equal

APPLICABLE_SYS_TYPES = [
    HVAC_SYS.SYS_1,
    HVAC_SYS.SYS_5,
    HVAC_SYS.SYS_7,
    HVAC_SYS.SYS_11_2,
    HVAC_SYS.SYS_12,
    HVAC_SYS.SYS_1A,
    HVAC_SYS.SYS_7A,
    HVAC_SYS.SYS_11_2A,
    HVAC_SYS.SYS_12A,
]

FLUID_LOOP = SchemaEnums.schema_enums["FluidLoopOptions"]
HEATING_LOOP_CONDITIONED_AREA_THRESHOLD = 15_000 * ureg("ft2")


class PRM9012019Rule34r52(RuleDefinitionListIndexedBase):
    """Rule 5 of ASHRAE 90.1-2019 Appendix G Section 21 (Hot water loop)"""

    def __init__(self):
        super(PRM9012019Rule34r52, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=PRM9012019Rule34r52.RulesetModelInstanceRule(),
            index_rmd=BASELINE_0,
            id="21-5",
            description="The baseline building design boiler plant shall be modeled as having a single boiler if the baseline building design plant serves a conditioned floor area of 15,000sq.ft. or less, and as having two equally sized boilers for plants serving more than 15,000sq.ft.",
            ruleset_section_title="HVAC - Water Side",
            standard_section="Section G3.1.3.2 Building System-Specific Modeling Requirements for the Baseline model",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0]",
            required_fields={
                "$.ruleset_model_descriptions[*]": ["weather"],
                "weather": ["climate_zone"],
            },
        )

    class RulesetModelInstanceRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012019Rule34r52.RulesetModelInstanceRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                precision={
                    "heating_loop_conditioned_zone_area": {
                        "precision": 1,
                        "unit": "ft2",
                    },
                    # add this as a workaround to avoid error
                    "boiler_capacity": {
                        "precision": 0.0001,
                        "unit": "Btu/hr",
                    },
                },
            )

        def is_applicable(self, context, data=None):
            rmd_b = context.BASELINE_0
            baseline_system_types_dict = get_baseline_system_types(rmd_b)
            # create a list containing all HVAC systems that are modeled in the rmd_b
            available_types_list = [
                hvac_type
                for hvac_type in baseline_system_types_dict
                if len(baseline_system_types_dict[hvac_type]) > 0
            ]
            return any(
                [
                    available_type in APPLICABLE_SYS_TYPES
                    for available_type in available_types_list
                ]
            )

        def get_calc_vals(self, context, data=None):
            rmd_b = context.BASELINE_0
            climate_zone = rmd_b["weather"]["climate_zone"]

            # get zone conditions from buildings
            zone_conditioning_category_dict = {}
            constructions = find_all("$.constructions[*]", rmd_b)
            for bldg in find_all("$.buildings[*]", rmd_b):
                zone_conditioning_category_dict = {
                    **zone_conditioning_category_dict,
                    **get_zone_conditioning_category_dict(
                        climate_zone, bldg, constructions
                    ),
                }

            loop_zone_list_w_area_dict = get_hw_loop_zone_list_w_area(rmd_b)

            # loop to boiler dict
            boiler_loop_ids = [
                getattr_(boiler, "boiler", "loop")
                for boiler in find_all("$.boilers[*]", rmd_b)
            ]

            # Initialize the variables
            # The heating_loop_conditioned_zone_area will include sum of all connected zones and indirectly zone areas.
            heating_loop_conditioned_zone_area = ZERO.AREA
            # The connected zones list, zones in this list can be residential, nonresidential, mixed or semi-heated
            loop_zone_list = []

            for fluid_loop in find_all("$.fluid_loops[*]", rmd_b):
                # Make sure heating loop, and its heating is supplied by a boiler(s)
                if (
                    getattr_(fluid_loop, "fluid_loops", "type") == FLUID_LOOP.HEATING
                    and fluid_loop["id"] in boiler_loop_ids
                ):
                    boiler_loop_id = fluid_loop["id"]
                    loop_zone_list.extend(
                        loop_zone_list_w_area_dict[boiler_loop_id]["zone_list"]
                    )
                    heating_loop_conditioned_zone_area += loop_zone_list_w_area_dict[
                        boiler_loop_id
                    ]["total_area"]

            # check indirectly conditioned zones, add them to the total area
            for zone_id in zone_conditioning_category_dict:
                if (
                    zone_conditioning_category_dict[zone_id]
                    in [
                        ZCC.CONDITIONED_MIXED,
                        ZCC.CONDITIONED_RESIDENTIAL,
                        ZCC.CONDITIONED_NON_RESIDENTIAL,
                    ]
                    and zone_id not in loop_zone_list
                ):
                    heating_loop_conditioned_zone_area += sum(
                        find_all(
                            "$..floor_area",
                            find_exactly_one_with_field_value(
                                "$..zones[*]", "id", zone_id, rmd_b
                            ),
                        ),
                        ZERO.AREA,
                    )

            num_boilers = len(find_all("$.boilers[*]", rmd_b))
            boiler_capacity_list = [
                CalcQ("capacity", getattr_(boiler, "boiler", "rated_capacity"))
                for boiler in find_all("$.boilers[*]", rmd_b)
            ]

            return {
                "heating_loop_conditioned_zone_area": heating_loop_conditioned_zone_area,
                "num_boilers": num_boilers,
                "boiler_capacity_list": boiler_capacity_list,
            }

        def rule_check(self, context, calc_vals=None, data=None):
            heating_loop_conditioned_zone_area = calc_vals[
                "heating_loop_conditioned_zone_area"
            ]
            num_boilers = calc_vals["num_boilers"]
            boiler_capacity_list = calc_vals["boiler_capacity_list"]
            return (
                (
                    heating_loop_conditioned_zone_area
                    < HEATING_LOOP_CONDITIONED_AREA_THRESHOLD
                    or self.precision_comparison["heating_loop_conditioned_zone_area"](
                        heating_loop_conditioned_zone_area,
                        HEATING_LOOP_CONDITIONED_AREA_THRESHOLD,
                    )
                )
                and num_boilers == 1
            ) or (
                heating_loop_conditioned_zone_area
                > HEATING_LOOP_CONDITIONED_AREA_THRESHOLD
                and num_boilers == 2
                and len(boiler_capacity_list) == 2
                and self.precision_comparison["boiler_capacity"](
                    boiler_capacity_list[0], boiler_capacity_list[1]
                )
            )

        def is_tolerance_fail(self, context, calc_vals=None, data=None):
            heating_loop_conditioned_zone_area = calc_vals[
                "heating_loop_conditioned_zone_area"
            ]
            num_boilers = calc_vals["num_boilers"]
            boiler_capacity_list = calc_vals["boiler_capacity_list"]
            return (
                (
                    std_le(
                        val=heating_loop_conditioned_zone_area,
                        std_val=HEATING_LOOP_CONDITIONED_AREA_THRESHOLD,
                    )
                )
                and num_boilers == 1
            ) or (
                heating_loop_conditioned_zone_area
                > HEATING_LOOP_CONDITIONED_AREA_THRESHOLD
                and num_boilers == 2
                and len(boiler_capacity_list) == 2
                and std_equal(boiler_capacity_list[0], boiler_capacity_list[1])
            )
