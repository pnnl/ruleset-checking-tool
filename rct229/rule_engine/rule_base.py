from jsonpointer import resolve_pointer

from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.utils.json_utils import slash_prefix_guarantee
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.match_lists import match_lists


class RuleDefinitionBase:
    """Baseclass for all Rule Definitions."""

    def __init__(
        self,
        rmrs_used,
        id=None,
        description=None,
        rmr_context="",
        required_fields=None,
        must_match_by_ids=[],
    ):
        """Base class for all Rule definitions

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
        self.rmrs_used = rmrs_used
        self.id = id
        self.description = description
        # rmr_context is a jsonpointer string
        # As a convenience, any leading '/' should not be included and will
        # be inserted when the pointer is used in _get_context().
        # Default rm_context is the root of the RMR
        self.rmr_context = slash_prefix_guarantee(rmr_context)
        self.required_fields = required_fields

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

        # context will be a string if the context does not exist for any of the RMR used
        context_or_string = self.get_context(rmrs, data)
        if isinstance(context_or_string, UserBaselineProposedVals):
            context = context_or_string

            # Check the context for general validity
            context_validity_dict = self.check_context_validity(context, data)
            # If the context is valid, context_validity_dict will be the falsey {}
            if not context_validity_dict:

                # Check if rule is applicable
                if self.is_applicable(context, data):

                    # Get calculated values; these can be used by
                    # manual_check_required() or rule_check() and will
                    # be included in the output
                    calc_vals = self.get_calc_vals(context, data)
                    if calc_vals is not None:
                        outcome["calc_vals"] = calc_vals

                    # Determine if manual check is required
                    if self.manual_check_required(context, calc_vals, data):
                        outcome["result"] = "MANUAL_CHECK_REQUIRED"
                    else:
                        # Evaluate the actual rule check
                        result = self.rule_check(context, calc_vals, data)
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
                outcome["result"] = context_validity_dict
        else:
            # context should be a string indicating the RMRs that are missing
            # such as "MISSING_BASELINE"
            outcome["result"] = context_or_string

        return outcome

    def _get_context(self, rmrs, rmr_context=None):
        """Get the context for each RMR

        Private method, not to be overridden

        Parameters
        ----------
        rmrs : UserBaselineProposedVals
            Object containing the user, baseline, and proposed RMRs
        rmr_context : string|None
            Optional jsonpointer for rmr_context to override self.rmr_context.
            If None, then self.rmr_context is used.

        Returns
        -------
        UserBaselineProposedVals
            Object containing the contexts for the user, baseline, and proposed
            RMRs; an RMR's context is set to None if the corresponding flag
            in self.rmrs_used is not set
        """
        rmr_context = self.rmr_context if rmr_context is None else rmr_context
        # Prepend the leading '/' as needed. It is optional in rmr_context for
        # improved readability
        pointer = rmr_context

        # Note: if there is no match for pointer, resolve_pointer returns None
        return UserBaselineProposedVals(
            user=resolve_pointer(rmrs.user, pointer, None)
            if self.rmrs_used.user
            else None,
            baseline=resolve_pointer(rmrs.baseline, pointer, None)
            if self.rmrs_used.baseline
            else None,
            proposed=resolve_pointer(rmrs.proposed, pointer, None)
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
        UserBaselineProposedVals or str
            The return value from self._get_context() when the context exists
            in each RMR for which the correponding self.rmrs_used flag is set;
            otherwise retrns a string such as "MISSING_BASELINE" that indicates all
            the RMRs that are missing.
        """

        context = self._get_context(rmrs)
        missing_contexts = []
        if self.rmrs_used.user and context.user is None:
            missing_contexts.append("USER")
        if self.rmrs_used.baseline and context.baseline is None:
            missing_contexts.append("BASELINE")
        if self.rmrs_used.proposed and context.proposed is None:
            missing_contexts.append("PROPOSED")

        if len(missing_contexts) > 0:
            retval = "MISSING_" + "_".join(missing_contexts)
        else:
            retval = context

        return retval

    def check_context_validity(self, context, data=None):
        """Check the validity of each used part of the context trio

        It collects the validity error strings from the
        check_user_context_validity, check_baseline_context_validity,
        check_proposed_context_validity methods for the parts in self.rmrs_used.

        This should not be overridden. Override the other check validity methods
        as needed instead.

        Parameters
        ----------
        context : UserBaselineProposedVals
            Object containing the contexts for the user, baseline, and proposed RMRs
        data : An optional data object of any form.

        Returns
        -------
        dict
            A dict of the form
            {
                "INVALID_USER_CONTEXT": Error message,
                "INVALID_BASELINE_CONTEXT": Error message,
                "INVALID_PROPOSED_CONTEXT": Error message
            },
            where the fields are only included if the cooresponding context is
            invalid. Therefore, if the context trio is completely valid, then
            the empty dict, {}, is returned.
        """
        retval = {}

        user_invalid_str = (
            self.check_user_context_validity(context.user, data)
            if self.rmrs_used.user
            else ""
        )
        if user_invalid_str:
            retval["INVALID_USER_CONTEXT"] = user_invalid_str

        baseline_invalid_str = (
            self.check_baseline_context_validity(context.baseline, data)
            if self.rmrs_used.baseline
            else ""
        )
        if baseline_invalid_str:
            retval["INVALID_BASELINE_CONTEXT"] = baseline_invalid_str

        proposed_invalid_str = (
            self.check_proposed_context_validity(context.proposed, data)
            if self.rmrs_used.proposed
            else ""
        )
        if proposed_invalid_str:
            retval["INVALID_PROPOSED_CONTEXT"] = proposed_invalid_str

        return retval

    def check_single_context_validity(self, single_context, data=None):
        """Check the validity of a single part of the context trio

        This may be overridden to provide alternate validation that, by default,
        will be used to validate each part of the context trio.

        This implementation checks for required fields.

        Parameters
        ----------
        single_context : object
            A single part of the context trio
        data : object
            An optional data object of any form. It is ignored by this
            implementation.

        Returns
        -------
        string
            A validation error message. The empty string indicates a valid
            context part.
        """
        invalid_list = []
        if self.required_fields:
            for jpath, fields in self.required_fields.items():
                invalid_str = self._missing_fields_str(jpath, fields, single_context)
                if invalid_str:
                    invalid_list.append(invalid_str)

        return "; ".join(invalid_list) if len(invalid_list) > 0 else ""

    def check_user_context_validity(self, user_context, data=None):
        """Check the validity of the USER part of the context trio

        This may be overridden to provide alternate validation for the USER part
        of the context trio.

        This implementation simply calls the check_single_context_validity
        method with the user_context.

        Parameters
        ----------
        user_context : object
            The USER part of the context trio
        data : object
            An optional data object of any form

        Returns
        -------
        string
            A validation error message. The empty string indicates a valid
            user_context.
        """
        return self.check_single_context_validity(user_context, data)

    def check_baseline_context_validity(self, baseline_context, data=None):
        """Check the validity of the BASELINE part of the context trio

        This may be overridden to provide alternate validation for the BASELINE
        part of the context trio.

        This implementation simply calls the check_single_context_validity
        method with the baseline_context.

        Parameters
        ----------
        baseline_context : object
            The BASELINE part of the context trio
        data : object
            An optional data object of any form

        Returns
        -------
        string
            A validation error message. The empty string indicates a valid
            baseline_context.
        """
        return self.check_single_context_validity(baseline_context, data)

    def check_proposed_context_validity(self, proposed_context, data=None):
        """Check the validity of the PROPOSED part of the context trio

        This may be overridden to provide alternate validation for the PROPOSED
        part of the context trio.

        This implementation simply calls the check_single_context_validity
        method with the proposed_context.

        Parameters
        ----------
        proposed_context : object
            The PROPOSED part of the context trio
        data : object
            An optional data object of any form

        Returns
        -------
        string
            A validation error message. The empty string indicates a valid
            proposed_context.
        """
        return self.check_single_context_validity(proposed_context, data)

    def _missing_fields_str(self, jpath, required_fields, single_context):
        """Untility method for listing missing required fields in a single
        part of the context trio

        Do NOT override this utility method.

        Parameters
        ----------
        jpath: string
            A json path to zero or more dictionaries
        required_fields : list of strings
            A list of the required fields
        single_context : object
            A single part of the context trio

        Returns
        -------
        string
            A string of semicolon separated list of strings of the form
            'id:<id> missing:<comma separated list of missing fields>'
        """
        dicts = find_all(jpath, single_context)
        dicts_errors = []
        for dictionary in dicts:
            missing_fields = []
            for field in required_fields:
                if not field in dictionary:
                    missing_fields.append(field)
            if len(missing_fields) > 0:
                id_or_name_str = (
                    "id:" + str(dictionary["id"])
                    if "id" in dictionary
                    else ("name:" + dictionary["name"] if "name" in dictionary else "")
                )
                dicts_errors.append(
                    id_or_name_str + " missing:" + ",".join(missing_fields)
                )

        return "; ".join(dicts_errors)

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

    def get_calc_vals(self, context, data=None):
        """Calculates values for the rule and returns them in a dict.

        If present, the calculated values become part of the report.

        This method should be overridden if the rule involves calculated values.

        Parameters
        ----------
        context : UserBaselineProposedVals
            Object containing the contexts for the user, baseline, and proposed RMRs
        data : An optional data object. It is ignored by this base implementation.

        Returns
        -------
        dict or None
            Any overriding method should return a dict of the calculated values.
            This base implementation returns None to indicate that there are
            no calculated values for this rule.
        """

        return None

    def manual_check_required(self, context, calc_vals=None, data=None):
        """Checks whether the rule must be manually checked for the
        given context

        This will often be overridden. This base implementation always
        returns False, which allows the workflow to proceed.

        Parameters
        ----------
        context : UserBaselineProposedVals
            Object containing the contexts for the user, baseline, and proposed RMRs
        calc_vals : dict or None

        data : An optional data object. It is ignored by this base implementation.

        Returns
        -------
        boolean
            True if the rule must be manually checked
        """

        return False

    def rule_check(self, context, calc_vals=None, data=None):
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

    def __init__(self, rmrs_used, each_rule, id=None, description=None, rmr_context=""):
        self.each_rule = each_rule
        super(RuleDefinitionListBase, self).__init__(
            rmrs_used=rmrs_used,
            id=id,
            description=description,
            rmr_context=rmr_context,
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
        outcomes = []

        for ubp in context_list:
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


class RuleDefinitionListIndexedBase(RuleDefinitionListBase):
    """
    Baseclass for List-type Rule Definitions that use one of the RMR lists as an index list

    Applicable rules typically have the form "for each ___ in the ??? RMR, ...".

    Parameters
    ----------
    rmrs_used : UserBaselineProposedVals
        A trio of boolen values indicating which RMRs are required by the
        rule
    each_rule : RuleDefinitionBase | RuleDefinitionListBase
        The rule to be applied to each element in the list
    index_rmr : "user" | "baseline" | "proposed"
        Indicates the RMR to be indexed over
    id : string
        Unique id for the rule
        Usually unspecified for nested rules
    description : string
        Rule description
        Usually unspecified for nested rules
    rmr_context : string
        A json pointer into each RMR, or RMR fragment, provided to the rule.
        For better human readability, the leading "/" may be ommitted.
    list_path : string
        A json path string into each RMR fragment that was produced by applying
        rmr_context. The resulting sub-RMR fragments should be the lists to be
        looped over. The default is "[*]" which assumes that the rmr_context is
        the list to be looped over.
        Note: the create_context_list() method can be overridden and
        ignore list_context.
        For better human readability, the leading "/" may be ommitted.
    match_by : string
        A json pointer into each element of the list, generally to a field
        of the list element. The default is "/id" since the id is assumed to
        be unique to the entire RMR.
    """

    def __init__(
        self,
        rmrs_used,
        each_rule,
        index_rmr,
        id=None,
        description=None,
        rmr_context="",
        list_path="[*]",
        match_by="id",
    ):
        self.index_rmr = index_rmr
        self.list_path = list_path
        self.match_by = slash_prefix_guarantee(match_by)
        super(RuleDefinitionListIndexedBase, self).__init__(
            rmrs_used=rmrs_used,
            each_rule=each_rule,
            id=id,
            description=description,
            rmr_context=rmr_context,
        )

    def create_context_list(self, context, data=None):
        """Generates a list of context trios

        Overrides the base implementation to create a list that has an entry
        for each item in the index_rmr RMR, the other RMR entries are padded with
        None for non-matches.

        This may be overridden to produce lists that do not directly appear in
        the RMR.

        Parameters
        ----------
        context : UserBaselineProposedVals
            Object containing the contexts for the user, baseline, and proposed RMRs.
            The base implementation here takes the list context from the rmr context
            and assumes each part is a list.
        data : An optional data object. It is ignored by this base implementation.

        Returns
        -------
        list of UserBaselineProposedVals
            A list of context trios
        """
        UNKNOWN_INDEX_RMR = "Unknown index_rmr"
        UNUSED_INDEX_RMR_MSG = "index_rmr is not being used"
        CONTEXT_NOT_LIST = "The list contexts must be lists"

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

        # Get the list contexts
        list_trio = UserBaselineProposedVals(
            find_all(self.list_path, context.user) if rmrs_used.user else None,
            find_all(self.list_path, context.baseline) if rmrs_used.baseline else None,
            find_all(self.list_path, context.proposed) if rmrs_used.proposed else None,
        )

        # # This implementation assumes the used lists contexts are in fact lists
        # if (
        #     (rmrs_used.user and not isinstance(list_context_trio.user, list))
        #     or (rmrs_used.baseline and not isinstance(list_context_trio.baseline, list))
        #     or (rmrs_used.proposed and not isinstance(list_context_trio.proposed, list))
        # ):
        #     raise ValueError(CONTEXT_NOT_LIST)

        user_list = None
        baseline_list = None
        proposed_list = None

        # User indexed
        if index_rmr == "user":
            user_list = list_trio.user
            context_list_len = len(user_list)
            if rmrs_used.baseline:
                baseline_list = match_lists(
                    list_trio.user, list_trio.baseline, match_by
                )
            if rmrs_used.proposed:
                proposed_list = match_lists(
                    list_trio.user, list_trio.proposed, match_by
                )

        # Baseline indexed
        elif index_rmr == "baseline":
            baseline_list = list_trio.baseline
            context_list_len = len(baseline_list)
            if rmrs_used.user:
                user_list = match_lists(list_trio.baseline, list_trio.user, match_by)
            if rmrs_used.proposed:
                proposed_list = match_lists(
                    list_trio.baseline, list_trio.proposed, match_by
                )

        # Proposed indexed
        elif index_rmr == "proposed":
            proposed_list = list_trio.proposed
            context_list_len = len(proposed_list)
            if rmrs_used.user:
                user_list = match_lists(list_trio.proposed, list_trio.user, match_by)
            if rmrs_used.baseline:
                baseline_list = match_lists(
                    list_trio.proposed, list_trio.baseline, match_by
                )

        # Generate the context list
        context_list = []
        for index in range(context_list_len):
            user_entry = None if user_list is None else user_list[index]
            baseline_entry = None if baseline_list is None else baseline_list[index]
            proposed_entry = None if proposed_list is None else proposed_list[index]

            context_list.append(
                UserBaselineProposedVals(user_entry, baseline_entry, proposed_entry)
            )

        return context_list
