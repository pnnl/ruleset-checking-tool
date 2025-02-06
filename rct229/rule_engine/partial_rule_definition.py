from typing import Mapping

from rct229.rule_engine.rule_base import RCTPrecision, RuleDefinitionBase


class PartialRuleDefinition(RuleDefinitionBase):
    def __init__(
        self,
        rmds_used,
        id=None,
        description=None,
        ruleset_section_title=None,
        standard_section=None,
        is_primary_rule=False,
        rmd_context="",
        required_fields=None,
        manual_check_required_msg="",
        not_applicable_msg="",
        precision: Mapping[str, RCTPrecision] = None,
    ):
        """Base class for all Partial Rule definitions (secondary)

        Parameters
        ----------
        rmds_used : RuleSetModels
            A trio of boolean values indicating which RMDs are required by the rule
        id : string
            Unique id for the rule
            Usually unspecified for nested rules
        description : string
            Rule description
            Usually unspecified for nested rules
        ruleset_section_title : string
            Ruleset section title
            e.g., Envelope
        standard_section: string
            The section id in the standard (ruleset)
            e.g., Section G3.1-5(b) Building Envelope Modeling Requirements for the Baseline building
        is_primary_rule: boolean
            Indicate whether this rule is primary rule (True) or secondary rule (False)
        required_fields : dict
            A dictionary of the form
            {
                "<json path>": [<required field names>],
                ...
            },
            where the json path should resolve to a list of dictionaries.
        manual_check_required_msg: string
            default message for UNDETERMINED outcome
        not_applicable_msg: string
            default message for NOT_APPLICABLE outcome
        """
        super(PartialRuleDefinition, self).__init__(
            rmds_used=rmds_used,
            id=id,
            description=description,
            rmd_context=rmd_context,
            required_fields=required_fields,
            manual_check_required_msg=manual_check_required_msg,
            not_applicable_msg=not_applicable_msg,
            ruleset_section_title=ruleset_section_title,
            standard_section=standard_section,
            is_primary_rule=is_primary_rule,
            precision=precision,
        )

    def rule_check(self, context, calc_vals=None, data={}):
        """Overrides the base implementation to apply applicability check

        Parameters
        ----------
        context : RuleSetModels
            Object containing the contexts for RMDs
        calc_vals: dictionary
            Dictionary contains calculated values for rule check and reporting.
        data : dict
            An optional dictionary. New data, based on data_pointers, data_paths, or
            create_data() will be merged into this data dictionary and passed to each
            subrule.

        Returns
        -------
        boolean
            True if the rule UNDETERMINED and NOT_APPLICABLE if the rule fails
        """
        return self.applicability_check(context=context, calc_vals=calc_vals, data=data)

    def applicability_check(self, context, calc_vals, data):
        """This checks the applicability of a partial rule

        This must be overridden. The base implementation
        raises a NotImplementedError

        Parameters
        ----------
        context : RuleSetModels
            Object containing the contexts for RMDs
        calc_vals: dict. It contains the calculated values
        data : An optional data object. It is ignored by this base implementation.

        Returns
        -------
        boolean
            True if the rule passes and False if the rule fails
        """
        raise NotImplementedError
