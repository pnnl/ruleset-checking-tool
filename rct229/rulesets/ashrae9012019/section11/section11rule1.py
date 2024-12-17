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
from rct229.utils.jsonpath_utils import find_all, find_one


class Section11Rule1(RuleDefinitionListIndexedBase):
    """Rule 1 of ASHRAE 90.1-2019 Appendix G Section 11 (Service Water Heating)"""

    def __init__(self):
        super(Section11Rule1, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=True, BASELINE_0=True, PROPOSED=True
            ),
            each_rule=Section11Rule1.RMDRule(),
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

    class RMDRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section11Rule1.RMDRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=True
                ),
                each_rule=Section11Rule1.RMDRule.SWHDistributionRule(),
                index_rmd=BASELINE_0,
                list_path="$.service_water_heating_distribution_systems[*]",
            )

        def create_data(self, context, data):
            rmd_u = context.user
            rmd_b = context.BASELINE_0
            rmd_p = context.PROPOSED

            swh_and_equip_dict_u = (
                get_swh_equipment_associated_with_each_swh_distribution_system(rmd_u)
            )
            swh_and_equip_dict_b = (
                get_swh_equipment_associated_with_each_swh_distribution_system(rmd_b)
            )
            swh_and_equip_dict_p = (
                get_swh_equipment_associated_with_each_swh_distribution_system(rmd_p)
            )

            errors = []
            user_proposed_comparison = []
            user_baseline_comparison = []
            for swh_dist_id_u in find_all(
                "$.service_water_heating_distribution_systems[*].id", rmd_u
            ):
                if swh_and_equip_dict_u[swh_dist_id_u].uses:
                    swh_use_u = find_one(
                        f'$.buildings[*].building_segments[*].zones[*].spaces[*].service_water_heating_uses[*][?(@.id="{swh_dist_id_u}")]',
                        rmd_u,
                    )
                    if swh_use_u is not None and swh_use_u.get("use") > 0.0:
                        user_proposed_comparison = (
                            compare_swh_dist_systems_and_components(
                                rmd1=rmd_p,
                                rmd2=rmd_u,
                                compare_context_str="AppG 11-1 P_RMD Equals U_RMD",
                                swh_distribution_id=swh_dist_id_u,
                            )
                        )
                else:
                    user_baseline_comparison = compare_swh_dist_systems_and_components(
                        rmd1=rmd_p,
                        rmd2=rmd_b,
                        compare_context_str="AppG 11-1 P_RMD Equals B_RMD",
                        swh_distribution_id=swh_dist_id_u,
                    )

                if swh_dist_id_u not in swh_and_equip_dict_p:
                    errors.append(
                        f"{swh_dist_id_u} was not found in the Proposed model. Because there are no SWH loads in the User model, "
                        f"we are expecting the Proposed and Baseline systems to match."
                    )
                if swh_dist_id_u not in swh_and_equip_dict_b:
                    errors.append(
                        f"{swh_dist_id_u} was not found in the Baseline model. Because there are no SWH loads in the User model, "
                        f"we are expecting the Proposed and Baseline systems to match."
                    )

            return {
                "user_proposed_comparison": user_proposed_comparison,
                "user_baseline_comparison": user_baseline_comparison,
            }

        class SWHDistributionRule(RuleDefinitionBase):
            def __init__(self):
                super(Section11Rule1.RMDRule.SWHDistributionRule, self).__init__(
                    rmds_used=produce_ruleset_model_description(
                        USER=True, BASELINE_0=True, PROPOSED=True
                    ),
                )

            def get_calc_vals(self, context, data=None):
                user_proposed_comparison = data["user_proposed_comparison"]
                user_baseline_comparison = data["user_baseline_comparison"]

                return not user_proposed_comparison and not user_baseline_comparison
