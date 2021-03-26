from jsonpointer import resolve_pointer

from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.utils.match_lists import match_lists

class RuleDefinitionBase:
    """Baseclass for all Rule Definitions.
    """
    def __init__(self, id = None, description = None, rmr_context = '', rmrs_used = UserBaselineProposedVals(True, True, True)):
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

    def evaluate(self, rmrs):
        """ Generates the outcome dictionary for the rule

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
            outcome['id'] = self.id
        if self.description:
            outcome['description'] = self.description
        if self.rmr_context:
            outcome['rmr_context'] = self.rmr_context

        # context will be None if the context does not exist for any of the RMR used
        context = self.get_context(rmrs)
        if context is not None:

            # Check if rule is applicable
            if self.is_applicable(context):

                # Determine if manual check is required
                if self.manual_check_required(context):
                    outcome['result'] = 'MANUAL_CHECK_REQUIRED'
                else:
                    # Evaluate the actual rule check
                    result = self.rule_check(context)
                    if isinstance(result, list):
                        # The result is a list of outcomes
                        outcome['result'] = result
                    # Assume result type is bool
                    elif result:
                        outcome['result'] = 'PASSED'
                    else:
                        outcome['result'] = 'FAILED'

            else:
                outcome['result'] = 'NA'
        else:
            outcome['result'] = 'MISSING_CONTEXT'

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
        if self.rmr_context == '' or self.rmr_context.startswith('/'):
            pointer = self.rmr_context
        else:
            pointer = '/' + self.rmr_context

        # Note: if there is no match for pointer, resolve_pointer returns None
        return UserBaselineProposedVals(
            user = resolve_pointer(rmrs.user, pointer) if self.rmrs_used.user else None,
            baseline = resolve_pointer(rmrs.baseline, pointer) if self.rmrs_used.baseline else None,
            proposed = resolve_pointer(rmrs.proposed, pointer) if self.rmrs_used.proposed else None
        )

    def get_context(self, rmrs):
        """Gets the context for each RMR

        May be be overridden for different behavior

        Parameters
        ----------
        rmrs : UserBaselineProposedVals
            Object containing the user, baseline, and proposed RMRs
            A return value of None indicates that the context
            does not exist in one or more of the RMRs used.

        Returns
        -------
        UserBaselineProposedVals
            The return value from self._get_context() when the context exists
            in each RMR for which the correponding self.rmrs_used flag is set;
            otherwise None
        """

        context = self._get_context(rmrs)

        return (
            context if (
                (context.user is not None if self.rmrs_used.user else True)
                and (context.baseline is not None if self.rmrs_used.baseline else True)
                and (context.proposed is not None if self.rmrs_used.proposed else True))
            else None
        )


    def is_applicable(self, context):
        """Checks that the rule applies

        This will often be overridden. This base implementation always
        returns True, which allows the workflow to proceed.

        Parameters
        ----------
        context : UserBaselineProposedVals
            Object containing the contexts for the user, baseline, and proposed RMRs

        Returns
        -------
        boolean
            True if the rule is applicable for the context
        """

        return True

    def manual_check_required(self, context):
        """Checks whether the rule must be manually checked for the
        given context

        This will often be overridden. This base implementation always
        returns False, which allows the workflow to proceed.

        Parameters
        ----------
        context : UserBaselineProposedVals
            Object containing the contexts for the user, baseline, and proposed RMRs

        Returns
        -------
        boolean
            True if the rule must be manually checked
        """

        return False

    def rule_check(self, context):
        """This actually checks the rule for the given context

        This must be overridden. The base implementation
        raises a NotImplementedError

        Parameters
        ----------
        context : UserBaselineProposedVals
            Object containing the contexts for the user, baseline, and proposed RMRs

        Returns
        -------
        boolean
            True if the rule passes and False if the rule fails
        """

        raise NotImplementedError


# class RuleDefinitionSingleElementBase(RuleDefinitionBase):
#     """
#     Baseclass for Rule Definitions that are applied to an entire list of elements.
#     """
#     def __init__(self, id, description, rmr_context, rmrs_used):
#         super(RuleDefinitionSingleElementBase, self).__init__(id, description, rmr_context, rmrs_used)
#         print()
#
#     def rule_check(self, user, baseline, proposed):
#         # Throw an exception if not overridden by inherited class
#         #outcome = False # Boolean
#         #<Calculation>
#         #return outcome
#
#         raise NotImplementedError


class RuleDefinitionListBase(RuleDefinitionBase):
    """
    Baseclass for Rule Definitions that apply to each element in a list context.
    """
    def __init__(self, id, description, rmr_context, rmrs_used, each_rule):
        self.each_rule = each_rule
        super(RuleDefinitionListBase, self).__init__(id, description, rmr_context, rmrs_used)

    def create_context_list(self, context):
        """Generates a list of context trios from a context that is a trio of
        lists

        For a list-type rule, we generaly need to match up the entries in the
        RMR lists by name and then apply a rule to each trio of entries. This
        method does this matching and returns a list of trios (the contexts
        needed for a particular matching).


        This may be overridden for different matching strategies. The
        base implementation sorts by the name field, matches by name to the
        extent possible, and pads with None for non-mathes.

        Parameters
        ----------
        context : UserBaselineProposedVals
            Object containing the contexts for the user, baseline, and proposed RMRs

        Returns
        -------
        list of UserBaselineProposedVals
            A list of context trios
        """
        u_len = len(context.user) if isinstance(context.user, list) else 0
        b_len = len(context.baseline) if isinstance(context.baseline, list) else 0
        p_len = lem(context.proposed) if isinstance(context.proposed, list) else 0
        context_list_len = max(u_len, b_len, p_len)
        none_list = [None for i in range(context_list_len)]

        def get_name(obj):
            return obj['name']

        # Create three sorted, equal-length lists, padding with None as needed
        u_list = context.user.sort(key = get_name) if context.user is not None else none_list
        u_list.extend([None for i in range(context_list_len - len(u_list))])
        b_list = context.baseline.sort(key = get_name) if context.baseline is not None else none_list
        b_list.extend([None for i in range(context_list_len - len(b_list))])
        p_list = context.proposed.sort(key = get_name) if context.proposed is not None else none_list
        p_list.extend([None for i in range(context_list_len - len(p_list))])

        context_list = [UserBaselineProposedVals(u_list[i], b_list[i], p_list[i]) for i in range(context_list_len)]

        return context_list

    def rule_check(self, context):
        """Overrides the base implementation to apply a rule to each entry in
        a list

        This should not be overridden. Override create_context_list() instead.

        Parameters
        ----------
        context : UserBaselineProposedVals
            Object containing the contexts for the user, baseline, and proposed RMRs

        Returns
        -------
        list
            A list of rule outcomes. The each outcome in the list is augmented
            with a name field that is the name of the entry in the context list.
        """
        context_list = self.create_context_list(context)
        outcomes = []

        for ubp in context_list:
            item_outcome = self.each_rule.evaluate(ubp)

            # Set the name for item_outcome
            if ubp.user and ubp.user['name']:
                item_outcome['name'] = ubp.user['name']
            elif ubp.baseline and ubp.baseline['name']:
                item_outcome['name'] = ubp.baseline['name']
            elif ubp.proposed and ubp.proposed['name']:
                item_outcome['name'] = ubp.proposed['name']

            outcomes.append(item_outcome)
        return outcomes


class RuleDefinitionListIndexedBase(RuleDefinitionListBase):
    """
    Baseclass for List-type Rule Definitions that use one of the RMR lists as an index list

    Applicable rules typically have the form "for each ___ in the ??? RMR, ...".
    """
    def __init__(self, id, description, rmr_context, rmrs_used, each_rule, index_rmr = 'user'):
        self.index_rmr = index_rmr
        super(RuleDefinitionListIndexedBase, self).__init__(id, description, rmr_context, rmrs_used, each_rule)

    def create_context_list(self, context):
        """Overrides the base implementation to create a list that has an entry
        for each item in the index_rmr RMR, the other RMR entries are padded with
        None for non-matches.

        Parameters
        ----------
        context : UserBaselineProposedVals
            Object containing the contexts for the user, baseline, and proposed RMRs

        Returns
        -------
        list of UserBaselineProposedVals
            A list of context trios
        """
        # This implimentation assumes at most two rmrs being used
        if self.rmrs_used.user and self.rmrs_used.baseline and self.rmrs_used.proposed:
            raise NotImplementedError

        UNUSED_INDEX_RMR_MSG = 'Index RMR is not being used'

        context_list = None
        # User indexed
        if self.index_rmr == 'user':
            if not self.rmrs_used.user:
                raise ValueError(UNUSED_INDEX_RMR_MSG)

            index_range = range(len(context.user))
            if self.rmrs_used.baseline:
                # Match baseline to user
                matched_lists = match_lists(context.user, context.baseline, '/name')
                context_list = [UserBaselineProposedVals(matched_lists[0][index], matched_lists[1][index], None) for index in index_range]
            elif self.rmrs_used.proposed:
                # Match proposed to user
                matched_lists = match_lists(context.user, context.proposed, '/name')
                context_list = [UserBaselineProposedVals(matched_lists[0][index], None, matched_lists[1][index]) for index in index_range]
            else:
                # Only user
                context_list = [UserBaselineProposedVals(context.user[index], None, None) for index in index_range]
        # Baseline indexed
        elif self.index_rmr == 'baseline':
            if not self.rmrs_used.baseline:
                raise ValueError(UNUSED_INDEX_RMR_MSG)

            index_range = range(len(context.baseline))
            if self.rmrs_used.user:
                # Match user to baseline
                matched_lists = match_lists(context.baseline, context.user, '/name')
                context_list = [UserBaselineProposedVals(matched_lists[1][index], matched_lists[0][index], None) for index in index_range]
            elif self.rmrs_used.proposed:
                # Match proposed to baseline
                matched_lists = match_lists(context.baseline, context.proposed, '/name')
                context_list = [UserBaselineProposedVals(None, matched_lists[0][index], matched_lists[1][index]) for index in index_range]
            else:
                # Only baseline
                context_list = [UserBaselineProposedVals(None, context.baseline[index], None) for index in index_range]
        # Proposed indexed
        elif self.index_rmr == 'proposed':
            if not self.rmrs_used.proposed:
                raise ValueError(UNUSED_INDEX_RMR_MSG)

            index_range = range(len(context.proposed))
            if self.rmrs_used.user:
                # Match usr to proposed
                matched_lists = match_lists(context.proposed, context.user, '/name')
                context_list = [UserBaselineProposedVals(matched_lists[1][index], None, matched_lists[0][index]) for index in index_range]
            elif self.rmrs_used.baseline:
                # Match baseline to proposed
                matched_lists = match_lists(context.proposed, context.baseline, '/name')
                context_list = [UserBaselineProposedVals(None, matched_lists[1][index], matched_lists[0][index]) for index in index_range]
            else:
                # Only proposed
                context_list = [UserBaselineProposedVals(None, None, context.proposed[index]) for index in index_range]
        else:
            raise ValueError('Unknown index_rmr')

        return context_list
