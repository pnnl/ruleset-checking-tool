import copy
import inspect

import rct229.rulesets as rulesets
from rct229.rule_engine.ruleset_model_factory import RuleSetModels, get_rmd_instance
from rct229.schema.schema_utils import quantify_rmd
from rct229.schema.validate import validate_rpd
from rct229.utils.assertions import RCTException, assert_
from rct229.utils.file import deserialize_rpd_file
from rct229.utils.jsonpath_utils import find_all, find_exactly_one
from rct229.utils.pint_utils import UNIT_SYSTEM, calcq_to_str


def get_available_rules():
    modules = [
        f
        for f in inspect.getmembers(rulesets, inspect.ismodule)
        if f in rulesets.__all__
    ]

    available_rules = []
    for module in modules:
        available_rules += [
            f for f in inspect.getmembers(module[1], inspect.isfunction)
        ]

    return available_rules


def evaluate_all_rules_rpd(ruleset_project_descriptions, session_id=""):
    # Get reference to rule functions in rules model
    available_rule_definitions = rulesets.__getrules__()
    ruleset_models = get_rmd_instance()

    # register all ruleset model list
    rpd_rmd_map_list = []
    for rpd_json in ruleset_project_descriptions:
        for rmd_json in find_all("$.ruleset_model_descriptions[*]", rpd_json):
            model_type = find_exactly_one("$.type", rmd_json)
            # if a rpd json contains multiple, we need to recreate rpd_json
            rpd_json_copy = copy.deepcopy(rpd_json)
            rpd_json_copy["ruleset_model_descriptions"] = [rmd_json]
            ruleset_models.__setitem__(model_type, rpd_json_copy)
            rpd_rmd_map = {
                "ruleset_model_type": model_type,
                "file_name": rpd_json["id"],
            }
            rpd_rmd_map_list.append(rpd_rmd_map)

    print("Processing rules...")
    rules_list = [rule_def[1]() for rule_def in available_rule_definitions]
    report = evaluate_rules(rules_list, ruleset_models, session_id=session_id)
    report["rpd_files"] = rpd_rmd_map_list

    return report


# Functions for evaluating rules
def evaluate_all_rules(ruleset_model_path_list):
    """
    Function to evaluation all rules

    Parameters
    ----------
    ruleset_model_path_list: List
        list of file paths to the ruleset project description files

    Returns
    -------

    """
    if not ruleset_model_path_list:
        raise RCTException("Missing ruleset project description files")
    # Get reference to rule functions in rules model
    available_rule_definitions = rulesets.__getrules__()
    ruleset_models = get_rmd_instance()

    # register all ruleset model list
    rpd_rmd_map_list = []
    for rpd_path in ruleset_model_path_list:
        rpd_json = None
        try:
            rpd_json = deserialize_rpd_file(rpd_path)
        except:
            print(f"{rpd_path} is not a valid JSON file")
            return

        for rmd_json in find_all("$.ruleset_model_descriptions[*]", rpd_json):
            model_type = find_exactly_one("$.type", rmd_json)
            # if a rpd json contains multiple, we need to recreate rpd_json
            rpd_json_copy = copy.deepcopy(rpd_json)
            rpd_json_copy["ruleset_model_descriptions"] = [rmd_json]
            ruleset_models.__setitem__(model_type, rpd_json_copy)
            rpd_rmd_map = {"ruleset_model_type": model_type, "file_name": rpd_path}
            rpd_rmd_map_list.append(rpd_rmd_map)

    print("Processing rules...")
    rules_list = [rule_def[1]() for rule_def in available_rule_definitions]
    report = evaluate_rules(rules_list, ruleset_models)
    report["rpd_files"] = rpd_rmd_map_list

    return report


def evaluate_rule(rule, rmds, test=False):
    """Evaluates a single rule against an RMD trio

    Parameters
    ----------
    rmds : RuleSetModels
        Object containing the RMDs required by enum schema
    test: Boolean
        A flag to indicate whether the evaluate rule is a software test workflow or not.

    Returns
    -------
    dict
        A dictionary of the form:
        {
            invalid_rmds: dict - The keys are the names of the invalid RMDs.
                The values are the corresponding schema validation errors.
            outcomes: [dict] - A list containing a single rule outcome as
                a dictionary of the form:
                {
                    id: string - A unique identifier for the rule
                    description: string
                    rmd_context: string - a JSON pointer into the RMD
                    result: string or list - One of the strings "PASS", "FAIL", "NA", or "REQUIRES_MANUAL_CHECK" or a list
                        of outcomes for a list-type rule
                }
        }
    """

    return evaluate_rules([rule], rmds, test=test)


def evaluate_rules(
    rules_list: list,
    rmds: RuleSetModels,
    unit_system=UNIT_SYSTEM.IP,
    test=False,
    session_id="",
):
    """Evaluates a list of rules against an RMDs

    Parameters
    ----------
    rules_list : list
        list of rule definitions
    rmds : RuleSetModels
        Object containing RPDs for ruleset evaluation
    test: Boolean
        Flag to indicate whether this run is for software testing workflow or not.
    session_id: string

    Returns
    -------
    dict
        A dictionary of the form:
        {
            invalid_rmds: dict - The keys are the names of the invalid RMDs.
                The values are the corresponding schema validation errors.
            outcomes: [dict] - A list of rule outcomes; each outcome is
                a dictionary of the form:
                {
                    id: string - A unique identifier for the rule
                    description: string
                    rmd_context: string - a JSON pointer into the RMD
                    result: string or list - One of the strings "PASS", "FAIL", "NA", or "REQUIRES_MANUAL_CHECK" or a list
                        of outcomes for a list-type rule
                }
        }
    """

    # Validate the rmds against the schema and other high-level checks
    outcomes = []
    invalid_rmds = {}
    rmds_used = get_rmd_instance()
    for rule in rules_list:
        for ruleset_model in rmds.get_ruleset_model_types():
            if rule.rmds_used[ruleset_model] and not (
                rule.rmds_used_optional and rule.rmds_used_optional[ruleset_model]
            ):
                rmds_used[ruleset_model] = True

    for ruleset_model in rmds.get_ruleset_model_types():
        if rmds_used[ruleset_model]:
            rmd_validation = validate_rpd(rmds[ruleset_model], test)
            if rmd_validation["passed"] is not True:
                invalid_rmds[ruleset_model] = rmd_validation["errors"]

    assert_(
        len(invalid_rmds) == 0,
        f"Required RPDs provided are invalid. See error messages: {invalid_rmds}",
    )

    ## Now check the optional RMDs
    invalid_rmds = {}
    for ruleset_model in rmds.get_ruleset_model_types():
        # used is None but rmds contain this ruleset model
        if not rmds_used[ruleset_model] and rmds.__getitem__(ruleset_model):
            rmd_validation = validate_rpd(rmds[ruleset_model], test)
            if rmd_validation["passed"] is not True:
                invalid_rmds[ruleset_model] = rmd_validation["errors"]

    assert_(
        len(invalid_rmds) == 0,
        f"Optional RPDs provided are invalid. See error messages in terminal.",
    )
    # Evaluate the rules if all the used rmds are valid
    # Replace the numbers that have schema units in the RMDs with the
    # appropriate pint quantities
    # TODO: quantitization should happen right after schema validation and
    # before other validations
    copied_rmds = get_rmd_instance()
    for rule_model in copied_rmds.get_ruleset_model_types():
        if rmds[rule_model]:
            copied_rmds[rule_model] = quantify_rmd(rmds.__getitem__(rule_model))

    total_num_rules = len(rules_list)
    if total_num_rules < 10:
        step = 1
    elif total_num_rules < 20:
        step = total_num_rules // 10 + 1
    else:
        step = round(total_num_rules * 0.05)
    counting_steps = list(range(0, total_num_rules, step))
    if counting_steps[-1] < total_num_rules:
        # ensure to add the 100% report
        counting_steps.append(total_num_rules)

    # counter starts at 1
    rule_counter = 0
    # Evaluate the rules
    if len(rules_list) == 1:
        outcome = rules_list[0].evaluate(copied_rmds)
        outcomes.append(outcome)
    else:
        for rule in rules_list:
            print(f"Processing Rule {rule.id}")
            outcome = rule.evaluate(copied_rmds)
            outcomes.append(outcome)
            rule_counter += 1
            if rule_counter in counting_steps:
                print(
                    f"Project Evaluation Session ID: #{session_id}# => Compliance evaluation progress: {round(rule_counter / total_num_rules * 100)}%"
                )

    return {
        "invalid_rmds": invalid_rmds,
        "outcomes": calcq_to_str(unit_system, outcomes),
    }
