from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.match_lists import match_lists_by_id
from rct229.utils.pint_utils import ZERO

COMPLIANCE_PATH_TYPE = SchemaEnums.schema_enums["CompliancePathOptions2019ASHRAE901"]
MANUAL_CHECK_REQUIRED_MSG = "The proposed building miscellaneous equipment load is less than the baseline, which is only permitted when the model is being used to quantify performance that exceeds the requirements of Standard 90.1."


class PRM9012019Rule88h78(RuleDefinitionListIndexedBase):
    """Rule 1 of ASHRAE 90.1-2019 Appendix G Section 12 (Receptacle)"""

    def __init__(self):
        super(PRM9012019Rule88h78, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=True
            ),
            each_rule=PRM9012019Rule88h78.RMDRule(),
            index_rmd=BASELINE_0,
            id="12-1",
            description=(
                "Receptacle and process power shall be modeled as identical to the proposed design"
            ),
            ruleset_section_title="Receptacle",
            standard_section="Section Table G3.1-12 Modeling Requirements for the Proposed design",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0]",
            data_items={"compliance_path": (BASELINE_0, "compliance_path")},
        )

    class RMDRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012019Rule88h78.RMDRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=True
                ),
                manual_check_required_msg=MANUAL_CHECK_REQUIRED_MSG,
            )

        def get_calc_vals(self, context, data=None):
            rmd_b = context.BASELINE_0
            rmd_p = context.PROPOSED
            unexpected_misc_equipment_power = []
            reduced_misc_equipment_power = []
            misc_equipment_list_b = find_all(
                "$.buildings[*].building_segments[*].zones[*].spaces[*].miscellaneous_equipment[*]",
                rmd_b,
            )
            misc_equipment_list_p = find_all(
                "$.buildings[*].building_segments[*].zones[*].spaces[*].miscellaneous_equipment[*]",
                rmd_p,
            )
            # This assumes that the miscellaneous_equipment all match
            matched_misc_equipment_list_p = match_lists_by_id(
                misc_equipment_list_b, misc_equipment_list_p
            )
            proposed_baseline_misc_equipment_pairs = zip(
                misc_equipment_list_b, matched_misc_equipment_list_p
            )

            for (
                misc_equipment_b,
                misc_equipment_p,
            ) in proposed_baseline_misc_equipment_pairs:
                misc_equipment_power_b = misc_equipment_b.get("power", ZERO.POWER)
                misc_equipment_power_p = misc_equipment_p.get("power", ZERO.POWER)
                if misc_equipment_power_b > misc_equipment_power_p:
                    reduced_misc_equipment_power.append(
                        {
                            "id": misc_equipment_b.get("id"),
                            "baseline_power": misc_equipment_power_b,
                            "proposed_power": misc_equipment_power_p,
                        }
                    )
                elif misc_equipment_power_b < misc_equipment_power_p:
                    unexpected_misc_equipment_power.append(
                        {
                            "id": misc_equipment_b.get("id"),
                            "baseline_power": misc_equipment_power_b,
                            "proposed_power": misc_equipment_power_p,
                        }
                    )

            return {
                "reduced_misc_equipment_power": reduced_misc_equipment_power,
                "unexpected_misc_equipment_power": unexpected_misc_equipment_power,
                "compliance_path": data["compliance_path"],
            }

        def manual_check_required(self, context, calc_vals=None, data=None):
            unexpected_misc_equipment_power = calc_vals[
                "unexpected_misc_equipment_power"
            ]
            compliance_path = calc_vals["compliance_path"]
            return len(unexpected_misc_equipment_power) == 0 and (
                compliance_path != COMPLIANCE_PATH_TYPE.CODE_COMPLIANT
            )

        def rule_check(self, context, calc_vals=None, data=None):
            reduced_misc_equipment_power = calc_vals["reduced_misc_equipment_power"]
            unexpected_misc_equipment_power = calc_vals[
                "unexpected_misc_equipment_power"
            ]
            return (
                len(reduced_misc_equipment_power) == 0
                and len(unexpected_misc_equipment_power) == 0
            )
