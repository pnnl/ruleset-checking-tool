from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.data_fns.table_G3_1_1_2_fns import (
    table_g3_1_2_lookup,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_swh_equipment_type import (
    get_swh_equipment_type,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_swh_uses_associated_with_each_building_segment import (
    get_swh_uses_associated_with_each_building_segment,
)
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_exactly_one_with_field_value
from rct229.utils.pint_utils import ZERO

SERVICE_WATER_HEATING_SPACE = SchemaEnums.schema_enums[
    "ServiceWaterHeatingSpaceOptions2019ASHRAE901"
]


def get_swh_bats_and_swh_use():
    """
    This function will be removed once the function is developed
    """

    return {}


class Section11Rule7(RuleDefinitionListIndexedBase):
    """Rule 7 of ASHRAE 90.1-2019 Appendix G Section 11 (Service Water Heating)"""

    def __init__(self):
        super(Section11Rule7, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=True
            ),
            each_rule=Section11Rule7.RMDRule(),
            index_rmd=BASELINE_0,
            id="11-7",
            description="Except in buildings that will have no service water heating loads, the service water heating system type in the baseline building design shall be as specified in Table G3.1.1-2 for each building area type in the proposed design.",
            ruleset_section_title="Service Water Heating",
            standard_section="Table G3.1 #11, baseline column, a & b",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0]",
        )

    class RMDRule(RuleDefinitionBase):
        def __init__(self):
            super(Section11Rule7.RMDRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False,
                    BASELINE_0=True,
                    PROPOSED=True,
                ),
            )

        def is_applicable(self, context, data=None):
            rmd_p = context.PROPOSED

            swh_bats_and_uses_p = get_swh_bats_and_swh_use(rmd_p)

            for swh_bat in swh_bats_and_uses_p:
                for swh_use_id in swh_bats_and_uses_p[swh_bat]:
                    swh_uses = find_exactly_one_with_field_value(
                        "$.buildings[*].building_segments[*].zones[*].spaces[*].service_water_heating_uses[*]",
                        "id",
                        swh_use_id,
                        rmd_p,
                    )
                    if (
                        getattr_(swh_uses, "service_water_heating_uses", "use")
                        > ZERO.VOLUME
                        or swh_bat != SERVICE_WATER_HEATING_SPACE.PARKING_GARAGE
                    ):
                        return True
                    else:
                        return False

        def get_calc_vals(self, context, data=None):
            rmd_b = context.BASELINE_0
            rmd_p = context.PROPOSED

            swh_bats_and_uses_b = get_swh_uses_associated_with_each_building_segment(
                rmd_b
            )
            swh_bats_and_uses_p = get_swh_bats_and_swh_use(rmd_p)

            for swh_bat in swh_bats_and_uses_p:
                for swh_equip_id in swh_bats_and_uses_b[swh_bat]["SWHHeatingEq"]:
                    swh_equip_type = get_swh_equipment_type(rmd_b, swh_equip_id)
                    expected_swh_equip_type = table_g3_1_2_lookup(swh_bat)

                return {
                    "swh_equip_type": swh_equip_type,
                    "expected_swh_equip_type": expected_swh_equip_type,
                }

        def rule_check(self, context, calc_vals=None, data=None):
            swh_equip_type = calc_vals["swh_equip_type"]
            expected_swh_equip_type = calc_vals["expected_swh_equip_type"]

            return swh_equip_type == expected_swh_equip_type
