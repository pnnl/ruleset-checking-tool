import importlib


def get_ruleset_test_sections(ruleset_name: str):
    """
    Dynamically load the test directory list for a given ruleset.
    """
    module_path = f"rct229.ruletest_engine.ruletest_jsons.{ruleset_name}"
    try:
        module = importlib.import_module(module_path)

        if getattr(module, "RULETEST_SECTION_LIST") is None:
            print(f"Warning: No RULETEST_SECTION_LIST found in module '{module_path}'")

        return getattr(module, "RULETEST_SECTION_LIST", [])

    except ModuleNotFoundError:
        print(f"Warning: No ruletest module found for ruleset '{ruleset_name}'")

        return []
