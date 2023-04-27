from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.rulesets.ashrae9012019.ruleset_functions.get_dict_of_zones_and_terminal_units_served_by_hvac_sys import (
    get_dict_of_zones_and_terminal_units_served_by_hvac_sys,
)
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all



class Section19Rule21(RuleDefinitionListIndexedBase):
    """Rule 21 of ASHRAE 90.1-2019 Appendix G Section 19 (HVAC - General)"""

    def __init__(self):
        super(Section19Rule21, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            each_rule=Section19Rule21.HVACRule(),
            index_rmr="baseline",
            id="19-21",
            description="Baseline systems with >= 5,000 CFM supply air and >= 70 %OA shall have energy recovery modeled in the baseline design model (this RDS does not check the modeled value for the enthalpy recovery ratio). The following exceptions apply:"
                        "1. Systems serving spaces that are not cooled and that are heated to less than 60°F."
                        "2. Systems exhausting toxic, flammable, or corrosive fumes or paint or dust. This exception shall only be used if exhaust air energy recovery is not used in the proposed design."
                        "3. Commercial kitchen hoods (grease) classified as Type 1 by NFPA 96. This exception shall only be used if exhaust air energy recovery is not used in the proposed design."
                        "4. Heating systems in Climate Zones 0 through 3."
                        "5. Cooling systems in Climate Zones 3C, 4C, 5B, 5C, 6B, 7, and 8."
                        "6. Where the largest exhaust source is less than 75% of the design outdoor airflow. This exception shall only be used if exhaust air energy recovery is not used in the proposed design."
                        "7. Systems requiring dehumidification that employ energy recovery in series with the cooling coil. This exception shall only be used if exhaust air energy recovery and series-style energy recovery coils are not used in the proposed design.",
            ruleset_section_title="HVAC - General",
            standard_section=" Section G3.1.2.10 and exceptions 1-7",
            is_primary_rule=True,
            rmr_context="ruleset_model_instances/0",
            list_path="$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*]",
        )

    def create_data(self, context, data):
        rmi_b = context.baseline



        return {}

    class HVACRule(RuleDefinitionBase):
        def __init__(self):
            super(Section19Rule21.HVACRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
            )

        def is_applicable(self, context, data=None):
            hvac_b = context.baseline
            hvac_id_b = hvac_b["id"]
            hvac_id_to_flags = data["hvac_id_to_flags"]

            return (
                hvac_id_to_flags[hvac_id_b]["is_hvac_sys_heating_type_furnace_flag"]
                or hvac_id_to_flags[hvac_id_b][
                    "is_hvac_sys_heating_type_heat_pump_flag"
                ]
                or hvac_id_to_flags[hvac_id_b]["is_hvac_sys_cooling_type_dx_flag"]
            )

        def get_calc_vals(self, context, data=None):
            hvac_b = context.baseline
            hvac_id_b = hvac_b["id"]


        def rule_check(self, context, calc_vals=None, data=None):
            pass
