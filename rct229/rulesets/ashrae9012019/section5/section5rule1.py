from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_instance
from rct229.rulesets.ashrae9012019 import (
    BASELINE_0,
    BASELINE_90,
    BASELINE_180,
    BASELINE_270,
    PROPOSED,
    USER,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_opaque_surface_type import (
    OpaqueSurfaceType as OST,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_opaque_surface_type import (
    get_opaque_surface_type,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_surface_conditioning_category_dict import (
    SurfaceConditioningCategory as SCC,
)
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.assertions import getattr_
from rct229.utils.pint_utils import ZERO

SUBSURFACE_CLASSIFICATION = SchemaEnums.schema_enums["SubsurfaceClassificationOptions"]
RULESET_MODEL = SchemaEnums.schema_enums["RulesetModelOptions2019ASHRAE901"]


class Section5Rule1(RuleDefinitionListIndexedBase):
    """Rule 1 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(Section5Rule1, self).__init__(
            rmrs_used=produce_ruleset_model_instance(
                USER=True, BASELINE_0=True, PROPOSED=True
            ),
            each_rule=Section5Rule1.SurfaceRule(),
            index_rmr=BASELINE_0,
            id="5-1",
            description="There are four baseline rotations (i.e., four baseline models differing in azimuth by 90 degrees and four sets of baseline model results) if vertical fenestration area per each orientation differ by more than 5%.",
            ruleset_section_title="Envelope",
            standard_section="Table G3.1#5a baseline column",
            is_primary_rule=True,
            # rmr_context="ruleset_model_descriptions[0]",
        )

    # class RMDRule(RuleDefinitionListIndexedBase):
    #     def __init__(self):
    #         super(Section5Rule1.RMDRule, self).__init__(
    #             rmrs_used=produce_ruleset_model_instance(
    #                 USER=True, BASELINE_0=True, PROPOSED=True
    #             ),
    #             each_rule=Section5Rule1.RMDRule.SurfaceRule(),
    #             index_rmr=BASELINE_0,
    #             list_path="$.buildings[*].building_segments[*].zones[*].surfaces[*]",
    #         )

    def create_data(self, context, data):
        RMD_u = context.USER
        RMD_b0 = context.BASELINE_0
        RMD_b90 = context.BASELINE_90
        RMD_b180 = context.BASELINE_180
        RMD_b270 = context.BASELINE_270
        RMD_p = context.PROPOSED

        return

    class SurfaceRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section5Rule1.SurfaceRule, self).__init__(
                rmrs_used=produce_ruleset_model_instance(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                each_rule=Section5Rule1.SurfaceRule.SubsurfaceRule(),
                index_rmr=BASELINE_0,
                list_path="$.subsurfaces[*]",
            )

        def create_data(self, context, data):
            surface_b = context.BASELINE_0

            azimuth_fen_area_dict_b = {}
            if get_opaque_surface_type(surface_b) == OST.ABOVE_GRADE_WALL:
                surface_azimuth_b = getattr_(surface_b, "surfaces", "azimuth")

                if surface_azimuth_b not in azimuth_fen_area_dict_b:
                    azimuth_fen_area_dict_b[surface_azimuth_b] = 0

            return {"azimuth_fen_area_dict_b": azimuth_fen_area_dict_b}

        class SubsurfaceRule(RuleDefinitionBase):
            def __init__(self):
                super(
                    Section5Rule1.SurfaceRule.SubsurfaceRule,
                    self,
                ).__init__(
                    rmrs_used=produce_ruleset_model_instance(
                        USER=False, BASELINE_0=True, PROPOSED=False
                    ),
                )

            def get_calc_vals(self, context, data=None):
                subsurface_b = context.BASELINE_0

                total_surface_fenestration_area_b = ZERO.AREA
                glazed_area_b = subsurface_b.get("glazed_area", ZERO.AREA)
                opaque_area_b = subsurface_b.get("opaque_area", ZERO.AREA)
                if subsurface_b["classification"] == SUBSURFACE_CLASSIFICATION.DOOR:
                    if glazed_area_b > opaque_area_b:
                        total_surface_fenestration_area_b += (
                            glazed_area_b + opaque_area_b
                        )
                else:
                    total_surface_fenestration_area_b += (
                        glazed_area_b + opaque_area_b
                    )

                return

            def rule_check(self, context, calc_vals=None, data=None):
                return
