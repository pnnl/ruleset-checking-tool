import rct229.rulesets as rulesets
from rct229.ruletest_engine.ruletest_jsons.scripts.excel_to_test_json_utilities import (
    generate_rule_test_dictionary,
)


def count_number_of_rules(ruleset_standard):
    """Returns the number of rules in a standard

     Parameters
     ----------
     ruleset_standard : str
         Name of the code standard you're interested in counting under the rct229/rulesets directory.
         Ex: 'ashrae9012019'

     Returns
    -------
    count_dict: dict
        Python dict with keys for each section in a given standard and their respective count.
        Also contains 'Total' as a key with the sum total rules

    """

    # Collect rule modules as a list of tuples
    available_rule_definitions = rulesets.__getrules__()

    # Dictionary with rule counts
    count_dict = {}

    for rule_definition_tuple in available_rule_definitions:

        # Parse section name from Section{N}Rule{N}, then add it to the dictionary count
        section_name = rule_definition_tuple[0].split("Rule")[0].lower()
        count_dict[section_name] = count_dict.get(section_name, 0) + 1

    # Get total number of rules
    count_dict["total"] = sum(count_dict.values())

    return count_dict


def count_number_of_ruletest_cases(ruleset_standard):
    """Returns the number of rule test cases in a standard

     Parameters
     ----------
     ruleset_standard : str
         Name of the code standard you're interested in counting under the rct229/rulesets directory.
         Ex: 'ashrae9012019'

     Returns
    -------
    count_dict: dict
        Python dict with keys for each section in a given standard and their respective count.
        Also contains 'Total' as a key with the sum total rule tests

    """

    # Aggregate rule test information into a dictionary
    master_ruletest_dict = generate_rule_test_dictionary(ruleset_standard)

    # Dictionary with ruletest counts
    count_dict = {}

    # Iterate through each section and get the number of rule unit tests
    for section_name, section_dict in master_ruletest_dict.items():
        count_dict[section_name] = len(section_dict["Rule_Unit_Test"])

    # Get total rule unit tests
    count_dict["total"] = sum(count_dict.values())

    return count_dict
