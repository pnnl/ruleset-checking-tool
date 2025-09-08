import re
from functools import partial

from pint import Quantity
from rct229.rulesets.ashrae9012019.data import data

EXTRA_SCHEMA = data["ASHRAE229.9012019.extra.schema"]

exception_list = [
    "Enumerations2019ASHRAE901",
    "EnumerationsRESNET",
    "Enumerations2019T24",
    "Output2019ASHRAE901",
]


def if_required(required) -> bool:
    """
    Convert required data from extra schema to a boolean
    If the data is string, then return false else return boolean

    Parameters
    ----------
    required: boolean | str | None

    Returns
    -------
    boolean

    """
    if required is None or isinstance(required, str):
        # unknown
        return False
    else:
        # boolean true or false
        return required


def get_extra_schema_by_data_type(data_type):
    """
    Map the referenced data_type to extra schema element

    Parameters
    ----------
    data_type: string of data reference

    Returns
    -------
    dict | str | None

    """
    if (
        data_type.startswith("[")
        or data_type.startswith("{")
        or data_type.startswith("(")
    ):
        # this is a data group
        data_type = "".join(re.findall(r"\{([^}]+)\}", data_type))
        if (
            EXTRA_SCHEMA.get(data_type)
            and EXTRA_SCHEMA[data_type]["Object Type"] == "Data Group"
        ):
            return EXTRA_SCHEMA[data_type]["Data Elements"]
    elif data_type.startswith("({"):
        # this is for a referenced external schema.
        data_type = "".join(re.findall(r"[\w\s]+", data_type))
        return data_type
    return None


def compare_context_pair(
    index_context,
    compare_context,
    element_json_path,
    extra_schema,
    required_equal,
    search_key,
    error_msg_list,
) -> bool:
    """
    Perform equality comparison between two RPD context
    based on the value in the extra schema specification

    Parameters
    ----------
    index_context: dict|list|str|None, the indexed context (RPD)
    compare_context: dict|list|str|None, the compare context (RPD)
    element_json_path: str, The json path of the compare context
    extra_schema: dict|str, extra schema element
    required_equal: boolean, flag indicates whether the comparison is equal or not required.
    search_key: str, The key in the extra schema that contains the value needed for the comparison
    error_msg_list: list[str] message list

    Returns
    -------
    boolean - true if all comparison checked and confirmed, false otherwise

    """
    matched = True
    if (
        isinstance(index_context, dict)
        and isinstance(compare_context, dict)
        and not isinstance(extra_schema, str)
    ):
        # context shall be aligned and have the same data type.
        if compare_context.get("id") and index_context["id"] != compare_context["id"]:
            error_msg_list.append(
                f'path: {element_json_path}: data object {index_context["id"]} in index context does not match the one {compare_context["id"]} in compare context'
            )
            matched = False

        for key in index_context:
            # id check is performed at the beginning so it should be excluded here.
            if key != "id":
                key_schema = extra_schema[key]
                extra_schema_data_group = get_extra_schema_by_data_type(
                    key_schema["Data Type"]
                )

                new_extra_schema = (
                    extra_schema_data_group
                    if extra_schema_data_group
                    else key_schema["Data Type"]
                )
                if (
                    isinstance(new_extra_schema, str)
                    and new_extra_schema in exception_list
                ):
                    # avoid processing data outside the master schema
                    continue
                # if compare_context is None:
                # Not possible due to the if else condition
                #    print(index_context)
                matched = (
                    compare_context_pair(
                        index_context[key],
                        compare_context.get(key),
                        f"{element_json_path}.{key}",
                        new_extra_schema,
                        if_required(key_schema.get(search_key)),
                        search_key,
                        error_msg_list,
                    )
                    and matched
                )

    elif isinstance(index_context, list) and isinstance(compare_context, list):
        if required_equal and len(compare_context) != len(index_context):
            error_msg_list.append(
                f"path: {element_json_path}: length of objects ({len(index_context)}) in index context != length of objects ({len(compare_context)}) in compare context."
            )
            matched = False

        compare_by_index = "operating_points" in element_json_path.lower()

        if any(isinstance(item, dict) for item in index_context):
            if compare_by_index:
                # position-based comparison for operating_points
                limit = min(len(index_context), len(compare_context))
                for i in range(limit):
                    matched = (
                        compare_context_pair(
                            index_context[i],
                            compare_context[i],
                            f"{element_json_path}[{i}]",
                            extra_schema,
                            if_required(extra_schema.get(search_key)),
                            search_key,
                            error_msg_list,
                        )
                        and matched
                    )
            else:
                # For list that has mix of objects and strings (primary_layers)
                # avoid processing any list of primitive data types
                # sort the proposed and user
                sorted_dict_index = sorted(
                    [
                        item
                        for item in index_context
                        if isinstance(item, dict) and "id" in item
                    ],
                    key=lambda x: x["id"],
                )
                sorted_dict_compare = sorted(
                    [
                        item
                        for item in compare_context
                        if isinstance(item, dict) and "id" in item
                    ],
                    key=lambda x: x["id"],
                )
                for i in range(len(sorted_dict_index)):
                    if i < len(sorted_dict_compare):
                        # in this case, we are still using the same extra_schema
                        matched = (
                            compare_context_pair(
                                sorted_dict_index[i],
                                sorted_dict_compare[i],
                                f"{element_json_path}[{i}]",
                                extra_schema,
                                if_required(extra_schema.get(search_key)),
                                search_key,
                                error_msg_list,
                            )
                            and matched
                        )
            sorted_str_index = sorted(
                [item for item in index_context if isinstance(item, str)]
            )
            sorted_str_compare = sorted(
                [item for item in compare_context if isinstance(item, str)]
            )
            for i in range(len(sorted_str_index)):
                # This should be the leaf, no need further nest
                if i < len(sorted_str_compare):
                    matched = sorted_str_index[i] == sorted_str_compare[i] and matched

    elif isinstance(extra_schema, str):
        # in this case, it is either string, numerical, references or other simple data type
        index_value = index_context
        compare_value = compare_context
        if type(index_context) == type(compare_context) and isinstance(
            index_context, Quantity
        ):
            index_value = index_context.magnitude
            compare_value = compare_context.magnitude

        if required_equal and index_value != compare_value:
            # the != takes care of None data type. if both None, this will still pass.
            error_msg_list.append(
                f"path: {element_json_path}: index context data: {index_context} does not equal to compare context data: {compare_context}"
            )
            matched = False
    else:
        # if the two index_context and compare_context are identical at this point, then it pass, otherwise it failed
        if (
            type(index_context) != type(compare_context)
            or index_context != compare_context
        ):
            # accomodating to mix reference and object type data - in this case, it is a string referenced.
            matched = False
    return matched


proposed_equals_user = partial(
    compare_context_pair,
    element_json_path="$",
    extra_schema=EXTRA_SCHEMA["RulesetProjectDescription"]["Data Elements"],
    required_equal=True,
    search_key="AppG P_RMD Equals U_RMD",
)

baseline_equals_proposed = partial(
    compare_context_pair,
    element_json_path="$",
    extra_schema=EXTRA_SCHEMA["RulesetProjectDescription"]["Data Elements"],
    required_equal=True,
    search_key="AppG B_RMD Equals P_RMD",
)

baseline_equals_baseline = partial(
    compare_context_pair,
    element_json_path="$",
    extra_schema=EXTRA_SCHEMA["RulesetProjectDescription"]["Data Elements"],
    required_equal=True,
    search_key="AppG B_RMDs Same",
)
