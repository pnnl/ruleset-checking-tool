from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import ZERO

ENERGY_SOURCE_OPTIONS = SchemaEnums.schema_enums["EnergySourceOptions"]


class PRM9012019Rule10d53(RuleDefinitionListIndexedBase):
    """Rule 6 of ASHRAE 90.1-2019 Appendix G Section 1 (Performance Calculation)"""

    def __init__(self):
        super(PRM9012019Rule10d53, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False,
                BASELINE_0=True,
                BASELINE_90=True,
                BASELINE_180=True,
                BASELINE_270=True,
                PROPOSED=False,
            ),
            rmds_used_optional=produce_ruleset_model_description(
                BASELINE_90=True,
                BASELINE_180=True,
                BASELINE_270=True,
            ),
            id="1-6",
            description="On-site renewable energy shall not be included in the baseline building performance.  ",
            ruleset_section_title="Performance Calculation",
            standard_section="G3.11 18 Baseline",
            is_primary_rule=True,
            index_rmd=BASELINE_0,
            each_rule=PRM9012019Rule10d53.RMDRule(),
            list_path="ruleset_model_descriptions[0]",
        )

    class RMDRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012019Rule10d53.RMDRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False,
                    BASELINE_0=True,
                    BASELINE_90=True,
                    BASELINE_180=True,
                    BASELINE_270=True,
                    PROPOSED=False,
                ),
                rmds_used_optional=produce_ruleset_model_description(
                    BASELINE_90=True,
                    BASELINE_180=True,
                    BASELINE_270=True,
                ),
                required_fields={
                    "$": ["model_output"],
                    "$.model_output": ["annual_end_use_results"],
                    "$.model_output.annual_end_use_results[*]": ["energy_source"],
                },
            )

    def get_calc_vals(self, context, data=None):
        rmd_b0 = context.BASELINE_0
        rmd_b90 = context.BASELINE_90
        rmd_b180 = context.BASELINE_180
        rmd_b270 = context.BASELINE_270
        renewable_annual_site_energy_use_list = [
            sum(
                find_all(
                    f'$.ruleset_model_descriptions[0].model_output.annual_end_use_results[*][?(@.energy_source="{ENERGY_SOURCE_OPTIONS.ON_SITE_RENEWABLES}")].annual_site_energy_use',
                    rmd,
                )
            )
            for rmd in (rmd_b0, rmd_b90, rmd_b180, rmd_b270)
        ]

        return {
            "has_renewable": sum(renewable_annual_site_energy_use_list) > ZERO.ENERGY,
        }

    def rule_check(self, context, calc_vals=None, data=None):
        result = calc_vals["has_renewable"]
        return result
