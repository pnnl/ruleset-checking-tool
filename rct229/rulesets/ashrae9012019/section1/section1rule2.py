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


class Section1Rule2(RuleDefinitionBase):
    """Rule 2 of ASHRAE 90.1-2019 Appendix G Section 1 (Performance Calculations)"""

    def __init__(self):
        super(Section1Rule2, self).__init__(
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
            id="1-2",
            description="The performance of the proposed design is calculated in accordance with Standard 90.1-2019 Appendix G, where Performance Cost Index = Proposed building performance (PBP) /Baseline building performance (BBP), "
            "where both the PBP and the BBP include all end-use load components associated with the building when calculating the Performance Cost Index (PCI).",
            ruleset_section_title="Performance Calculations",
            standard_section="Section G1.2.2",
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

        pci_set = []
        pbp_set = []
        bbp_set = []
        for rmd in (rmd_u, rmd_b0, rmd_b90, rmd_b180, rmd_b270, rmd_p):
            if rmd is not None:
                pci_set.append(find_one("$.output.performance_cost_index", rmd))
                pbp_set.append(
                    find_one(
                        "$.output.total_proposed_building_energy_cost_including_renewable_energy",
                        rmd,
                    )
                )
                bbp_set.append(
                    find_one("$.output.baseline_building_performance_energy_cost", rmd)
                )

        pci_set = filter_(pci_set, lambda x: x is not None)
        pbp_set = filter_(pbp_set, lambda x: x is not None)
        bbp_set = filter_(bbp_set, lambda x: x is not None)

        assert_(
            len(pci_set) >= 1, "At least one `performance_cost_index` value must exist."
        )
        assert_(
            len(pbp_set) >= 1,
            "At least one `total_proposed_building_energy_cost_including_renewable_energy` value must exist.",
        )
        assert_(
            len(bbp_set) >= 1,
            "At least one `baseline_building_performance_energy_cost` value must exist.",
        )

        return {
            "pci_set": list(set(pci_set)),
            "pbp_set": list(set(pbp_set)),
            "bbp_set": list(set(bbp_set)),
        }

    def rule_check(self, context, calc_vals=None, data=None):
        pci_set = calc_vals["pci_set"]
        pbp_set = calc_vals["pbp_set"]
        bbp_set = calc_vals["bbp_set"]

        return len(pci_set) == len(pbp_set) == len(bbp_set) == 1 and std_equal(
            pbp_set[0] / bbp_set[0], pci_set[0]
        )  # TODO: what if  bbp_set[0] == 0?

    def get_fail_msg(self, context, calc_vals=None, data=None):
        pci_set = calc_vals["pci_set"]
        pbp_set = calc_vals["pbp_set"]
        bbp_set = calc_vals["bbp_set"]

        FAIL_MSG = ""
        if len(pci_set) != 1:
            FAIL_MSG = "Ruleset expects exactly one PCI value to be used in the project"
        elif len(pbp_set) != 1:
            FAIL_MSG = "Ruleset expects exactly one PBP value to be used in the project"
        elif len(bbp_set) != 1:
            FAIL_MSG = "Ruleset expects exactly one BBP value to be used in the project"

        return FAIL_MSG
