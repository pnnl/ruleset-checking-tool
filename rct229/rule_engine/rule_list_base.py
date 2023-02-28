from jsonpointer import resolve_pointer

from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.utils.json_utils import slash_prefix_guarantee


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
        ruleset_section_title=None,
        standard_section=None,
        is_primary_rule=None,
        rmr_context="",
        required_fields=None,
        manual_check_required_msg="Manual Check Required",
        not_applicable_msg="Not Applicable",
        # An example data object:
        #    {"cliimate_zone": ("baseline", weather/climate_zone")}
        data_items=None,
    ):
        self.each_rule = each_rule
        self.data_items = data_items
        super(RuleDefinitionListBase, self).__init__(
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

    def create_context_list(self, context, data):
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

    def create_data(self, context, data):
        """Create the new data dictionary to be merged into the existing data dictionary
        that will be passed to the subrule

        This new data will be merged into the existing data dictionary by the
        rule_check method.

        This method is typically overridden to collect data available at this rule's
        level that is needed by some subrule.

        This default implementation checks for a data argument to the initializer being
        set. If set, the object is resolved as json pointers
        to extract the new data from context.

        If the new data is only one or more elements that can be obtained directly from
        context, then do not override this method; use the data initializer
        instead. Override this method if any calculations are required to obtain the
        new data.

        Parameters
        ----------
        context : UserBaselineProposedVals
            Object containing the user, baseline, and proposed contexts
        data : any
            The data object that was passed into the rule.

        Returns
        -------
        dict
            A dictionary representing new data to be merged into the current data
            dictionary
        """
        new_data = {}
        if self.data_items:
            for key, (component, jptr) in self.data_items.items():
                new_data[key] = resolve_pointer(
                    getattr(context, component), slash_prefix_guarantee(jptr), None
                )

        return new_data

    def list_filter(self, context_item, data):
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
        bool True iff context_item should passed through the filter.
        """
        return True

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
        # Merge in new data to be passed to the subrule indicated by each_rule
        data = {**data, **self.create_data(context, data)}
        if "is_primary_rule" not in data.keys():
            data["is_primary_rule"] = self.is_primary_rule

        # Create the context list
        # Note: create_context_list has access to the new data included just above
        context_list = self.create_context_list(context, data)
        filtered_context_list = [
            context_item
            for context_item in context_list
            if self.list_filter(context_item, data)
        ]

        # Evalutate the subrule for each item in the context list
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
