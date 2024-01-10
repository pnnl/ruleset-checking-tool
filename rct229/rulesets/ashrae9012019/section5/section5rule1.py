from pydash import filter_
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
from rct229.schema.config import ureg
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.jsonpath_utils import find_all, find_one
from rct229.utils.pint_utils import ZERO

SUBSURFACE_CLASSIFICATION = SchemaEnums.schema_enums["SubsurfaceClassificationOptions"]
RULESET_MODEL = SchemaEnums.schema_enums["RulesetModelOptions2019ASHRAE901"]
ACCEPTABLE_FEN_PERCENTAGE_DIFFERENCE = 0.05


class Section5Rule1(RuleDefinitionListIndexedBase):
    """Rule 1 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(Section5Rule1, self).__init__(
            rmrs_used=produce_ruleset_model_instance(
                USER=True,
                BASELINE_0=True,
                BASELINE_90=True,
                BASELINE_180=True,
                BASELINE_270=True,
                PROPOSED=True,
            ),
            each_rule=Section5Rule1.RMDRule(),
            index_rmr=BASELINE_0,
            id="5-1",
            description="There are four baseline rotations (i.e., four baseline models differing in azimuth by 90 degrees and four sets of baseline model results) if vertical fenestration area per each orientation differ by more than 5%.",
            ruleset_section_title="Envelope",
            standard_section="Table G3.1#5a baseline column",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0]",
        )

    class RMDRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section5Rule1.RMDRule, self).__init__(
                rmrs_used=produce_ruleset_model_instance(
                    USER=True,
                    BASELINE_0=True,
                    BASELINE_90=True,
                    BASELINE_180=True,
                    BASELINE_270=True,
                    PROPOSED=True,
                ),
                each_rule=Section5Rule1.RMDRule.BuildingRule(),
                index_rmr=BASELINE_0,
                list_path="$.buildings[*]",
            )

        def create_data(self, context, data):
            rmd_b0 = context.BASELINE_0
            rmd_b90 = context.BASELINE_90
            rmd_b180 = context.BASELINE_180
            rmd_b270 = context.BASELINE_270
            rmd_p = context.PROPOSED
            rmd_u = context.USER

            has_proposed = True if find_one("$.type", rmd_p) else False
            has_user = True if find_one("$.type", rmd_u, False) else False

            baseline_rmd_list = [rmd_b0, rmd_b90, rmd_b180, rmd_b270]
            rmd_list = [rmd_b0, rmd_b90, rmd_b180, rmd_b270, rmd_p, rmd_u]

            # count the rmds that aren't None
            no_of_rmds = len(
                filter_(
                    rmd_list,
                    lambda rmd: rmd is not None,
                )
            )

            # filter out baseline rmds that have the type key
            baseline_list = [
                find_one("$.type", rmd_b)
                for rmd_b in baseline_rmd_list
                if find_one("$.type", rmd_b, False)
            ]

            no_of_output_instance = len(baseline_list)

            return {
                "has_proposed": has_proposed,
                "has_user": has_user,
                "baseline_list": baseline_list,
                "no_of_rmds": no_of_rmds,
                "no_of_output_instance": no_of_output_instance,
            }

        class BuildingRule(RuleDefinitionBase):
            def __init__(self):
                super(Section5Rule1.RMDRule.BuildingRule, self).__init__(
                    rmrs_used=produce_ruleset_model_instance(
                        USER=True,
                        BASELINE_0=True,
                        BASELINE_90=True,
                        BASELINE_180=True,
                        BASELINE_270=True,
                        PROPOSED=True,
                    ),
                    required_fields={
                        "$.building_segments[*].zones[*].surfaces[*]": ["azimuth"],
                    },
                    fail_msg="Fail unless Table G3.1#5a exception #2 is applicable and it can be demonstrated that the building orientation is dictated by site considerations.",
                )

            def get_calc_vals(self, context, data=None):
                building_b0 = context.BASELINE_0
                building_b90 = context.BASELINE_90
                building_b180 = context.BASELINE_180
                building_b270 = context.BASELINE_270
                building_p = context.PROPOSED
                building_u = context.USER

                has_proposed = data["has_proposed"]
                has_user = data["has_user"]
                baseline_list = data["baseline_list"]
                no_of_rmds = data["no_of_rmds"]
                no_of_output_instance = data["no_of_output_instance"]

                has_baseline_0 = RULESET_MODEL.BASELINE_0 in baseline_list
                has_baseline_90 = RULESET_MODEL.BASELINE_90 in baseline_list
                has_baseline_180 = RULESET_MODEL.BASELINE_180 in baseline_list
                has_baseline_270 = RULESET_MODEL.BASELINE_270 in baseline_list

                has_proposed_output = has_proposed and find_one(
                    "$.output.output_instance", building_p, False
                )
                has_user_output = has_user and find_one(
                    "$.output.output_instance", building_u, False
                )
                has_basseline_0_output = has_baseline_0 and find_one(
                    "$.output.output_instance", building_b0, False
                )
                has_basseline_90_output = has_baseline_90 and find_one(
                    "$.output.output_instance", building_b90, False
                )
                has_basseline_180_output = has_baseline_180 and find_one(
                    "$.output.output_instance", building_b180, False
                )
                has_basseline_270_output = has_baseline_270 and find_one(
                    "$.output.output_instance", building_b270, False
                )

                # define a function to find the azimuth's corresponding key
                find_key_for_azi = lambda azi: next(
                    (
                        key
                        for key, _ in azimuth_fen_area_dict_b.items()
                        if int(key.split("-")[0])
                        <= azi.to(ureg("degree")).m
                        <= int(key.split("-")[1])
                    ),
                    None,
                )

                azimuth_fen_area_dict_b = {
                    f"{azi}-{azi+3}": ZERO.AREA for azi in range(0, 360, 3)
                }
                total_surface_fenestration_area_b = ZERO.AREA
                for surface_b in find_all(
                    "$.building_segments[*].zones[*].surfaces[*]", building_b0
                ):
                    if get_opaque_surface_type(surface_b) == OST.ABOVE_GRADE_WALL:
                        surface_azimuth_b = surface_b["azimuth"]

                        for subsurface_b in find_all("$.subsurfaces[*]", surface_b):
                            glazed_area_b = subsurface_b.get("glazed_area", ZERO.AREA)
                            opaque_area_b = subsurface_b.get("opaque_area", ZERO.AREA)

                            if (
                                subsurface_b["classification"]
                                == SUBSURFACE_CLASSIFICATION.DOOR
                            ):
                                if glazed_area_b > opaque_area_b:
                                    total_surface_fenestration_area_b += (
                                        glazed_area_b + opaque_area_b
                                    )
                            else:
                                total_surface_fenestration_area_b += (
                                    glazed_area_b + opaque_area_b
                                )
                    azimuth_fen_area_dict_b[
                        find_key_for_azi(surface_azimuth_b)
                    ] += total_surface_fenestration_area_b

                max_fen_area_b = azimuth_fen_area_dict_b[
                    max(azimuth_fen_area_dict_b, key=azimuth_fen_area_dict_b.get)
                ]
                min_fen_area_b = azimuth_fen_area_dict_b[
                    min(azimuth_fen_area_dict_b, key=azimuth_fen_area_dict_b.get)
                ]

                percent_difference = max(
                    abs(max_fen_area_b - min_fen_area_b) / max_fen_area_b
                    if max_fen_area_b != ZERO.AREA
                    else 0.0,
                    abs(min_fen_area_b - max_fen_area_b) / min_fen_area_b
                    if min_fen_area_b != ZERO.AREA
                    else 0.0,
                )

                rotation_expected_b = (
                    percent_difference >= ACCEPTABLE_FEN_PERCENTAGE_DIFFERENCE
                )

                return {
                    "no_of_rmds": no_of_rmds,
                    "no_of_output_instance": no_of_output_instance,
                    "rotation_expected_b": rotation_expected_b,
                    "has_proposed": has_proposed,
                    "has_user": has_user,
                    "has_baseline_0": has_baseline_0,
                    "has_baseline_90": has_baseline_90,
                    "has_baseline_180": has_baseline_180,
                    "has_baseline_270": has_baseline_270,
                    "has_proposed_output": has_proposed_output,
                    "has_user_output": has_user_output,
                    "has_basseline_0_output": has_basseline_0_output,
                    "has_basseline_90_output": has_basseline_90_output,
                    "has_basseline_180_output": has_basseline_180_output,
                    "has_basseline_270_output": has_basseline_270_output,
                }

            def rule_check(self, context, calc_vals=None, data=None):
                rotation_expected_b = calc_vals["rotation_expected_b"]

                no_of_rmds = calc_vals["no_of_rmds"]
                no_of_output_instance = calc_vals["no_of_output_instance"]

                has_proposed = calc_vals["has_proposed"]
                has_user = calc_vals["has_user"]
                has_baseline_0 = calc_vals["has_baseline_0"]
                has_baseline_90 = calc_vals["has_baseline_90"]
                has_baseline_180 = calc_vals["has_baseline_180"]
                has_baseline_270 = calc_vals["has_baseline_270"]

                has_proposed_output = calc_vals["has_proposed_output"]
                has_basseline_0_output = calc_vals["has_basseline_0_output"]
                has_basseline_90_output = calc_vals["has_basseline_90_output"]
                has_basseline_180_output = calc_vals["has_basseline_180_output"]
                has_basseline_270_output = calc_vals["has_basseline_270_output"]

                return (
                    has_user
                    and has_proposed
                    and has_baseline_0
                    and has_proposed_output
                    and has_basseline_0_output
                ) and (
                    (
                        rotation_expected_b
                        and has_baseline_90
                        and has_baseline_180
                        and has_baseline_270
                        and has_basseline_90_output
                        and has_basseline_180_output
                        and has_basseline_270_output
                        and no_of_rmds == 5
                        and no_of_output_instance == 6
                    )
                    or (not rotation_expected_b)
                )
