from collections import deque

from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import PROPOSED
from rct229.utils.jsonpath_utils import find_all


class PRM9012019Rule23f92(RuleDefinitionListIndexedBase):
    """Rule 5 of ASHRAE 90.1-2019 Appendix G Section 11 (Service Water Heating)"""

    def __init__(self):
        super(PRM9012019Rule23f92, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=False, PROPOSED=True
            ),
            each_rule=PRM9012019Rule23f92.RMDRule(),
            index_rmd=PROPOSED,
            id="11-5",
            description="Piping losses shall not be modeled.",
            ruleset_section_title="Service Hot Heating",
            standard_section="Table G3.1 #11, proposed column, f",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0]",
        )

    class RMDRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(PRM9012019Rule23f92.RMDRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=False, PROPOSED=True
                ),
                each_rule=PRM9012019Rule23f92.RMDRule.SWHDistRule(),
                index_rmd=PROPOSED,
                list_path="$.service_water_heating_distribution_systems[*]",
            )

        def is_applicable(self, context, data=None):
            rmd_p = context.PROPOSED

            swh_dist_sys_list_p = find_all(
                "$.service_water_heating_distribution_systems[*]", rmd_p
            )

            return swh_dist_sys_list_p

        class SWHDistRule(RuleDefinitionBase):
            def __init__(self):
                super(PRM9012019Rule23f92.RMDRule.SWHDistRule, self).__init__(
                    rmds_used=produce_ruleset_model_description(
                        USER=False,
                        BASELINE_0=False,
                        PROPOSED=True,
                    ),
                    required_fields={
                        "$": ["service_water_piping"],
                    },
                )

            def get_calc_vals(self, context, data=None):
                swh_dist_sys_p = context.PROPOSED

                piping_losses_modeled_p = []
                piping = swh_dist_sys_p.get("service_water_piping")
                if piping:
                    queue = deque([piping])

                    while queue:
                        current_piping = queue.popleft()
                        children_piping = current_piping.get("child", [])
                        queue.extend(children_piping)

                        piping_losses_modeled_p.append(
                            current_piping.get("are_thermal_losses_modeled")
                        )

                return {"piping_losses_modeled_p": piping_losses_modeled_p}

            def rule_check(self, context, calc_vals=None, data=None):
                piping_losses_modeled_p = calc_vals["piping_losses_modeled_p"]

                return not any(piping_losses_modeled_p)
