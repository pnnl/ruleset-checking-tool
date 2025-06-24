from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.data_fns.table_4_2_1_1_fns import (
    table_4_2_1_1_lookup,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_BPF_building_area_types_and_zones import (
    get_BPF_building_area_types_and_zones,
)
from rct229.utils.assertions import assert_
from rct229.utils.pint_utils import ZERO
from rct229.utils.std_comparisons import std_equal

MANUAL_CHECK_REQUIRED_MSG = (
    "One or more building area types could not be determined for the project's building "
    "segments. Assigning a lighting building area type to all building segments will fix this"
    " issue. "
)

FAIL_MSG = "More than one BPF value was used in the project."


class PRM9012019Rule73j65(RuleDefinitionListIndexedBase):
    """Rule 73j65 of ASHRAE 90.1-2019 Appendix G Section 1 (Performance Calculations)"""

    def __init__(self):
        super(PRM9012019Rule73j65, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=True,
                BASELINE_0=True,
                BASELINE_90=True,
                BASELINE_180=True,
                BASELINE_270=True,
                PROPOSED=True,
            ),
            rmds_used_optional=produce_ruleset_model_description(
                BASELINE_90=True,
                BASELINE_180=True,
                BASELINE_270=True,
            ),
            index_rmd=BASELINE_0,
            each_rule=PRM9012019Rule73j65.RMDRule(),
            id="1-1",
            description="Building performance factors shall be from Standard 90.1-2019, Table 4.2.1.1, based on the "
            "building area type and climate zone. For building area types not listed in Table 4.2.1.1 "
            "“All others.” shall be used to determine the BPF.",
            ruleset_section_title="Performance Calculations",
            standard_section="Section G4.2.1.1",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0]",
        )

    def create_data(self, context, data=None):
        return {
            key: getattr(context, key)
            .get("output", {})
            .get("total_area_weighted_building_performance_factor")
            for key in context.__dict__
            if getattr(context, key) is not None
        }

    class RMDRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012019Rule73j65.RMDRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=True,
                    BASELINE_0=True,
                    BASELINE_90=True,
                    BASELINE_180=True,
                    BASELINE_270=True,
                    PROPOSED=True,
                ),
                rmds_used_optional=produce_ruleset_model_description(
                    BASELINE_90=True,
                    BASELINE_180=True,
                    BASELINE_270=True,
                ),
                required_fields={
                    "$": ["weather"],
                    "weather": ["climate_zone"],
                },
                manual_check_required_msg=MANUAL_CHECK_REQUIRED_MSG,
                fail_msg=FAIL_MSG,
            )

        def get_calc_vals(self, context, data=None):
            rmd_b0 = context.BASELINE_0

            output_bpf_list = list(set(filter(lambda x: x is not None, data.values())))
            assert_(
                len(output_bpf_list) >= 1,
                "At least one `output_bpf_set` value must exist.",
            )
            bpf_building_area_type_dict = get_BPF_building_area_types_and_zones(rmd_b0)
            has_undetermined = "UNDETERMINED" in bpf_building_area_type_dict
            bpf_bat_sum_prod = ZERO.AREA
            total_area = ZERO.AREA
            climate_zone = rmd_b0["weather"]["climate_zone"]
            for bpf_bat in bpf_building_area_type_dict:
                if bpf_bat != "UNDETERMINED":
                    expected_bpf = table_4_2_1_1_lookup(bpf_bat, climate_zone)[
                        "building_performance_factor"
                    ]
                    bpf_bat_dict_area = bpf_building_area_type_dict[bpf_bat]["area"]
                    total_area += bpf_bat_dict_area
                    bpf_bat_sum_prod += expected_bpf * bpf_bat_dict_area

            # Checks if only undetermined was returned. If so, skip check for total area.
            only_undetermined = (
                len(bpf_building_area_type_dict) == 1
                and "UNDETERMINED" in bpf_building_area_type_dict
            )

            if not only_undetermined:
                assert_(
                    total_area > 0,
                    "The `total_area ` value must be greater than 0.",
                )

            return {
                "output_bpf_list": output_bpf_list,
                "bpf_bat_sum_prod": bpf_bat_sum_prod,
                "total_area": total_area,
                "has_undetermined": has_undetermined,
            }

        def manual_check_required(self, context, calc_vals=None, data=None):
            has_undetermined = calc_vals["has_undetermined"]
            return has_undetermined

        def rule_check(self, context, calc_vals=None, data=None):
            output_bpf_list = calc_vals["output_bpf_list"]
            bpf_bat_sum_prod = calc_vals["bpf_bat_sum_prod"]
            total_area = calc_vals["total_area"]

            return len(output_bpf_list) == 1 and self.precision_comparison(
                bpf_bat_sum_prod / total_area, output_bpf_list[0]
            )

        def is_tolerance_fail(self, context, calc_vals=None, data=None):
            output_bpf_list = calc_vals["output_bpf_list"]
            bpf_bat_sum_prod = calc_vals["bpf_bat_sum_prod"]
            total_area = calc_vals["total_area"]
            return len(output_bpf_list) == 1 and std_equal(
                output_bpf_list[0], bpf_bat_sum_prod / total_area
            )
