import inspect

import rct229.rule_engine.rule_base as base_classes
import rct229.rulesets as rulesets
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.schema.schema_utils import quantify_rmr
from rct229.schema.validate import validate_rmr
from rct229.utils.pint_utils import UNIT_SYSTEM, calcq_to_str


def get_available_rules(ruleset_doc):
    modules = [
        f for f in inspect.getmembers(rulesets, inspect.ismodule) if f in rules.__all__
    ]

    available_rules = []
    for module in modules:
        available_rules += [
            f for f in inspect.getmembers(module[1], inspect.isfunction)
        ]

    return available_rules


# Functions for evaluating rules
def evaluate_all_rules(user_rmr, baseline_rmr, proposed_rmr, ruleset_doc):
    # Get reference to rule functions in rules model
    AvailableRuleDefinitions = rulesets.__getrules__(ruleset_doc)

    rules_list = [RuleDef[1]() for RuleDef in AvailableRuleDefinitions]
    rmrs = UserBaselineProposedVals(user_rmr, baseline_rmr, proposed_rmr)
    report = evaluate_rules(rules_list, rmrs)

    return report


def evaluate_rule(rule, rmrs):
    """Evaluates a single rule against an RMR trio

    Parameters
    ----------
    rmrs : UserBaselineProposedVals
        Object containing the user, baseline, and proposed RMRs

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


def evaluate_rules(rules_list, rmrs, unit_system=UNIT_SYSTEM.IP):
    """Evaluates a list of rules against an RMR trio

    Parameters
    ----------
    rules_list : list
        list of rule definitions
    rmrs : UserBaselineProposedVals
        Object containing the user, baseline, and proposed RMRs

    Returns
    -------
    dict
        A dictionary of the form:
        {
            invalid_rmrs: dict - The keys are the names of the invalid RMRs.
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

    # Determine which rmrs are used by the rule definitions
    rmrs_used = UserBaselineProposedVals(user=False, baseline=False, proposed=False)
    for rule in rules_list:
        if rule.rmrs_used.user:
            rmrs_used.user = True
        if rule.rmrs_used.baseline:
            rmrs_used.baseline = True
        if rule.rmrs_used.proposed:
            rmrs_used.proposed = True

    # Validate the rmrs against the schema and other high-level checks
    outcomes = []
    invalid_rmrs = {}

    if rmrs_used.user:
        user_validation = validate_rmr(rmrs.user)
        if user_validation["passed"] is not True:
            invalid_rmrs["User"] = user_validation["error"]

    if rmrs_used.baseline:
        baseline_validation = validate_rmr(rmrs.baseline)
        if baseline_validation["passed"] is not True:
            invalid_rmrs["Baseline"] = baseline_validation["error"]

    if rmrs_used.proposed:
        proposed_validation = validate_rmr(rmrs.proposed)
        if proposed_validation["passed"] is not True:
            invalid_rmrs["Proposed"] = proposed_validation["error"]

    # Evaluate the rules if all the used rmrs are valid
    if len(invalid_rmrs) == 0:
        # Replace the numbers that have schema units in the RMRs with the
        # appropriate pint quantities
        # TODO: quantitization should happen right after schema validation and
        # before other validations
        rmrs = UserBaselineProposedVals(
            user=quantify_rmr(rmrs.user),
            baseline=quantify_rmr(rmrs.baseline),
            proposed=quantify_rmr(rmrs.proposed),
        )

        # Evaluate the rules
        for rule in rules_list:
            print(f"Processing Rule {rule.id}")
            outcome = rule.evaluate(rmrs)
            outcomes.append(outcome)

    return {
        "invalid_rmrs": invalid_rmrs,
        "outcomes": calcq_to_str(unit_system, outcomes),
    }
