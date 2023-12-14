import inspect

from rct229.schema.schema_utils import quantify_rmr
from rct229.schema.validate import validate_rmr
from rct229.utils.assertions import assert_
from rct229.utils.file import deserialize_rpd_file
from rct229.utils.jsonpath_utils import (
    find_all,
    find_exactly_one,
)
from rct229.utils.pint_utils import UNIT_SYSTEM, calcq_to_str
import rct229.rulesets as rulesets
from rct229.rule_engine.ruleset_model_factory import RuleSetModels, get_rmd_instance


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
            ruleset_models.__setitem__(model_type, rpd_json)
            rpd_rmd_map = {"ruleset_model_type": model_type, "file_name": rpd_path}
            rpd_rmd_map_list.append(rpd_rmd_map)

    print("Processing rules...")
    rules_list = [rule_def[1]() for rule_def in available_rule_definitions]
    report = evaluate_rules(rules_list, ruleset_models)
    report["rpd_files"] = rpd_rmd_map_list

    return report


def evaluate_rule(rule, rmrs):
    """Evaluates a single rule against an RMR trio

    Parameters
    ----------
    rmrs : RuleSetModels
        Object containing the RMRs required by enum schema

    Returns
    -------
    dict
        A dictionary of the form:
        {
            invalid_rmrs: dict - The keys are the names of the invalid RMRs.
                The values are the corresponding schema validation errors.
            outcomes: [dict] - A list containing a single rule outcome as
                a dictionary of the form:
                {
                    id: string - A unique identifier for the rule
                    description: string
                    rmr_context: string - a JSON pointer into the RMR
                    result: string or list - One of the strings "PASS", "FAIL", "NA", or "REQUIRES_MANUAL_CHECK" or a list
                        of outcomes for a list-type rule
                }
        }
    """

    return evaluate_rules([rule], rmrs)


def evaluate_rules(rules_list: list, rmds: RuleSetModels, unit_system=UNIT_SYSTEM.IP):
    """Evaluates a list of rules against an RMDs

    Parameters
    ----------
    rules_list : list
        list of rule definitions
    rmds : RuleSetModels
        Object containing RPDs for ruleset evaluation

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
                    rmr_context: string - a JSON pointer into the RMR
                    result: string or list - One of the strings "PASS", "FAIL", "NA", or "REQUIRES_MANUAL_CHECK" or a list
                        of outcomes for a list-type rule
                }
        }
    """

    # Validate the rmrs against the schema and other high-level checks
    outcomes = []
    invalid_rmds = {}
    rmds_used = get_rmd_instance()
    for rule in rules_list:
        for rule_model in rmds.get_ruleset_model_types():
            if rule.rmrs_used[rule_model]:
                rmds_used[rule_model] = True

    for rule_model in rmds.get_ruleset_model_types():
        if rmds_used[rule_model]:
            rmd_validation = validate_rmr(rmds[rule_model])
            if rmd_validation["passed"] is not True:
                invalid_rmds[rule_model] = rmd_validation["error"]

    assert_(
        len(invalid_rmds) == 0,
        f"RPDs provided are invalid. See error messages in terminal.",
    )

    # Evaluate the rules if all the used rmrs are valid
    # Replace the numbers that have schema units in the RMRs with the
    # appropriate pint quantities
    # TODO: quantitization should happen right after schema validation and
    # before other validations
    copied_rmds = get_rmd_instance()
    for rule_model in copied_rmds.get_ruleset_model_types():
        if rmds[rule_model]:
            copied_rmds[rule_model] = quantify_rmr(rmds.__getitem__(rule_model))

    # Evaluate the rules
    for rule in rules_list:
        print(f"Processing Rule {rule.id}")
        outcome = rule.evaluate(copied_rmds)
        outcomes.append(outcome)

    return {
        "invalid_rmrs": invalid_rmds,
        "outcomes": calcq_to_str(unit_system, outcomes),
    }
