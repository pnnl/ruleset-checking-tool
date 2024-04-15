from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_instance
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.data_fns.table_G3_4_fns import table_G34_lookup
from rct229.rulesets.ashrae9012019.ruleset_functions.get_opaque_surface_type import (
    OpaqueSurfaceType as OST,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_opaque_surface_type import (
    get_opaque_surface_type,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_surface_conditioning_category_dict import (
    SurfaceConditioningCategory as SCC,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_surface_conditioning_category_dict import (
    get_surface_conditioning_category_dict,
)
from rct229.utils.pint_utils import CalcQ
from rct229.utils.std_comparisons import std_equal


class Section5Rule10(RuleDefinitionListIndexedBase):
    """Rule 10 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(Section5Rule10, self).__init__(
            rmrs_used=produce_ruleset_model_instance(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            required_fields={
                "$": ["weather"],
                "weather": ["climate_zone"],
            },
            each_rule=Section5Rule10.BuildingRule(),
            index_rmr=BASELINE_0,
            id="5-10",
            description="Baseline floor assemblies must match the appropriate assembly maximum U-factors in Tables G3.4-1 through G3.4-9.",
            ruleset_section_title="Envelope",
            standard_section="Section G3.1-5(b) Building Envelope Modeling Requirements for the Baseline building",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0].buildings[*]",
            data_items={"climate_zone": (BASELINE_0, "weather/climate_zone")},
        )

    class BuildingRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section5Rule10.BuildingRule, self).__init__(
                rmrs_used=produce_ruleset_model_instance(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                required_fields={},
                each_rule=Section5Rule10.BuildingRule.FloorRule(),
                index_rmr=BASELINE_0,
                list_path="$.building_segments[*].zones[*].surfaces[*]",
            )

        def create_data(self, context, data=None):
            building = context.BASELINE_0
            return {
                "surface_conditioning_category_dict": get_surface_conditioning_category_dict(
                    data["climate_zone"], building
                ),
            }

        def list_filter(self, context_item, data=None):
            surface_b = context_item.BASELINE_0
            scc = data["surface_conditioning_category_dict"][surface_b["id"]]
            return (
                get_opaque_surface_type(surface_b) == OST.FLOOR
                and scc is not SCC.UNREGULATED
            )

        class FloorRule(RuleDefinitionBase):
            def __init__(self):
                super(Section5Rule10.BuildingRule.FloorRule, self).__init__(
                    rmrs_used=produce_ruleset_model_instance(
                        USER=False, BASELINE_0=True, PROPOSED=False
                    ),
                    required_fields={
                        "$": ["construction"],
                        "construction": ["u_factor"],
                    },
                )

            def get_calc_vals(self, context, data=None):
                climate_zone: str = data["climate_zone"]
                floor = context.BASELINE_0
                scc: str = data["surface_conditioning_category_dict"][floor["id"]]
                floor_u_factor = floor["construction"]["u_factor"]

                target_u_factor = None
                target_u_factor_res = None
                target_u_factor_nonres = None

                if scc in [
                    SCC.EXTERIOR_RESIDENTIAL,
                    SCC.EXTERIOR_NON_RESIDENTIAL,
                    SCC.SEMI_EXTERIOR,
                ]:
                    target_u_factor = table_G34_lookup(climate_zone, scc, OST.FLOOR)[
                        "u_value"
                    ]
                elif scc == SCC.EXTERIOR_MIXED:
                    target_u_factor_res = table_G34_lookup(
                        climate_zone, SCC.EXTERIOR_RESIDENTIAL, OST.FLOOR
                    )["u_value"]
                    target_u_factor_nonres = table_G34_lookup(
                        climate_zone, SCC.EXTERIOR_NON_RESIDENTIAL, OST.FLOOR
                    )["u_value"]
                    if target_u_factor_res == target_u_factor_nonres:
                        target_u_factor = target_u_factor_res

                return {
                    "floor_u_factor": CalcQ("thermal_transmittance", floor_u_factor),
                    "target_u_factor": CalcQ("thermal_transmittance", target_u_factor),
                    "target_u_factor_res": CalcQ(
                        "thermal_transmittance", target_u_factor_res
                    ),
                    "target_u_factor_nonres": CalcQ(
                        "thermal_transmittance", target_u_factor_nonres
                    ),
                }

            def manual_check_required(self, context, calc_vals=None, data=None):
                target_u_factor_res = calc_vals["target_u_factor_res"]
                target_u_factor_nonres = calc_vals["target_u_factor_nonres"]

                return (
                    target_u_factor_res is not None
                    and target_u_factor_nonres is not None
                    and target_u_factor_res != target_u_factor_nonres
                )

            def rule_check(self, context, calc_vals=None, data=None):
                floor_u_factor = calc_vals["floor_u_factor"]
                target_u_factor = calc_vals["target_u_factor"]

                return std_equal(val=floor_u_factor, std_val=target_u_factor)
