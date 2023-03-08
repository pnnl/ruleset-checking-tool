from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_system_type_compare import (
    baseline_system_type_compare,
)

from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_heating_type_furnace import (
    is_hvac_sys_heating_type_furnace,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_heating_type_heat_pump import (
    is_hvac_sys_heating_type_heat_pump,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_cooling_type_DX import (
    is_hvac_sys_cooling_type_dx,
)
from rct229.utils.assertions import getattr_
from rct229.utils.pint_utils import CalcQ
from rct229.utils.std_comparisons import std_equal

REQ_HEATING_OVERSIZING_FACTOR = 0.25
REQ_COOLING_OVERSIZING_FACTOR = 0.15


class Section19Rule1(RuleDefinitionListIndexedBase):
    """Rule 1 of ASHRAE 90.1-2019 Appendix G Section 19 (HVAC - General)"""

    def __init__(self):
        super(Section19Rule1, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            each_rule=Section19Rule1.HVACRule(),
            index_rmr="baseline",
            id="19-1",
            description="HVAC system coil capacities for the baseline building design shall be oversized by 15% for cooling and 25% for heating.",
            ruleset_section_title="HVAC - General",
            standard_section=" Section G3.1.2.2",
            is_primary_rule=True,
            rmr_context="ruleset_model_instances/0",
            list_path="$..heating_ventilating_air_conditioning_systems[*]",
        )

    def is_applicable(self, context, data=None):
        rmi_b = context.baseline
        hvac_id = rmi_b["heating_ventilating_air_conditioning_systems"]["id"]

        return (
            is_hvac_sys_heating_type_furnace(rmi_b, hvac_id)
            or is_hvac_sys_heating_type_heat_pump(rmi_b, hvac_id)
            or is_hvac_sys_cooling_type_dx(rmi_b, hvac_id)
        )

    # def create_data(self, context, data):
    #     rmi_b = context.baseline
    #     baseline_system_types_dict = get_baseline_system_types(rmi_b)
    #     applicable_hvac_sys_ids = [
    #         hvac_id
    #         for sys_type in baseline_system_types_dict.keys()
    #         for target_sys_type in APPLICABLE_SYS_TYPES
    #         if baseline_system_type_compare(sys_type, target_sys_type, False)
    #         for hvac_id in baseline_system_types_dict[sys_type]
    #     ]
    #
    #     return {"applicable_hvac_sys_ids": applicable_hvac_sys_ids}

    class HVACRule(RuleDefinitionBase):
        def __init__(self):
            super(Section19Rule1.HVACRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
            )

        def get_calc_vals(self, context, data=None):
            hvac_b = context.baseline
            hvac_id_b = hvac_b["id"]

            heating_oversizing_factor = 0.0
            cooling_oversizing_factor = 0.0
            heating_is_autosized = False
            cooling_is_autosized = False
            heating_oversizing_applicable = True
            cooling_oversizing_applicable = True
            if is_hvac_sys_heating_type_furnace(
                hvac_b, hvac_id_b
            ) or is_hvac_sys_heating_type_heat_pump(hvac_b, hvac_id_b):
                heating_oversizing_factor = getattr_(
                    hvac_b, "oversizing_factor", "heating_system", "oversizing_factor"
                )
                heating_is_autosized = getattr_(
                    hvac_b, "is_autosized", "heating_system", "is_autosized"
                )
            else:
                heating_oversizing_applicable = False

            if is_hvac_sys_cooling_type_dx(hvac_b, hvac_id_b):
                cooling_oversizing_factor = getattr_(
                    hvac_b, "oversizing_factor", "cooling_system", "oversizing_factor"
                )
                cooling_is_autosized = getattr_(
                    hvac_b, "is_autosized", "cooling_system", "is_autosized"
                )
            else:
                cooling_oversizing_applicable = False

            return {
                "heating_oversizing_factor": heating_oversizing_factor,
                "cooling_oversizing_factor": cooling_oversizing_factor,
                "heating_is_autosized": heating_is_autosized,
                "cooling_is_autosized": cooling_is_autosized,
                "heating_oversizing_applicable": heating_oversizing_applicable,
                "cooling_oversizing_applicable": cooling_oversizing_applicable,
            }

        def rule_check(self, context, calc_vals=None, data=None):
            heating_oversizing_factor = calc_vals["heating_oversizing_factor"]
            cooling_oversizing_factor = calc_vals["cooling_oversizing_factor"]
            heating_is_autosized = calc_vals["heating_is_autosized"]
            cooling_is_autosized = calc_vals["cooling_is_autosized"]
            heating_oversizing_applicable = calc_vals["heating_oversizing_applicable"]
            cooling_oversizing_applicable = calc_vals["cooling_oversizing_applicable"]

            return (
                (
                    std_equal(REQ_HEATING_OVERSIZING_FACTOR, heating_oversizing_factor)
                    and std_equal(
                        REQ_COOLING_OVERSIZING_FACTOR, cooling_oversizing_factor
                    )
                    and heating_is_autosized
                    and cooling_is_autosized
                )
                or (
                    std_equal(REQ_HEATING_OVERSIZING_FACTOR, heating_oversizing_factor)
                    and heating_is_autosized
                    and not cooling_oversizing_applicable
                )
                or (
                    std_equal(REQ_COOLING_OVERSIZING_FACTOR, cooling_oversizing_factor)
                    and cooling_is_autosized
                    and not heating_oversizing_applicable
                )
            )
