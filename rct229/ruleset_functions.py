import os
import ast
import astor

from rct229.rulesets.ashrae9012019 import rules_dict


def renumber_rule_ids():
    """Update the id attribute in the Root classes of each Rule Module to match the correct rule id."""
    for ruleset_section in os.listdir(
        os.path.join(os.path.dirname(__file__), "rulesets", "ashrae9012019")
    ):
        if ruleset_section.startswith("section"):
            section_mod_list = []
            ruleset_section_path = os.path.join(
                os.path.dirname(__file__), "rulesets", "ashrae9012019", ruleset_section
            )
            for rule_module in os.listdir(ruleset_section_path):
                if rule_module.startswith("prm") and rule_module.endswith(".py"):
                    process_file(os.path.join(ruleset_section_path, rule_module))


def process_file(file_path):
    rule_ref_id = file_path.split(os.sep)[-1].split(".")[0]
    section_rule = rules_dict.get(rule_ref_id)

    if not section_rule:
        print(f"Rule {rule_ref_id} not found in rules_dict")
        return

    rule_id = (
        section_rule.split("section")[1].split("rule")[0]
        + "-"
        + section_rule.split("rule")[1]
    )
    with open(file_path, "r", encoding="utf-8") as file:
        tree = ast.parse(file.read(), filename=file_path)
        modified = False

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                if any(
                    isinstance(base, ast.Name)
                    and (
                        "RuleDefinitionBase" in base.id
                        or "RuleDefinitionListBase" in base.id
                        or "RuleDefinitionListIndexedBase" in base.id
                        or "PartialRuleDefinition" in base.id
                    )
                    for base in node.bases
                ):
                    modified = update_class_id_attributes(node, rule_id) or modified

    if modified:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(astor.to_source(tree))
            print(f"Updated file: {file_path}")


def update_class_id_attributes(class_node, correct_id):
    modified = False
    for body_item in class_node.body:
        if isinstance(body_item, ast.FunctionDef) and body_item.name == "__init__":
            # Look for assignments within the __init__ method
            for stmt in ast.walk(body_item):
                if isinstance(stmt, ast.Call):
                    for keyword in stmt.keywords:
                        if keyword.arg == "id" and isinstance(keyword.value, ast.Str):
                            # Update the value only if it differs from the correct_id
                            if keyword.value.s != correct_id:
                                print(
                                    f"Updating id attribute in class {class_node.name} from {keyword.value.s} to {correct_id}"
                                )
                                keyword.value.s = correct_id
                                modified = True
    return modified


if __name__ == "__main__":
    renumber_rule_ids()
