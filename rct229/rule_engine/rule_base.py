from jsonpointer import resolve_pointer

from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.utils.match_lists import match_lists


class RuleDefinitionBase:
    """Baseclass for all Rule Definitions."""

    def __init__(
        self,
        id=None,
        description=None,
        rmr_context="",
        rmrs_used=UserBaselineProposedVals(True, True, True),
    ):
        """Base class for all Rule definitions

        Parameters
        ----------
        id : string
            Unique id for the rule
            Usually unspecified for nested rules
        description : string
            Rule description
            Usually unspecified for nested rules
        rmr_context : string
            A json pointer into each RMR, or RMR fragment, provided to the rule.
            For better human readability, the leading "/" may be ommitted.
        rmrs_used : UserBaselineProposedVals
            A trio of boolen values indicating which RMRs are required by the
            rule
        """
        self.id = id
        self.description = description
        # rmr_context is a jsonpointer string
        # As a convenience, any leading '/' should not be included and will
        # be inserted when the pointer is used in _get_context().
        # Default rm_context is the root of the RMR
        self.rmr_context = rmr_context
        self.rmrs_used = rmrs_used

    def evaluate(self, rmrs, data=None):
        """Generates the outcome dictionary for the rule

        This method also orchestrates the high-level workflow for any rule.
        Namely:
            - Call get_context(rmrs); check for any missing RMR contexts
            - Call is_applicable(context)
            - Call manual_check_required()
            - Call rule_check()
            - Return an outcome dictionary based on the calls above

        This method should NOT be overridden. Instead override get_context,
        is_applicable, manual_check_required, or rule_check as needed.

        Parameters
        ----------
        rmrs : RMR trio or a context trio
        data : Any data object (optional). This is designed as a way to pass in data
            to nested rules. This data passed on to the workflow methods
            get_context(), is_applicable(), manual_check_required(), and
            rule_check().

        Returns
        -------
        dict
            A dictionary of the form:
            {
                id: string - A unique identifier for the rule; ommitted if None
                description: string - The rule description; ommitted if None
                rmr_context: string - a JSON pointer into the RMR; omitted if empty
                result: string or list - One of the strings "PASS", "FAIL", "NA",
                    or "REQUIRES_MANUAL_CHECK" or a list of outcomes for
                    a list-type rule
            }
        """

        # Initialize the outcome dictionary
        outcome = {}
        if self.id:
            outcome["id"] = self.id
        if self.description:
            outcome["description"] = self.description
        if self.rmr_context:
            outcome["rmr_context"] = self.rmr_context

        # context will be None if the context does not exist for any of the RMR used
        context = self.get_context(rmrs, data)
        if context is not None:

            # Check if rule is applicable
            if self.is_applicable(context, data):

                # Determine if manual check is required
                if self.manual_check_required(context, data):
                    outcome["result"] = "MANUAL_CHECK_REQUIRED"
                else:
                    # Evaluate the actual rule check
                    result = self.rule_check(context, data)
                    if isinstance(result, list):
                        # The result is a list of outcomes
                        outcome["result"] = result
                    # Assume result type is bool
                    elif result:
                        outcome["result"] = "PASSED"
                    else:
                        outcome["result"] = "FAILED"

            else:
                outcome["result"] = "NA"
        else:
            outcome["result"] = "MISSING_CONTEXT"

        return outcome

    def _get_context(self, rmrs):
        """Get the context for each RMR

        Private method, not to be overridden

        Parameters
        ----------
        rmrs : UserBaselineProposedVals
            Object containing the user, baseline, and proposed RMRs

        Returns
        -------
        UserBaselineProposedVals
            Object containing the contexts for the user, baseline, and proposed
            RMRs; an RMR's context is set to None if the corresponding flag
            in self.rmrs_used is not set
        """

        # Prepend the leading '/' as needed. It is optional in rmr_context for
        # improved readability
        if self.rmr_context == "" or self.rmr_context.startswith("/"):
            pointer = self.rmr_context
        else:
            pointer = "/" + self.rmr_context

        # Note: if there is no match for pointer, resolve_pointer returns None
        return UserBaselineProposedVals(
            user=resolve_pointer(rmrs.user, pointer) if self.rmrs_used.user else None,
            baseline=resolve_pointer(rmrs.baseline, pointer)
            if self.rmrs_used.baseline
            else None,
            proposed=resolve_pointer(rmrs.proposed, pointer)
            if self.rmrs_used.proposed
            else None,
        )

    def get_context(self, rmrs, data=None):
        """Gets the context for each RMR

        May be be overridden for different behavior

        Parameters
        ----------
        rmrs : UserBaselineProposedVals
            Object containing the user, baseline, and proposed RMRs
            A return value of None indicates that the context
            does not exist in one or more of the RMRs used.
        data : An optional data object. It is ignored by this base implementation.

        Returns
        -------
        UserBaselineProposedVals
            The return value from self._get_context() when the context exists
            in each RMR for which the correponding self.rmrs_used flag is set;
            otherwise None
        """

        context = self._get_context(rmrs)

        return (
            context
            if (
                (context.user is not None if self.rmrs_used.user else True)
                and (context.baseline is not None if self.rmrs_used.baseline else True)
                and (context.proposed is not None if self.rmrs_used.proposed else True)
            )
            else None
        )

    def is_applicable(self, context, data=None):
        """Checks that the rule applies

        This will often be overridden. This base implementation always
        returns True, which allows the workflow to proceed.

        Parameters
        ----------
        context : UserBaselineProposedVals
            Object containing the contexts for the user, baseline, and proposed RMRs
        data : An optional data object. It is ignored by this base implementation.

        Returns
        -------
        boolean
            True if the rule is applicable for the context
        """

        return True

    def manual_check_required(self, context, data=None):
        """Checks whether the rule must be manually checked for the
        given context

        This will often be overridden. This base implementation always
        returns False, which allows the workflow to proceed.

        Parameters
        ----------
        context : UserBaselineProposedVals
            Object containing the contexts for the user, baseline, and proposed RMRs
        data : An optional data object. It is ignored by this base implementation.

        Returns
        -------
        boolean
            True if the rule must be manually checked
        """

        return False

    def rule_check(self, context, data=None):
        """This actually checks the rule for the given context

        This must be overridden. The base implementation
        raises a NotImplementedError

        Parameters
        ----------
        context : UserBaselineProposedVals
            Object containing the contexts for the user, baseline, and proposed RMRs
        data : An optional data object. It is ignored by this base implementation.

        Returns
        -------
        boolean
            True if the rule passes and False if the rule fails
        """

        raise NotImplementedError


class RuleDefinitionListBase(RuleDefinitionBase):
    """
    Baseclass for Rule Definitions that apply to each element in a list context.
    """

    def __init__(self, id, description, rmr_context, rmrs_used, each_rule):
        self.each_rule = each_rule
        super(RuleDefinitionListBase, self).__init__(
            id=id, description=description, rmr_context=rmr_context, rmrs_used=rmrs_used
        )

    def create_context_list(self, context, data=None):
        """Generates a list of context trios from a context that is a trio of
        lists

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

    def rule_check(self, context, data=None):
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
        outcomes = []

        for ubp in context_list:
            item_outcome = self.each_rule.evaluate(ubp, data)

            # Set the name for item_outcome
            if ubp.user and ubp.user["name"]:
                item_outcome["name"] = ubp.user["name"]
            elif ubp.baseline and ubp.baseline["name"]:
                item_outcome["name"] = ubp.baseline["name"]
            elif ubp.proposed and ubp.proposed["name"]:
                item_outcome["name"] = ubp.proposed["name"]

            outcomes.append(item_outcome)
        return outcomes


class RuleDefinitionListIndexedBase(RuleDefinitionListBase):
    """
    Baseclass for List-type Rule Definitions that use one of the RMR lists as an index list

    Applicable rules typically have the form "for each ___ in the ??? RMR, ...".
    """

    def __init__(
        self,
        id,
        description,
        rmr_context,
        rmrs_used,
        each_rule,
        index_rmr="user",
        match_by="/name",
    ):
        self.index_rmr = index_rmr
        self.match_by = match_by
        super(RuleDefinitionListIndexedBase, self).__init__(
            id, description, rmr_context, rmrs_used, each_rule
        )

    def create_context_list(self, context, data=None):
        """Overrides the base implementation to create a list that has an entry
        for each item in the index_rmr RMR, the other RMR entries are padded with
        None for non-matches.

        Parameters
        ----------
        context : UserBaselineProposedVals
            Object containing the contexts for the user, baseline, and proposed RMRs.
            The base implementation here assumes that each rmr context is a list.
        data : An optional data object. It is ignored by this base implementation.

        Returns
        -------
        list of UserBaselineProposedVals
            A list of context trios
        """
        UNKNOWN_INDEX_RMR = "Unknown index_rmr"
        UNUSED_INDEX_RMR_MSG = "index_rmr is not being used"
        CONTEXT_NOT_LIST = "The RMR contexts must be lists"

        index_rmr = self.index_rmr
        rmrs_used = self.rmrs_used
        match_by = self.match_by

        # The index RMR must be either user, baseline, or proposed
        if index_rmr not in ["user", "baseline", "proposed"]:
            raise ValueError(UNKNOWN_INDEX_RMR)

        # The index RMR must be used
        if (
            (index_rmr == "user" and not self.rmrs_used.user)
            or (index_rmr == "baseline" and not self.rmrs_used.baseline)
            or (index_rmr == "proposed" and not self.rmrs_used.proposed)
        ):
            raise ValueError(CONTEXT_NOT_LIST)

        # This implementation assumes the used contexts are lists
        if (
            (rmrs_used.user and not isinstance(context.user, list))
            or (rmrs_used.baseline and not isinstance(context.baseline, list))
            or (rmrs_used.proposed and not isinstance(context.proposed, list))
        ):
            raise ValueError(CONTEXT_NOT_LIST)

        user_list = None
        baseline_list = None
        proposed_list = None

        # User indexed
        if index_rmr == "user":
            user_list = context.user
            context_list_len = len(user_list)
            if rmrs_used.baseline:
                baseline_list = match_lists(context.user, context.baseline, match_by)
            if rmrs_used.proposed:
                matched_lists = match_lists(context.user, context.proposed, match_by)

        # Baseline indexed
        elif index_rmr == "baseline":
            baseline_list = context.baseline
            context_list_len = len(baseline_list)
            if rmrs_used.user:
                user_list = match_lists(context.baseline, context.user, match_by)
            elif rmrs_used.proposed:
                proposed_list = match_lists(
                    context.baseline, context.proposed, match_by
                )

        # Proposed indexed
        elif index_rmr == "proposed":
            proposed_list = context.proposed
            context_list_len = len(proposed_list)
            if rmrs_used.user:
                user_list = match_lists(context.proposed, context.user, match_by)
            elif rmrs_used.baseline:
                baseline_list = match_lists(
                    context.proposed, context.baseline, match_by
                )

        # Generate the context list
        context_list = []
        for index in range(context_list_len):
            if user_list is None:
                user_entry = None
            else:
                user_entry = user_list[index]
            if baseline_list is None:
                baseline_entry = None
            else:
                baseline_entry = baseline_list[index]
            if proposed_list is None:
                proposed_entry = None
            else:
                proposed_entry = proposed_list[index]

            context_list.append(
                UserBaselineProposedVals(user_entry, baseline_entry, proposed_entry)
            )

        return context_list
