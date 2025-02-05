from rct229.rule_engine.partial_rule_definition import PartialRuleDefinition
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0, PROPOSED
from rct229.rulesets.ashrae9012019.ruleset_functions.aggregate_min_OA_schedule_across_zones import aggregate_min_OA_schedule_across_zones
from rct229.rulesets.ashrae9012019.ruleset_functions.get_dict_of_zones_and_terminal_units_served_by_hvac_sys import get_dict_of_zones_and_terminal_units_served_by_hvac_sys
from rct229.rulesets.ashrae9012019.ruleset_functions.get_min_oa_cfm_sch_zone import get_min_oa_cfm_sch_zone
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.jsonpath_utils import find_all
LIGHTING_SPACE = SchemaEnums.schema_enums[
    'LightingSpaceOptions2019ASHRAE901TG37']


class PRM9012019Rule40n43(RuleDefinitionListIndexedBase):
    """Rule 35 of ASHRAE 90.1-2019 Appendix G Section 19 (HVAC - General)"""

    def __init__(self):
        super(PRM9012019Rule40n43, self).__init__(rmds_used=
            produce_ruleset_model_description(USER=False, BASELINE_0=True,
            PROPOSED=True), each_rule=PRM9012019Rule40n43.RMDRule(),
            index_rmd=BASELINE_0, id='section19rule35', description=
            'For baseline systems serving only laboratory spaces that are prohibited from recirculating return air by code or accreditation standards, the baseline system shall be modeled as 100% outdoor air. Rule only applies when baseline outdoor air CFM is modeled as greater than proposed design outdoor air CFM.'
            , ruleset_section_title='HVAC - General', standard_section=
            'Section G3.1-10 HVAC Systems proposed column c and d',
            is_primary_rule=False, list_path=
            'ruleset_model_descriptions[0]', required_fields={'$': [
            'calendar', 'ruleset_model_descriptions'], 'calendar': [
            'is_leap_year']}, data_items={'is_leap_year_b': (BASELINE_0,
            'calendar/is_leap_year'), 'is_leap_year_p': (PROPOSED,
            'calendar/is_leap_year')})


    class RMDRule(RuleDefinitionListIndexedBase):

        def __init__(self):
            super(PRM9012019Rule40n43.RMDRule, self).__init__(rmds_used=
                produce_ruleset_model_description(USER=False, BASELINE_0=
                True, PROPOSED=True), each_rule=PRM9012019Rule40n43.RMDRule
                .HVACRule(), index_rmd=BASELINE_0, list_path=
                '$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*]'
                )

        def create_data(self, context, data):
            rmd_b = context.BASELINE_0
            rmd_p = context.PROPOSED
            leap_year_b = data['is_leap_year_b']
            leap_year_p = data['is_leap_year_p']
            dict_of_zones_and_terminal_units_served_by_hvac_sys_b = (
                get_dict_of_zones_and_terminal_units_served_by_hvac_sys(rmd_b))
            hvac_system_serves_only_labs = True
            are_any_lighting_space_types_defined = False
            all_lighting_space_types_defined = True
            zone_OA_flow_list_of_schedules_b = []
            zone_OA_flow_list_of_schedules_p = []
            for hvac_id_b in find_all(
                '$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*].id'
                , rmd_b):
                for zone_id_b in dict_of_zones_and_terminal_units_served_by_hvac_sys_b[
                    hvac_id_b]['zone_list']:
                    lighting_space_types_b = find_all(
                        f'$.buildings[*].building_segments[*].zones[*][?(@.id="{zone_id_b}")].spaces[*].lighting_space_type'
                        , rmd_b)
                    all_lighting_space_types_defined = all(
                        lighting_space_types_b
                        ) and all_lighting_space_types_defined
                    are_any_lighting_space_types_defined = any(
                        lighting_space_types_b
                        ) or are_any_lighting_space_types_defined
                    hvac_system_serves_only_labs = all(map(lambda
                        space_type: space_type == LIGHTING_SPACE.
                        LABORATORY_EXCEPT_IN_OR_AS_A_CLASSROOM,
                        lighting_space_types_b)
                        ) and hvac_system_serves_only_labs
                    zone_OA_flow_list_of_schedules_b.append(
                        get_min_oa_cfm_sch_zone(rmd_b, zone_id_b, leap_year_b))
                    zone_OA_flow_list_of_schedules_p.append(
                        get_min_oa_cfm_sch_zone(rmd_p, zone_id_b, leap_year_p))
            aggregated_min_OA_schedule_across_zones_b = (
                aggregate_min_OA_schedule_across_zones(
                zone_OA_flow_list_of_schedules_b))
            aggregated_min_OA_schedule_across_zones_p = (
                aggregate_min_OA_schedule_across_zones(
                zone_OA_flow_list_of_schedules_p))
            modeled_baseline_total_zone_min_OA_flow = sum(
                aggregated_min_OA_schedule_across_zones_b)
            modeled_proposed_total_zone_min_OA_flow = sum(
                aggregated_min_OA_schedule_across_zones_p)
            return {'dict_of_zones_and_terminal_units_served_by_hvac_sys_b':
                dict_of_zones_and_terminal_units_served_by_hvac_sys_b,
                'hvac_system_serves_only_labs':
                hvac_system_serves_only_labs,
                'are_any_lighting_space_types_defined':
                are_any_lighting_space_types_defined,
                'all_lighting_space_types_defined':
                all_lighting_space_types_defined,
                'modeled_baseline_total_zone_min_OA_flow':
                modeled_baseline_total_zone_min_OA_flow,
                'modeled_proposed_total_zone_min_OA_flow':
                modeled_proposed_total_zone_min_OA_flow}


        class HVACRule(PartialRuleDefinition):

            def __init__(self):
                super(PRM9012019Rule40n43.RMDRule.HVACRule, self).__init__(
                    rmds_used=produce_ruleset_model_description(USER=False,
                    BASELINE_0=True, PROPOSED=True))

            def is_applicable(self, context, data=None):
                hvac_system_serves_only_labs = data[
                    'hvac_system_serves_only_labs']
                modeled_baseline_total_zone_min_OA_flow = data[
                    'modeled_baseline_total_zone_min_OA_flow']
                modeled_proposed_total_zone_min_OA_flow = data[
                    'modeled_proposed_total_zone_min_OA_flow']
                return (hvac_system_serves_only_labs and 
                    modeled_baseline_total_zone_min_OA_flow >
                    modeled_proposed_total_zone_min_OA_flow)

            def applicability_check(self, context, calc_vals, data):
                hvac_system_serves_only_labs = data[
                    'hvac_system_serves_only_labs']
                modeled_baseline_total_zone_min_OA_flow = data[
                    'modeled_baseline_total_zone_min_OA_flow']
                modeled_proposed_total_zone_min_OA_flow = data[
                    'modeled_proposed_total_zone_min_OA_flow']
                all_lighting_space_types_defined = data[
                    'all_lighting_space_types_defined']
                are_any_lighting_space_types_defined = data[
                    'are_any_lighting_space_types_defined']
                return (modeled_baseline_total_zone_min_OA_flow >
                    modeled_proposed_total_zone_min_OA_flow and (
                    hvac_system_serves_only_labs and (
                    all_lighting_space_types_defined or
                    are_any_lighting_space_types_defined) or not
                    are_any_lighting_space_types_defined))

            def get_manual_check_required_msg(self, context, calc_vals=None,
                data=None):
                hvac_b = context.BASELINE_0
                hvac_id_b = hvac_b['id']
                hvac_system_serves_only_labs = data[
                    'hvac_system_serves_only_labs']
                are_any_lighting_space_types_defined = data[
                    'are_any_lighting_space_types_defined']
                all_lighting_space_types_defined = data[
                    'all_lighting_space_types_defined']
                undetermined_msg = ''
                if hvac_system_serves_only_labs:
                    if all_lighting_space_types_defined:
                        undetermined_msg = (
                            f'Baseline hvac system {hvac_id_b} serves only lab spaces and the modeled baseline outdoor air flow was modeled as greater than the proposed outdoor air flow. Conduct a manual check that these spaces meet G3.1.2.5 Exception 4 and that they are prohibited from recirculating return air by code or accreditation standards and confirm that the hvac system was modeled as a 100% outdoor air system.'
                            )
                    elif are_any_lighting_space_types_defined:
                        undetermined_msg = (
                            f'Baseline hvac system {hvac_id_b} serves some lab spaces (not all space types were defined in the RMD so all space types associated with this hvac system could not be checked) and the modeled baseline outdoor air flow was modeled as greater than the proposed outdoor air flow. Conduct a manual check that these spaces meet G3.1.2.5 Exception 4 and that they are prohibited from recirculating return air by code or accreditation standards and, if so, confirm that the hvac system was modeled as a 100% outdoor air system.'
                            )
                elif not are_any_lighting_space_types_defined:
                    undetermined_msg = (
                        f'No space types were defined in the RMD for baseline system {hvac_id_b} and the modeled baseline outdoor air flow was modeled as greater than the proposed outdoor air flow. Conduct a manual check to determine if these spaces meet G3.1.2.5 Exception 4 and that they are prohibited from recirculating return air by code or accreditation standards and, if so, confirm that the hvac system was modeled as a 100% outdoor air system. If this exception does not apply then outcome is fail unless another exception to G3.1.2.5 applies.'
                        )
                return undetermined_msg
