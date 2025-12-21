import subprocess
import ast
import astor
import re
import csv
import importlib
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


def _module_has_non_primary_rule(module_name: str) -> bool:
    """
    Parse the module's AST and return True if any rule-class __init__ calls
    super().__init__(..., is_primary_rule=False).
    """
    try:
        module = importlib.import_module(module_name)
    except Exception:
        return False

    module_file = getattr(module, "__file__", None)
    # Only parse source files
    if not module_file or not module_file.endswith(".py"):
        return False

    try:
        with open(module_file, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=module_file)
    except Exception:
        return False

    # Names that identify rule base classes by simple name
    RULE_BASE_NAMES = {
        "RuleDefinitionBase",
        "RuleDefinitionListBase",
        "RuleDefinitionListIndexedBase",
        "PartialRuleDefinition",
    }

    def _is_rule_class(class_node: ast.ClassDef) -> bool:
        for base in class_node.bases:
            # Handles simple "BaseName" and qualified "pkg.BaseName"
            if isinstance(base, ast.Name) and base.id in RULE_BASE_NAMES:
                return True
            if (
                isinstance(base, ast.Attribute)
                and isinstance(base.attr, str)
                and base.attr in RULE_BASE_NAMES
            ):
                return True
        return False

    def _const_bool(node) -> object:
        # py3.8+: ast.Constant; older: ast.NameConstant
        if isinstance(node, ast.Constant):
            return node.value if isinstance(node.value, bool) else None
        if hasattr(ast, "NameConstant") and isinstance(node, ast.NameConstant):
            return node.value if isinstance(node.value, bool) else None
        return None

    # Look through rule classes and their __init__ bodies for super().__init__(..., is_primary_rule=...)
    for class_node in (
        n for n in ast.walk(tree) if isinstance(n, ast.ClassDef) and _is_rule_class(n)
    ):
        # find __init__
        init_funcs = [
            b
            for b in class_node.body
            if isinstance(b, ast.FunctionDef) and b.name == "__init__"
        ]
        for init in init_funcs:
            for call in ast.walk(init):
                if isinstance(call, ast.Call):
                    for kw in call.keywords:
                        if kw.arg == "is_primary_rule":
                            val = _const_bool(kw.value)
                            if not val:
                                return True  # found a non-primary rule
    return False


def write_rule_info_to_file(ruleset_doc):
    """
    Writes a CSV file with the rule evaluation types for each rule in the specified ruleset,
    using the 'is_primary_rule' keyword passed to super().__init__(...) in the rule class __init__.
      - is_primary_rule=True or omitted  => "Full"
      - is_primary_rule=False            => "Applicability"
    """
    SchemaStore.set_ruleset(ruleset_doc)
    SchemaEnums.update_schema_enum()
    available_rule_definitions = rulesets.__getrules__()
    rule_map = rulesets.__getrulemap__()

    if not rule_map:
        raise ValueError(
            f"Rule map not found. Please define 'rules_dict' mapping in rulesets/{SchemaStore.SELECTED_RULESET}/__init__.py"
        )

    output_file = Path(__file__).parent / f"{ruleset_doc}_rule_evaluation_types.csv"

    with output_file.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Section", "Rule #", "Rule Name", "Evaluation Type"])

        for rule_id, rule_class in available_rule_definitions:
            rule_unique_id_string = str(rule_id)
            rule_name = rule_map.get(rule_unique_id_string)

            # fallback for case mismatch
            if not rule_name:
                for k, v in rule_map.items():
                    if k.lower() == rule_unique_id_string.lower():
                        rule_name = v
                        break

            if not rule_name:
                print(f"Skipping unknown rule ID: {rule_unique_id_string}")
                continue

            # Parse section and rule number from rule_name
            match = re.match(r"section(\d+)rule(\d+)", rule_name, re.IGNORECASE)
            if not match:
                print(
                    f"Could not parse section/rule number from rule name: {rule_name}"
                )
                section = rule_number = ""
            else:
                section, rule_number = match.groups()

            module_name = rule_class.__module__

            # AST-inspect the module for is_primary_rule=False in any rule class
            has_non_primary = _module_has_non_primary_rule(module_name)

            evaluation_type = "Applicability" if has_non_primary else "Full"
            writer.writerow([section, rule_number, rule_name, evaluation_type])

    print(f"Rule evaluation types written to {output_file}")


if __name__ == "__main__":
    # write_rule_info_to_file(rulesets.RuleSet.ASHRAE9012019_RULESET)
    # renumber_rules(rulesets.RuleSet.ASHRAE9012019_RULESET)
    pass
