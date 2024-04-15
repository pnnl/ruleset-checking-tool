from rct229.rule_engine.rule_list_base import RuleDefinitionListBase
from rct229.rule_engine.ruleset_model_factory import get_rmd_instance
from rct229.utils.json_utils import slash_prefix_guarantee
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.match_lists import match_lists


class RuleDefinitionListIndexedBase(RuleDefinitionListBase):
    """
    Baseclass for List-type Rule Definitions that use one of the RMR lists as an index list

    Applicable rules typically have the form "for each ___ in the ??? RMR, ...".

    Parameters
    ----------
    rmrs_used : RuleSetModels
        A list of boolean values indicating which RMRs are required by the
        rule
    rmrs_used_optional: RulesetModels
        A boolean values indicating which RMDs are optional by the rule (True optional, False not optional).
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
        rmrs_used_optional=None,
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
            rmrs_used_optional=rmrs_used_optional,
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
        context : RuleSetModels
            Object containing the contexts for RMRs required by the ruleset.
            The base implementation here takes the list context from the rmr context
            and assumes each part is a list.
        data : An optional data object. It is ignored by this base implementation.

        Returns
        -------
        list of RuleSetModels
            A list of context
        """
        UNKNOWN_INDEX_RMR = "Unknown index_rmr"
        CONTEXT_NOT_LIST = "The list contexts must be lists"

        match_by = self.match_by

        # The index RMR must be either user, baseline, or proposed
        if self.index_rmr not in context.get_ruleset_model_types():
            raise ValueError(UNKNOWN_INDEX_RMR)

        # The index RMR must be used
        context_on_list = any(
            map(
                lambda ruleset_model: self.index_rmr == ruleset_model
                and context[ruleset_model],
                context.get_ruleset_model_types(),
            )
        )
        if not context_on_list:
            raise ValueError(CONTEXT_NOT_LIST)

        # Get the list contexts
        list_context = get_rmd_instance()
        for ruleset_model in list_context.get_ruleset_model_types():
            if self.rmrs_used[ruleset_model]:
                list_context.__setitem__(
                    ruleset_model, find_all(self.list_path, context[ruleset_model])
                )
            else:
                list_context.__setitem__(ruleset_model, None)

        # # This implementation assumes the used lists contexts are in fact lists
        # if (
        #     (rmrs_used.user and not isinstance(list_context_trio.user, list))
        #     or (rmrs_used.baseline and not isinstance(list_context_trio.baseline, list))
        #     or (rmrs_used.proposed and not isinstance(list_context_trio.proposed, list))
        # ):
        #     raise ValueError(CONTEXT_NOT_LIST)

        index_rmd_list = list_context[self.index_rmr]
        context_list_len = len(index_rmd_list)
        for ruleset_model in list_context.get_ruleset_model_types():
            if self.rmrs_used[ruleset_model] and ruleset_model != self.index_rmr:
                rmd_list = match_lists(
                    index_rmd_list, list_context[ruleset_model], match_by
                )
                list_context.__setitem__(ruleset_model, rmd_list)

        # Generate the context list
        context_list = []
        for index in range(context_list_len):
            context = get_rmd_instance()
            for ruleset_model in context.get_ruleset_model_types():
                context.__setitem__(
                    ruleset_model,
                    None
                    if list_context[ruleset_model] is None
                    else list_context[ruleset_model][index],
                )
            context_list.append(context)

        return context_list
