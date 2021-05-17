from rct229.data.schema_enums import schema_enums
from rct229.data_fns.table_8_4_4_eff import (table_8_4_4_eff,
                                             table_8_4_4_in_range)
from rct229.rule_engine.rule_base import (RuleDefinitionBase,
                                          RuleDefinitionListIndexedBase)
from rct229.rule_engine.user_baseline_proposed_vals import \
    UserBaselineProposedVals
from rct229.rule_engine.utils import (_assert_equal_rule,
                                      _select_equal_or_lesser)
from rct229.utils.jsonpath_utils import find_all

_DRY_TYPE = schema_enums["TransformerType"].DRY_TYPE.name

# Rule Definitions for Section 15 of 90.1-2019 Appendix G

# def _check_user_transformer_exists(user_rmr, rmr_context):
#     user_transformers = user_rmr[rmr_context]
#     num_user_transformers = len(user_transformers)
#     if num_user_transformers > 0:
#         applicable = True
#     else:
#         applicable = False
#
#     return applicable


# ------------------------


class Section15Rule1(RuleDefinitionBase):
    """Rule 1 of ASHRAE 90.1-2019 Appendix G Section 15 (Transformers)."""

    def __init__(self):
        id = "15-1"
        description = (
            "Number of transformers modeled in User RMR and Baseline RMR are the same"
        )
        rmr_context = "transformers"
        rmrs_used = UserBaselineProposedVals(True, True, False)
        super(Section15Rule1, self).__init__(id, description, rmr_context, rmrs_used)

    def is_applicable(self, context, data=None):
        return len(context.user) > 0

    def get_calc_vals(self, context, data=None):
        return {
            "num_user_transformers": len(context.user),
            "num_baseline_transformers": len(context.baseline),
        }

    def rule_check(self, context, calc_vals=None, data=None):
        return (
            calc_vals["num_user_transformers"] == calc_vals["num_baseline_transformers"]
        )


# ------------------------


class Section15Rule2(RuleDefinitionBase):
    """Rule 2 of ASHRAE 90.1-2019 Appendix G Section 15 (Transformers)."""

    def __init__(self):
        id = "15-2"
        description = (
            "Number of transformers modeled in User RMR and Proposed RMR are the same"
        )
        rmr_context = "transformers"
        rmrs_used = UserBaselineProposedVals(True, False, True)
        super(Section15Rule2, self).__init__(id, description, rmr_context, rmrs_used)

    def is_applicable(self, context, data=None):
        return len(context.user) > 0

    def get_calc_vals(self, context, data=None):
        return {
            "num_user_transformers": len(context.user),
            "num_proposed_transformers": len(context.proposed),
        }

    def rule_check(self, context, calc_vals=None, data=None):
        return (
            calc_vals["num_user_transformers"] == calc_vals["num_proposed_transformers"]
        )


# ------------------------


class Section15Rule3(RuleDefinitionListIndexedBase):
    """Rule 3 of ASHRAE 90.1-2019 Appendix G Section 15 (Transformers)."""

    def __init__(self):
        super(Section15Rule3, self).__init__(
            id="15-3",
            description="User RMR transformer Name in Proposed RMR",
            rmr_context="transformers",
            rmrs_used=UserBaselineProposedVals(True, False, True),
            each_rule=Section15Rule3.TransformerRule(),
            index_rmr="user",
        )

    def create_data(self, context, data):
        # Get the Proposed transformer names
        return find_all("[*].name", context.proposed)

    class TransformerRule(RuleDefinitionBase):
        def __init__(self):
            super(Section15Rule3.TransformerRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(True, False, False)
            )

        def get_calc_vals(self, context, data=None):
            return {
                "user_transformer_name": context.user["name"],
                "proposed_transformer_names": data,
            }

        def rule_check(self, context, calc_vals=None, data=None):
            return (
                calc_vals["user_transformer_name"]
                in calc_vals["proposed_transformer_names"]
            )


# ------------------------


class Section15Rule4(RuleDefinitionListIndexedBase):
    """Rule 4 of ASHRAE 90.1-2019 Appendix G Section 15 (Transformers)."""

    def __init__(self):
        super(Section15Rule4, self).__init__(
            id="15-4",
            description="User RMR transformer Name in Baseline RMR",
            rmr_context="transformers",
            rmrs_used=UserBaselineProposedVals(True, True, False),
            each_rule=Section15Rule4.TransformerRule(),
            index_rmr="user",
        )

    def create_data(self, context, data):
        # Get the Baseline transformer names
        return find_all("[*].name", context.baseline)

    class TransformerRule(RuleDefinitionBase):
        def __init__(self):
            super(Section15Rule4.TransformerRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(True, False, False),
            )

        def get_calc_vals(self, context, data=None):
            return {
                "user_transformer_name": context.user["name"],
                "baseline_transformer_names": data,
            }

        def rule_check(self, context, calc_vals=None, data=None):
            return (
                calc_vals["user_transformer_name"]
                in calc_vals["baseline_transformer_names"]
            )


# ------------------------


class Section15Rule5(RuleDefinitionListIndexedBase):
    """Rule 5 of ASHRAE 90.1-2019 Appendix G Section 15 (Transformers)."""

    def __init__(self):
        super(Section15Rule5, self).__init__(
            id="15-5",
            description="Transformer efficiency reported in Baseline RMR equals Table 8.4.4",
            rmr_context="transformers",
            rmrs_used=UserBaselineProposedVals(True, True, False),
            each_rule=Section15Rule5.TransformerRule(),
            index_rmr="user",
        )

    class TransformerRule(RuleDefinitionBase):
        def __init__(self):
            super(Section15Rule5.TransformerRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(True, True, False),
            )

        def is_applicable(self, context, data=None):
            # Provide conversion from VA to kVA
            user_transformer_kVA = context.user["capacity"] / 1000
            baseline_transformer_kVA = context.baseline["capacity"] / 1000

            user_transformer_type = context.user["type"]
            user_transformer_phase = context.user["phase"]
            user_transformer_efficiency = context.user["efficiency"]
            user_transformer_capacity_in_range = table_8_4_4_in_range(
                phase=user_transformer_phase, kVA=user_transformer_kVA
            )

            baseline_transformer_type = context.baseline["type"]
            baseline_transformer_phase = context.baseline["phase"]
            baseline_transformer_capacity_in_range = table_8_4_4_in_range(
                phase=baseline_transformer_phase, kVA=baseline_transformer_kVA
            )

            return (
                user_transformer_type == _DRY_TYPE
                and user_transformer_capacity_in_range
                and user_transformer_efficiency
                >= table_8_4_4_eff(
                    phase=user_transformer_phase, kVA=user_transformer_kVA
                )
                and baseline_transformer_type == _DRY_TYPE
                and baseline_transformer_capacity_in_range
            )

        def get_calc_vals(self, context, data=None):
            baseline_transformer_phase = context.baseline["phase"]
            # Convert from VA to user_kVA
            baseline_transformer_kVA = context.baseline["capacity"] / 1000

            return {
                "baseline_transformer_efficiency": context.baseline["efficiency"],
                "required_baseline_transformer_efficiency": table_8_4_4_eff(
                    phase=baseline_phase, kVA=baseline_kVA
                ),
            }

        def rule_check(self, context, calc_vals=None, data=None):

            # TODO: Allow tolerance?
            return (
                calc_vals["baseline_transformer_efficiency"]
                == calc_vals["required_baseline_transformer_efficiency"]
            )


# ------------------------


class Section15Rule6(RuleDefinitionListIndexedBase):
    """Rule 6 of ASHRAE 90.1-2019 Appendix G Section 15 (Transformers)."""

    def __init__(self):
        super(Section15Rule6, self).__init__(
            id="15-6",
            description="Transformer efficiency reported in User RMR equals Table 8.4.4",
            rmr_context="transformers",
            rmrs_used=UserBaselineProposedVals(True, False, False),
            each_rule=Section15Rule6.TransformerRule(),
        )

    class TransformerRule(RuleDefinitionBase):
        def __init__(self):
            super(Section15Rule6.TransformerRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(True, False, False),
            )

        def is_applicable(self, context, data=None):
            # Provide conversion from VA to kVA
            user_transformer_kVA = context.user["capacity"] / 1000

            user_transformer_type = context.user["type"]
            user_transformer_phase = context.user["phase"]
            user_transformer_capacity_in_range = table_8_4_4_in_range(
                phase=user_transformer_phase, kVA=user_transformer_kVA
            )

            return (
                user_transformer_type == _DRY_TYPE
                and user_transformer_capacity_in_range
            )

        def get_calc_vals(self, context, data=None):
            user_transformer_phase = context.user["phase"]
            # Provide conversion from VA to kVA
            user_transformer_kVA = context.user["capacity"] / 1000

            return {
                "user_transformer_efficiency": context.user["efficiency"],
                "required_user_transformer_min_efficiency": table_8_4_4_eff(
                    phase=user_transformer_phase, kVA=user_transformer_kVA
                ),
            }

        def rule_check(self, context, calc_vals=None, data=None):
            return (
                calc_vals["user_transformer_efficiency"]
                >= calc_vals["required_user_transformer_min_efficiency"]
            )


# ------------------------
