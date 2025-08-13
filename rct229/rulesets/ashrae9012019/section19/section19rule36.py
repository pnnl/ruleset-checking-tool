from rct229.rule_engine.partial_rule_definition import PartialRuleDefinition
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.schema.config import ureg
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_one
from rct229.utils.pint_utils import CalcQ
from rct229.utils.std_comparisons import std_equal

ENERGY_RECOVERY = SchemaEnums.schema_enums["EnergyRecoveryOptions"]
REQ_SENSIBLE_EFFECTIVENESS = 0.5
REQ_LATENT_EFFECTIVENESS = 0.5


class PRM9012019Rule45j93(RuleDefinitionListIndexedBase):
    """Rule 36 of ASHRAE 90.1-2019 Appendix G Section 19 (HVAC - General)"""

    def __init__(self):
        super(PRM9012019Rule45j93, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=PRM9012019Rule45j93.HVACRule(),
            index_rmd=BASELINE_0,
            id="19-36",
            description="Baseline systems required to model energy recovery per G3.1.2.10 shall be modeled with a 50% enthalpy recovery ratio.",
            ruleset_section_title="HVAC - General",
            standard_section="Section G3.1-5(a)5 Building Envelope Modeling Requirements for the Proposed design",
            is_primary_rule=False,
            list_path="ruleset_model_descriptions[0].buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*]",
        )

    class HVACRule(PartialRuleDefinition):
        def __init__(self):
            super(PRM9012019Rule45j93.HVACRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                required_fields={"$": ["fan_system"]},
            )

        def is_applicable(self, context, data=None):
            hvac_b = context.BASELINE_0

            return (
                hvac_b.get("fan_system")
                and find_one("$.fan_system.air_energy_recovery", hvac_b)
                and find_one("$.fan_system.air_energy_recovery", hvac_b)
                != ENERGY_RECOVERY.NONE
            )

        def get_calc_vals(self, context, data=None):
            hvac_b = context.BASELINE_0
            energy_recovery_b = find_one("$.fan_system.air_energy_recovery", hvac_b)

            sensible_eff_b = getattr_(
                energy_recovery_b,
                "air_energy_recovery",
                "design_sensible_effectiveness",
            )
            latent_eff_b = getattr_(
                energy_recovery_b, "air_energy_recovery", "design_latent_effectiveness"
            )
            ERV_OA_airflow_b = getattr_(
                energy_recovery_b, "air_energy_recovery", "outdoor_airflow"
            )
            ERV_EA_airflow_b = getattr_(
                energy_recovery_b, "air_energy_recovery", "exhaust_airflow"
            )
            hvac_min_oa_flow_b = getattr_(
                hvac_b, "HVAC", "fan_system", "minimum_outdoor_airflow"
            )

            return {
                "sensible_eff_b": sensible_eff_b,
                "latent_eff_b": latent_eff_b,
                "ERV_OA_airflow_b": CalcQ("air_flow_rate", ERV_OA_airflow_b),
                "ERV_EA_airflow_b": CalcQ("air_flow_rate", ERV_EA_airflow_b),
                "hvac_min_oa_flow_b": CalcQ("air_flow_rate", hvac_min_oa_flow_b),
            }

        def applicability_check(self, context, calc_vals, data):
            sensible_eff_b = calc_vals["sensible_eff_b"]
            latent_eff_b = calc_vals["latent_eff_b"]
            ERV_OA_airflow_b = calc_vals["ERV_OA_airflow_b"]
            ERV_EA_airflow_b = calc_vals["ERV_EA_airflow_b"]
            hvac_min_oa_flow_b = calc_vals["hvac_min_oa_flow_b"]

            return (
                self.precision_comparison(sensible_eff_b, REQ_SENSIBLE_EFFECTIVENESS)
                and self.precision_comparison(latent_eff_b, REQ_LATENT_EFFECTIVENESS)
                and self.precision_comparison(ERV_OA_airflow_b, hvac_min_oa_flow_b)
                and self.precision_comparison(ERV_OA_airflow_b, ERV_EA_airflow_b)
            )

        def get_manual_check_required_msg(self, context, calc_vals=None, data=None):
            hvac_b = context.BASELINE_0
            hvac_id_b = hvac_b["id"]

            sensible_eff_b = calc_vals["sensible_eff_b"]
            latent_eff_b = calc_vals["latent_eff_b"]
            ERV_OA_airflow_b = calc_vals["ERV_OA_airflow_b"]
            ERV_EA_airflow_b = calc_vals["ERV_EA_airflow_b"]
            hvac_min_oa_flow_b = calc_vals["hvac_min_oa_flow_b"]

            return (
                f"{hvac_id_b} was modeled with a design sensible effectiveness of {sensible_eff_b}, a design latent effectiveness of {latent_eff_b}, and with {ERV_OA_airflow_b.to(ureg.cfm).m} outdoor air cfm and with {ERV_EA_airflow_b.to(ureg.cfm).m} exhaust air cfm going through the energy recovery device. "
                f"The HVAC system's minimum outside air CFM is {hvac_min_oa_flow_b.to(ureg.cfm).m}. Verify that it is equivalent to 50% enthalpy recovery ratio required by G3.1.2.10."
            )
