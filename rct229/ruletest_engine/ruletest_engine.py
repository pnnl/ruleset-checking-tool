import glob
import json

# from jsonpointer import JsonPointer
import os
from copy import deepcopy
from typing import Optional

from pint import Quantity
from rct229.reports.ashrae9012019.ashrae901_2019_software_test_report import (
    ASHRAE9012019SoftwareTestReport,
)
from rct229.rule_engine.engine import evaluate_rule
from rct229.rule_engine.rct_outcome_label import RCTOutcomeLabel
from rct229.rule_engine.rulesets import RuleSet, RuleSetTest
from rct229.rulesets import rulesets
from rct229.rulesets.ashrae9012019 import rules_dict as rules_hash_dict
from rct229.rulesets.ashrae9012019 import section_dict
from rct229.ruletest_engine.ruletest_rmd_factory import get_ruletest_rmd_models
from rct229.schema.schema_enums import SchemaEnums
from rct229.schema.schema_store import SchemaStore
from rct229.schema.validate import validate_rpd


# Generates the RMD triplet dictionaries from a test_dictionary's "rmd_transformation" element.
# -test_dict = Dictionary with elements 'rmd_transformations' and 'rmd_transformations/user,baseline,proposed'
def generate_test_rmds(test_dict):
    """Generates the RMD triplet dictionaries from a test_dictionary's "rmd_transformation" element.

    Parameters
    ----------
    test_dict : dict
        A dictionary including an optional rmd_template field and a
        required rmd_transformations field.

        The rmd_transformations field has optional user, baseline,
        and proposed fields. If any of these fields is present, its
        corresponding RMD will be referenced. If the user, baseline,
        or proposed fields are missing, then its corresponding RMD is
        set to None.


    Returns
    -------
    tuple : a triplet containing:
        - user_rmd (dictionary): User RMD dictionary built from RMD Transformation definition
        - baseline_rmd (dictionary): Baseline RMD dictionary built from RMD Transformation definition
        - proposed_rmd (dictionary): Proposed RMD dictionary built from RMD Transformation definition
    """

    # Each of these will remain None unless it is specified in
    # rmd_transformations.
    user_rmd = None
    baseline_rmd = None
    proposed_rmd = None

    # Read in transformations dictionary. This will perturb a template or fully define an RMD (if no template defined)
    rmd_transformations_dict = test_dict["rmd_transformations"]

    # If user/baseline/proposed RMD transformations exist, either update their existing template or set them directly
    # from RMD transformations
    if "user" in rmd_transformations_dict:
        user_rmd = rmd_transformations_dict["user"]

    if "baseline" in rmd_transformations_dict:
        baseline_rmd = rmd_transformations_dict["baseline"]

    if "proposed" in rmd_transformations_dict:
        proposed_rmd = rmd_transformations_dict["proposed"]

    return user_rmd, baseline_rmd, proposed_rmd


def evaluate_outcome_enumeration_str(outcome_enumeration_str):
    """Evaluate the test outcome string. Translates Rule outcome string to a string matching ruletest JSON convention
        # (e.g., "PASSED" => "pass")

    Parameters
    ----------
    outcome_enumeration_str : str

        String equal to a set of predetermined enumerations for rule outcomes. These enumerations describe things such
        as whether a test passed, failed, undetermined, etc.

    Returns
    -------
    test_result : str

        Translated Rule outcome string to one matching ruletest JSON convention (e.g., 'pass')
    """

    # Check result of rule evaluation against known string constants
    if outcome_enumeration_str == RCTOutcomeLabel.PASS:
        test_result = "pass"
    elif outcome_enumeration_str == RCTOutcomeLabel.FAILED:
        test_result = "fail"
    elif (
        outcome_enumeration_str == RCTOutcomeLabel.UNDETERMINED
    ):  # previously used for manual_check
        test_result = "undetermined"
    elif outcome_enumeration_str == RCTOutcomeLabel.NOT_APPLICABLE:
        test_result = "not_applicable"
    else:
        raise ValueError(
            f"OUTCOME: The enumeration {outcome_enumeration_str} does not have a test result interpretation."
        )

    return test_result


def process_test_result(test_result, raised_message, test_dict, test_id):
    """Returns a string describing whether or not a test resulted in its expected outcome

    Parameters
    ----------
    test_result : str

        String describing rule outcome. OPTIONS: 'pass', 'fail', 'undetermined', 'not_applicable'

    raised_message : str

        String describing any outcome or exception message from running the rule.

    test_dict : dict

        Python dictionary containing the test's expected outcome and description

    test_id: str

        String describing the test's section, rule, and test case ID (e.g. rule-15-1a)

    Returns
    -------

    outcome_text: str

        String describing whether or not a test resulted in its expected outcome

    received_expected_outcome: bool

        Boolean describing if the ruletest resulted in the expected outcome (i.e., passed when expected to pass,
        failed when expected to fail)

    """

    # Get reporting parameters. Check if the test is expected to pass/fail and read in the description.
    # expected_outcome = test_dict["expected_rule_outcome"] == "pass"
    description = test_dict["test_description"]

    # Check if the test results agree with the expected outcome. Write an appropriate response based on their agreement
    received_expected_outcome = test_result == test_dict["expected_rule_outcome"]

    # TODO - ask about tests where a raised message exists but is not captured. Code written to catch those.

    # Check for any raised message in the rule test. If none exists, return empty string ""
    expected_raised_message = test_dict.get("expected_raised_message_includes", "")

    # Check if the raised message is a substring in the expected raised message (tests often don't have the full
    # message)
    messages_matched = expected_raised_message in str(raised_message)

    # Success and failure tied to
    overall_outcome = messages_matched and received_expected_outcome

    # Check if the test results agree with the expected outcome. Write an appropriate response based on their agreement
    if received_expected_outcome:
        if test_result == "pass":
            outcome_text = "PASS"
        elif test_result == "fail":
            outcome_text = "FAIL"
        elif test_result == "undetermined":
            outcome_text = "UNDETERMINED"
        elif test_result == "not_applicable":
            outcome_text = "NOT_APPLICABLE"

    else:

        expected_result = test_dict["expected_rule_outcome"]

        if test_result == "pass":
            outcome_text = f"FAILURE: Test {test_id} passed unexpectedly. Expected '{expected_result}'. The following condition was not identified: {description}"
        elif test_result == "fail":
            outcome_text = f"FAILURE: Test {test_id} failed unexpectedly. Expected '{expected_result}'. The following condition was not identified: {description}"
        elif test_result == "undetermined":
            outcome_text = f"FAILURE: Test {test_id} returned 'undetermined' unexpectedly. Expected '{expected_result}'."
        elif test_result == "not_applicable":
            outcome_text = f"FAILURE: Test {test_id} returned 'not_applicable' unexpectedly.  Expected '{expected_result}'."
        else:
            outcome_text = (
                f"FAILURE: Test {test_id} returned '{test_result}' unexpectedly"
            )

    # Check if exception messages matched. If not, append that to the outcome message.
    if not messages_matched:
        outcome_text += (
            f"\rMessages did not match. Expected outcome message was '{expected_raised_message}' and "
            f"instead received '{raised_message}'"
        )

    return outcome_text, overall_outcome


def run_section_tests(
    test_json_name: str, ruleset_doc: RuleSet, test_json_path: Optional[str] = None
):
    """Runs all tests found in a given test JSON and prints results to console. Returns true/false describing whether
    or not all tests in the JSON result in the expected outcome.

    Parameters
    ----------
    test_json_name : string

        Name of test JSON in 'test_json_path' directory. (e.g., transformer_tests.json)

    ruleset_doc: string

        Name of the ruleset

    test_json_path: str

        Path to test JSON's directory. This parameter is optional and will default to
        os.path.dirname(__file__)/ruletest_jsons if left undefined.

    Returns
    -------
    all_tests_successful : bool

        Boolean describing if all tests in the JSON result in the expected outcome.
    """

    # Create path to test JSON (e.g. 'transformer_tests.json')
    if test_json_path is None:
        test_json_path = os.path.join(
            os.path.dirname(__file__), "ruletest_jsons", test_json_name
        )
    else:
        test_json_path = os.path.join(test_json_path, test_json_name)

    # hash for capturing test results. Keys include: "results, log"
    test_result_dict = {}
    test_result_dict["results"] = []

    # Flag checking if all tests succeed. Ensures a message gets printed if so.
    all_tests_pass = True

    # Open
    with open(test_json_path) as f:
        test_list_dictionary = json.load(f)

    # get all rules in the ruleset.
    SchemaStore.set_ruleset(ruleset_doc)
    SchemaEnums.update_schema_enum()
    available_rule_definitions = rulesets.__getrules__()
    available_rule_definitions_dict = {
        rule_class[1].__module__.split(".")[-1]: rule_class[1]
        for rule_class in available_rule_definitions
    }

    # Cycle through tests in test JSON and run each individually
    for test_id in test_list_dictionary:
        print(f"Processing Test: {test_id}")
        # Load next test dictionary from test list
        test_dict = test_list_dictionary[test_id]

        # Generate RMD dictionaries for testing
        rmd_trio = get_ruletest_rmd_models(test_dict)

        # Identify Section and rule
        section = test_dict["Section"]
        rule = test_dict["Rule"]

        # Construction function name for Section and rule
        # section_name = f"section{section}rule{rule}"
        function_name = f"section{section}rule{rule}"

        test_result_dict["log"] = []  # Initialize log for this test result
        test_result_dict[
            f"{test_id}"
        ] = []  # Initialize log of this tests multiple results

        # Flag determining if an error was found when running this specific rule test
        test_error_found = False

        # Pull in rule, if written. If not found, fail the test and log which Section and Rule could not be found.
        try:
            rule = available_rule_definitions_dict[function_name]()
        except KeyError:
            # Print message communicating that a rule cannot be found
            print(f"RULE NOT FOUND: {function_name}. Cannot test {test_id}")

            # Append failed message to rule
            test_result_dict["results"].append(False)
            all_tests_pass = False
            continue

        # Evaluate rule and check for invalid RMDs
        evaluation_dict = evaluate_rule(rule, rmd_trio, True)
        # pprint.pprint(evaluation_dict)
        invalid_rmds_dict = evaluation_dict["invalid_rmds"]

        # If invalid RMDs exist, fail this rule and append failed message
        if len(invalid_rmds_dict) != 0:
            # Find which RMDs were invalid
            for invalid_rmd, invalid_rmd_message in invalid_rmds_dict.items():
                # Print message communicating that the schema is invalid
                print(
                    f"INVALID SCHEMA: Test {test_id}: {invalid_rmd} RMD: {invalid_rmd_message}"
                )

            # Append failed message to rule
            test_result_dict["results"].append(False)
            all_tests_pass = False

        # If RMDs are valid, check their outcomes
        else:
            # Check the evaluation dictionary "outcomes" element
            # NOTE: The outcome structure can either be a string for a single result or a list of dictionaries with
            # multiple results based on the Rule being tested.
            outcome_structure = evaluation_dict["outcomes"][0]

            # Update test_results_dict "log" and f"{test_id}" keys.
            # -The "log" element contains a list string describing errors, if any.
            # -The f"{test_id} element contains a list of booleans describing whether or not each testable element in
            #  outcome structure met the expected outcome for this test_id
            evaluate_outcome_object(
                outcome_structure, test_result_dict, test_dict, test_id
            )

            match test_dict["expected_rule_outcome"]:

                case "pass":
                    # For an expected pass, ALL tested elements in the RMR triplet must pass
                    if not all(test_result_dict[f"{test_id}"]):
                        test_error_found = True

                case "fail" | "undetermined" | "not_applicable":
                    # If all elements don't meet the expected outcome, flag this as an error
                    # (e.g., every test_result_dict element is false with 'fail' as the expected outcome. At least
                    #  one element must equal 'fail' for this to be a successful test)
                    if not any(test_result_dict[f"{test_id}"]):
                        test_error_found = True

                case _:
                    rule_outcome = test_dict["expected_rule_outcome"]
                    # Print message communicating that a rule cannot be found
                    print(
                        f"RULE OUTCOME NOT FOUND: {rule_outcome} is not a valid rule outcome. Expected 'pass', 'fail',"
                        f"'undetermined' or 'not_applicable'."
                    )
                    test_error_found = True

            # If errors were found, communicate the error logs
            if test_error_found:
                all_tests_pass = False

                if len(test_result_dict["log"]) == 0:
                    rule_outcome = test_dict["expected_rule_outcome"]
                    print(
                        f"FAILURE: {test_id} failed but produced no log errors. Expected '{rule_outcome}'."
                    )
                # Print log of all errors
                for test_result_string in test_result_dict["log"]:
                    print(test_result_string)

    # Print results to console
    if all_tests_pass:
        print("All tests passed!")

    print("")  # Buffer line

    return all_tests_pass


def generate_software_test_report(ruleset, section_list, output_json_path):
    """Runs list of rule test JSONs and aggregates them into a ashrae901_2019_detail_report

    Parameters
    ----------
    ruleset: string

        Name of the ruleset (e.g., 'ashrae9012019')

    section_list : list

        List of test JSON directorys in 'test_jsons/[MY_STANDARD]' directory. (e.g., ['section5', 'section6'])

    output_json_path: str

        output_dir: str - directory in which you want the ashrae901_2019_software_testing_report.json to appear


    """

    # Initialize report dictionary from which to continue testing. TODO- Future rulesets can be added here
    if ruleset == RuleSet.ASHRAE9012019_RULESET:
        SchemaStore.set_ruleset(RuleSet.ASHRAE9012019_RULESET)
        SchemaEnums.update_schema_enum()
        report_dict = ASHRAE9012019SoftwareTestReport()
        report_dict.initialize_ruleset_report()
    else:
        raise Exception(f"Ruleset '{ruleset}' has no default software test report.")

    if section_list is None:
        if ruleset == RuleSet.ASHRAE9012019_RULESET:
            section_list = RuleSetTest.ASHRAE9012019_TEST_LIST
        else:
            raise Exception(
                f"Ruleset '{ruleset}' has no default list of section tests."
            )

    # Master list of RCT engine outcomes, used to populate report.
    rct_outcomes = generate_rct_outcomes_list_from_section_list(section_list)

    # Generate
    report_dict.generate(rct_outcomes, output_json_path)
    return os.path.join(output_json_path, report_dict.ruleset_report_file)


def generate_rct_outcomes_list_from_section_list(section_list):
    """Runs all the ruletest JSONs for every section in section_list for a given ruleset. Returns the aggregated
    results as a dictionary that can be used in the generate function for ashrae901_2019_software_test_report

    Parameters
    ----------
    section_list : list

        List of test JSON directorys in 'test_jsons/[MY_STANDARD]' directory. (e.g., ['section5', 'section6'])

    Returns
    ----------
    rct_outcomes_dict: dict

        The dictionary with aggregated results to used in the generate function for the
        ashrae901_2019_software_test_report

    """

    # Master list of RCT engine outcomes and invalid RMD messages used to populate starting point for an RCTReport.
    # Initialize them here
    rct_outcomes_list = []
    invalid_rmd_messages = []

    # Maps excel enumerations for pass/fail etc. to RCTOutcomeLabel. Unfortunately there's a disconnect.
    ruletest_outcome_dict = {
        "pass": RCTOutcomeLabel.PASS,
        "fail": RCTOutcomeLabel.FAILED,
        "undetermined": RCTOutcomeLabel.UNDETERMINED,
        "not_applicable": RCTOutcomeLabel.NOT_APPLICABLE,
        "manual_check": RCTOutcomeLabel.NOT_APPLICABLE,
    }

    # get all rules in the ruleset.
    available_rule_definitions = rulesets.__getrules__()
    available_rule_definitions_dict = {
        rule_class[0]: rule_class[1] for rule_class in available_rule_definitions
    }

    # For every section in the section list, append outcomes to master rct_outcomes list. This list contains the
    # outcome for every rule in the section and the resulting lists of results for each of them. This list is what's
    # required by the ASHRAE9012019SoftwareTestReport's generate function as a starting point
    for section in section_list:
        # Get list of rule JSONs in section
        master_json_path = os.path.join(
            os.path.dirname(__file__),
            "ruletest_jsons",
            SchemaStore.SELECTED_RULESET,
            section,
            "rule*.json",
        )
        json_list = glob.glob(master_json_path)

        print(
            f"Running rule tests for {section.capitalize()}:{section_dict[section.replace('section','')]}..."
        )

        for rule_test_json_path in json_list:
            # Open the rule test JSON and perform rule evaluation for each test in JSON
            with open(rule_test_json_path) as f:
                test_list_dictionary = json.load(f)

                # Cycle through tests in test JSON and run each individually
                for test_id in test_list_dictionary:
                    rule_test_outcome_dict = dict()

                    # Load next test dictionary from test list
                    test_dict = test_list_dictionary[test_id]

                    rmd_trio = get_ruletest_rmd_models(test_dict)

                    # Identify Section and rule
                    section = test_dict["Section"]
                    rule = test_dict["Rule"]

                    # Construct look-up name for Section and Rule to map back to its corresponding python function
                    section_name = f"section{section}rule{rule}"

                    # Inverted dictionary: from 'sectionNruleN' -> 'prm9012019rule<hash>'
                    section_rule_to_rule_hash_dict = {
                        v: k for k, v in rules_hash_dict.items()
                    }
                    function_name = (
                        section_rule_to_rule_hash_dict[section_name]
                        .replace("prm", "PRM")
                        .replace("rule", "Rule")
                    )

                    # Pull in rule, if written. If not found, relay RULE_NOT_FOUND message to console and continue testing
                    try:
                        rule = available_rule_definitions_dict[function_name]()
                    except KeyError:
                        # Print message communicating that a rule cannot be found
                        print(f"RULE NOT FOUND: {function_name}. Cannot test {test_id}")
                        continue

                    # Evaluate rule and check for invalid RMDs
                    evaluation_dict = evaluate_rule(rule, rmd_trio, True)

                    invalid_rmds_dict = evaluation_dict["invalid_rmds"]

                    # If invalid RMDs exist, append failed message
                    if len(invalid_rmds_dict) != 0:
                        # Find which RMDs were invalid
                        for (
                            invalid_rmd,
                            invalid_rmd_message,
                        ) in invalid_rmds_dict.items():
                            # Record message communicating that the schema is invalid
                            invalid_rmd_messages.append(
                                f"INVALID SCHEMA: Test {test_id}: {invalid_rmd} RMD: {invalid_rmd_message}"
                            )

                    # If RMDs are valid, check their outcomes
                    else:
                        # Get standard information
                        standard_dict = test_dict["standard"]

                        rule_test_outcome_dict["rule_id"] = standard_dict["rule_id"]
                        rule_test_outcome_dict["test_id"] = test_dict["Test"]
                        rule_test_outcome_dict["test_description"] = test_dict[
                            "test_description"
                        ]
                        # Add ruleset reference, if it exists (not all rule tests have ruleset reference objects)
                        if (
                            "ruleset_reference" in standard_dict
                            and standard_dict["ruleset_reference"] != "0"
                        ):
                            rule_test_outcome_dict["ruleset_section"] = standard_dict[
                                "ruleset_reference"
                            ]
                        else:
                            rule_test_outcome_dict["ruleset_section"] = None

                        rule_test_outcome_dict["ruleset_section_title"] = section_dict[
                            str(test_dict["Section"])
                        ]
                        rule_test_outcome_dict["evaluation_type"] = (
                            "FULL" if rule.is_primary_rule else "APPLICABILITY"
                        )
                        rule_test_outcome_dict[
                            "expected_rule_unit_test_evaluation_outcome"
                        ] = ruletest_outcome_dict[test_dict["expected_rule_outcome"]]

                        # Outcomes come in nested dictionaries. Flatten these results and return them for this ruletest
                        rule_test_outcome_dict[
                            "rule_unit_test_evaluation"
                        ] = flatten_outcome_object(evaluation_dict["outcomes"], [])

                        # Append outcome from this test case to list of dictionaries
                        rct_outcomes_list.append(rule_test_outcome_dict)

    # Aggregate results from section tests for report
    rct_outcomes_dict = dict()
    rct_outcomes_dict["outcomes"] = rct_outcomes_list
    rct_outcomes_dict["invalid_rmds"] = invalid_rmd_messages

    return rct_outcomes_dict


def validate_test_json_schema(test_json_path):
    """Evaluates a test JSON against the JSON schema. Raises flags for any errors found in any rule tests. Results
    are printed to console

    Parameters
    ----------
    test_json_path : string

        Path to the test JSON in 'test_jsons' directory. (e.g., transformer_tests.json)

    """

    # List capturing messages describing failed RMD schemas
    failure_list = []

    # Open
    with open(test_json_path) as f:
        test_list_dictionary = json.load(f)

    # Cycle through tests in test JSON and run each individually
    for test_id in test_list_dictionary:
        # Load next test dictionary from test list
        test_dict = test_list_dictionary[test_id]

        # Generate RMD dictionaries for testing
        user_rmd, baseline_rmd, proposed_rmd = generate_test_rmds(test_dict)

        # Evaluate RMDs against the schema
        user_result = validate_rpd(user_rmd) if user_rmd != None else None
        baseline_result = validate_rpd(baseline_rmd) if baseline_rmd != None else None
        proposed_result = validate_rpd(proposed_rmd) if proposed_rmd != None else None

        results_list = [user_result, baseline_result, proposed_result]
        rmd_type_list = ["User", "Baseline", "Proposed"]

        for result, rmd_type in zip(results_list, rmd_type_list):
            # If result contains a dictionary with failure information, append failure to failure list
            if isinstance(result, dict):
                if result["passed"] is not True:
                    if "error" in result:
                        error_message = result["error"]
                    else:
                        error_message = result["errors"]

                    failure_message = f"Schema validation in {test_id} for the {rmd_type} RMD: {error_message}"
                    failure_list.append(failure_message)

    if len(failure_list) == 0:
        base_name = os.path.basename(test_json_path)
        print(f"No schema errors found in {base_name}")
        return True

    else:
        for failure in failure_list:
            print(failure)

        return False


def evaluate_outcome_object(outcome_dict, test_result_dict, test_dict, test_id):
    """Evaluates the outcome of an evaluate_rule function call (can be either a dictionary or a list), comparing it
    against the expected outcome for  given rule test. Results populate the "log" and "test_id" keys in the
    test_result_dict dictionary.

    Parameters
    ----------
    outcome_dict : list or dict

       The evaluate_rule function returns a dictionary with an "outcome" key. This is an instance of the object
       contained in that dictionary.

    test_result_dict: dict

        Dictionary used to log errors and aggregate the test results for a given outcome_dict. Updating this dictionary
        is the chief purpose of this function. Most notably the test_result_dict[f"{test_id}"] element is populated with
        a list of booleans describing whether or not the elements of the outcome_dict meet the expected outcome described
        in test_dict.

    test_dict: dict

       Dictionary containing the rule test RMD triplets, expected outcome, and description information for the ruletest
       being tested against

    test_id: str
       String describing the particular section, rule, and test case for a given rule test (e.g., rule-6-1-a)


    """

    # If the result key is a list of results (i.e. many elements get tested), keep drilling down until you get single
    # dictionary
    if isinstance(outcome_dict["result"], list):

        # If the outcome result is an empty list, flag this as a blanket error
        if len(outcome_dict["result"]) == 0:

            expected_outcome = test_dict["expected_rule_outcome"]
            outcome_test = f"FAILURE: Running test {test_id} returned an empty set of results without any reference to 'pass', 'fail', 'undetermined', or 'not_applicable'. Expected '{expected_outcome}'."
            test_result_dict["log"].append(outcome_test)

        else:
            # Iterate through each outcome in outcome results recursively until you get down to individual results
            for nested_outcome in outcome_dict["result"]:
                # Check outcome of each in list recursively until "result" key is not a list, but a dictionary
                evaluate_outcome_object(
                    nested_outcome, test_result_dict, test_dict, test_id
                )  # , outcome_result_list)

    else:
        # Process this tests results
        outcome_enumeration_str = outcome_dict[
            "result"
        ]  # enumeration for result (e.g., PASS, FAIL, CONTEXT_MISSING)

        # Evaluate the test outcome. Translates Rule outcome a string matching ruletest JSON convention
        # (e.g., "PASSED" => "pass")
        test_result = evaluate_outcome_enumeration_str(outcome_enumeration_str)

        # Check for any raised message in the outcome results. If none exists, return empty string ""
        raised_message = outcome_dict.get("message", "")

        # Write outcome text based and "receive_expected_outcome" boolean based on the test result
        outcome_text, received_expected_outcome = process_test_result(
            test_result, raised_message, test_dict, test_id
        )

        # Append results if expected outcome not received
        if not received_expected_outcome:
            # Describe failure if not yet included in log
            if outcome_text not in test_result_dict["log"]:
                test_result_dict["log"].append(outcome_text)

            # Context for the result (e.g., "Space 1"), if included
            outcome_result_context = (
                outcome_dict["name"] if "name" in outcome_dict else "Unknown context"
            )

            # Dictionary of calculated values converted to string
            outcome_calc_vals_string = (
                str(outcome_dict["calc_vals"]) if "calc_vals" in outcome_dict else "N/A"
            )

            test_result_dict["log"].append(
                # Append calculations but cap length of string to avoid printing long arrays
                f"{outcome_result_context}: Calculated values - {outcome_calc_vals_string[:300]}"
            )

        test_result_dict[f"{test_id}"].append(received_expected_outcome)


def flatten_outcome_object(outcome_object, flattened_outcome_list=[]):
    """Checks every element in an RCT outcome dictionary and unravels the nested structure to produce a list of outcome
    results to be read in by rule_unit_test_evaluation as part of the software testing report

    Parameters
    ----------
    outcome_object : list or dict

       The evaluate_rule function returns a dictionary with an "outcome" key. This is an instance of the object
       contained in that dictionary.

    Returns:
    --------
    flattened_outcome_list: list

        The flattened list of ruletest evaluations

    """

    # Recursively looks in calculated values for any Quantity types and rewriting them as str
    def correct_types_in_calculated_vals(calc_value_item):
        # Skip if any dictionary comes up as None
        if calc_value_item is None:
            return

        # If list, recursively check each element and correct when appropriate
        if isinstance(calc_value_item, list):
            for i in range(len(calc_value_item)):
                item = calc_value_item[i]
                if isinstance(item, Quantity):
                    calc_value_item[i] = str(item)
                elif isinstance(item, list):
                    correct_types_in_calculated_vals(item)
                elif isinstance(item, dict):
                    correct_types_in_calculated_vals(item)

        # If dictionary, recursively check each element and correct when appropriate
        elif isinstance(calc_value_item, dict):
            for key, value in calc_value_item.items():
                if isinstance(value, list):
                    correct_types_in_calculated_vals(value)

                # Rewrite Quantity values as strings
                elif isinstance(value, Quantity):
                    calc_value_item[key] = str(value)

                elif isinstance(value, dict):
                    correct_types_in_calculated_vals(
                        value
                    )  # Recursively check nested dictionary

    # If the result key is a list of results (i.e. many elements get tested), keep drilling down until you get single
    # dictionary
    if isinstance(outcome_object, list):
        # Iterate through each outcome in outcome results recursively until you get down to individual results
        for nested_outcome in outcome_object:
            # Check outcome of each in list recursively until "result" key is not a list, but a dictionary
            flatten_outcome_object(nested_outcome, flattened_outcome_list)

    # If not a list, assumed to be a dictionary with key "result". Check if the value for "key" is a list.
    elif isinstance(outcome_object["result"], list):
        # Iterate through each outcome in outcome results recursively until you get down to individual results
        for nested_outcome in outcome_object["result"]:
            # Check outcome of each in list recursively until "result" key is not a list, but a dictionary
            flatten_outcome_object(nested_outcome, flattened_outcome_list)

    # Else, process result as you've dug down to final dictionary
    else:
        # Extract relevant data and append it to unraveled_outcome_list
        rule_unit_test_evaluation_dict = dict()

        # Extract relevant information
        rule_unit_test_evaluation_dict["id"] = outcome_object["id"]
        rule_unit_test_evaluation_dict["result"] = outcome_object["result"]
        rule_unit_test_evaluation_dict["message"] = (
            outcome_object["message"] if "message" in outcome_object else None
        )
        rule_unit_test_evaluation_dict["calculated_values"] = (
            deepcopy(outcome_object["calc_vals"])
            if "calc_vals" in outcome_object
            else None
        )

        # Convert any Quantity in calculated values to a str. This allows them to be serializable for a JSON
        correct_types_in_calculated_vals(
            rule_unit_test_evaluation_dict["calculated_values"]
        )

        # Append rule unit test evaluation to outcome list
        flattened_outcome_list.append(rule_unit_test_evaluation_dict)

    return deepcopy(flattened_outcome_list)


def validate_229_rmd(rmd_name, rmd_path):
    # Open
    with open(rmd_path) as f:
        rmd = json.load(f)

    result = validate_rpd(rmd)

    # If result contains a dictionary with failure information, append failure to failure list
    if isinstance(result, dict):
        if result["passed"] is not True:
            error_message = result["error"]
            print(f"Schema validation failed for {rmd_name} - {error_message}")

        else:
            print(f"{rmd_name} is valid ASHRAE 229 schema")

    else:
        print(f"Error validating RMD: {rmd_name}")
