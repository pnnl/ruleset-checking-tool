import json
import os
from rct229.rules.section15 import *

# TODO: Temporarily used to randomize pass/fail.
import random


# Generates the RMR triplet dictionaries from a test_dictionary's "rmr_transformation" element.
# -test_dict = Dictionary with elements 'rmr_transformations' and 'rmr_transformations/user,baseline,proposed'
def generate_test_rmrs(test_dict):
    """Generates the RMR triplet dictionaries from a test_dictionary's "rmr_transformation" element.

    Parameters
    ----------
    test_dict : dictionary

    Dictionary containing both the required RMR template and RMR transformation elements used to create the
    RMR dictionary triplets. Includes elements 'rmr_transformations' and 'rmr_transformations/user,baseline,proposed'

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


def run_section_tests(test_json_name):
    """Runs all tests found in a given test JSON and prints results to console.

    Parameters
    ----------
    test_json_name : string

        Name of test JSON in 'test_jsons' directory. (e.g., transformer_tests.json)

    Returns
    -------
    None
    """

    # Create path to test JSON (e.g. 'transformer_tests.json')
    test_json_path = os.path.join('test_jsons', test_json_name)

    title_text = f'TESTS RESULTS FOR: {test_json_name}'.center(50)
    test_result_strings = ['-----------------------------------------------------------------------------------------',
                           f'--------------------{title_text}-------------------',
                           '-----------------------------------------------------------------------------------------',
                           '']

    # Open
    with open(test_json_path) as f:
        test_list_dictionary = json.load(f)

    # Cycle through tests in test JSON and run each individually
    for test_id in test_list_dictionary:

        # Load next test dictionary from test list
        test_dict = test_list_dictionary[test_id]

        # Generate RMR dictionaries for testing
        user_rmr, baseline_rmr, proposed_rmr = generate_test_rmrs(test_dict)

        # Identify Section and rule
        section = test_dict['Section']
        rule = test_dict['Rule']

        # Construction function name
        function_name = f'Section{section}Rule{rule}'

        rule = globals()[function_name]()

        # TODO: Temporarily using random pass/fail for testing purposes.
        test_result = random.choice(['pass', 'fail'])

        # Get reporting paramaters
        expected_outcome = test_dict['expected_rule_outcome']
        description = test_dict['description']

        if test_result == expected_outcome:

            if expected_outcome == 'pass':
                outcome_text = f' SUCCESS: Test {test_id} passed as expected. The following condition was identified: {description}'
            else:
                outcome_text = f' SUCCESS: Test {test_id} failed as expected. The following condition was identified: {description}'

        else:

            if expected_outcome == 'pass':
                outcome_text = f' FAILURE: Test {test_id} passed unexpectedly. The following condition was not identified: {description}'
            else:
                outcome_text = f' FAILURE: Test {test_id} failed unexpectedly. The following condition was not identified: {description}'

        test_result_strings.append(outcome_text)

    for test_result in test_result_strings:

        print(test_result)


def run_transformer_tests():
    """Runs all tests found in the transformer tests JSON.

    Returns
    -------
    None

    Results of transformer test are spit out to console
    """


    transformer_rule_json = 'transformer_tests.json'

    run_section_tests(transformer_rule_json)


run_transformer_tests()
