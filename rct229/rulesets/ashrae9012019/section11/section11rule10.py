from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.ruleset_functions.get_swh_components_associated_with_each_swh_bat import (
    get_swh_components_associated_with_each_swh_bat
)
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.jsonpath_utils import find_all


SWHEfficiencyMetricOptions = SchemaEnums.schema_enums["ServiceWaterHeatingEfficiencyMetricOptions"]


class Section11Rule10(RuleDefinitionListIndexedBase):
    """Rule 10 of ASHRAE 90.1-2019 Appendix G Section 11 (Service Water Heating)"""

    def __init__(self):
        super(Section11Rule10, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=True
            ),
            each_rule=Section11Rule10.RMDRule(),
            index_rmd=BASELINE_0,
            id="11-10",
            description="The service water heating system type in the baseline building design shall match the minimum efficiency requirements in Section 7.4.2.",
            ruleset_section_title="Service Water Heating",
            standard_section="Table G3.1 #11, baseline column, a & b",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0]",
        )

    class RMDRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section11Rule10.RMDRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                each_rule=Section11Rule10.RMDRule.SWHEquipRule(),
                index_rmd=BASELINE_0,
                list_path="$.service_water_heating_equipment[*]",
            )

        def is_applicable(self, context, data=None):
            rmd_b = context.BASELINE_0

            swh_equipment_list_b = find_all(
                "$.service_water_heating_equipment[*]", rmd_b
            )

            return swh_equipment_list_b

        class SWHEquipRule(RuleDefinitionBase):
            def __init__(self):
                super(Section11Rule10.RMDRule.SWHEquipRule, self).__init__(
                    rmds_used=produce_ruleset_model_description(
                        USER=False,
                        BASELINE_0=True,
                        PROPOSED=False,
                    ),
                    required_fields={
                        "$": ["efficiency_metric_types", "efficiency_metric_values"],
                    },
                )

            def get_calc_vals(self, context, data=None):
                table_f_2 = [
                    {
                        "Product Class": "Gas-fired storage water heater",
                        "Storage Volume (min threshold, inclusive?)": (20, True),
                        "Storage Volume (max threshold, inclusive?)": (55, True),
                        "Draw Pattern": "Very small",
                        "Efficiency (value/equation, metric)": (lambda v_r: 0.3456 - (0.0020 * v_r), SWHEfficiencyMetricOptions.UNIFORM_ENERGY_FACTOR),
                    },
                    {
                        "Product Class": "Gas-fired storage water heater",
                        "Storage Volume (min threshold, inclusive?)": (20, True),
                        "Storage Volume (max threshold, inclusive?)": (55, True),
                        "Draw Pattern": "Low",
                        "Efficiency (value/equation, metric)": (lambda v_r: 0.5982 - (0.0019 * v_r), SWHEfficiencyMetricOptions.UNIFORM_ENERGY_FACTOR),
                    },
                    {
                        "Product Class": "Gas-fired storage water heater",
                        "Storage Volume (min threshold, inclusive?)": (20, True),
                        "Storage Volume (max threshold, inclusive?)": (55, True),
                        "Draw Pattern": "Medium",
                        "Efficiency (value/equation, metric)": (lambda v_r: 0.6483 - (0.0017 * v_r), SWHEfficiencyMetricOptions.UNIFORM_ENERGY_FACTOR),
                    },
                    {
                        "Product Class": "Gas-fired storage water heater",
                        "Storage Volume (min threshold, inclusive?)": (20, True),
                        "Storage Volume (max threshold, inclusive?)": (55, True),
                        "Draw Pattern": "High",
                        "Efficiency (value/equation, metric)": (lambda v_r: 0.6920 - (0.0013 * v_r), SWHEfficiencyMetricOptions.UNIFORM_ENERGY_FACTOR),
                    },
                    {
                        "Product Class": "Gas-fired storage water heater",
                        "Storage Volume (min threshold, inclusive?)": (55, False),
                        "Storage Volume (max threshold, inclusive?)": (100, True),
                        "Draw Pattern": "Very small",
                        "Efficiency (value/equation, metric)": (lambda v_r: 0.6470 - (0.0006 * v_r), SWHEfficiencyMetricOptions.UNIFORM_ENERGY_FACTOR),
                    },
                    {
                        "Product Class": "Gas-fired storage water heater",
                        "Storage Volume (min threshold, inclusive?)": (55, False),
                        "Storage Volume (max threshold, inclusive?)": (100, True),
                        "Draw Pattern": "Low",
                        "Efficiency (value/equation, metric)": (lambda v_r: 0.7689 - (0.0005 * v_r), SWHEfficiencyMetricOptions.UNIFORM_ENERGY_FACTOR),
                    },
                    {
                        "Product Class": "Gas-fired storage water heater",
                        "Storage Volume (min threshold, inclusive?)": (55, False),
                        "Storage Volume (max threshold, inclusive?)": (100, True),
                        "Draw Pattern": "Medium",
                        "Efficiency (value/equation, metric)": (lambda v_r: 0.7897 - (0.0004 * v_r), SWHEfficiencyMetricOptions.UNIFORM_ENERGY_FACTOR),
                    },
                    {
                        "Product Class": "Gas-fired storage water heater",
                        "Storage Volume (min threshold, inclusive?)": (55, False),
                        "Storage Volume (max threshold, inclusive?)": (100, True),
                        "Draw Pattern": "High",
                        "Efficiency (value/equation, metric)": (lambda v_r: 0.8072 - (0.0003 * v_r), SWHEfficiencyMetricOptions.UNIFORM_ENERGY_FACTOR),
                    },
                    {
                        "Product Class": "Electric storage water heaters",
                        "Storage Volume (min threshold, inclusive?)": (20, True),
                        "Storage Volume (max threshold, inclusive?)": (55, True),
                        "Draw Pattern": "Very small",
                        "Efficiency (value/equation, metric)": (lambda v_r: 0.8808 - (0.0008 * v_r), SWHEfficiencyMetricOptions.UNIFORM_ENERGY_FACTOR),
                    },
                    {
                        "Product Class": "Electric storage water heaters",
                        "Storage Volume (min threshold, inclusive?)": (20, True),
                        "Storage Volume (max threshold, inclusive?)": (55, True),
                        "Draw Pattern": "Low",
                        "Efficiency (value/equation, metric)": (lambda v_r: 0.9254 - (0.0003 * v_r), SWHEfficiencyMetricOptions.UNIFORM_ENERGY_FACTOR),
                    },
                    {
                        "Product Class": "Electric storage water heaters",
                        "Storage Volume (min threshold, inclusive?)": (20, True),
                        "Storage Volume (max threshold, inclusive?)": (55, True),
                        "Draw Pattern": "Medium",
                        "Efficiency (value/equation, metric)": (lambda v_r: 0.9307 - (0.0002 * v_r), SWHEfficiencyMetricOptions.UNIFORM_ENERGY_FACTOR),
                    },
                    {
                        "Product Class": "Electric storage water heaters",
                        "Storage Volume (min threshold, inclusive?)": (20, True),
                        "Storage Volume (max threshold, inclusive?)": (55, True),
                        "Draw Pattern": "High",
                        "Efficiency (value/equation, metric)": (lambda v_r: 0.9349 - (0.0001 * v_r), SWHEfficiencyMetricOptions.UNIFORM_ENERGY_FACTOR),
                    },
                    {
                        "Product Class": "Electric storage water heaters",
                        "Storage Volume (min threshold, inclusive?)": (55, False),
                        "Storage Volume (max threshold, inclusive?)": (100, True),
                        "Draw Pattern": "Very small",
                        "Efficiency (value/equation, metric)": (lambda v_r: 1.9236 - (0.0011 * v_r), SWHEfficiencyMetricOptions.UNIFORM_ENERGY_FACTOR),
                    },
                    {
                        "Product Class": "Electric storage water heaters",
                        "Storage Volume (min threshold, inclusive?)": (55, False),
                        "Storage Volume (max threshold, inclusive?)": (100, True),
                        "Draw Pattern": "Low",
                        "Efficiency (value/equation, metric)": (lambda v_r: 2.0440 - (0.0011 * v_r), SWHEfficiencyMetricOptions.UNIFORM_ENERGY_FACTOR),
                    },
                    {
                        "Product Class": "Electric storage water heaters",
                        "Storage Volume (min threshold, inclusive?)": (55, False),
                        "Storage Volume (max threshold, inclusive?)": (100, True),
                        "Draw Pattern": "Medium",
                        "Efficiency (value/equation, metric)": (lambda v_r: 2.1171 - (0.0011 * v_r), SWHEfficiencyMetricOptions.UNIFORM_ENERGY_FACTOR),
                    },
                    {
                        "Product Class": "Electric storage water heaters",
                        "Storage Volume (min threshold, inclusive?)": (55, False),
                        "Storage Volume (max threshold, inclusive?)": (100, True),
                        "Draw Pattern": "High",
                        "Efficiency (value/equation, metric)": (lambda v_r: 2.2418 - (0.0011 * v_r), SWHEfficiencyMetricOptions.UNIFORM_ENERGY_FACTOR),
                    }
                ]





                pass
                # return {
                #     "tank_type_b": tank_type_b,
                #     "storage_volume_b": storage_volume_b,
                #     "expected_efficiency_b": expected_efficiency_b,
                #     "standby_loss_target_b": standby_loss_target_b,
                #     "modeled_efficiency_b": modeled_efficiency_b,
                #     "modeled_standby_loss_b": modeled_standby_loss_b,
                # }

            def manual_check_required(self, context, calc_vals=None, data=None):
                pass

            def get_manual_check_required_msg(self, context, calc_vals=None, data=None):
                pass

            def rule_check(self, context, calc_vals=None, data=None):
                pass
