from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_instance
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.data_fns.table_G3_5_1_fns import table_G3_5_1_lookup
from rct229.rulesets.ashrae9012019.data_fns.table_G3_5_2_fns import table_G3_5_2_lookup
from rct229.utils.jsonpath_utils import find_all
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
        baseline_sys_serve_more_than_one_flr_list = (
            get_hvac_systems_5_6_serving_multiple_floors(rmd_b).keys()
        )

        return any(
            baseline_system_type_compare(system_type, applicable_sys_type, True)
            and any(
                system_id not in baseline_sys_serve_more_than_one_flr_list
                for system_id in system_ids
            )
            for system_type, system_ids in baseline_system_types_dict.items()
            for applicable_sys_type in APPLICABLE_SYS_TYPES
        )