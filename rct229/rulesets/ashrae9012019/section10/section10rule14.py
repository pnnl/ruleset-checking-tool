from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_instance
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.data_fns.table_G3_5_2_fns import table_G3_5_2_lookup
from rct229.rulesets.ashrae9012019.data_fns.table_G3_5_4_fns import table_G3_5_4_lookup
from rct229.rulesets.ashrae9012019.data_fns.table_G3_5_5_fns import table_G3_5_5_lookup
from rct229.rulesets.ashrae9012019.ruleset_functions.get_baseline_system_types import (
    get_baseline_system_types,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_system_type_compare import (
    baseline_system_type_compare,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_hvac_zone_list_w_area_dict import (
    get_hvac_zone_list_w_area_dict,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
)
from rct229.utils.utility_functions import (
    find_exactly_one_zone,
)
from rct229.utils.assertions import getattr_
from rct229.schema.config import ureg

APPLICABLE_SYS_TYPES = [
    HVAC_SYS.SYS_2,
    HVAC_SYS.SYS_3,
    HVAC_SYS.SYS_3A,
    HVAC_SYS.SYS_4,
    HVAC_SYS.SYS_9,
]

HEATPUMP_CAPACITY_LOW_RANGE_SAMPLE = 64999 * ureg("Btu/hr")
FURNACE_CAPACITY_LOW_RANGE_SAMPLE = 224999 * ureg("Btu/hr")
HEATPUMP_CAPACITY_LOW_THRESHOLD = 65000 * ureg("Btu/hr")
FURNACE_CAPACITY_LOW_THREHSOLD = 225000 * ureg("Btu/hr")


class Section10Rule14(RuleDefinitionListIndexedBase):
    """Rule 14 of ASHRAE 90.1-2019 Appendix G Section 10 (HVAC General)"""

    def __init__(self):
        super(Section10Rule14, self).__init__(
            rmrs_used=produce_ruleset_model_instance(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=Section10Rule14.HVACRule(),
            index_rmr=BASELINE_0,
            id="10-14",
            description=(
                "Baseline shall be modeled with the heating HVAC system efficiency per Tables G3.5.1-G3.5.6 (applies only to the heating efficiency of baseline furnaces and heat pumps). Where multiple HVAC zones or residential spaces are combined into a single thermal block the heating efficiencies (for baseline HVAC System Types 3 and 4) shall be based on the equipment capacity of the thermal block divided by the number of HVAC zones or residential spaces."
            ),
            ruleset_section_title="HVAC General",
            standard_section="",
            is_primary_rule=True,
            rmr_context="ruleset_model_descriptions/0",
        )

    def is_applicable(self, context, data=None):
        rmd_b = context.BASELINE_0
        baseline_system_types_dict = get_baseline_system_types(rmd_b)

        return any(
            baseline_system_type_compare(system_type, applicable_sys_type, True)
            for system_type in baseline_system_types_dict
            for applicable_sys_type in APPLICABLE_SYS_TYPES
        )

    def create_data(self, context, data):
        rmd_b = context.BASELINE_0
        baseline_system_types_dict = get_baseline_system_types(rmd_b)
        baseline_system_zones_served_dict = {
            hvac_id: [
                find_exactly_one_zone(rmd_b, zone_id)
                for zone_id in hvac_data["zone_list"]
            ]
            for hvac_id, hvac_data in get_hvac_zone_list_w_area_dict(rmd_b).items()
        }

        return {
            "baseline_system_types_dict": {
                system_type: [system_id for system_id in system_list]
                for system_type, system_list in baseline_system_types_dict.items()
                if system_type in APPLICABLE_SYS_TYPES and system_list
            },
            "baseline_system_zones_served_dict": baseline_system_zones_served_dict,
        }

    class HVACRule(RuleDefinitionBase):
        def __init__(self):
            super(Section10Rule14.HVACRule, self).__init__(
                rmrs_used=produce_ruleset_model_instance(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                required_fields={
                    "$": ["heating_system"],
                    "heating_system": [
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
            heating_system_b = data["heating_system"]
            cooling_system_b = hvac_b.get("cooling_system")
            baseline_system_types_dict_b = data["baseline_system_types_dict"]
            hvac_zone_list_w_area_dict_b = data["baseline_system_zones_served_dict"]
            zone_list_b = hvac_zone_list_w_area_dict_b[hvac_b.id]
            is_zone_agg_factor_undefined_and_needed = False

            hvac_system_type_b = next(
                (
                    system_type
                    for system_type, hvac_b_ids in baseline_system_types_dict_b.items()
                    if hvac_b["id"] in hvac_b_ids
                ),
                None,
            )

            if hvac_system_type_b in [
                HVAC_SYS.SYS_2,
                HVAC_SYS.SYS_3,
                HVAC_SYS.SYS_3A,
                HVAC_SYS.SYS_9,
            ]:
                total_capacity_b = heating_system_b.get("rated_capacity")

                if total_capacity_b is None:
                    total_capacity_b = heating_system_b.get("design_capacity")

            else:  # HVAC_SYS.SYS_4
                total_capacity_b = cooling_system_b.get("rated_total_cool_capacity")

                if total_capacity_b is None:
                    total_capacity_b = cooling_system_b.get(
                        "design_total_cool_capacity"
                    )

            if total_capacity_b is not None and hvac_system_type_b in [
                HVAC_SYS.SYS_3,
                HVAC_SYS.SYS_3A,
                HVAC_SYS.SYS_4,
            ]:
                hvac_zone_aggregation_factor = zone_list_b[0].get("aggregation_factor")
                if hvac_zone_aggregation_factor is not None:
                    total_capacity_b = total_capacity_b / hvac_zone_aggregation_factor

                elif (
                    hvac_zone_aggregation_factor is None
                    and hvac_system_type_b in [HVAC_SYS.SYS_3, HVAC_SYS.SYS_3A]
                    and total_capacity_b > FURNACE_CAPACITY_LOW_THREHSOLD
                ):
                    is_zone_agg_factor_undefined_and_needed = True

                elif (
                    hvac_zone_aggregation_factor is None
                    and hvac_system_type_b == HVAC_SYS.SYS_4
                    and total_capacity_b > HEATPUMP_CAPACITY_LOW_THRESHOLD
                ):
                    is_zone_agg_factor_undefined_and_needed = True

            if hvac_system_type_b == HVAC_SYS.SYS_2:
                expected_baseline_eff_data = table_G3_5_4_lookup(hvac_system_type_b)

            elif hvac_system_type_b in [HVAC_SYS.SYS_3, HVAC_SYS.SYS_3A]:
                if total_capacity_b is None:
                    expected_baseline_eff_data = table_G3_5_5_lookup(
                        "Warm-air furnace, gas-fired",
                        FURNACE_CAPACITY_LOW_RANGE_SAMPLE,
                    )
                else:
                    expected_baseline_eff_data = table_G3_5_5_lookup(
                        "Warm-air furnace, gas-fired",
                        total_capacity_b,
                    )

            elif hvac_system_type_b == HVAC_SYS.SYS_9:
                if total_capacity_b is None:
                    expected_baseline_eff_data = table_G3_5_5_lookup(
                        "Warm-air unit heaters, gas-fired",
                        FURNACE_CAPACITY_LOW_RANGE_SAMPLE,
                    )
                else:
                    expected_baseline_eff_data = table_G3_5_5_lookup(
                        "Warm-air unit heaters, gas-fired", total_capacity_b
                    )

            else:  # HVAC_SYS.SYS_4
                if total_capacity_b is None:
                    expected_baseline_eff_data = [
                        table_G3_5_2_lookup(
                            "heat pumps, air-cooled (heating mode)",
                            "47F db/43F wb",
                            HEATPUMP_CAPACITY_LOW_RANGE_SAMPLE,
                        ),
                        table_G3_5_2_lookup(
                            "heat pumps, air-cooled (heating mode)",
                            "17F db/15F wb",
                            HEATPUMP_CAPACITY_LOW_RANGE_SAMPLE,
                        ),
                    ]

                else:
                    expected_baseline_eff_data = [
                        table_G3_5_2_lookup(
                            "heat pumps, air-cooled (heating mode)",
                            "47F db/43F wb",
                            total_capacity_b,
                        ),
                        table_G3_5_2_lookup(
                            "heat pumps, air-cooled (heating mode)",
                            "17F db/15F wb",
                            total_capacity_b,
                        ),
                    ]

            modeled_efficiency_values = getattr_(
                heating_system_b, "HeatingSystem", "efficiency_metric_values"
            )
            modeled_efficiency_metrics = getattr_(
                heating_system_b, "HeatingSystem", "efficiency_metric_types"
            )

            if hvac_system_type_b in [
                HVAC_SYS.SYS_2,
                HVAC_SYS.SYS_3,
                HVAC_SYS.SYS_3A,
                HVAC_SYS.SYS_9,
            ]:
                expected_high_temp_eff_b = None
                expected_low_temp_eff_b = None
                modeled_high_temp_eff_b = None
                modeled_low_temp_eff_b = None
                expected_eff_b = expected_baseline_eff_data["minimum_efficiency"]
                expected_eff_metric_b = expected_baseline_eff_data["efficiency_metric"]

                modeled_eff_b = next(
                    (
                        eff
                        for eff, metric in zip(
                            modeled_efficiency_values, modeled_efficiency_metrics
                        )
                        if metric == expected_eff_metric_b
                    ),
                    None,
                )

            else:
                expected_eff_b = None
                modeled_eff_b = None
                expected_high_temp_eff_b = expected_baseline_eff_data[0][
                    "minimum_efficiency"
                ]
                expected_high_temp_eff_metric_b = expected_baseline_eff_data[0][
                    "efficiency_metric"
                ]
                expected_low_temp_eff_b = expected_baseline_eff_data[1][
                    "minimum_efficiency"
                ]
                expected_low_temp_eff_metric_b = expected_baseline_eff_data[1][
                    "efficiency_metric"
                ]

                modeled_high_temp_eff_b = next(
                    (
                        eff
                        for eff, metric in zip(
                            modeled_efficiency_values, modeled_efficiency_metrics
                        )
                        if metric == expected_high_temp_eff_metric_b
                    ),
                    None,
                )
                modeled_low_temp_eff_b = next(
                    (
                        eff
                        for eff, metric in zip(
                            modeled_efficiency_values, modeled_efficiency_metrics
                        )
                        if metric == expected_low_temp_eff_metric_b
                    ),
                    None,
                )

            return {
                "hvac_system_type_b": hvac_system_type_b,
                "total_capacity_b": total_capacity_b,
                "is_zone_agg_factor_undefined_and_needed": is_zone_agg_factor_undefined_and_needed,
                "expected_eff_b": expected_eff_b,
                "modeled_eff_b": modeled_eff_b,
                "expected_high_temp_eff_b": expected_high_temp_eff_b,
                "modeled_high_temp_eff_b": modeled_high_temp_eff_b,
                "expected_low_temp_eff_b": expected_low_temp_eff_b,
                "modeled_low_temp_eff_b": modeled_low_temp_eff_b,
            }

        def manual_check_required(self, context, calc_vals=None, data=None):
            return

        def get_manual_check_required_msg(self, context, calc_vals=None, data=None):
            return

        def rule_check(self, context, calc_vals=None, data=None):
            expected_eff_b = calc_vals["expected_eff_b"]
            modeled_eff_b = calc_vals["modeled_eff_b"]

            return modeled_eff_b == expected_eff_b
