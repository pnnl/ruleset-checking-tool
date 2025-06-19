from pydash import compact
from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import (
    BASELINE_0,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_opaque_surface_type import (
    OpaqueSurfaceType as OST,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_opaque_surface_type import (
    get_opaque_surface_type,
)
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.jsonpath_utils import find_all, find_one
from rct229.utils.pint_utils import ZERO

SUBSURFACE_CLASSIFICATION = SchemaEnums.schema_enums["SubsurfaceClassificationOptions"]
RULESET_MODEL = SchemaEnums.schema_enums["RulesetModelOptions2019ASHRAE901"]
ACCEPTABLE_FEN_PERCENTAGE_DIFFERENCE = 0.05


class PRM9012019Rule77j30(RuleDefinitionListIndexedBase):
    """Rule 1 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(PRM9012019Rule77j30, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=True,
                BASELINE_0=True,
                BASELINE_90=True,
                BASELINE_180=True,
                BASELINE_270=True,
                PROPOSED=True,
            ),
            rmds_used_optional=produce_ruleset_model_description(
                BASELINE_90=True, BASELINE_180=True, BASELINE_270=True
            ),
            each_rule=PRM9012019Rule77j30.RMDRule(),
            index_rmd=BASELINE_0,
            id="5-1",
            description="There are four baseline rotations (i.e., four baseline models differing in azimuth by 90 degrees and four sets of baseline model results) if vertical fenestration area per each orientation differ by more than 5%.",
            ruleset_section_title="Envelope",
            standard_section="Table G3.1#5a baseline column",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0]",
        )

    class RMDRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(PRM9012019Rule77j30.RMDRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=True,
                    BASELINE_0=True,
                    BASELINE_90=True,
                    BASELINE_180=True,
                    BASELINE_270=True,
                    PROPOSED=True,
                ),
                rmds_used_optional=produce_ruleset_model_description(
                    BASELINE_90=True, BASELINE_180=True, BASELINE_270=True
                ),
                each_rule=PRM9012019Rule77j30.RMDRule.BuildingRule(),
                index_rmd=BASELINE_0,
                list_path="$.buildings[*]",
            )

        def create_data(self, context, data):
            rmd_b0 = context.BASELINE_0
            rmd_b90 = context.BASELINE_90
            rmd_b180 = context.BASELINE_180
            rmd_b270 = context.BASELINE_270
            rmd_p = context.PROPOSED
            rmd_u = context.USER

            has_baseline_0 = rmd_b0 is not None
            has_baseline_90 = rmd_b90 is not None
            has_baseline_180 = rmd_b180 is not None
            has_baseline_270 = rmd_b270 is not None
            has_proposed = rmd_p is not None
            has_user = rmd_u is not None

            has_baseline_0_output = has_baseline_0 and bool(
                find_one("$.model_output", rmd_b0)
            )
            has_baseline_90_output = has_baseline_90 and bool(
                find_one("$.model_output", rmd_b90)
            )
            has_baseline_180_output = has_baseline_180 and bool(
                find_one("$.model_output", rmd_b180)
            )
            has_baseline_270_output = has_baseline_270 and bool(
                find_one("$.model_output", rmd_b270)
            )
            has_proposed_output = has_proposed and bool(
                find_one("$.model_output", rmd_p)
            )
            has_user_output = has_user and bool(find_one("$.model_output", rmd_u))

            rmd_list = [rmd_b0, rmd_b90, rmd_b180, rmd_b270, rmd_p, rmd_u]
            rmd_list_no_user = [rmd_b0, rmd_b90, rmd_b180, rmd_b270, rmd_p]

            # count the rmds that aren't None
            no_of_rmds = len(compact(rmd_list))

            # filter out rmds that aren't None then count the length
            no_of_output_instance = len(
                compact([find_one("$.model_output", rmd) for rmd in rmd_list_no_user])
            )

            return {
                "has_baseline_0": has_baseline_0,
                "has_baseline_90": has_baseline_90,
                "has_baseline_180": has_baseline_180,
                "has_baseline_270": has_baseline_270,
                "has_proposed": has_proposed,
                "has_user": has_user,
                "has_baseline_0_output": has_baseline_0_output,
                "has_baseline_90_output": has_baseline_90_output,
                "has_baseline_180_output": has_baseline_180_output,
                "has_baseline_270_output": has_baseline_270_output,
                "has_proposed_output": has_proposed_output,
                "has_user_output": has_user_output,
                "no_of_rmds": no_of_rmds,
                "no_of_output_instance": no_of_output_instance,
            }

        class BuildingRule(RuleDefinitionBase):
            def __init__(self):
                super(PRM9012019Rule77j30.RMDRule.BuildingRule, self).__init__(
                    rmds_used=produce_ruleset_model_description(
                        BASELINE_0=True,
                    ),
                    required_fields={
                        "$.building_segments[*].zones[*].surfaces[*]": ["azimuth"],
                    },
                    precision={
                        "percent_difference_max_min_fen_area_per_orientation": {
                            "precision": 0.01,
                            "unit": "",
                        }
                    },
                    fail_msg="Fail unless Table G3.1#5a exception #2 is applicable and it can be demonstrated that the building orientation is dictated by site considerations.",
                )

            def get_calc_vals(self, context, data=None):
                building_b0 = context.BASELINE_0

                has_baseline_0 = data["has_baseline_0"]
                has_baseline_90 = data["has_baseline_90"]
                has_baseline_180 = data["has_baseline_180"]
                has_baseline_270 = data["has_baseline_270"]
                has_proposed = data["has_proposed"]
                has_user = data["has_user"]
                has_baseline_0_output = data["has_baseline_0_output"]
                has_baseline_90_output = data["has_baseline_90_output"]
                has_baseline_180_output = data["has_baseline_180_output"]
                has_baseline_270_output = data["has_baseline_270_output"]
                has_proposed_output = data["has_proposed_output"]
                has_user_output = data["has_user_output"]
                no_of_rmds = data["no_of_rmds"]
                no_of_output_instance = data["no_of_output_instance"]

                # define a function to get the azimuth's corresponding key
                def get_key_for_azi(azi):
                    azi_value = azi.to("degrees").m
                    low_bound = azi_value - (azi_value % 3)
                    high_bound = low_bound + 3
                    return f"{low_bound}-{high_bound}"

                azimuth_fen_area_dict_b = {}
                for surface_b in find_all(
                    "$.building_segments[*].zones[*].surfaces[*]", building_b0
                ):
                    if get_opaque_surface_type(surface_b) == OST.ABOVE_GRADE_WALL:
                        surface_azimuth_b = surface_b["azimuth"]
                        total_surface_fenestration_area_b = ZERO.AREA
                        surface_azimuth_bin = get_key_for_azi(surface_azimuth_b)

                        if surface_azimuth_bin not in azimuth_fen_area_dict_b:
                            azimuth_fen_area_dict_b[surface_azimuth_bin] = ZERO.AREA

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
                            surface_azimuth_bin
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
                    percent_difference > ACCEPTABLE_FEN_PERCENTAGE_DIFFERENCE
                    or self.precision_comparison[
                        "percent_difference_max_min_fen_area_per_orientation"
                    ](
                        percent_difference.magnitude,
                        ACCEPTABLE_FEN_PERCENTAGE_DIFFERENCE,
                    )
                )

                return {
                    "no_of_rmds": no_of_rmds,
                    "no_of_output_instance": no_of_output_instance,
                    "rotation_expected_b": rotation_expected_b,
                    "has_baseline_0": has_baseline_0,
                    "has_baseline_90": has_baseline_90,
                    "has_baseline_180": has_baseline_180,
                    "has_baseline_270": has_baseline_270,
                    "has_proposed": has_proposed,
                    "has_user": has_user,
                    "has_baseline_0_output": has_baseline_0_output,
                    "has_baseline_90_output": has_baseline_90_output,
                    "has_baseline_180_output": has_baseline_180_output,
                    "has_baseline_270_output": has_baseline_270_output,
                    "has_proposed_output": has_proposed_output,
                    "has_user_output": has_user_output,
                }

            def rule_check(self, context, calc_vals=None, data=None):
                rotation_expected_b = calc_vals["rotation_expected_b"]

                no_of_rmds = calc_vals["no_of_rmds"]
                no_of_output_instance = calc_vals["no_of_output_instance"]

                has_baseline_0 = calc_vals["has_baseline_0"]
                has_baseline_90 = calc_vals["has_baseline_90"]
                has_baseline_180 = calc_vals["has_baseline_180"]
                has_baseline_270 = calc_vals["has_baseline_270"]
                has_proposed = calc_vals["has_proposed"]
                has_user = calc_vals["has_user"]

                has_baseline_0_output = calc_vals["has_baseline_0_output"]
                has_baseline_90_output = calc_vals["has_baseline_90_output"]
                has_baseline_180_output = calc_vals["has_baseline_180_output"]
                has_baseline_270_output = calc_vals["has_baseline_270_output"]
                has_proposed_output = calc_vals["has_proposed_output"]

                return (
                    has_user
                    and has_proposed
                    and has_baseline_0
                    and has_proposed_output
                    and has_baseline_0_output
                ) and (
                    (
                        rotation_expected_b
                        and has_baseline_90
                        and has_baseline_180
                        and has_baseline_270
                        and has_baseline_90_output
                        and has_baseline_180_output
                        and has_baseline_270_output
                        and no_of_rmds == 6
                        and no_of_output_instance == 5
                    )
                    or (not rotation_expected_b)
                )
