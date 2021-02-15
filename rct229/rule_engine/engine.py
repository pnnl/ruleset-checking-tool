import inspect
import rct229.rule_engine.rule_base as base_classes
import rct229.rules as rules
from rct229.schema.validate import validate_rmr
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals

def get_available_rules():
    modules = [f for f in inspect.getmembers(rules, inspect.ismodule) if f in rules.__all__]

    available_rules = []
    for module in modules:
        available_rules += [f for f in inspect.getmembers(module[1], inspect.isfunction)]

    return available_rules

# def get_base_class(rule_def_class):
#     rule_def_base = rule_def_class.__bases__[0]
#     base_class_name = [f[0] for f in inspect.getmembers(base_classes, inspect.isclass) if f[1] == rule_def_base][0]
#
#     return base_class_name
#
# def check_rule_definition_format():
#     pass

# Functions for evaluating rules
def evaluate_all_rules(user_rmr, baseline_rmr, proposed_rmr):

    # Get reference to rule functions in rules model
    AvailableRuleDefinitions = rules.__getrules__()

    rules_list = [RuleDef[1]() for RuleDef in AvailableRuleDefinitions]
    rmrs = UserBaselineProposedVals(user_rmr, baseline_rmr, proposed_rmr)
    report = evaluate_rules(rules_list, rmrs)

    return report

def evaluate_rule(rule, rmrs):
    """ Evaluates a single rule against an RMR trio

    Parameters
    ----------
    rmrs : UserBaselineProposedVals
        Object containing the user, baseline, and proposed RMRs

    Returns
    -------
    dict
        A dictionary of the form:
        {
            invalid_rmrs: [string] - The names of the RMRs that are invalid
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

    return evalute_rules([rule], rmrs)

def evaluate_rules(rules_list, rmrs):
    """ Evaluates a list of rules against an RMR trio

    Parameters
    ----------
    rmrs : UserBaselineProposedVals
        Object containing the user, baseline, and proposed RMRs

    Returns
    -------
    dict
        A dictionary of the form:
        {
            invalid_rmrs: [string] - The names of the RMRs that are invalid
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
    invalid_rmrs = []
    user_validation = validate_rmr(rmrs.user)
    if user_validation["passed"] is not True:
        invalid_rmrs.append('User')

    baseline_validation = validate_rmr(rmrs.baseline)
    if baseline_validation["passed"] is not True:
        invalid_rmrs.append('Baseline')

    proposed_validation = validate_rmr(rmrs.proposed)
    if proposed_validation["passed"] is not True:
        invalid_rmrs.append('Proposed')

    if len(invalid_rmrs) == 0:
        # The RMRs are valid
        for rule in rules_list:
            outcome = rule.evaluate(rmrs)
            outcomes.append(outcome)

    return { 'invalid_rmrs': invalid_rmrs, 'outcomes': outcomes }
