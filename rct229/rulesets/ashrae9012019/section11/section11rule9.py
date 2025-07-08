from rct229.rule_engine.partial_rule_definition import PartialRuleDefinition
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.ruleset_functions.get_swh_bats_and_swh_use import (
    get_swh_bats_and_swh_use,
)
from rct229.utils.jsonpath_utils import find_all


class PRM9012019Rule93n40(RuleDefinitionListIndexedBase):
    """Rule 9 of ASHRAE 90.1-2019 Appendix G Section 11 (Service Water Heating)"""

    def __init__(self):
        super(PRM9012019Rule93n40, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=PRM9012019Rule93n40.RMDRule(),
            index_rmd=BASELINE_0,
            id="11-9",
            description="The baseline system must be sized according to Standard 90.1 2019, Section 7.4.1.",
            ruleset_section_title="Service Water Heating",
            standard_section="Table G3.1 #11, baseline column, a",
            is_primary_rule=False,
            list_path="ruleset_model_descriptions[0]",
        )

    class RMDRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(PRM9012019Rule93n40.RMDRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False,
                    BASELINE_0=True,
                    PROPOSED=False,
                ),
                index_rmd=BASELINE_0,
                each_rule=PRM9012019Rule93n40.RMDRule.SWHBATRule(),
            )

        def create_data(self, context, data):
            rmd_b = context.BASELINE_0

            service_water_heating_uses_dict_b = {
                swh_use["id"]: swh_use.get("use", 0.0)
                for swh_use in find_all(
                    "$.service_water_heating_uses[*]",
                    rmd_b,
                )
            }
            shw_bat_uses_dict_b = get_swh_bats_and_swh_use(rmd_b)

            return {
                "service_water_heating_uses_dict_b": service_water_heating_uses_dict_b,
                "shw_bat_uses_dict_b": shw_bat_uses_dict_b,
            }

        def create_context_list(self, context, data=None):
            shw_bat_uses_dict_b = data["shw_bat_uses_dict_b"]

            building_area_type_and_uses = {}
            for (
                bat_type,
                SWH_use_ids,
            ) in shw_bat_uses_dict_b.items():
                building_area_type_and_uses[bat_type] = {}
                building_area_type_and_uses[bat_type]["id"] = bat_type
                building_area_type_and_uses[bat_type]["swh_use_ids"] = SWH_use_ids

            return [
                produce_ruleset_model_description(
                    USER=False,
                    BASELINE_0=building_area_type_and_uses[bat_type],
                    PROPOSED=False,
                )
                for bat_type, SWH_use_id in shw_bat_uses_dict_b.items()
            ]

        class SWHBATRule(PartialRuleDefinition):
            def __init__(self):
                super(PRM9012019Rule93n40.RMDRule.SWHBATRule, self).__init__(
                    rmds_used=produce_ruleset_model_description(
                        USER=False, BASELINE_0=True, PROPOSED=False
                    ),
                )

            def applicability_check(self, context, calc_vals, data):
                swh_bat_id_list_b = context.BASELINE_0["swh_use_ids"]
                service_water_heating_uses_dict_b = data[
                    "service_water_heating_uses_dict_b"
                ]

                return all(
                    [
                        (
                            True
                            if service_water_heating_uses_dict_b[swh_use_id] > 0.0
                            else False
                        )
                        for swh_use_id in swh_bat_id_list_b
                    ]
                )

            def get_manual_check_required_msg(self, context, calc_vals=None, data=None):
                swh_bat_id_list_b = context.BASELINE_0["swh_use_ids"]
                service_water_heating_uses_dict_b = data[
                    "service_water_heating_uses_dict_b"
                ]

                swh_bat = ", ".join(
                    swh_bat_id
                    for swh_bat_id in swh_bat_id_list_b
                    if service_water_heating_uses_dict_b[swh_bat_id] > 0.0
                )

                return f"Check that the baseline Service Water Heating System for Building Area Type {swh_bat} is sized according to ASHRAE Standard 90.1 2019, Section 7.4.1."
