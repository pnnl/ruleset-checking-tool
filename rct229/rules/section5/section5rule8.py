from rct229.data_fns.table_G3_4_fns import table_G34_lookup
from rct229.rule_engine.rule_base import (
    RuleDefinitionBase,
    RuleDefinitionListIndexedBase,
)
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.ruleset_functions.get_opaque_surface_type import (
    BELOW_GRADE_WALL,
    get_opaque_surface_type,
)
from rct229.ruleset_functions.get_surface_conditioning_category_dict import (
    get_surface_conditioning_category_dict,
)
from rct229.utils.jsonpath_utils import find_all


class Section5Rule8(RuleDefinitionListIndexedBase):
    """Rule 8 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(Section5Rule8, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            each_rule=Section5Rule8.BuildingRule(),
            index_rmr="baseline",
            list_path="ruleset_model_instances[0].buildings[*]",
            id="5-8",
            description="Baseline below-grade walls shall match the appropriate assembly maximum C-factors in Table G3.4-1 through G3.4-8.",
            required_fields={
                "$": ["weather"],
                "weather": ["climate_zone"],
            },
        )

    def create_data(self, context, data=None):
        return {"climate_zone": context.baseline["weather"]["climate_zone"]}

    class BuildingRule(RuleDefinitionBase):
        def __init__(self):
            super(Section5Rule8.BuildingRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
                required_fields={"$..zones[*]": ["surfaces"]},
            )

        def get_calc_vals(self, context, data=None):
            # Climate zone should have only one in RMR
            climate_zone = data["climate_zone"]
            # Becasue list_path is building, the scope of the context.baseline here is building
            scc_dictionary_b = get_surface_conditioning_category_dict(
                climate_zone, context.baseline
            )
            # Retrieve all surfaces under the building
            surfaces_b = find_all("$..zones[*].surfaces[*]", context.baseline)
            # build-in manual check flag.
            calc_val = {}
            failing_surface_c_factor_ids = []
            mix_surface_c_factor_ids = []

            for surface_b in surfaces_b:
                if get_opaque_surface_type(surface_b) == BELOW_GRADE_WALL:
                    # construction info
                    surface_construction_b = surface_b["construction"]
                    scc_b = scc_dictionary_b[surface_b["id"]]
                    # QNS a good number to estimate?
                    target_c_factor = None
                    # TODO All these need to change to enum later
                    if scc_b in [
                        "EXTERIOR RESIDENTIAL",
                        "EXTERIOR NON-RESIDENTIAL",
                        "SEMI-EXTERIOR",
                    ]:
                        target = table_G34_lookup(climate_zone, scc_b, BELOW_GRADE_WALL)
                        target_c_factor = target["c_factor"]

                    elif scc_b == "EXTERIOR MIXED":
                        target = table_G34_lookup(
                            climate_zone, "EXTERIOR RESIDENTIAL", BELOW_GRADE_WALL
                        )
                        target_c_factor_res = target["c_factor"]

                        target = table_G34_lookup(
                            climate_zone, "EXTERIOR NON-RESIDENTIAL", BELOW_GRADE_WALL
                        )
                        target_c_factor_nonres = target["c_factor"]

                        if target_c_factor_res != target_c_factor_nonres:
                            mix_surface_c_factor_ids.append(surface_b["id"])
                        else:
                            target_c_factor = target_c_factor_res
                    # convert values to IP unit to compare with standard.
                    model_c_factor_magnitude = round(
                        surface_construction_b["c_factor"]
                        .to("Btu_h / square_foot / delta_degF")
                        .magnitude,
                        2,
                    )
                    target_c_factor_magnitude = target_c_factor.magnitude
                    if model_c_factor_magnitude != target_c_factor_magnitude:
                        failing_surface_c_factor_ids.append(surface_b["id"])

            return {
                "failed_c_factor_surface_id": failing_surface_c_factor_ids,
                "mix_surface_c_factor_ids": mix_surface_c_factor_ids,
            }

        def manual_check_required(self, context, calc_vals=None, data=None):
            """
            Return True or False if the results shall depends on manual check
            Parameters
            ----------
            context
            calc_vals
            data
            Returns
            -------
            """
            return len(calc_vals["mix_surface_c_factor_ids"]) > 0

        def rule_check(self, context, calc_vals, data=None):
            return len(calc_vals["failed_c_factor_surface_id"]) == 0
