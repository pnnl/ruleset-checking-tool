from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.ruleset_functions.compare_swh_dist_systems_and_components import (
    compare_swh_dist_systems_and_components,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_swh_equipment_associated_with_each_swh_distriubtion_system import (
    get_swh_equipment_associated_with_each_swh_distribution_system,
)
from rct229.utils.jsonpath_utils import find_all


class PRM9012019Rule72v93(RuleDefinitionListIndexedBase):
    """Rule 1 of ASHRAE 90.1-2019 Appendix G Section 11 (Service Water Heating)"""

    def __init__(self):
        super(PRM9012019Rule72v93, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=True, BASELINE_0=True, PROPOSED=True
            ),
            each_rule=PRM9012019Rule72v93.RMDRule(),
            index_rmd=BASELINE_0,
            id="11-1",
            description="Where a complete service water-heating system exists, the proposed design shall reflect the actual system type."
            "Where a service water-heating system has been designed the service waterheating type shall be consistent with design documents. "
            "Where no service water-heating system exists or has been designed and submitted with design documents but the building will have service water-heating loads,"
            "a service water-heating system shall be modeled that matches the system type in the baseline building design",
            ruleset_section_title="Service Water Heating",
            standard_section="Table G3.1 #11, proposed column, a & b",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0]",
        )

    class RMDRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012019Rule72v93.RMDRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=True, BASELINE_0=True, PROPOSED=True
                ),
            )

        def get_calc_vals(self, context, data=None):
            rmd_u = context.USER
            rmd_b = context.BASELINE_0
            rmd_p = context.PROPOSED

            swh_and_equip_dict_b = (
                get_swh_equipment_associated_with_each_swh_distribution_system(rmd_b)
            )
            swh_and_equip_dict_p = (
                get_swh_equipment_associated_with_each_swh_distribution_system(rmd_p)
            )

            proposed_user_comparison = []
            proposed_baseline_comparison = []
            swh_dist_systems_u = find_all(
                "$.service_water_heating_distribution_systems[*].id", rmd_u
            )
            for swh_dist_sys_id_u in swh_dist_systems_u:
                # has distribution system
                swh_use_load_u = sum(
                    [
                        swh_use_u.get("use", 0.0)
                        for swh_use_u in find_all(
                            f'$.service_water_heating_uses[*][?(@.served_by_distribution_system="{swh_dist_sys_id_u}")]',
                            rmd_u,
                        )
                    ]
                )

                if swh_use_load_u > 0.0:
                    # has loads
                    proposed_user_comparison = compare_swh_dist_systems_and_components(
                        rmd1=rmd_p,
                        rmd2=rmd_u,
                        compare_context_str="AppG 11-1 P_RMD Equals U_RMD",
                        swh_distribution_id=swh_dist_sys_id_u,
                    )
                    proposed_baseline_comparison = (
                        compare_swh_dist_systems_and_components(
                            rmd1=rmd_p,
                            rmd2=rmd_b,
                            compare_context_str="AppG 11-1 P_RMD Equals B_RMD",
                            swh_distribution_id=swh_dist_sys_id_u,
                        )
                    )
                else:
                    # no loads
                    proposed_baseline_comparison = (
                        compare_swh_dist_systems_and_components(
                            rmd1=rmd_p,
                            rmd2=rmd_b,
                            compare_context_str="AppG 11-1 P_RMD Equals B_RMD",
                            swh_distribution_id=swh_dist_sys_id_u,
                        )
                    )

                    if (
                        swh_dist_sys_id_u not in swh_and_equip_dict_p
                        and swh_dist_sys_id_u in swh_and_equip_dict_b
                    ):
                        proposed_baseline_comparison.append(
                            f"'{swh_dist_sys_id_u}' was not found in the Proposed model. Because there are no SWH loads in the User model, "
                            f"we are expecting the Proposed and Baseline systems to match."
                        )

                    if (
                        swh_dist_sys_id_u not in swh_and_equip_dict_b
                        and swh_dist_sys_id_u in swh_and_equip_dict_p
                    ):
                        proposed_baseline_comparison.append(
                            f"'{swh_dist_sys_id_u}' was not found in the Baseline model. Because there are no SWH loads in the User model, "
                            f"we are expecting the Proposed and Baseline systems to match."
                        )

            if not swh_dist_systems_u:
                # if no distribution systems in user model
                swh_dist_systems_p = find_all(
                    "$.service_water_heating_distribution_systems[*].id", rmd_p
                )
                if swh_dist_systems_p:
                    # propose has distribution system
                    for swh_dist_sys_id_p in swh_dist_systems_p:
                        proposed_baseline_comparison = (
                            compare_swh_dist_systems_and_components(
                                rmd1=rmd_p,
                                rmd2=rmd_b,
                                compare_context_str="AppG 11-1 P_RMD Equals B_RMD",
                                swh_distribution_id=swh_dist_sys_id_p,
                            )
                        )
                        if swh_dist_sys_id_p not in swh_and_equip_dict_b:
                            proposed_baseline_comparison.append(
                                f"'{swh_dist_sys_id_p}' was not found in the Baseline model. Because there are no SWH loads in the User model, "
                                f"we are expecting the Proposed and Baseline systems to match."
                            )
                else:
                    # proposed has no distribution system
                    swh_dist_systems_b = find_all(
                        "$.service_water_heating_distribution_systems[*].id", rmd_b
                    )
                    if swh_dist_systems_b:
                        for swh_dist_sys_id_b in swh_dist_systems_b:
                            proposed_baseline_comparison.append(
                                f"'{swh_dist_sys_id_b}' was not found in the Proposed model. Because there are no SWH loads in the User model, "
                                f"we are expecting the Proposed and Baseline systems to match."
                            )

            return {
                "proposed_user_comparison": proposed_user_comparison,
                "proposed_baseline_comparison": proposed_baseline_comparison,
            }

        def rule_check(self, context, calc_vals=None, data=None):
            proposed_user_comparison = calc_vals["proposed_user_comparison"]
            proposed_baseline_comparison = calc_vals["proposed_baseline_comparison"]

            return not (proposed_user_comparison or proposed_baseline_comparison)

        def get_fail_msg(self, context, calc_vals=None, data=None):
            proposed_baseline_comparison = calc_vals["proposed_baseline_comparison"]
            return (
                proposed_baseline_comparison[-1] if proposed_baseline_comparison else ""
            )
