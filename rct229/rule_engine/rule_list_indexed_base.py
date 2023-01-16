from rct229.rule_engine.rule_list_base import RuleDefinitionListBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.utils.json_utils import slash_prefix_guarantee
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.match_lists import match_lists


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
        function (preceding _) inside the enclosing rule definition.
    data_items: dict
        An object that specifies one or more context items to be added to the data
        dictionary. It has the form:
        {
            "key": ("user"|"baseline"|"proposed", "json pointer to an item in the context"),
            ...
        }
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
        ruleset_section_title=None,
        standard_section=None,
        is_primary_rule=None,
        rmr_context="",
        list_path="$[*]",
        match_by="id",
        required_fields=None,
        manual_check_required_msg="Manual Check Required",
        not_applicable_msg="Not Applicable",
        data_items=None,
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
            required_fields=required_fields,
            manual_check_required_msg=manual_check_required_msg,
            not_applicable_msg=not_applicable_msg,
            data_items=data_items,
            ruleset_section_title=ruleset_section_title,
            standard_section=standard_section,
            is_primary_rule=is_primary_rule,
        )

    def create_context_list(self, context, data):
        """Generates a list of context trios

        Overrides the base implementation to create a list that has an entry
        for each item in the index_rmr RMR, the other RMR entries are padded with
        None for non-matches.

        The resulting list can also be filtered using the list_filter field.

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
