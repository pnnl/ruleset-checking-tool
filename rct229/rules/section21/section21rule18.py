from rct229.data.schema_enums import schema_enums
from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals

APPLICABLE_SYS_TYPES = [
    "SYS-1",
    "SYS-5",
    "SYS-7",
    "SYS-11.2",
    "SYS-12",
    "SYS-1A",
    "SYS-7A",
    "SYS-11.2A",
    "SYS-12A",
]

FUEL_SOURCE_OPTION = schema_enums["EnergySourceOptions"]


class Section21Rule18(RuleDefinitionListIndexedBase):
    """Rule 18 of ASHRAE 90.1-2019 Appendix G Section 21 (Hot water loop)"""

    def __init__(self):
        super(Section21Rule18, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            each_rule=Section21Rule18.BoilerRule(),
            index_rmr="baseline",
            id="21-18",
            description="For baseline building, fossil fuel systems shall be modeled using natural gas as their fuel source. Exception: For fossil fuel systems where natural gas is not available for the proposed building site as determined by the rating authority, the baseline HVAC systems shall be modeled using propane as their fuel.",
            rmr_context="ruleset_model_instances/0",
            list_path="boilers[*]",
        )

    def is_applicable(self, context, data=None):
        rmi_b = context.baseline
        # FIXME: replace with baseline_system_types = get_baseline_system_types(rmi_b) when get_baseline_system_types
        #  is ready.
        baseline_system_types = {"SYS-7": ["hvac_sys_7"], "SYS-12": ["hvac_sys_12_a"]}
        # if any system type found in the APPLICABLE_SYS_TYPES then return applicable.
        return any(
            [key in APPLICABLE_SYS_TYPES for key in baseline_system_types.keys()]
        )

    class BoilerRule(RuleDefinitionBase):
        def __init__(self):
            super(Section21Rule18.BoilerRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
                required_fields={
                    "$": ["energy_source_type"],
                },
                manual_check_required_msg="Basline boiler fuel source is modeled as propane. Verify if natural gas is not available for the proposed building site as determined by the rating authority.",
            )

        def get_calc_vals(self, context, data=None):
            boiler_b = context.baseline
            boiler_energy_source_type_b = boiler_b["energy_source_type"]
            return {"boiler_energy_source_type_b": boiler_energy_source_type_b}

        def manual_check_required(self, context, calc_vals=None, data=None):
            boiler_energy_source_type_b = calc_vals["boiler_energy_source_type_b"]
            return boiler_energy_source_type_b == FUEL_SOURCE_OPTION.PROPANE

        def rule_check(self, context, calc_vals=None, data=None):
            boiler_energy_source_type_b = calc_vals["boiler_energy_source_type_b"]
            return boiler_energy_source_type_b == FUEL_SOURCE_OPTION.NATURAL_GAS
