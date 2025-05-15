from collections import deque

from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.ruleset_functions.get_swh_equipment_associated_with_each_swh_distriubtion_system import (
    get_swh_equipment_associated_with_each_swh_distribution_system,
)
from rct229.schema.config import ureg
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all, find_one_with_field_value
from rct229.utils.pint_utils import ZERO
from rct229.utils.utility_functions import find_exactly_one_service_water_heating_use

MIN_PUMP_POWER = 0.0 * ureg("Btu/hr")


class PRM9012019Rule62z26(RuleDefinitionListIndexedBase):
    """Rule 14 of ASHRAE 90.1-2019 Appendix G Section 11 (Service Water Heating)"""

    def __init__(self):
        super(PRM9012019Rule62z26, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=True
            ),
            each_rule=PRM9012019Rule62z26.RMDRule(),
            index_rmd=BASELINE_0,
            id="11-14",
            description=(
                "Where recirculation pumps are used to ensure prompt availability of service water-heating at the end use, "
                "the energy consumption of such pumps shall be calculated explicitly."
            ),
            ruleset_section_title="Service Water Heating",
            standard_section="Table G3.1 #11, baseline column, (f)",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0]",
        )

    class RMDRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(PRM9012019Rule62z26.RMDRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=True
                ),
                each_rule=PRM9012019Rule62z26.RMDRule.SWHDistributionRule(),
                index_rmd=BASELINE_0,
                list_path="$.service_water_heating_distribution_systems[*]",
            )

        def is_applicable(self, context, data=None):
            rmd_b = context.BASELINE_0
            rmd_p = context.PROPOSED

            swh_comps_dict_b = (
                get_swh_equipment_associated_with_each_swh_distribution_system(rmd_b)
            )

            swh_use_has_loads_p = all(
                [
                    find_exactly_one_service_water_heating_use(
                        rmd_p, swh_dist_sys_id_b
                    ).get("use", 0.0)
                    > 0.0
                    for swh_dist_id_b in find_all(
                        "$.service_water_heating_distribution_systems[*].id", rmd_b
                    )
                    for swh_dist_sys_id_b in swh_comps_dict_b[swh_dist_id_b].uses
                ]
            )

            return swh_use_has_loads_p

        def create_data(self, context, data):
            rmd_b = context.BASELINE_0

            swh_comps_dict_b = (
                get_swh_equipment_associated_with_each_swh_distribution_system(rmd_b)
            )

            piping_info_b = {}
            for swh_dist_sys_b in find_all(
                "$.service_water_heating_distribution_systems[*]", rmd_b
            ):
                service_water_piping = getattr_(
                    swh_dist_sys_b,
                    "service_water_heating_distribution_systems",
                    "service_water_piping",
                )
                if service_water_piping:
                    queue = deque([service_water_piping])
                    while queue:
                        current_piping = queue.popleft()
                        children_piping = current_piping.get("child", [])
                        queue.extend(children_piping)

                        current_piping_id = current_piping["id"]
                        if (
                            current_piping_id
                            in swh_comps_dict_b[swh_dist_sys_b["id"]].piping
                        ):
                            piping_info_b[current_piping_id] = {}
                            piping_info_b[current_piping_id][
                                "IS_RECIRC"
                            ] = current_piping.get("is_recirculation_loop")

                        piping_info_b[current_piping_id].setdefault(
                            "PUMP_POWER", ZERO.POWER
                        )
                        if piping_info_b[current_piping_id]["IS_RECIRC"]:
                            for pump_id in swh_comps_dict_b[swh_dist_sys_b["id"]].pumps:
                                pump = find_one_with_field_value(
                                    "$.pumps[*]",
                                    "id",
                                    pump_id,
                                    rmd_b,
                                )

                                piping_info_b[current_piping_id][
                                    "PUMP_POWER"
                                ] += pump.get("design_electric_power", ZERO.POWER)

            return {
                "swh_comps_dict_b": swh_comps_dict_b,
                "piping_info_b": piping_info_b,
            }

        class SWHDistributionRule(RuleDefinitionBase):
            def __init__(self):
                super(PRM9012019Rule62z26.RMDRule.SWHDistributionRule, self).__init__(
                    rmds_used=produce_ruleset_model_description(
                        USER=False, BASELINE_0=True, PROPOSED=True
                    ),
                )

            def manual_check_required(self, context, calc_vals=None, data=None):
                piping_info_b = data["piping_info_b"]

                return all(
                    not piping["IS_RECIRC"] or piping["PUMP_POWER"] > MIN_PUMP_POWER
                    for piping in piping_info_b.values()
                ) and not all(
                    [
                        piping["IS_RECIRC"] and piping["PUMP_POWER"] > MIN_PUMP_POWER
                        for piping in piping_info_b.values()
                    ]
                )

            def get_calc_vals(self, context, data=None):
                piping_info_b = data["piping_info_b"]

                return {"piping_info_b": piping_info_b}

            def rule_check(self, context, calc_vals=None, data=None):
                piping_info_b = calc_vals["piping_info_b"]

                return all(
                    [
                        piping["IS_RECIRC"] and piping["PUMP_POWER"] > MIN_PUMP_POWER
                        for piping in piping_info_b.values()
                    ]
                )
