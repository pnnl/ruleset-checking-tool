from functools import partial
from typing import TypedDict, Mapping

from jsonpointer import resolve_pointer
from rct229.rule_engine.rct_outcome_label import RCTOutcomeLabel
from rct229.rule_engine.ruleset_model_factory import RuleSetModels, get_rmd_instance
from rct229.schema.config import ureg
from rct229.utils.assertions import MissingKeyException, RCTFailureException
from rct229.utils.json_utils import slash_prefix_guarantee
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import calcq_to_q
from rct229.utils.std_comparisons import std_equal_with_precision, std_equal


class RCTPrecision(TypedDict):
    precision: float
    unit: str | None


class RuleDefinitionBase:
    """Baseclass for all Rule Definitions."""

    def __init__(
        self,
        rmds_used,
        rmds_used_optional=None,
        id: str = None,
        description: str = None,
        ruleset_section_title: str = None,
        standard_section: str = None,
        is_primary_rule: bool = None,
        rmd_context: str = "",
        required_fields=None,
        manual_check_required_msg: str = "",
        fail_msg: str = "",
        pass_msg: str = "",
        not_applicable_msg: str = "",
        precision: Mapping[str, RCTPrecision] = None,
    ):
        """Base class for all Rule definitions

        Parameters
        ----------
        rmds_used : RulesetModels
            A boolean values indicating which RMDs are required by the
            rule
        rmds_used_optional: RulesetModels
            A boolean values indicating which RMDs are optional by the rule (True optional, False not optional).
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
        rmd_context : string
            A json pointer into each RMD, or RMD fragment, provided to the rule.
            For better human readability, the leading "/" may be ommitted.
        required_fields : dict
            A dictionary of the form
            {
                "<json path>": [<required field names>],
                ...
            },
            where the json path should resolve to a list of dectionaries.
        manual_check_required_msg: string
            default message for UNDETERMINED outcome
        fail_msg: string
            default message for FAILED outcome
        pass_msg: string
            default message for PASS outcome
        not_applicable_msg: string
            default message for NOT_APPLICABLE outcome
        precision: dict
            precision value(s) in a dictionary
            e.g.,
            {
                "subsurface_u_factor_b": {
                    "precision": 0.01,
                    "unit": "Btu/(hr*ft2*R)"
                }
            }
        """
        self.rmds_used = rmds_used
        self.rmds_used_optional = rmds_used_optional
        self.id = id
        self.description = description
        self.ruleset_section_title = ruleset_section_title
        self.standard_section = standard_section
        self.is_primary_rule = is_primary_rule
        # rmd_context is a jsonpointer string
        # As a convenience, any leading '/' should not be included and will
        # be inserted when the pointer is used in _get_context().
        # Default rm_context is the root of the RMD
        self.rmd_context = slash_prefix_guarantee(rmd_context)
        self.required_fields = required_fields
        self.manual_check_required_msg = manual_check_required_msg
        self.not_applicable_msg = not_applicable_msg
        self.fail_msg = fail_msg
        self.pass_msg = pass_msg
        self.precision_comparison = None

        if precision:
            self.precision_comparison = {
                # if no unit, handle it as a dimensionless value.
                key: partial(
                    std_equal_with_precision,
                    precision=val["precision"] * ureg(val["unit"])
                    if val.get("unit")
                    else val["precision"],
                )
                for key, val in precision.items()
            }
        else:
            # default comparison to be strict equality comparison
            self.precision_comparison = lambda val, std_val: std_equal(std_val, val)

    def evaluate(self, rmds, data={}):
        """Generates the outcome dictionary for the rule

        This method also orchestrates the high-level workflow for any rule.
        Namely:
            - Call get_context(rmds); check for any missing RMD contexts
            - Call is_applicable(context)
            - Call manual_check_required()
            - Call rule_check()
            - Return an outcome dictionary based on the calls above

        This method should NOT be overridden. Instead override get_context,
        is_applicable, manual_check_required, or rule_check as needed.

        Parameters
        ----------
        rmds : RuleSetModels RMD models or a context list
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
                rmd_context: string - a JSON pointer into the RMD; omitted if empty
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
        if self.rmd_context:
            outcome["rmd_context"] = self.rmd_context

        # context will be a string if the context does not exist for any of the RMD used
        context_or_string = self.get_context(rmds, data)
        if isinstance(context_or_string, RuleSetModels):
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
                                if len(result) == 0:
                                    # empty list:
                                    outcome["result"] = RCTOutcomeLabel.NOT_APPLICABLE
                                    not_applicable_msg = self.get_not_applicable_msg(
                                        context, data
                                    )
                                    if not_applicable_msg:
                                        outcome["message"] = not_applicable_msg
                                    # The result is a list of outcomes
                                else:
                                    outcome["result"] = result
                            # using is False to include the None case.
                            elif self.is_primary_rule is False:
                                # secondary rule applicability check true-> undetermined, false -> not_applicable
                                if result:
                                    outcome["result"] = RCTOutcomeLabel.UNDETERMINED
                                    undetermined_msg = (
                                        self.get_manual_check_required_msg(
                                            context, calc_vals, data
                                        )
                                    )
                                    if undetermined_msg:
                                        outcome["message"] = undetermined_msg
                                else:
                                    outcome["result"] = RCTOutcomeLabel.NOT_APPLICABLE
                                    undetermined_msg = self.get_not_applicable_msg(
                                        context, data
                                    )
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
                                if self.is_tolerance_fail(context, calc_vals, data):
                                    fail_msg = fail_msg + " ::TOLERANCE::"
                                if fail_msg:
                                    outcome["message"] = fail_msg
                    else:
                        outcome["result"] = RCTOutcomeLabel.NOT_APPLICABLE
                        not_applicable_msg = self.get_not_applicable_msg(context, data)
                        if not_applicable_msg:
                            outcome["message"] = not_applicable_msg
                except MissingKeyException as ke:
                    outcome["result"] = RCTOutcomeLabel.UNDETERMINED
                    outcome["message"] = str(ke)
                except RCTFailureException as fe:
                    outcome["result"] = RCTOutcomeLabel.UNDETERMINED
                    outcome["message"] = str(fe)
            else:
                outcome["result"] = RCTOutcomeLabel.UNDETERMINED
                outcome["message"] = context_validity_dict
        else:
            # context should be a string indicating the RMDs that are missing
            # such as "MISSING_BASELINE"
            outcome["result"] = RCTOutcomeLabel.UNDETERMINED
            outcome["message"] = context_or_string

        return outcome

    def _get_context(self, rmds, rmd_context=None):
        """Get the context for each RMD

        Private method, not to be overridden

        Parameters
        ----------
        rmds : RuleSetModels
            Object containing the RMDs for each required ruleset model type
        rmd_context : string|None
            Optional jsonpointer for rmd_context to override self.rmd_context.
            If None, then self.rmd_context is used.

        Returns
        -------
        RuleSetModels
            Object containing the contexts for RMDs; an RMD's context is set to None if the corresponding flag
            in self.rmds_used is not set
        """
        rmd_context = self.rmd_context if rmd_context is None else rmd_context
        # Prepend the leading '/' as needed. It is optional in rmd_context for
        # improved readability
        pointer = rmd_context

        ruleset_models = get_rmd_instance()
        for ruleset_model_type in ruleset_models.get_ruleset_model_types():
            if self.rmds_used[ruleset_model_type]:
                ruleset_models.__setitem__(
                    ruleset_model_type,
                    resolve_pointer(rmds[ruleset_model_type], pointer, None),
                )

        # Note: if there is no match for pointer, resolve_pointer returns None
        return ruleset_models

    def get_context(self, rmds, data=None):
        """Gets the context for each RMD

        May be be overridden for different behavior

        Parameters
        ----------
        rmds : RuleSetModels
            Object containing the RMDs for each required ruleset model types
            A return value of None indicates that the context
            does not exist in one or more of the RMDs used.
        data : An optional data object. It is ignored by this base implementation.

        Returns
        -------
        RulesetModelTypes or str
            The return value from self._get_context() when the context exists
            in each RMD for which the corresponding self.rmds_used flag is set;
            otherwise retrns a string such as "MISSING_BASELINE" that indicates all
            the RMDs that are missing.
        """

        context = self._get_context(rmds)
        missing_contexts = []
        ruleset_model_types = rmds.get_ruleset_model_types()
        for ruleset_model in ruleset_model_types:
            if (
                # rmd used
                self.rmds_used[ruleset_model]
                and not (
                    # and rmd is not optional
                    self.rmds_used_optional
                    and self.rmds_used_optional[ruleset_model]
                )
                # and rmds[ruleset_model] is None or empty
                and (rmds[ruleset_model] is None or not rmds[ruleset_model])
            ):
                missing_contexts.append(ruleset_model)

        if len(missing_contexts) > 0:
            retval = "MISSING_" + "_".join(missing_contexts)
        else:
            retval = context

        return retval

    def check_context_validity(self, context, data=None):
        """Check the validity of each used part of the context trio

        It collects the validity error strings from the
        check_user_context_validity, check_baseline_context_validity,
        check_proposed_context_validity methods for the parts in self.rmds_used.

        This should not be overridden. Override the other check validity methods
        as needed instead.

        Parameters
        ----------
        context : RuleSetModels
            Object containing the contexts for RMDs of required ruleset model type
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
        ruleset_models = context.get_ruleset_model_types()
        for ruleset_model in ruleset_models:
            invalid_str = (
                self.check_single_context_validity(context[ruleset_model], data)
                if context[ruleset_model]
                else ""
            )
            if invalid_str:
                retval[f"{ruleset_model}_MISSING_DATA"] = invalid_str

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
        context : RuleSetModels
            Object containing the contexts for RMDs
        data : An optional data object. It is ignored by this base implementation.

        Returns
        -------
        boolean
            True if the rule is applicable for the context
        """

        return True

    def get_not_applicable_msg(self, context, data=None):
        """Gets the message to include in the outcome for the NOT_APPLICABLE case.

        This base implementation simply returns the value of
        self.not_applicable_msg, which defaults to the empty string.

        This method should only be overridden if there is more than one string
        used for the NOT_APPLICABLE case. A fixed string can be given in the
        `not_applicable_msg` field passed to the initializer.

        Parameters
        ----------
        context : RuleSetModels
            Object containing the contexts for RMDs
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
        context : RuleSetModels
            Object containing the contexts for RMDs
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
        context : RuleSetModels
            Object containing the contexts for RMDs
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
        context : RuleSetModels
            Object containing the contexts for RMDs
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
        context : RuleSetModels
            Object containing the contexts for RMDs
        calc_vals: dictionary
            Dictionary contains calculated values for rule check and reporting.
        data : An optional data object. It is ignored by this base implementation.

        Returns
        -------
        boolean
            True if the rule passes and False if the rule fails
        """

        raise NotImplementedError

    def is_tolerance_fail(self, context, calc_vals=None, data=None):
        """Check if the failure is because of tolerance

        This method should only be overridden if the rule check is comparing
        a number with another number.

        Parameters
        ----------
        context : RuleSetModels
            Object containing the contexts for RMDs
        calc_vals : dict or None

        data : An optional data object. It is ignored by this base implementation.

        Returns
        -------
        bool
            True fail because of tolerance, False otherwise.
        """
        return False

    def get_fail_msg(self, context, calc_vals=None, data=None):
        """Gets the message to include in the outcome for the FAIL case.

        This base implementation simply returns the value of
        self.fail_msg, which defaults to the empty string.

        This method should only be overridden if there is more than one string
        used for the PASS or FAIL case. A fixed string can be given in the
        `fail_msg` field passed to the initializer.

        Parameters
        ----------
        context : RuleSetModels
            Object containing the contexts for RMDs
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
        context : RuleSetModels
            Object containing the contexts for RMDs
        calc_vals : dict or None

        data : An optional data object. It is ignored by this base implementation.

        Returns
        -------
        str
            The message associated with the Pass case
        """

        return self.pass_msg
