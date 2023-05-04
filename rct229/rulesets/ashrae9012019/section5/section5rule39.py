from rct229.rule_engine.partial_rule_definition import PartialRuleDefinition
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.rulesets.ashrae9012019.data.schema_enums import schema_enums

SUBSURFACE_DYNAMIC_GLAZING = schema_enums["SubsurfaceDynamicGlazingOptions"]
UNDETERMINED_MSG = "SUBSURFACE INCLUDES MANUALLY CONTROLLED DYNAMIC GLAZING IN THE PROPOSED DESIGN. VERIFY THAT SHGC AND VT WERE MODELED AS THE AVERAGE OF THE MINIMUM AND MAXIMUM SHGC AND VT."


class Section5Rule39(RuleDefinitionListIndexedBase):
    """Rule 39 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(Section5Rule39, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, False, True),
            each_rule=Section5Rule39.SubsurfaceRule(),
            index_rmr="proposed",
            id="5-39",
            description="Manually controlled dynamic glazing shall use the average of the minimum and maximum SHGC and VT.",
            ruleset_section_title="Envelope",
            standard_section="Section G3.1-5(a)5 Building Envelope Modeling Requirements for the Proposed design",
            is_primary_rule=False,
            list_path="ruleset_model_instances[0].buildings[*].building_segments[*].zones[*].surfaces[*].subsurfaces[*]",
        )

    class SubsurfaceRule(PartialRuleDefinition):
        def __init__(self):
            super(Section5Rule39.SubsurfaceRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, False, True),
                required_fields={"$": ["dynamic_glazing_type"]},
                manual_check_required_msg=UNDETERMINED_MSG,
            )

        def get_calc_vals(self, context, data=None):
            subsurface_p = context.proposed
            subsurface_dynamic_glazing_type_p = subsurface_p["dynamic_glazing_type"]
            return {
                "subsurface_dynamic_glazing_type_p": subsurface_dynamic_glazing_type_p
            }

        def applicability_check(self, context, calc_vals, data):
            subsurface_dynamic_glazing_type_p = calc_vals[
                "subsurface_dynamic_glazing_type_p"
            ]
            return (
                subsurface_dynamic_glazing_type_p
                == SUBSURFACE_DYNAMIC_GLAZING.MANUAL_DYNAMIC
            )
