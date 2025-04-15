import random
import string

import rct229.rulesets as rulesets


rule_map = rulesets.__getrulemap__()


def generate_unique_rule_id():
    """
    Generate a unique rule ID for a rule. The rule ID is generated in the format of:
    prm9012019rule + 2 digits + 1 lowercase letter + 2 digits
    """
    random_numbers12 = "".join([str(random.randint(0, 9)) for _ in range(2)])
    random_letter3 = random.choice(string.ascii_lowercase)
    random_numbers45 = "".join([str(random.randint(0, 9)) for _ in range(2)])
    unique_rule_id = f"{random_numbers12}{random_letter3}{random_numbers45}"

    # Check if the generated rule ID already exists
    while unique_rule_id in rule_map:
        random_numbers12 = "".join([str(random.randint(0, 9)) for _ in range(2)])
        random_letter3 = random.choice(string.ascii_lowercase)
        random_numbers45 = "".join([str(random.randint(0, 9)) for _ in range(2)])
        unique_rule_id = f"{random_numbers12}{random_letter3}{random_numbers45}"

    return f"prm9012019rule{unique_rule_id}"


if __name__ == "__main__":
    print(generate_unique_rule_id())
