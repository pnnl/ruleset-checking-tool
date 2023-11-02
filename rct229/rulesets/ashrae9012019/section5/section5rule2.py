from rct229.rule_engine.partial_rule_definition import PartialRuleDefinition
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_instance
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.jsonpath_utils import find_all

SurfaceAdjacency = SchemaEnums.schema_enums["SurfaceAdjacencyOptions"]

# Json path for surfaces filtered to those with adjacent_to set to exterior
EXTERIOR_SURFACES_JSONPATH = f'$.building_segments[*].zones[*].surfaces[*][?(@.adjacent_to="{SurfaceAdjacency.EXTERIOR}")]'


class Section5Rule2(RuleDefinitionListIndexedBase):
    """Rule 2 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(Section5Rule2, self).__init__(
            rmrs_used=produce_ruleset_model_instance(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=Section5Rule2.BuildingRule(),
            index_rmr=BASELINE_0,
            id="5-2",
            description="The building shall be modeled so that it does not shade itself",
            ruleset_section_title="Envelope",
            standard_section="Section G3.1-5(b) Building Envelope Modeling Requirements for the Baseline building",
            is_primary_rule=False,
            rmr_context="ruleset_model_descriptions/0/buildings",
        )

    class BuildingRule(PartialRuleDefinition):
        def __init__(self):
            super(Section5Rule2.BuildingRule, self).__init__(
                rmrs_used=produce_ruleset_model_instance(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                required_fields={
                    "$.building_segments[*].zones[*].surfaces[*]": ["adjacent_to"],
                    EXTERIOR_SURFACES_JSONPATH: ["does_cast_shade"],
                },
            )

        def get_calc_vals(self, context, data=None):
            baseline_surfaces_casting_shade_ids = []
            for surface in find_all(EXTERIOR_SURFACES_JSONPATH, context.BASELINE_0):
                if surface["does_cast_shade"]:
                    baseline_surfaces_casting_shade_ids.append(surface["id"])

            return {
                "baseline_surfaces_casting_shade_ids": baseline_surfaces_casting_shade_ids
            }

        def applicability_check(self, context, calc_vals, data):
            return len(calc_vals["baseline_surfaces_casting_shade_ids"]) == 0
