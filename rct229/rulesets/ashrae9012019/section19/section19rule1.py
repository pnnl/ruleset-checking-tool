from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_instance
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_cooling_type_DX import (
    is_hvac_sys_cooling_type_dx,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_heating_type_furnace import (
    is_hvac_sys_heating_type_furnace,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_heating_type_heat_pump import (
    is_hvac_sys_heating_type_heat_pump,
)
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all

REQ_HEATING_OVERSIZING_FACTOR = 0.25
REQ_COOLING_OVERSIZING_FACTOR = 0.15


class Section19Rule1(RuleDefinitionListIndexedBase):
    """Rule 1 of ASHRAE 90.1-2019 Appendix G Section 19 (HVAC - General)"""

    def __init__(self):
        super(Section19Rule1, self).__init__(
            rmrs_used=produce_ruleset_model_instance(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=Section19Rule1.HVACRule(),
            index_rmr=BASELINE_0,
            id="19-1",
            description="HVAC system coil capacities for the baseline building design shall be oversized by 15% for cooling and 25% for heating.",
            ruleset_section_title="HVAC - General",
            standard_section="Section G3.1.2.2",
            is_primary_rule=True,
            rmr_context="ruleset_model_descriptions/0",
            list_path="$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*]",
        )

    def create_data(self, context, data):
        rmi_b = context.BASELINE_0

        hvac_id_to_flags = {
            hvac_id: {
                "is_hvac_sys_heating_type_furnace_flag": is_hvac_sys_heating_type_furnace(
                    rmi_b, hvac_id
                ),
                "is_hvac_sys_heating_type_heat_pump_flag": is_hvac_sys_heating_type_heat_pump(
                    rmi_b, hvac_id
                ),
                "is_hvac_sys_cooling_type_dx_flag": is_hvac_sys_cooling_type_dx(
                    rmi_b, hvac_id
                ),
            }
            for hvac_id in find_all(
                "$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*].id",
                rmi_b,
            )
        }

        return {"hvac_id_to_flags": hvac_id_to_flags}

    class HVACRule(RuleDefinitionBase):
        def __init__(self):
            super(Section19Rule1.HVACRule, self).__init__(
                rmrs_used=produce_ruleset_model_instance(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
            )

        def is_applicable(self, context, data=None):
            hvac_b = context.BASELINE_0
            hvac_id_b = hvac_b["id"]
            hvac_id_to_flags = data["hvac_id_to_flags"]

            return (
                hvac_id_to_flags[hvac_id_b]["is_hvac_sys_heating_type_furnace_flag"]
                or hvac_id_to_flags[hvac_id_b][
                    "is_hvac_sys_heating_type_heat_pump_flag"
                ]
                or hvac_id_to_flags[hvac_id_b]["is_hvac_sys_cooling_type_dx_flag"]
            )

        def get_calc_vals(self, context, data=None):
            hvac_b = context.BASELINE_0
            hvac_id_b = hvac_b["id"]

            is_hvac_sys_heating_type_furnace_flag = data["hvac_id_to_flags"][hvac_id_b][
                "is_hvac_sys_heating_type_furnace_flag"
            ]
            is_hvac_sys_heating_type_heat_pump_flag = data["hvac_id_to_flags"][
                hvac_id_b
            ]["is_hvac_sys_heating_type_heat_pump_flag"]
            is_hvac_sys_cooling_type_dx_flag = data["hvac_id_to_flags"][hvac_id_b][
                "is_hvac_sys_cooling_type_dx_flag"
            ]

            heating_oversizing_factor = 0.0
            cooling_oversizing_factor = 0.0
            heating_is_sized_based_on_design_day = False
            cooling_is_sized_based_on_design_day = False
            heating_oversizing_applicable = True
            cooling_oversizing_applicable = True
            if (
                is_hvac_sys_heating_type_furnace_flag
                or is_hvac_sys_heating_type_heat_pump_flag
            ):
                heating_oversizing_factor = getattr_(
                    hvac_b, "oversizing_factor", "heating_system", "oversizing_factor"
                )
                heating_is_sized_based_on_design_day = getattr_(
                    hvac_b,
                    "is_sized_based_on_design_day",
                    "heating_system",
                    "is_sized_based_on_design_day",
                )
            else:
                heating_oversizing_applicable = False

            if is_hvac_sys_cooling_type_dx_flag:
                cooling_oversizing_factor = getattr_(
                    hvac_b, "oversizing_factor", "cooling_system", "oversizing_factor"
                )
                cooling_is_sized_based_on_design_day = getattr_(
                    hvac_b,
                    "is_sized_based_on_design_day",
                    "cooling_system",
                    "is_sized_based_on_design_day",
                )
            else:
                cooling_oversizing_applicable = False

            return {
                "heating_oversizing_factor": heating_oversizing_factor,
                "cooling_oversizing_factor": cooling_oversizing_factor,
                "heating_is_sized_based_on_design_day": heating_is_sized_based_on_design_day,
                "cooling_is_sized_based_on_design_day": cooling_is_sized_based_on_design_day,
                "heating_oversizing_applicable": heating_oversizing_applicable,
                "cooling_oversizing_applicable": cooling_oversizing_applicable,
            }

        def rule_check(self, context, calc_vals=None, data=None):
            heating_oversizing_factor = calc_vals["heating_oversizing_factor"]
            cooling_oversizing_factor = calc_vals["cooling_oversizing_factor"]
            heating_is_sized_based_on_design_day = calc_vals[
                "heating_is_sized_based_on_design_day"
            ]
            cooling_is_sized_based_on_design_day = calc_vals[
                "cooling_is_sized_based_on_design_day"
            ]
            heating_oversizing_applicable = calc_vals["heating_oversizing_applicable"]
            cooling_oversizing_applicable = calc_vals["cooling_oversizing_applicable"]

            return (
                (
                    REQ_HEATING_OVERSIZING_FACTOR == heating_oversizing_factor
                    and REQ_COOLING_OVERSIZING_FACTOR == cooling_oversizing_factor
                    and heating_is_sized_based_on_design_day
                    and cooling_is_sized_based_on_design_day
                )
                or (
                    REQ_HEATING_OVERSIZING_FACTOR == heating_oversizing_factor
                    and heating_is_sized_based_on_design_day
                    and not cooling_oversizing_applicable
                )
                or (
                    REQ_COOLING_OVERSIZING_FACTOR == cooling_oversizing_factor
                    and cooling_is_sized_based_on_design_day
                    and not heating_oversizing_applicable
                )
            )
