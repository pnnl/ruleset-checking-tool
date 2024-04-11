from pydash import filter_
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
from rct229.utils.assertions import assert_
from rct229.utils.jsonpath_utils import find_one
from rct229.utils.std_comparisons import std_equal


class Section1Rule3(RuleDefinitionBase):
    """Rule 3 of ASHRAE 90.1-2019 Appendix G Section 1 (Performance Calculations)"""

    def __init__(self):
        super(Section1Rule3, self).__init__(
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
            id="1-3",
            description="The Performance Cost Index-Target (PCIt) shall be calculated using the procedures defined in Section 4.2.1.1. "
            "The PCIt shall be equal to [baseline building unregulated energy cost (BBUEC) + BPF x baseline building regulated energy cost (BBREC)]/ BBP",
            ruleset_section_title="Performance Calculations",
            standard_section="Section 4.2.1.1",
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

        pci_target_set = []
        bpf_set = []
        bbp_set = []
        bbrec_set = []
        bbuec_set = []
        for rmd in (rmd_u, rmd_b0, rmd_b90, rmd_b180, rmd_b270, rmd_p):
            if rmd is not None:
                pci_target_set.append(
                    find_one("$.output.performance_cost_index_target", rmd)
                )
                bpf_set.append(
                    find_one(
                        "$.output.total_area_weighted_building_performance_factor",
                        rmd,
                    )
                )
                bbp_set.append(
                    find_one("$.output.baseline_building_performance_energy_cost", rmd)
                )
                bbrec_set.append(
                    find_one("$.output.baseline_building_regulated_energy_cost", rmd)
                )
                bbuec_set.append(
                    find_one("$.output.baseline_building_unregulated_energy_cost", rmd)
                )

        pci_target_set = filter_(pci_target_set, lambda x: x is not None)
        bpf_set = filter_(bpf_set, lambda x: x is not None)
        bbp_set = filter_(bbp_set, lambda x: x is not None)
        bbrec_set = filter_(bbrec_set, lambda x: x is not None)
        bbuec_set = filter_(bbuec_set, lambda x: x is not None)

        assert_(
            len(pci_target_set) >= 1,
            "At least one `performance_cost_index_target` value must exist.",
        )
        assert_(len(bpf_set) >= 1, "At least one `bpf_set` value must exist.")
        assert_(len(bbp_set) >= 1, "At least one `bbp_set` value must exist.")
        assert_(len(bbrec_set) >= 1, "At least one `bbrec_set` value must exist.")
        assert_(len(bbuec_set) >= 1, "At least one `bbuec_set` value must exist.")

        return {
            "pci_target_set": list(set(pci_target_set)),
            "bpf_set": list(set(bpf_set)),
            "bbp_set": list(set(bbp_set)),
            "bbrec_set": list(set(bbrec_set)),
            "bbuec_set": list(set(bbuec_set)),
        }

    def rule_check(self, context, calc_vals=None, data=None):
        pci_target_set = calc_vals["pci_target_set"]
        bpf_set = calc_vals["bpf_set"]
        bbp_set = calc_vals["bbp_set"]
        bbrec_set = calc_vals["bbrec_set"]
        bbuec_set = calc_vals["bbuec_set"]

        return (
            len(pci_target_set)
            == len(bpf_set)
            == len(bbp_set)
            == len(bbrec_set)
            == len(bbuec_set)
            == 1
            and bbp_set[0] != 0
            and std_equal(
                (bbuec_set[0] + (bpf_set[0] * bbrec_set[0]) / bbp_set[0]),
                pci_target_set[0],
            )
        )

    def get_fail_msg(self, context, calc_vals=None, data=None):
        pci_target_set = calc_vals["pci_target_set"]
        bpf_set = calc_vals["bpf_set"]
        bbp_set = calc_vals["bbp_set"]
        bbrec_set = calc_vals["bbrec_set"]
        bbuec_set = calc_vals["bbuec_set"]

        FAIL_MSG = ""
        if len(pci_target_set) != 1:
            FAIL_MSG = "Ruleset expects exactly one PCI Target value to be used in the project."
        elif len(bpf_set) != 1:
            FAIL_MSG = (
                "Ruleset expects exactly one BPF value to be used in the project."
            )
        elif len(bbp_set) != 1:
            FAIL_MSG = (
                "Ruleset expects exactly one BBP value to be used in the project."
            )
        elif len(bbrec_set) != 1:
            FAIL_MSG = (
                "Ruleset expects exactly one BBREC value to be used in the project."
            )
        elif len(bbuec_set) != 1:
            FAIL_MSG = (
                "Ruleset expects exactly one BBUEC value to be used in the project."
            )
        elif bbp_set[0] == 0:
            FAIL_MSG = "Ruleset expects baseline_building_performance_energy_cost to be greater than 0."

        return FAIL_MSG
