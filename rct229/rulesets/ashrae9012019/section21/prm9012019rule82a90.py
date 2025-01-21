from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_baseline_system_types import (
    get_baseline_system_types,
)
from rct229.schema.schema_enums import SchemaEnums

APPLICABLE_SYS_TYPES = [
    HVAC_SYS.SYS_1,
    HVAC_SYS.SYS_1A,
    HVAC_SYS.SYS_5,
    HVAC_SYS.SYS_7,
    HVAC_SYS.SYS_7A,
    HVAC_SYS.SYS_11_2,
    HVAC_SYS.SYS_11_2A,
    HVAC_SYS.SYS_12,
    HVAC_SYS.SYS_12A,
]

FUEL_SOURCE = SchemaEnums.schema_enums["EnergySourceOptions"]


class PRM9012019Rule82a90(RuleDefinitionListIndexedBase):
    """Rule 18 of ASHRAE 90.1-2019 Appendix G Section 21 (Hot water loop)"""

    def __init__(self):
        super(PRM9012019Rule82a90, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=PRM9012019Rule82a90.BoilerRule(),
            index_rmd=BASELINE_0,
            id="21-18",
            description="For baseline building, fossil fuel systems shall be modeled using natural gas as their fuel source. Exception: For fossil fuel systems where natural gas is not available for the proposed building site as determined by the rating authority, the baseline HVAC systems shall be modeled using propane as their fuel.",
            ruleset_section_title="HVAC - Water Side",
            standard_section="Section G3.1.2.1 General Baseline HVAC System Requirements - Equipment Efficiencies",
            is_primary_rule=True,
            rmd_context="ruleset_model_descriptions/0",
            list_path="boilers[*]",
        )

    def is_applicable(self, context, data=None):
        rmd_b = context.BASELINE_0
        baseline_system_types_dict = get_baseline_system_types(rmd_b)
        # create a list containing all HVAC systems that are modeled in the rmd_b
        available_type_list = [
            hvac_type
            for hvac_type in baseline_system_types_dict
            if len(baseline_system_types_dict[hvac_type]) > 0
        ]
        return any(
            [
                available_type in APPLICABLE_SYS_TYPES
                for available_type in available_type_list
            ]
        )

    class BoilerRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012019Rule82a90.BoilerRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                required_fields={
                    "$": ["energy_source_type"],
                },
                manual_check_required_msg="Baseline boiler fuel source is modeled as propane. Verify if natural gas is not available for the proposed building site as determined by the rating authority.",
            )

        def get_calc_vals(self, context, data=None):
            boiler_b = context.BASELINE_0
            boiler_energy_source_type_b = boiler_b["energy_source_type"]
            return {"boiler_energy_source_type_b": boiler_energy_source_type_b}

        def manual_check_required(self, context, calc_vals=None, data=None):
            boiler_energy_source_type_b = calc_vals["boiler_energy_source_type_b"]
            return boiler_energy_source_type_b == FUEL_SOURCE.PROPANE

        def rule_check(self, context, calc_vals=None, data=None):
            boiler_energy_source_type_b = calc_vals["boiler_energy_source_type_b"]
            return boiler_energy_source_type_b == FUEL_SOURCE.NATURAL_GAS
