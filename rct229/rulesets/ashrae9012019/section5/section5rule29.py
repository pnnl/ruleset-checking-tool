from rct229.rule_engine.partial_rule_definition import PartialRuleDefinition
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_instance
from rct229.rulesets.ashrae9012019 import PROPOSED
from rct229.schema.schema_enums import SchemaEnums

SUBSURFACE_DYNAMIC_GLAZING = SchemaEnums.schema_enums["SubsurfaceDynamicGlazingOptions"]
UNDETERMINED_MSG = "SUBSURFACE INCLUDES MANUALLY CONTROLLED DYNAMIC GLAZING IN THE PROPOSED DESIGN. VERIFY THAT SHGC AND VT WERE MODELED AS THE AVERAGE OF THE MINIMUM AND MAXIMUM SHGC AND VT."


class Section5Rule29(RuleDefinitionListIndexedBase):
    """Rule 29 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(Section5Rule29, self).__init__(
            rmrs_used=produce_ruleset_model_instance(
                USER=False, BASELINE_0=False, PROPOSED=True
            ),
            each_rule=Section5Rule29.SubsurfaceRule(),
            index_rmr=PROPOSED,
            id="5-29",
            description="Manually controlled dynamic glazing shall use the average of the minimum and maximum SHGC and VT.",
            ruleset_section_title="Envelope",
            standard_section="Section G3.1-5(a)5 Building Envelope Modeling Requirements for the Proposed design",
            is_primary_rule=False,
            list_path="ruleset_model_descriptions[0].buildings[*].building_segments[*].zones[*].surfaces[*].subsurfaces[*]",
        )

    class SubsurfaceRule(PartialRuleDefinition):
        def __init__(self):
            super(Section5Rule29.SubsurfaceRule, self).__init__(
                rmrs_used=produce_ruleset_model_instance(
                    USER=False, BASELINE_0=False, PROPOSED=True
                ),
                required_fields={"$": ["dynamic_glazing_type"]},
                manual_check_required_msg=UNDETERMINED_MSG,
            )

        def get_calc_vals(self, context, data=None):
            subsurface_p = context.PROPOSED
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
