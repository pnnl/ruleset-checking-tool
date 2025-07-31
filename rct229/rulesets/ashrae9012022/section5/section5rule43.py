from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.jsonpath_utils import find_all

EXTERIOR = SchemaEnums.schema_enums["SurfaceAdjacencyOptions"].EXTERIOR


class PRM9012019Rule86r63(RuleDefinitionListIndexedBase):
    """Rule 11 of ASHRAE 90.1-2019 Appendix G Section 6 (Lighting)"""

    def __init__(self):
        super(PRM9012019Rule86r63, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=PRM9012019Rule86r63.SpaceRule(),
            index_rmd=BASELINE_0,
            id="5-43",
            description="Automatic fenestration shading devices shall not be modeled in the Baseline.",
            ruleset_section_title="Envelope",
            standard_section="Appendix G Section:** Section G3.1-5(f) Building Envelope Modeling Requirements"
            "for the Baseline building",
            is_primary_rule=True,
            list_path="$.buildings[*]",
            rmd_context="ruleset_model_descriptions/0",
        )

    def is_applicable(self, context, data=None):
        rmd_b = context.BASELINE_0

        return any(
            subsurface_b
            for subsurface_b in find_all(
                "$.buildings[*].building_segments[*].zones[*].surfaces[*].subsurfaces[*]",
                rmd_b,
            )
        )

    class BuildingRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012019Rule86r63.BuildingRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
            )

        def get_calc_vals(self, context, data=None):
            building_b = context.BASELINE_0
            automatic_shades_modeled = [
                subsurface_b.get("has_automatic_shades")
                for surface_b in find_all(
                    "$.building_segments[*].zones[*].surfaces[*]", building_b
                )
                if surface_b.get("adjacent_to") == EXTERIOR
                for subsurface_b in surface_b.get("subsurfaces", [])
                if subsurface_b.get("has_automatic_shades")
            ]
            return {"automatic_shades_modeled": automatic_shades_modeled}

        def rule_check(self, context, calc_vals=None, data=None):
            automatic_shades_modeled = calc_vals["automatic_shades_modeled"]
            return len(automatic_shades_modeled) > 0
