import subprocess
import ast
import astor
from pathlib import Path

import rct229.rulesets as rulesets
from rct229.schema.schema_enums import SchemaEnums
from rct229.schema.schema_store import SchemaStore
from rct229.ruletest_engine.ruletest_jsons.scripts.json_generation_utilities import (
    disaggregate_master_ruletest_json,
)


def renumber_rules(ruleset_doc):
    SchemaStore.set_ruleset(ruleset_doc)
    SchemaEnums.update_schema_enum()
    available_rule_definitions = rulesets.__getrules__()
    rule_map = rulesets.__getrulemap__()
    if not rule_map:
        raise ValueError(
            f"Rule map not found. Please define 'rules_dict' mapping in rulesets/{SchemaStore.SELECTED_RULESET}/__init__.py"
        )
    rulesets_path = Path(__file__).parent

    # Iterate through the available rules to determine whether the rule needs to be renumbered
    for rule in available_rule_definitions:
        rule_unique_id_string = str(rule[0]).lower()
        rule_name = rule_map.get(rule_unique_id_string)
        original_module_name = rule[1].__module__.split(".")[-1]

        if not rule_name:
            raise ValueError(f"Rule {rule_unique_id_string} not found in rule_map")

        # If the rule name does not match the module name, this indicates that the rule needs to be renumbered
        if original_module_name != rule_name:
            print(
                f"Rule {rule[1].__module__.split('.')[-1]} does not match rule name {rule_name}. Renumbering..."
            )

            path_relative_to_rulesets = Path(
                "\\".join(rule[1].__module__.split(".")[2:]) + ".py"
            )
            process_file(rulesets_path / path_relative_to_rulesets, rule_name)

    # Remove the -new suffix from the file names after processing is complete
    for file_path in rulesets_path.rglob("*"):
        if file_path.is_file() and file_path.stem.endswith("-new"):
            new_name = file_path.stem[:-4] + file_path.suffix
            new_path = file_path.with_name(new_name)
            try:
                file_path.rename(new_path)
            except FileExistsError:
                print(
                    f"Tried to remove the -new suffix but {new_path} already exists. You must resolve {file_path}."
                )

    # collect the files in the ruleset's ruletest_jsons directory that start with section and end with master.json
    ruletest_jsons_dir = (
        Path(__file__).parent.parent
        / "ruletest_engine"
        / "ruletest_jsons"
        / SchemaStore.SELECTED_RULESET
    )
    section_master_ruletest_files = list(ruletest_jsons_dir.glob("section*master.json"))

    # Disaggregate the master ruletest json files, effectively renumbering each of the individual ruletest json files
    for file in section_master_ruletest_files:
        disaggregate_master_ruletest_json(file.name, ruleset_doc)

    # Run black on the rulesets directory
    subprocess.run(["black", str(rulesets_path)], check=True)


def process_file(file_path, rule_name):
    rule_id = (
        rule_name.split("section")[1].split("rule")[0]
        + "-"
        + rule_name.split("rule")[1]
    )
    with file_path.open("r", encoding="utf-8") as file:
        tree = ast.parse(file.read(), filename=str(file_path))
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
        # Rename the file based on rule_name
        rule_section = rule_name.split("section")[1].split("rule")[0]
        current_section = file_path.parent.name

        if rule_section != current_section:
            correct_dir = file_path.parent.parent / f"section{rule_section}"
            correct_dir.mkdir(parents=True, exist_ok=True)
        else:
            correct_dir = file_path.parent

        new_file_path = correct_dir / f"{rule_name}-new.py"
        file_path.rename(new_file_path)

        with new_file_path.open("w", encoding="utf-8") as file:
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
    renumber_rules(rulesets.RuleSet.ASHRAE9012019_RULESET)
