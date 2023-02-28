from jsonpointer import resolve_pointer

from rct229.rule_engine.rct_outcome_label import RCTOutcomeLabel
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.utils.assertions import MissingKeyException, RCTFailureException
from rct229.utils.json_utils import slash_prefix_guarantee
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import calcq_to_q


class RuleDefinitionBase:
    """Baseclass for all Rule Definitions."""

    def __init__(
        self,
        rmrs_used,
        id=None,
        description=None,
        ruleset_section_title=None,
        standard_section=None,
        is_primary_rule=None,
        rmr_context="",
        required_fields=None,
        must_match_by_ids=[],
        manual_check_required_msg="",
        fail_msg="",
        pass_msg="",
        not_applicable_msg="",
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
        self.ruleset_section_title = ruleset_section_title
        self.standard_section = standard_section
        self.is_primary_rule = is_primary_rule
        # rmr_context is a jsonpointer string
        # As a convenience, any leading '/' should not be included and will
        # be inserted when the pointer is used in _get_context().
        # Default rm_context is the root of the RMR
        self.rmr_context = slash_prefix_guarantee(rmr_context)
        self.required_fields = required_fields
        self.manual_check_required_msg = manual_check_required_msg
        self.not_applicable_msg = not_applicable_msg
        self.fail_msg = fail_msg
        self.pass_msg = pass_msg

    def evaluate(self, rmrs, data={}):
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
                result: string or list - One of the strings "PASS", "FAIL", "UNDETERMINED", "NOT_APPLICABLE"
                    or a list of outcomes for
                    a list-type rule
            }
        """
        # Initialize the outcome dictionary
        outcome = {}
        if self.id:
            outcome["id"] = self.id
        if self.description:
            outcome["description"] = self.description
        if self.ruleset_section_title:
            outcome["ruleset_section_title"] = self.ruleset_section_title
        if self.standard_section:
            outcome["standard_section"] = self.standard_section
        if self.is_primary_rule is not None:
            outcome["primary_rule"] = True if self.is_primary_rule else False
        if self.rmr_context:
            outcome["rmr_context"] = self.rmr_context

        # context will be a string if the context does not exist for any of the RMD used
        context_or_string = self.get_context(rmrs, data)
        if isinstance(context_or_string, UserBaselineProposedVals):
            context = context_or_string

            # Check the context for general validity
            context_validity_dict = self.check_context_validity(context, data)
            # If the context is valid, context_validity_dict will be the falsey {}
            if not context_validity_dict:
                try:
                    # Check if rule is applicable
                    if self.is_applicable(context, data):
                        # Get calculated values; these can be used by
                        # manual_check_required() or rule_check() and will
                        # be included in the output
                        raw_calc_vals = self.get_calc_vals(context, data)
                        # Convert all CalcQ values to its q value for use in the
                        # remaining methods
                        calc_vals = calcq_to_q(raw_calc_vals)
                        if calc_vals is not None:
                            outcome["calc_vals"] = raw_calc_vals

                        # Determine if manual check is required
                        if self.manual_check_required(context, calc_vals, data):
                            outcome["result"] = RCTOutcomeLabel.UNDETERMINED
                            manual_check_required_msg = (
                                self.get_manual_check_required_msg(
                                    context, calc_vals, data
                                )
                            )
                            if manual_check_required_msg:
                                outcome["message"] = manual_check_required_msg
                        else:
                            # Evaluate the actual rule check
                            result = self.rule_check(context, calc_vals, data)
                            if isinstance(result, list):
                                # The result is a list of outcomes
                                outcome["result"] = result
                            # Assume result type is bool
                            # using is False to include the None case.
                            elif self.is_primary_rule is False or data.get("is_primary_rule") is False:
                                # secondary rule applicability check true-> undetermined, false -> not_applicable
                                if result:
                                    outcome["result"] = RCTOutcomeLabel.UNDETERMINED
                                    undetermined_msg = self.get_manual_check_required_msg(context, calc_vals, data)
                                    if undetermined_msg:
                                        outcome["message"] = undetermined_msg
                                else:
                                    outcome["result"] = RCTOutcomeLabel.NOT_APPLICABLE
                                    undetermined_msg = self.get_not_applicable_msg(context, data)
                                    if undetermined_msg:
                                        outcome["message"] = undetermined_msg
                            elif result:
                                outcome["result"] = RCTOutcomeLabel.PASS
                                pass_msg = self.get_pass_msg(context, calc_vals, data)
                                if pass_msg:
                                    outcome["message"] = pass_msg
                            else:
                                outcome["result"] = RCTOutcomeLabel.FAILED
                                fail_msg = self.get_fail_msg(context, calc_vals, data)
                                if fail_msg:
                                    outcome["message"] = fail_msg
                    else:
                        outcome["result"] = RCTOutcomeLabel.NOT_APPLICABLE
                        not_applicable_msg = self.get_not_applicable_msg(context, data=data)
                        if not_applicable_msg:
                            outcome["message"] = not_applicable_msg
                except MissingKeyException as ke:
                    outcome["result"] = RCTOutcomeLabel.UNDETERMINED
                    outcome["message"] = str(ke)
                except RCTFailureException as fe:
                    outcome["result"] = RCTOutcomeLabel.FAILED
                    outcome["message"] = str(fe)
            else:
                outcome["result"] = "UNDETERMINED"
                outcome["message"] = context_validity_dict
        else:
            # context should be a string indicating the RMDs that are missing
            # such as "MISSING_BASELINE"
            outcome["result"] = "UNDETERMINED"
            outcome["message"] = context_or_string

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

    def get_not_applicable_msg(self, context, calc_vals=None, data=None):
        """Gets the message to include in the outcome for the NOT_APPLICABLE case.

        This base implementation simply returns the value of
        self.not_applicable_msg, which defaults to the empty string.

        This method should only be overridden if there is more than one string
        used for the NOT_APPLICABLE case. A fixed string can be given in the
        `not_applicable_msg` field passed to the initializer.

        Parameters
        ----------
        context : UserBaselineProposedVals
            Object containing the contexts for the user, baseline, and proposed RMRs
        calc_vals : dict | None
        data : dict | None
            An optional data dictionary

        Returns
        -------
        str
            The message associated with the NOT_APPLICABLE case
        """

        return self.not_applicable_msg

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

    def get_manual_check_required_msg(self, context, calc_vals=None, data=None):
        """Gets the message to include in the outcome for the MANUAL_CHECK_REQUIRED case.

        This base implementation simply returns the value of
        self.manual_check_required_msg, which defaults to the empty string.

        This method should only be overridden if there is more than one string
        used for the MANUAL_CHECK_REQUIRED case. A fixed string can be given in the
        `manual_check_required_msg` field passed to the initializer.

        Parameters
        ----------
        context : UserBaselineProposedVals
            Object containing the contexts for the user, baseline, and proposed RMRs
        calc_vals : dict or None

        data : An optional data object. It is ignored by this base implementation.

        Returns
        -------
        str
            The message associated with the MANUAL_CHECK_REQUIRED case
        """

        return self.manual_check_required_msg

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

    def get_fail_msg(self, context, calc_vals=None, data=None):
        """Gets the message to include in the outcome for the FAIL case.

        This base implementation simply returns the value of
        self.fail_msg, which defaults to the empty string.

        This method should only be overridden if there is more than one string
        used for the PASS or FAIL case. A fixed string can be given in the
        `fail_msg` field passed to the initializer.

        Parameters
        ----------
        context : UserBaselineProposedVals
            Object containing the contexts for the user, baseline, and proposed RMRs
        calc_vals : dict or None

        data : An optional data object. It is ignored by this base implementation.

        Returns
        -------
        str
            The message associated with the Pass or Fail case
        """

        return self.fail_msg

    def get_pass_msg(self, context, calc_vals=None, data=None):
        """Gets the message to include in the outcome for the PASS case.

        This base implementation simply returns the value of
        self.pass_msg, which defaults to the empty string.

        This method should only be overridden if there is more than one string
        used for the PASS or PASS case. A fixed string can be given in the
        `pass_msg` field passed to the initializer.

        Parameters
        ----------
        context : UserBaselineProposedVals
            Object containing the contexts for the user, baseline, and proposed RMRs
        calc_vals : dict or None

        data : An optional data object. It is ignored by this base implementation.

        Returns
        -------
        str
            The message associated with the Pass case
        """

        return self.pass_msg
