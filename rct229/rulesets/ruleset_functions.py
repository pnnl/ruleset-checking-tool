import os
import ast
import astor
from pathlib import Path

import rct229.rulesets as rulesets
from rct229.schema.schema_enums import SchemaEnums
from rct229.schema.schema_store import SchemaStore


def renumber_rule_ids(ruleset_doc):
    SchemaStore.set_ruleset(ruleset_doc)
    SchemaEnums.update_schema_enum()
    available_rule_definitions = rulesets.__getrules__()
    rule_map = rulesets.__getrulemap__()
    for rule in available_rule_definitions:
        rulesets_path = Path(__file__).parent
        rule_unique_id_string = str(rule[0]).lower()
        rule_name = rule_map.get(rule_unique_id_string)
        if not rule_name:
            print(f"Rule {rule_unique_id_string} not found in rule_map")
            continue
        if rule[1].__module__.split(".")[-1] != rule_name:
            print(
                f"Rule {rule[1].__module__.split('.')[-1]} does not match rule name {rule_name}"
            )

            path_relative_to_rulesets = (
                "\\".join(rule[1].__module__.split(".")[2:]) + ".py"
            )
            process_file(
                str(rulesets_path / path_relative_to_rulesets),
                rule_name,
            )


def process_file(file_path, rule_name):
    rule_id = (
        rule_name.split("section")[1].split("rule")[0]
        + "-"
        + rule_name.split("rule")[1]
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

        # Rename the file based on rule_name
        directory, old_filename = os.path.split(file_path)
        new_filename = f"{rule_name}.py"
        new_file_path = os.path.join(directory, new_filename)
        os.rename(file_path, new_file_path)


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
    renumber_rule_ids(rulesets.RuleSet.ASHRAE9012019_RULESET)
