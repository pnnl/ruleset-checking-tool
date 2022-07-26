from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals


class RuleDefinitionListBase(RuleDefinitionBase):
    """
    Baseclass for Rule Definitions that apply to each element in a list context.
    """

    def __init__(
        self,
        rmrs_used,
        each_rule,
        id=None,
        description=None,
        rmr_context="",
        required_fields=None,
        manual_check_required_msg="Manual Check Required",
        not_applicable_msg="Not Applicable",
    ):
        self.each_rule = each_rule
        super(RuleDefinitionListBase, self).__init__(
            rmrs_used=rmrs_used,
            id=id,
            description=description,
            rmr_context=rmr_context,
            required_fields=required_fields,
            manual_check_required_msg=manual_check_required_msg,
            not_applicable_msg=not_applicable_msg,
        )

    def create_context_list(self, context, data=None):
        """Generates a list of context trios

        For a list-type rule, we need to create a list of contexts to pass on
        to the sub-rule. Often, we need to match up the entries in the
        RMR lists by name or id and then apply the sub-rule to each trio of entries.
        This method is responsible for creating the list of trios.

        This method must be overridden.

        Parameters
        ----------
        context : UserBaselineProposedVals
            Object containing the contexts for the user, baseline, and proposed RMRs
        data : An optional data object.

        Returns
        -------
        list of UserBaselineProposedVals
            A list of context trios
        """
        raise NotImplementedError

    def create_data(self, context, data=None):
        """Create the data object to be passed to each_rule

        This is typically overridden to collect data available at this rule's
        level that is needed by each_rule.

        This default implementation simply returns the data that was passed in.

        Parameters
        ----------
        context : UserBaselineProposedVals
            Object containing the user, baseline, and proposed contexts
        data : any
            The data object that was passed into the rule.

        Returns
        -------
        UserBaselineProposedVals
            Object containing the contexts for the user, baseline, and proposed
            RMRs; an RMR's context is set to None if the corresponding flag
            in self.rmrs_used is not set
        """
        return data

    def list_filter(self, context_item, data=None):
        """Function used to filter the context_list

        The default implementation simply passes each list_item through (no filtering)

        An inheriting rule can override this function to reduce the context list that
        is returned from create_context_list.

        NOTE: when overriding this function, it is important to know that rmd scope for none-index rmd, could be NONE.
        It is recommended to add a NONE check for those rmd scope.

        Parameters
        ----------
        context_item : dict
            An item from the context_list
        data : object
            The data object for the rule. Note: list_filter will be used after
            create_data is called, so this function will have access to any data
            this rule added to the data object.
            This implementation ignores the data argument, but overriding functions
            are free to make use of it.

        Returns
        -------
        list of UserBaselineProposedVals
            A filtered list of context trios
        """
        return context_item

    def rule_check(self, context, calc_vals=None, data=None):
        """Overrides the base implementation to apply a rule to each entry in
        a list

        This should not be overridden. Override create_context_list() instead.

        Parameters
        ----------
        context : UserBaselineProposedVals
            Object containing the contexts for the user, baseline, and proposed RMRs
        data : An optional data object. It is ignored by this base implementation.

        Returns
        -------
        list
            A list of rule outcomes. The each outcome in the list is augmented
            with a name field that is the name of the entry in the context list.
        """
        # Create the data to be passed to each_rule
        data = self.create_data(context, data)
        context_list = self.create_context_list(context, data)
        filtered_context_list = [
            context_item
            for context_item in context_list
            if self.list_filter(context_item, data)
        ]
        outcomes = []

        for ubp in filtered_context_list:
            item_outcome = self.each_rule.evaluate(ubp, data)

            # Set the id for item_outcome
            if ubp.user and ubp.user["id"]:
                item_outcome["id"] = ubp.user["id"]
            elif ubp.baseline and ubp.baseline["id"]:
                item_outcome["id"] = ubp.baseline["id"]
            elif ubp.proposed and ubp.proposed["id"]:
                item_outcome["id"] = ubp.proposed["id"]

            outcomes.append(item_outcome)
        return outcomes
