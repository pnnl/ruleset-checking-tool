from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.utils.assertions import assert_
from rct229.utils.compare_standard_val import std_le
from rct229.utils.jsonpath_utils import find_one

APPLICABLE_LIMIT = 0.05


class PRM9012019Rule86h31(RuleDefinitionBase):
    """Rule 5 of ASHRAE 90.1-2019 Appendix G Section 1 (Performance Calculations)"""

    def __init__(self):
        super(PRM9012019Rule86h31, self).__init__(
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
            id="1-5",
            description="When on-site renewable energy generation exceeds the thresholds defined in Section 4.2.1.1, the methodology defined in this section shall be used to calculate the PCI.",
            ruleset_section_title="Performance Calculations",
            standard_section="Section 4.2.1.1",
            is_primary_rule=True,
        )

    def is_applicable(self, context, data=None):
        rmd_u = context.USER
        rmd_b0 = context.BASELINE_0
        rmd_b90 = context.BASELINE_90
        rmd_b180 = context.BASELINE_180
        rmd_b270 = context.BASELINE_270
        rmd_p = context.PROPOSED

        pbp_set = []
        bbp_set = []
        pbp_nre_set = []
        for rmd in (rmd_u, rmd_b0, rmd_b90, rmd_b180, rmd_b270, rmd_p):
            if rmd is not None:
                pbp_set.append(
                    find_one(
                        "$.output.total_proposed_building_energy_cost_including_renewable_energy",
                        rmd,
                    )
                )
                bbp_set.append(
                    find_one(
                        "$.output.baseline_building_performance_energy_cost",
                        rmd,
                    )
                )
                pbp_nre_set.append(
                    find_one(
                        "$.output.total_proposed_building_energy_cost_excluding_renewable_energy",
                        rmd,
                    )
                )

        pbp_set = list(set(filter(lambda x: x is not None, pbp_set)))
        bbp_set = list(set(filter(lambda x: x is not None, bbp_set)))
        pbp_nre_set = list(set(filter(lambda x: x is not None, pbp_nre_set)))

        assert_(
            len(pbp_set) >= 1,
            "Ruleset expects exactly one PBP value to be used in the project.",
        )
        assert_(
            len(bbp_set) >= 1,
            "Ruleset expects exactly one BBP value to be used in the project.",
        )
        assert_(
            len(pbp_nre_set) >= 1,
            "Ruleset expects exactly one PBP_nre value to be used in the project.",
        )
        assert_(
            bbp_set[0] > 0,
            "The `baseline_building_performance_energy_cost` value must be greater than 0.",
        )

        return (pbp_nre_set[0] - pbp_set[0]) / bbp_set[0] > APPLICABLE_LIMIT

    def get_calc_vals(self, context, data=None):
        rmd_u = context.USER
        rmd_b0 = context.BASELINE_0
        rmd_b90 = context.BASELINE_90
        rmd_b180 = context.BASELINE_180
        rmd_b270 = context.BASELINE_270
        rmd_p = context.PROPOSED

        pbp_set = []
        bbp_set = []
        pbp_nre_set = []
        pci_set = []
        pci_target_set = []
        for rmd in (rmd_u, rmd_b0, rmd_b90, rmd_b180, rmd_b270, rmd_p):
            if rmd is not None:
                pbp_set.append(
                    find_one(
                        "$.output.total_proposed_building_energy_cost_including_renewable_energy",
                        rmd,
                    )
                )
                bbp_set.append(
                    find_one(
                        "$.output.baseline_building_performance_energy_cost",
                        rmd,
                    )
                )
                pbp_nre_set.append(
                    find_one(
                        "$.output.total_proposed_building_energy_cost_excluding_renewable_energy",
                        rmd,
                    )
                )
                pci_set.append(
                    find_one(
                        "$.output.performance_cost_index",
                        rmd,
                    )
                )
                pci_target_set.append(
                    find_one(
                        "$.output.performance_cost_index_target",
                        rmd,
                    )
                )

        pbp_set = list(set(filter(lambda x: x is not None, pbp_set)))
        bbp_set = list(set(filter(lambda x: x is not None, bbp_set)))
        pbp_nre_set = list(set(filter(lambda x: x is not None, pbp_nre_set)))
        pci_set = list(set(filter(lambda x: x is not None, pci_set)))
        pci_target_set = list(set(filter(lambda x: x is not None, pci_target_set)))

        assert_(
            len(pci_set) >= 1,
            "Ruleset expects exactly one PCI value to be used in the project.",
        )
        assert_(
            len(pci_target_set) >= 1,
            "Ruleset expects exactly one PCI Target value to be used in the project.",
        )

        return {
            "pbp_set": pbp_set,
            "bbp_set": bbp_set,
            "pbp_nre_set": pbp_nre_set,
            "pci_set": pci_set,
            "pci_target_set": pci_target_set,
        }

    def rule_check(self, context, calc_vals=None, data=None):
        pbp_set = calc_vals["pbp_set"]
        bbp_set = calc_vals["bbp_set"]
        pbp_nre_set = calc_vals["pbp_nre_set"]
        pci_set = calc_vals["pci_set"]
        pci_target_set = calc_vals["pci_target_set"]

        return (
            len(pbp_set)
            == len(bbp_set)
            == len(pbp_nre_set)
            == len(pci_set)
            == len(pci_target_set)
            == 1
            and (
                pci_set[0]
                + ((pbp_nre_set[0] - pbp_set[0]) / bbp_set[0])
                - APPLICABLE_LIMIT
                < pci_target_set[0]
            )
            or self.precision_comparison(
                pci_set[0]
                + ((pbp_nre_set[0] - pbp_set[0]) / bbp_set[0])
                - APPLICABLE_LIMIT,
                pci_target_set[0],
            )
        )

    def is_tolerance_fail(self, context, calc_vals=None, data=None):
        pbp_set = calc_vals["pbp_set"]
        bbp_set = calc_vals["bbp_set"]
        pbp_nre_set = calc_vals["pbp_nre_set"]
        pci_set = calc_vals["pci_set"]
        pci_target_set = calc_vals["pci_target_set"]

        return len(pbp_set) == len(bbp_set) == len(pbp_nre_set) == len(pci_set) == len(
            pci_target_set
        ) == 1 and std_le(
            pci_set[0]
            + ((pbp_nre_set[0] - pbp_set[0]) / bbp_set[0])
            - APPLICABLE_LIMIT,
            pci_target_set[0],
        )
