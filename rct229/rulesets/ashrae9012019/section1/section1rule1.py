from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_instance
from rct229.rulesets.ashrae9012019 import (
    BASELINE_0,
    BASELINE_90,
    BASELINE_180,
    BASELINE_270,
    PROPOSED,
    USER,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_BPF_building_area_types_and_zones import \
    get_BPF_building_area_types_and_zones
from rct229.utils.assertions import assert_
from rct229.utils.jsonpath_utils import find_one
from rct229.utils.std_comparisons import std_equal

class Section1Rule1(RuleDefinitionBase):
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
                USER=True,
                BASELINE_0=True,
                BASELINE_90=True,
                BASELINE_180=True,
                BASELINE_270=True,
                PROPOSED=True,
            ),
            required_fields={
                "$": ["weather", "calendar"]},
            id="1-1",
            description="Building performance factors shall be from Standard 90.1-2019, Table 4.2.1.1, based on the building area type and climate zone. For building area types not listed in Table 4.2.1.1 “All others.” shall be used to determine the BPF.",
            ruleset_section_title="Performance Calculations",
            standard_section="Section G4.2.1.1",
            is_primary_rule=True,
            rmr_context="ruleset_model_descriptions/0",
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

        output_bpf_set = list(filter(lambda x: x is not None, output_bpf_set))
        assert_(len(output_bpf_set) >= 1, "At least one `output_bpf_set` value must exist.")
        bpf_building_area_type_dict = get_BPF_building_area_types_and_zones(rmd_b0)
        is_undetermined = "UNDETERMINED" in bpf_building_area_type_dict.keys()
        bpf_bat_sum_prod = 0
        total_area = 0

        for bpf_bat in bpf_building_area_type_dict.keys():
            # expected_bpf = data_lookup(Table_4_2_1_1, bpf_bat, climate_zone) ## need to implement this function
            total_area += bpf_building_area_type_dict[bpf_bat]["area"] ## quntity
            bpf_bat_sum_prod += (expected_bpf * bpf_building_area_type_dict[bpf_bat]["area"]) ## quntity
        return {
            "output_bpf_set": list(set(output_bpf_set)),
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

        return (
            len(output_bpf_set) == 1
            and output_bpf_set[0] != 0
            and bpf_bat_sum_prod/total_area == output_bpf_set[0]
        )

