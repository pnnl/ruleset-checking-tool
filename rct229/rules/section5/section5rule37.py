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
            id="5-17",
            description="Opaque surfaces that are not regulated (not part of opaque building envelope) must be modeled the same in the baseline as in the proposed design. ",
            list_path="ruleset_model_instances[0].buildings[*]",
        )