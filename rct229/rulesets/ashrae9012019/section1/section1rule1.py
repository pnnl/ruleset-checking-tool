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
from rct229.rulesets.ashrae9012019.data_fns.table_4_2_1_1_fns import (
    table_4_2_1_1_lookup,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_BPF_building_area_types_and_zones import (
    get_BPF_building_area_types_and_zones,
)
from rct229.utils.assertions import assert_
from rct229.utils.jsonpath_utils import find_one
from rct229.utils.pint_utils import ZERO
from rct229.utils.std_comparisons import std_equal

MANUAL_CHECK_REQUIRED_MSG = "One or more building area types could not be determined for the project's building segments. Assigning a lighting building area type to all building segments will fix this issue."


class Section1Rule1(RuleDefinitionListIndexedBase):
    """Rule 1 of ASHRAE 90.1-2019 Appendix G Section 1 (Performance Calculations)"""

    def __init__(self):
        super(Section1Rule1, self).__init__(
            rmrs_used=produce_ruleset_model_instance(
                USER=True,
                BASELINE_0=True,
                BASELINE_90=True,
                BASELINE_180=True,
                BASELINE_270=True,
                PROPOSED=True,
            ),
            rmrs_used_optional=produce_ruleset_model_instance(
                BASELINE_90=True,
                BASELINE_180=True,
                BASELINE_270=True,
            ),
            required_fields={
                "$": ["weather", "ruleset_model_descriptions"],
                "weather": ["climate_zone"],
            },
            index_rmr=BASELINE_0,
            each_rule=Section1Rule1.RMDRule(),
            id="1-1",
            description="Building performance factors shall be from Standard 90.1-2019, Table 4.2.1.1, based on the building area type and climate zone. For building area types not listed in Table 4.2.1.1 “All others.” shall be used to determine the BPF.",
            ruleset_section_title="Performance Calculations",
            standard_section="Section G4.2.1.1",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0]",
            data_items={"climate_zone": (BASELINE_0, "weather/climate_zone")},
        )

    class RMDRule(RuleDefinitionBase):
        def __init__(self):
            super(Section1Rule1.RMDRule, self).__init__(
                rmrs_used=produce_ruleset_model_instance(
                    BASELINE_90=True,
                    BASELINE_180=True,
                    BASELINE_270=True,
                ),
                rmrs_used_optional=produce_ruleset_model_instance(
                    BASELINE_90=True,
                    BASELINE_180=True,
                    BASELINE_270=True,
                ),
                manual_check_required_msg=MANUAL_CHECK_REQUIRED_MSG,
            )

        def get_calc_vals(self, context, data=None):
            rmd_u = context.USER
            rmd_b0 = context.BASELINE_0
            rmd_b90 = context.BASELINE_90
            rmd_b180 = context.BASELINE_180
            rmd_b270 = context.BASELINE_270
            rmd_p = context.PROPOSED
            output_bpf_set = []

            for rmd in (rmd_u, rmd_b0, rmd_b90, rmd_b180, rmd_b270, rmd_p):
                if rmd is not None:
                    output_bpf_set.append(
                        find_one(
                            "$.output.total_area_weighted_building_performance_factor",
                            rmd,
                        )
                    )

            output_bpf_set = list(set(filter(lambda x: x is not None, output_bpf_set)))
            assert_(
                len(output_bpf_set) >= 1,
                "At least one `output_bpf_set` value must exist.",
            )
            bpf_building_area_type_dict = get_BPF_building_area_types_and_zones(rmd_b0)
            assert_(
                len(bpf_building_area_type_dict) >= 1,
                "At least one building area type must exist.",
            )
            is_undetermined = "UNDETERMINED" in bpf_building_area_type_dict
            bpf_bat_sum_prod = ZERO.AREA
            total_area = ZERO.AREA
            climate_zone = data["climate_zone"]
            for bpf_bat in bpf_building_area_type_dict:
                if is_undetermined:
                    continue
                expected_bpf = table_4_2_1_1_lookup(bpf_bat, climate_zone)[
                    "building_performance_factor"
                ]
                bpf_bat_dict_area = bpf_building_area_type_dict[bpf_bat]["area"]
                total_area += bpf_bat_dict_area
                bpf_bat_sum_prod += expected_bpf * bpf_bat_dict_area
            assert_(
                total_area > 0,
                "The `total_area ` value must be greater than 0.",
            )
            return {
                "output_bpf_set": output_bpf_set,
                "bpf_bat_sum_prod": bpf_bat_sum_prod,
                "total_area": total_area,
                "is_undetermined": is_undetermined,
            }

        def manual_check_required(self, context, calc_vals=None, data=None):
            is_undetermined = calc_vals["is_undetermined"]
            return is_undetermined

        def rule_check(self, context, calc_vals=None, data=None):
            output_bpf_set = calc_vals["output_bpf_set"]
            bpf_bat_sum_prod = calc_vals["bpf_bat_sum_prod"]
            total_area = calc_vals["total_area"]

            return len(output_bpf_set) == 1 and std_equal(
                bpf_bat_sum_prod / total_area, output_bpf_set[0]
            )
