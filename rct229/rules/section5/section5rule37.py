from rct229.rule_engine.rule_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals


class Section5Rule37(RuleDefinitionListIndexedBase):
    """Rule 37 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(Section5Rule37, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, True),
            required_fields={
                "$": ["weather"],
                "weather": ["climate_zone"],
            },
            each_rule=Section5Rule37.BuildingRule(),
            index_rmr="baseline",
            id="5-37",
            description="Skylight U-factors for residential, non-residential and semi-heated spaces in the baseline model must match the appropriate requirements in Table G3.4-1 through G3.4-8.",
            list_path="ruleset_model_instances[0].buildings[*]",
        )