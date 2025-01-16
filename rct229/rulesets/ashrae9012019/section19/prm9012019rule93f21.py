from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.are_all_terminal_heating_loops_attached_to_boiler import (
    are_all_terminal_heating_loops_attached_to_boiler,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_cooling_type_fluid_loop import (
    is_hvac_sys_cooling_type_fluid_loop,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_fluid_loop_attached_to_boiler import (
    is_hvac_sys_fluid_loop_attached_to_boiler,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_fluid_loop_attached_to_chiller import (
    is_hvac_sys_fluid_loop_attached_to_chiller,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_heating_type_fluid_loop import (
    is_hvac_sys_heating_type_fluid_loop,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_preheat_fluid_loop_attached_to_boiler import (
    is_hvac_sys_preheat_fluid_loop_attached_to_boiler,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_preheating_type_fluid_loop import (
    is_hvac_sys_preheating_type_fluid_loop,
)
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all, find_one_with_field_value
from rct229.utils.utility_functions import (
    find_exactly_one_child_loop,
    find_exactly_one_hvac_system,
)

HEATING_SOURCE = SchemaEnums.schema_enums["HeatingSourceOptions"]
FLUID_LOOP = SchemaEnums.schema_enums["FluidLoopOptions"]


class PRM9012019Rule93f21(RuleDefinitionListIndexedBase):
    """Rule 2 of ASHRAE 90.1-2019 Appendix G Section 19 (HVAC - General)"""

    def __init__(self):
        super(PRM9012019Rule93f21, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=PRM9012019Rule93f21.FluidLoopRule(),
            index_rmd=BASELINE_0,
            id="19-2",
            description="Baseline building plant capacities shall be based on coincident loads.",
            ruleset_section_title="HVAC - General",
            standard_section="Section G3.1.2.2",
            is_primary_rule=True,
            rmd_context="ruleset_model_descriptions/0",
            list_path="$.fluid_loops[*]",
        )

    def create_data(self, context, data):
        rmd_b = context.BASELINE_0

        HW_fluid_loop_list = []
        CW_fluid_loop_list = []
        CHW_fluid_loop_list = []
        for hvac_b in find_all(
            "$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*]",
            rmd_b,
        ):
            hvac_id_b = hvac_b["id"]
            if is_hvac_sys_heating_type_fluid_loop(
                rmd_b, hvac_id_b
            ) and is_hvac_sys_fluid_loop_attached_to_boiler(rmd_b, hvac_id_b):
                HW_fluid_loop_list.append(
                    getattr_(
                        find_exactly_one_hvac_system(rmd_b, hvac_id_b),
                        "HVAC",
                        "heating_system",
                        "hot_water_loop",
                    )
                )

            if is_hvac_sys_preheating_type_fluid_loop(
                rmd_b, hvac_id_b
            ) and is_hvac_sys_preheat_fluid_loop_attached_to_boiler(rmd_b, hvac_id_b):
                HW_fluid_loop_list.append(
                    getattr_(
                        find_exactly_one_hvac_system(rmd_b, hvac_id_b),
                        "HVAC",
                        "preheat_system",
                        "hot_water_loop",
                    )
                )

            if is_hvac_sys_cooling_type_fluid_loop(
                rmd_b, hvac_id_b
            ) and is_hvac_sys_fluid_loop_attached_to_chiller(rmd_b, hvac_id_b):
                chilled_water_loop_b = getattr_(
                    find_exactly_one_hvac_system(rmd_b, hvac_id_b),
                    "HVAC",
                    "cooling_system",
                    "chilled_water_loop",
                )
                CHW_fluid_loop_list.append(chilled_water_loop_b)

                if chilled_water_loop_b in find_all(
                    f'$.fluid_loops[*][?(@.cooling_loop = "{FLUID_LOOP.COOLING}")]',
                    rmd_b,
                ):
                    chiller_b = find_one_with_field_value(
                        "$.chillers[*]",
                        "cooling_loop",
                        getattr_(
                            hvac_b, "HVAC", "cooling_system", "chilled_water_loop"
                        ),
                        rmd_b,
                    )

                else:
                    # when the fluid loop is the secondary loop, find the primary loop and add its id to the CHW_fluid_loop_list
                    # find out the primary loop from the secondary loop
                    child_loop_id_b = find_exactly_one_child_loop(
                        rmd_b, chilled_water_loop_b
                    )["id"]
                    primary_loop_id_b = find_one_with_field_value(
                        "$.fluid_loops[*]",
                        "child_loops[*].id",
                        child_loop_id_b,
                        rmd_b,
                    )["id"]
                    CHW_fluid_loop_list.append(primary_loop_id_b)

                    chiller_b = find_one_with_field_value(
                        "$.chillers[*]",
                        "cooling_loop",
                        primary_loop_id_b,
                        rmd_b,
                    )

                if chiller_b.get("condensing_loop"):
                    CW_fluid_loop_list.append(chiller_b["condensing_loop"])

        for CHW_child_loop in find_all(
            "$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*].cooling_system.chilled_water_loop",
            rmd_b,
        ):
            CHW_fluid_loop_list.append(CHW_child_loop)

        # extend `HW_fluid_loop_list` with terminals
        HW_fluid_loop_list.extend(
            [
                terminal["heating_from_loop"]
                for terminal in find_all(
                    "$.buildings[*].building_segments[*].zones[*].terminals[*]", rmd_b
                )
                if (
                    terminal.get("heating_source") == HEATING_SOURCE.HOT_WATER
                    and are_all_terminal_heating_loops_attached_to_boiler(
                        rmd_b, [terminal["id"]]
                    )
                )
            ]
        )

        return {
            "HW_fluid_loop_list": list(set(HW_fluid_loop_list)),
            "CHW_fluid_loop_list": list(set(CHW_fluid_loop_list)),
            "CW_fluid_loop_list": list(set(CW_fluid_loop_list)),
        }

    class FluidLoopRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012019Rule93f21.FluidLoopRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                required_fields={
                    "$": ["type"],
                },
            )

        def is_applicable(self, context, data=None):
            fluid_loop_b = context.BASELINE_0
            fluid_loop_id_b = fluid_loop_b["id"]

            HW_fluid_loop_list = data["HW_fluid_loop_list"]
            CHW_fluid_loop_list = data["CHW_fluid_loop_list"]
            CW_fluid_loop_list = data["CW_fluid_loop_list"]

            return fluid_loop_id_b in (
                HW_fluid_loop_list + CHW_fluid_loop_list + CW_fluid_loop_list
            )

        def get_calc_vals(self, context, data=None):
            fluid_loop_b = context.BASELINE_0
            HW_fluid_loop_list = data["HW_fluid_loop_list"]
            CHW_fluid_loop_list = data["CHW_fluid_loop_list"]
            CW_fluid_loop_list = data["CW_fluid_loop_list"]

            is_sized_using_coincident_load = False
            if (
                fluid_loop_b["type"] == FLUID_LOOP.COOLING
                and fluid_loop_b["id"] in CHW_fluid_loop_list
            ) or (
                fluid_loop_b["type"] == FLUID_LOOP.CONDENSER
                and fluid_loop_b["id"] in CW_fluid_loop_list
            ):
                is_sized_using_coincident_load = getattr_(
                    fluid_loop_b,
                    "Fluid Loop",
                    "cooling_or_condensing_design_and_control",
                    "is_sized_using_coincident_load",
                )
            elif (
                fluid_loop_b["type"] == FLUID_LOOP.HEATING
                and fluid_loop_b["id"] in HW_fluid_loop_list
            ):
                is_sized_using_coincident_load = getattr_(
                    fluid_loop_b,
                    "Fluid Loop",
                    "heating_design_and_control",
                    "is_sized_using_coincident_load",
                )

            return {"is_sized_using_coincident_load": is_sized_using_coincident_load}

        def rule_check(self, context, calc_vals=None, data=None):
            is_sized_using_coincident_load = calc_vals["is_sized_using_coincident_load"]

            return is_sized_using_coincident_load
