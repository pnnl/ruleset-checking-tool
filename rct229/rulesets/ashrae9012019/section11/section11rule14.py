from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.ruleset_functions.get_swh_equipment_associated_with_each_swh_distriubtion_system import (
    get_swh_equipment_associated_with_each_swh_distribution_system,
)
from rct229.utils.jsonpath_utils import find_all, find_one_with_field_value


class Section11Rule14(RuleDefinitionListIndexedBase):
    """Rule 14 of ASHRAE 90.1-2019 Appendix G Section 11 (Service Water Heating)"""

    def __init__(self):
        super(Section11Rule14, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=True
            ),
            each_rule=Section11Rule14.RMDRule(),
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
            super(Section11Rule14.RMDRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=True
                ),
                each_rule=Section11Rule14.RMDRule.SWHDistributionRule(),
                index_rmd=BASELINE_0,
                list_path="$.service_water_heating_distribution_systems[*]",
            )

        def create_data(self, context, data):
            rmd_b = context.BASELINE_0

            swh_comps_dict_b = (
                get_swh_equipment_associated_with_each_swh_distribution_system(rmd_b)
            )

            piping_info_b = {}
            for swh_dist_sys_b in find_all(
                "$.service_water_heating_distribution_systems[*]", rmd_b
            ):
                for piping_id_b in swh_comps_dict_b[swh_dist_sys_b["id"]].piping:
                    piping = find_one_with_field_value(
                        "$.service_water_heating_distribution_systems[*].service_water_piping[*]",
                        "id",
                        piping_id_b,
                        rmd_b,
                    )
                    piping_id = piping["id"]
                    piping_info_b[piping_id] = {}
                    piping_info_b[piping_id]["IS_RECIRC"] = piping.get(
                        "is_recirculation_loop"
                    )

                    if piping_info_b[piping_id]["IS_RECIRC"]:
                        for pump_id in swh_comps_dict_b[swh_dist_sys_b["id"]].pumps:
                            pump = find_one_with_field_value(
                                "$.pumps[*]",
                                "id",
                                pump_id,
                                rmd_b,
                            )
                            piping_info_b[piping_id]["PUMP_POWER"] = pump.get(
                                "design_electric_power"
                            )

            return {
                "swh_comps_dict_b": swh_comps_dict_b,
                "piping_info_b": piping_info_b,
            }

        def is_applicable(self, context, data=None):
            rmd_b = context.BASELINE_0
            rmd_p = context.PROPOSED

            swh_comps_dict_b = data["swh_comps_dict_b"]

            swh_use_loads_p = all(
                [
                    True if swh_use_p.get("use", 0.0) > 0.0 else False
                    for swh_dist_id_b in find_all(
                        "$.service_water_heating_distribution_systems[*].id", rmd_b
                    )
                    for swh_dist_sys_id_b in swh_comps_dict_b[swh_dist_id_b].uses
                    for swh_use_p in find_all(
                        f'$.buildings[*].building_segments[*].zones[*].spaces[*].service_water_heating_uses[*][?(@.id="{swh_dist_sys_id_b}")].use',
                        rmd_p,
                    )
                ]
            )

            return swh_use_loads_p

        class SWHDistributionRule(RuleDefinitionBase):
            def __init__(self):
                super(Section11Rule14.RMDRule.SWHDistributionRule, self).__init__(
                    rmds_used=produce_ruleset_model_description(
                        USER=False, BASELINE_0=True, PROPOSED=True
                    ),
                )

            def manual_check_required(self, context, calc_vals=None, data=None):
                piping_info_b = data["piping_info_b"]

                return any(not piping["IS_RECIRC"] for piping in piping_info_b.values())

            def get_calc_vals(self, context, data=None):
                piping_info_b = data["piping_info_b"]

                return {"piping_info_b": piping_info_b}

            def rule_check(self, context, calc_vals=None, data=None):
                piping_info_b = calc_vals["piping_info_b"]

                return all(
                    piping["IS_RECIRC"] for piping in piping_info_b.values()
                ) and all(
                    piping["PUMP_POWER"] > 10 for piping in piping_info_b.values()
                )
