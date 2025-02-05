from rct229.rule_engine.partial_rule_definition import PartialRuleDefinition
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.ruleset_functions.get_heat_rejection_loops_connected_to_baseline_systems import get_heat_rejection_loops_connected_to_baseline_systems
from rct229.schema.config import ureg
from rct229.utils.assertions import getattr_
from rct229.utils.pint_utils import ZERO, CalcQ
from rct229.utils.jsonpath_utils import find_all
FAN_SHAFT_POWER_FACTOR = 0.9
HEAT_REJ_EFF_LIMIT = 38.2 * ureg('gpm/hp')


class PRM9012019Rule04g06(RuleDefinitionListIndexedBase):
    """Rule 17 of ASHRAE 90.1-2019 Appendix G Section 22 (Chilled water loop)"""

    def __init__(self):
        super(PRM9012019Rule04g06, self).__init__(rmds_used=
            produce_ruleset_model_description(USER=False, BASELINE_0=True,
            PROPOSED=False), each_rule=PRM9012019Rule04g06.
            HeatRejectionRule(), index_rmd=BASELINE_0, id='section22rule17',
            description=
            'The baseline heat rejection device shall have an efficiency of 38.2 gpm/hp.'
            , ruleset_section_title='HVAC - Chiller', standard_section=
            'Section 22 CHW&CW Loop', is_primary_rule=False, rmd_context=
            'ruleset_model_descriptions/0', list_path='$.heat_rejections[*]')

    def is_applicable(self, context, data=None):
        rmd_b = context.BASELINE_0
        return bool(find_all('$.heat_rejections[*]', rmd_b))

    def create_data(self, context, data):
        rmd_b = context.BASELINE_0
        heat_rejection_loop_ids_b = (
            get_heat_rejection_loops_connected_to_baseline_systems(rmd_b))
        return {'heat_rejection_loop_ids_b': heat_rejection_loop_ids_b}


    class HeatRejectionRule(PartialRuleDefinition):

        def __init__(self):
            super(PRM9012019Rule04g06.HeatRejectionRule, self).__init__(
                rmds_used=produce_ruleset_model_description(USER=False,
                BASELINE_0=True, PROPOSED=False), required_fields={'$': [
                'loop', 'rated_water_flowrate']}, precision={
                'heat_rejection_efficiency_b': {'precision': 0.1, 'unit':
                'gpm/hp'}})

        def is_applicable(self, context, data=None):
            heat_rejection_b = context.BASELINE_0
            heat_rejection_loop_ids_b = data['heat_rejection_loop_ids_b']
            heat_rejection_loop_b = heat_rejection_b['loop']
            return heat_rejection_loop_b in heat_rejection_loop_ids_b

        def get_calc_vals(self, context, data=None):
            heat_rejection_b = context.BASELINE_0
            fan_shaft_power_b = heat_rejection_b['fan_shaft_power'
                ] if heat_rejection_b.get('fan_shaft_power') else getattr_(
                heat_rejection_b, 'heat_rejections',
                'fan_motor_nameplate_power'
                ) * FAN_SHAFT_POWER_FACTOR * getattr_(heat_rejection_b,
                'heat_rejections', 'fan_motor_efficiency')
            rated_water_flowrate_b = heat_rejection_b['rated_water_flowrate']
            heat_rejection_efficiency_b = (0.0 if fan_shaft_power_b == ZERO
                .POWER else rated_water_flowrate_b / fan_shaft_power_b)
            return {'fan_shaft_power_b': CalcQ('electric_power',
                fan_shaft_power_b), 'rated_water_flowrate_b': CalcQ(
                'volumetric_flow_rate', rated_water_flowrate_b),
                'heat_rejection_efficiency_b': CalcQ(
                'liquid_flow_rate_per_power', heat_rejection_efficiency_b)}

        def get_manual_check_required_msg(self, context, calc_vals=None,
            data=None):
            heat_rejection_b = context.BASELINE_0
            additional_note_for_no_shaft_power_b = ('' if heat_rejection_b.
                get('fan_shaft_power') else
                f"*Note: The fan shaft power for {heat_rejection_b['id']} was not given. For this evaluation, the fan shaft power was calculated using a rule of thumb where fan_shaft_power = fan_motor_nameplate_power * {FAN_SHAFT_POWER_FACTOR} * fan_motor_efficiency."
                )
            heat_rejection_efficiency_b = calc_vals[
                'heat_rejection_efficiency_b']
            heat_rejection_efficiency_in_gpm_per_hp_b = (
                heat_rejection_efficiency_b)
            if self.precision_comparison['heat_rejection_efficiency_b'](
                heat_rejection_efficiency_b, HEAT_REJ_EFF_LIMIT):
                undetermined_msg = (
                    f'The project includes a cooling tower. We calculated the cooling tower efficiency to be correct at 38.2 gpm/hp. However, it was not possible to verify that the modeling inputs correspond to the rating conditions in Table 6.8.1-7. {additional_note_for_no_shaft_power_b}'
                    )
            elif heat_rejection_efficiency_b > HEAT_REJ_EFF_LIMIT:
                undetermined_msg = (
                    f'The project includes a cooling tower. We calculated the cooling tower efficiency to be {heat_rejection_efficiency_in_gpm_per_hp_b}, which is greater than the required efficiency of 38.2 gpm/hp, resulting in a more stringent baseline. However, it was not possible to verify that the modeling inputs correspond to the rating conditions in Table 6.8.1-7. {additional_note_for_no_shaft_power_b}'
                    )
            else:
                undetermined_msg = (
                    f'The project includes a cooling tower. We calculated the cooling tower efficiency to be {heat_rejection_efficiency_in_gpm_per_hp_b}, which is less than the required efficiency of 38.2 gpm / hp.  However, it was not possible to verify that the modeling inputs correspond to the rating conditions in Table 6.8.1-7. Please review the efficiency and ensure that it is correct at the rating conditions as specified in the Table 6.8.1-7. {additional_note_for_no_shaft_power_b}'
                    )
            return undetermined_msg

        def applicability_check(self, context, calc_vals, data):
            return True
