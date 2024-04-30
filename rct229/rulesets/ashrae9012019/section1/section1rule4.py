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


class Section1Rule4(RuleDefinitionBase):
    """Rule 4 of ASHRAE 90.1-2019 Appendix G Section 1 (Performance Calculations)"""

    def __init__(self):
        super(Section1Rule4, self).__init__(
            rmds_used=produce_ruleset_model_instance(
                USER=True,
                BASELINE_0=True,
                BASELINE_90=True,
                BASELINE_180=True,
                BASELINE_270=True,
                PROPOSED=True,
            ),
            rmds_used_optional=produce_ruleset_model_instance(
                BASELINE_90=True,
                BASELINE_180=True,
                BASELINE_270=True,
            ),
            id="1-4",
            description="The PCI shall be less than or equal to the PCIt when calculated in accordance with Standard 90.1 2019, Section 4.2.1.1",
            ruleset_section_title="Performance Calculations",
            standard_section="Section 4.2.1.1",
            is_primary_rule=True,
            rmd_context="ruleset_model_descriptions/0",
        )

    def get_calc_vals(self, context, data=None):
        rmd_u = context.USER
        rmd_b0 = context.BASELINE_0
        rmd_b90 = context.BASELINE_90
        rmd_b180 = context.BASELINE_180
        rmd_b270 = context.BASELINE_270
        rmd_p = context.PROPOSED

        pci_target_set = []
        pci_set = []
        for rmd in (rmd_u, rmd_b0, rmd_b90, rmd_b180, rmd_b270, rmd_p):
            if rmd is not None:
                pci_target_set.append(
                    find_one("$.output.performance_cost_index_target", rmd)
                )
                pci_set.append(
                    find_one(
                        "$.output.performance_cost_index",
                        rmd,
                    )
                )

        pci_target_set = list(set(filter(lambda x: x is not None, pci_target_set)))
        pci_set = list(set(filter(lambda x: x is not None, pci_set)))

        assert_(
            len(pci_target_set) >= 1, "At least one `pci_target_set` value must exist."
        )
        assert_(len(pci_set) >= 1, "At least one `pci_set` value must exist.")

        return {
            "pci_target_set": pci_target_set,
            "pci_set": pci_set,
        }

    def rule_check(self, context, calc_vals=None, data=None):
        pci_target_set = calc_vals["pci_target_set"]
        pci_set = calc_vals["pci_set"]

        return len(pci_target_set) == len(pci_set) == 1 and pci_set <= pci_target_set

    def get_fail_msg(self, context, calc_vals=None, data=None):
        pci_target_set = calc_vals["pci_target_set"]
        pci_set = calc_vals["pci_set"]

        FAIL_MSG = ""
        if len(pci_target_set) != 1:
            FAIL_MSG = "Ruleset expects exactly one PCI Target value to be used in the project."
        elif len(pci_set) != 1:
            FAIL_MSG = (
                "Ruleset expects exactly one PCI value to be used in the project."
            )

        return FAIL_MSG
