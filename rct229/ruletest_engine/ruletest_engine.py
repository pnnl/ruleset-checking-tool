import json
import os
from rct229.rules.section15 import *
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.rule_engine.engine import evaluate_rule


# Generates the RMR triplet dictionaries from a test_dictionary's "rmr_transformation" element.
# -test_dict = Dictionary with elements 'rmr_transformations' and 'rmr_transformations/user,baseline,proposed'
def generate_test_rmrs(test_dict):
    """Generates the RMR triplet dictionaries from a test_dictionary's "rmr_transformation" element.

    Parameters
    ----------
    test_dict : dict

        Dictionary containing both the required RMR template and RMR transformation elements used to create the
        RMR dictionary triplets. Includes elements 'rmr_transformations' and
        'rmr_transformations/user,baseline,proposed'

    Returns
    -------
    tuple : a tuple containing:
        - user_rmr (dictionary): User RMR dictionary built from RMR Transformation definition
        - baseline_rmr (dictionary): Baseline RMR dictionary built from RMR Transformation definition
        - proposed_rmr (dictionary): Proposed RMR dictionary built from RMR Transformation definition

        Returns the three RMR triplets. Order is user, baseline, proposed
    """

    # Read in transformations dictionary. This dictates how RMRs are built.
    rmr_transformations_dict = test_dict['rmr_transformations']

    # If RMRs are based on a template
    if 'rmr_template' in test_dict:

        template = test_dict['rmr_template']

        # TODO figure out how to handle templates, none needed yet
        return None, None, None

    else:

        # If RMR template does not exist, then simply use the transformations to populate RMRs
        user_rmr = rmr_transformations_dict['user'] if 'user' in rmr_transformations_dict else None
        baseline_rmr = rmr_transformations_dict['baseline'] if 'baseline' in rmr_transformations_dict else None
        proposed_rmr = rmr_transformations_dict['proposed'] if 'proposed' in rmr_transformations_dict else None

        return user_rmr, baseline_rmr, proposed_rmr


def evaluate_outcome(outcome):
    """Returns a boolean for whether a rule passed/failed based on the outcome string enumeration

        Parameters
        ----------
        outcome : str

            String equal to a set of predetermined enumerations for rule outcomes. These enumerations describe things such
            as whether a test passed, failed, required manual check, etc.

        Returns
        -------
        test_result : bool

            Boolean describing whether the rule should be treated as passing or failing. Pass = True, Fail = False
    """

    # Check result of rule evaluation against known string constants (TODO: write out these constants to new file)
    if outcome == 'PASSED':
        test_result = True
    elif outcome == 'FAILED':
        test_result = False
    elif outcome == 'MANUAL_CHECK_REQUIRED':
        test_result = False
    elif outcome == 'MISSING_CONTEXT':
        test_result = False
    elif outcome == 'NA':
        test_result = False
    else:
        test_result = 'TODO: Raise error'

    return test_result


def process_test_result(test_result, test_dict, test_id):
    """Returns a string describing whether or not a test resulted in its expected outcome

        Parameters
        ----------
        test_result : bool

            Boolean for whether or not a test passed. Passed = True, Failed = False

        test_dict : dict

            Python dictionary containing the a test's expected outcome and description

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
    expected_outcome = (test_dict['expected_rule_outcome'] == 'pass')
    description = test_dict['description']

    # Check if the test results agree with the expected outcome. Write an appropriate response based on their agreement
    received_expected_outcome = (test_result == expected_outcome)

    # Check if the test results agree with the expected outcome. Write an appropriate response based on their agreement
    if received_expected_outcome:

        if test_result:
            outcome_text = f'SUCCESS: Test {test_id} passed as expected. The following condition was identified: {description}'
        else:
            outcome_text = f'SUCCESS: Test {test_id} failed as expected. The following condition was identified: {description}'

    else:

        if test_result:
            outcome_text = f'FAILURE: Test {test_id} passed unexpectedly. The following condition was not identified: {description}'
        else:
            outcome_text = f'FAILURE: Test {test_id} failed unexpectedly. The following condition was not identified: {description}'

    return outcome_text, received_expected_outcome

def run_section_tests(test_json_name):
    """Runs all tests found in a given test JSON and prints results to console. Returns true/false describing whether
    or not all tests in the JSON result in the expected outcome.

    Parameters
    ----------
    test_json_name : string

        Name of test JSON in 'test_jsons' directory. (e.g., transformer_tests.json)

    Returns
    -------
    all_tests_successful : bool

        Boolean describing if all tests in the JSON result in the expected outcome.
    """

    # Create path to test JSON (e.g. 'transformer_tests.json')
    test_json_path = os.path.join('ruletest_jsons', test_json_name)

    title_text = f'TESTS RESULTS FOR: {test_json_name}'.center(50)
    test_result_strings = ['-----------------------------------------------------------------------------------------',
                           f'--------------------{title_text}-------------------',
                           '-----------------------------------------------------------------------------------------',
                           '']

    # List capturing all outcomes of the test_json being passed in
    test_results = []

    # Open
    with open(test_json_path) as f:
        test_list_dictionary = json.load(f)

    # Cycle through tests in test JSON and run each individually
    for test_id in test_list_dictionary:

        # Load next test dictionary from test list
        test_dict = test_list_dictionary[test_id]

        # Generate RMR dictionaries for testing
        user_rmr, baseline_rmr, proposed_rmr = generate_test_rmrs(test_dict)
        rmr_trio = UserBaselineProposedVals(user_rmr, baseline_rmr, proposed_rmr)

        # Identify Section and rule
        section = test_dict['Section']
        rule = test_dict['Rule']

        # Construction function name for Section and rule
        function_name = f'Section{section}Rule{rule}'

        # Pull in rule
        rule = globals()[function_name]()

        # Evaluate rule and check for invalid RMRs
        evaluation_dict = evaluate_rule(rule, rmr_trio)
        invalid_rmrs_dict = evaluation_dict['invalid_rmrs']

        # If invalid RMRs exist, fail this rule and append failed message
        if len(invalid_rmrs_dict)!= 0:

            # Find which RMRs were invalid and add them to test_result_strings
            for invalid_rmr, invalid_rmr_message in invalid_rmrs_dict.items():

                outcome_text = f'INVALID SCHEMA: Test {test_id}: {invalid_rmr} RMR: {invalid_rmr_message}'
                test_result_strings.append(outcome_text)

            # Append failed message to rule
            test_results.append(False)

        # If RMRs are valid, check their outcomes
        else:

            outcome_result = evaluation_dict['outcomes'][0]['result']

            # If outcome result is a list of results (i.e. many elements get tested), check each against expected result
            if isinstance(outcome_result, list):

                # Create list for collecting results of every test in list
                test_results = []

                # Iterate through each outcome in outcome results
                for outcome in outcome_result:
                    # Append test result for this outcome
                    test_results.append(evaluate_outcome(outcome['result']))

                # Checks that ALL tests pass in test_results. If any fail, the test fails
                test_result = all(result for result in test_results)

                # Write outcome text based on overall pass/fail string based on set of test and determine if the ruletest
                # behaved as expected
                outcome_text, received_expected_outcome = process_test_result(test_result, test_dict, test_id)

                # Append results
                test_result_strings.append(outcome_text)
                test_results.append(received_expected_outcome)

            # If a single result, check the result
            else:

                test_result = evaluate_outcome(outcome_result)
                outcome_text, received_expected_outcome = process_test_result(test_result, test_dict, test_id)
                test_result_strings.append(outcome_text)
                test_results.append(received_expected_outcome)


    # Print results to console
    for test_result in test_result_strings:

        print(test_result)

    # Return whether or not all tests received their expected outcome as a boolean
    all_tests_successful = all(test_results)

    return all_tests_successful

def run_transformer_tests():
    """Runs all tests found in the transformer tests JSON.

    Returns
    -------
    None

    Results of transformer test are spit out to console
    """

    transformer_rule_json = 'transformer_tests.json'

    return run_section_tests(transformer_rule_json)

