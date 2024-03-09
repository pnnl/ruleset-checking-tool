from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_instance
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.data_fns.table_G3_5_1_fns import table_G3_5_1_lookup
from rct229.rulesets.ashrae9012019.data_fns.table_G3_5_2_fns import table_G3_5_2_lookup
from rct229.rulesets.ashrae9012019.data_fns.table_G3_5_4_fns import table_G3_5_4_lookup
from rct229.rulesets.ashrae9012019.ruleset_functions.get_baseline_system_types import (
    get_baseline_system_types,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_system_type_compare import (
    baseline_system_type_compare,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_hvac_systems_5_6_serving_multiple_floors import (
    get_hvac_systems_5_6_serving_multiple_floors,
)
from rct229.utils.assertions import getattr_


APPLICABLE_SYS_TYPES = [
    HVAC_SYS.SYS_1,
    HVAC_SYS.SYS_1B,
    HVAC_SYS.SYS_2,
    HVAC_SYS.SYS_3,
    HVAC_SYS.SYS_3B,
    HVAC_SYS.SYS_4,
    HVAC_SYS.SYS_5,
    HVAC_SYS.SYS_5B,
    HVAC_SYS.SYS_6,
    HVAC_SYS.SYS_6B,
]


class Section10Rule7(RuleDefinitionListIndexedBase):
    """Rule 7 of ASHRAE 90.1-2019 Appendix G Section 10 (HVAC General)"""

    def __init__(self):
        super(Section10Rule7, self).__init__(
            rmrs_used=produce_ruleset_model_instance(
                USER=True, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=Section10Rule7.HVACRule(),
            index_rmr=BASELINE_0,
            id="10-7",
            description=(
                "Baseline shall be modeled with the COPnfcooling HVAC system efficiency per Tables G3.5.1-G3.5.6.  Where multiple HVAC zones or residential spaces are combined into a single thermal block the cooling efficiencies (for baseline HVAC System Types 3 and 4) shall be based on the equipment capacity of the thermal block divided by the number of HVAC zones or residential spaces."
            ),
            ruleset_section_title="HVAC General",
            standard_section="",
            is_primary_rule=True,
            rmr_context="ruleset_model_descriptions/0",
        )

    def is_applicable(self, context, data=None):
        rmd_b = context.BASELINE_0
        baseline_system_types_dict = get_baseline_system_types(rmd_b)
        baseline_sys_5_6_serve_more_than_one_flr_list = (
            get_hvac_systems_5_6_serving_multiple_floors(rmd_b).keys()
        )

        return any(
            baseline_system_type_compare(system_type, applicable_sys_type, True)
            and any(
                system_id not in baseline_sys_5_6_serve_more_than_one_flr_list
                for system_id in system_ids
            )
            for system_type, system_ids in baseline_system_types_dict.items()
            for applicable_sys_type in APPLICABLE_SYS_TYPES
        )

    def create_data(self, context, data):
        rmd_b = context.BASELINE_0
        baseline_system_types_dict = get_baseline_system_types(rmd_b)
        baseline_sys_serve_more_than_one_flr_list = (
            get_hvac_systems_5_6_serving_multiple_floors(rmd_b).keys()
        )

        return {
            "baseline_system_types_dict": {
                system_type: [
                    system_id
                    for system_id in system_list
                    if system_id not in baseline_sys_serve_more_than_one_flr_list
                ]
                for system_type, system_list in baseline_system_types_dict.items()
                if system_type in APPLICABLE_SYS_TYPES and system_list
            }
        }

    class HVACRule(RuleDefinitionBase):
        def __init__(self):
            super(Section10Rule7.HVACRule, self).__init__(
                rmrs_used=produce_ruleset_model_instance(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                required_fields={
                    "$": ["cooling_system"],
                    "cooling_system": [
                        "efficiency_metric_types",
                        "efficiency_metric_values",
                    ],
                },
            )

        def is_applicable(self, context, data=None):
            hvac_b = context.BASELINE_0
            hvac_id_b = hvac_b["id"]
            baseline_system_types_dict = data["baseline_system_types_dict"]

            return any(
                hvac_id_b in baseline_system_types_dict[system_type]
                for system_type in baseline_system_types_dict
            )

        def get_calc_vals(self, context, data=None):
            hvac_b = context.BASELINE_0
            cooling_system_b = hvac_b["cooling_system"]
            baseline_system_types_dict = data["baseline_system_types_dict"]
            hvac_system_type_b = next(
                (
                    system_type
                    for system_type, hvac_b_ids in baseline_system_types_dict.items()
                    if hvac_b["id"] in hvac_b_ids
                ),
                None,
            )

            total_cool_capacity_b = cooling_system_b.get("rated_total_cool_capacity")
            if total_cool_capacity_b is None:
                total_cool_capacity_b = cooling_system_b.get(
                    "design_total_cool_capacity"
                )

            if hvac_system_type_b in [HVAC_SYS.SYS_1, HVAC_SYS.SYS_1B, HVAC_SYS.SYS_2]:
                expected_baseline_eff_data = table_G3_5_4_lookup(hvac_system_type_b)
                most_conservative_eff_b = expected_baseline_eff_data[
                    "minimum_efficiency"
                ]

            elif hvac_system_type_b in [
                HVAC_SYS.SYS_3,
                HVAC_SYS.SYS_3B,
                HVAC_SYS.SYS_5,
                HVAC_SYS.SYS_5B,
                HVAC_SYS.SYS_6,
                HVAC_SYS.SYS_6B,
            ]:
                expected_baseline_eff_data = table_G3_5_1_lookup(total_cool_capacity_b)
                most_conservative_eff_b = expected_baseline_eff_data[
                    "most_conservative_efficiency"
                ]

            else:  # HVAC_SYS.SYS_4
                expected_baseline_eff_data = table_G3_5_2_lookup(
                    hvac_system_type_b,
                    "heat pumps, air-cooled (cooling mode)",
                    total_cool_capacity_b,
                )
                most_conservative_eff_b = expected_baseline_eff_data[
                    "most_conservative_efficiency"
                ]

            expected_eff_b = expected_baseline_eff_data["minimum_efficiency"]
            expected_eff_metric_b = expected_baseline_eff_data["efficiency_metric"]

            modeled_efficiency_values = getattr_(
                cooling_system_b, "CoolingSystem", "efficiency_values"
            )
            modeled_efficiency_metrics = getattr_(
                cooling_system_b, "CoolingSystem", "efficiency_metrics"
            )
            modeled_efficiency_b = next(
                (
                    eff
                    for eff, metric in zip(
                        modeled_efficiency_values, modeled_efficiency_metrics
                    )
                    if metric == expected_eff_metric_b
                ),
                None,
            )

            return {
                "total_cool_capacity_b": total_cool_capacity_b,
                "expected_baseline_eff_b": expected_eff_b,
                "expected_eff_metric": expected_eff_metric_b,
                "most_conservative_eff_b": most_conservative_eff_b,
                "modeled_efficiency_b": modeled_efficiency_b,
            }

        def rule_check(self, context, calc_vals=None, data=None):
            required_copnf_b = calc_vals["minimum_efficiency_copnf"]

            return
