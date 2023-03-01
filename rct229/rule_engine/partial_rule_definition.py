from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.utils.json_utils import slash_prefix_guarantee


class PartialRuleDefinition(RuleDefinitionBase):
    def __init__(
        self,
        rmrs_used,
        id=None,
        description=None,
        ruleset_section_title=None,
        standard_section=None,
        is_primary_rule=False,
        rmr_context="",
        required_fields=None,
        must_match_by_ids=[],
        manual_check_required_msg="",
        not_applicable_msg="",
    ):
        """Base class for all Partial Rule definitions (secondary)

        Parameters
        ----------
        rmrs_used : UserBaselineProposedVals
            A trio of boolen values indicating which RMRs are required by the
            rule
        id : string
            Unique id for the rule
            Usually unspecified for nested rules
        description : string
            Rule description
            Usually unspecified for nested rules
        rmr_context : string
            A json pointer into each RMR, or RMR fragment, provided to the rule.
            For better human readability, the leading "/" may be ommitted.
        required_fields : dict
            A dictionary of the form
            {
                "<json path>": [<required field names>],
                ...
            },
            where the json path should resolve to a list of dectionaries.

        """
        super(PartialRuleDefinition, self).__init__(
            rmrs_used=rmrs_used,
            id=id,
            description=description,
            rmr_context=rmr_context,
            required_fields=required_fields,
            manual_check_required_msg=manual_check_required_msg,
            not_applicable_msg=not_applicable_msg,
            ruleset_section_title=ruleset_section_title,
            standard_section=standard_section,
            is_primary_rule=is_primary_rule,
        )

    def rule_check(self, context, calc_vals=None, data={}):
        """Overrides the base implementation to apply a rule to each entry in
        a list

        This should not be overridden. Override create_context_list() instead.

        Parameters
        ----------
        context : UserBaselineProposedVals
            Object containing the contexts for the user, baseline, and proposed RMRs
        data : dict
            An optional dictionary. New data, based on data_pointers, data_paths, or
            create_data() will be merged into this data dictionary and passed to each
            subrule.

        Returns
        -------
        list
            A list of rule outcomes. The each outcome in the list is augmented
            with a name field that is the name of the entry in the context list.
        """
        return self.applicability_check(context=context, calc_vals=calc_vals, data=data)

    def applicability_check(self, context, calc_vals, data):
        """This checks the applicability of a partial rule

        This must be overridden. The base implementation
        raises a NotImplementedError

        Parameters
        ----------
        context : UserBaselineProposedVals
            Object containing the contexts for the user, baseline, and proposed RMRs
        calc_vals: dict. It contains the calculated values
        data : An optional data object. It is ignored by this base implementation.

        Returns
        -------
        boolean
            True if the rule passes and False if the rule fails
        """
        raise NotImplementedError
