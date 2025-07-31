import copy

from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rule_engine.rulesets import RuleSet
from rct229.rulesets.ashrae9012019 import (
    BASELINE_0,
    BASELINE_90,
    BASELINE_180,
    BASELINE_270,
)
from rct229.schema.schema_store import SchemaStore
from rct229.utils.assertions import getattr_


def get_ruletest_rmd_models(test_dict: dict):
    rmd = None
    if SchemaStore.SELECTED_RULESET == RuleSet.ASHRAE9012019_RULESET:
        rmd = get_9012019_rmd_models(test_dict)

    return rmd


def get_9012019_rmd_models(test_dict: dict):
    # Each of these will remain None unless it is specified in
    # rmd_transformations.
    user_rmd = None
    baseline_0_rmd = None
    baseline_90_rmd = None
    baseline_180_rmd = None
    baseline_270_rmd = None
    proposed_rmd = None

    # Read in transformations dictionary. This will perturb a template or fully define an RMD (if no template defined)
    rmd_transformations_dict = test_dict["rmd_transformations"]

    # If user/baseline/proposed RMD transformations exist, either update their existing template or set them directly
    # from RMD transformations
    if "user" in rmd_transformations_dict:
        user_rmd = rmd_transformations_dict["user"]

    if "baseline" in rmd_transformations_dict:
        baseline_rmd = rmd_transformations_dict["baseline"]

        for rmd_b in baseline_rmd["ruleset_model_descriptions"]:
            type_b = getattr_(rmd_b, "RMD", "type")
            if type_b == BASELINE_0:
                baseline_0_rmd = copy.deepcopy(baseline_rmd)
                baseline_0_rmd["ruleset_model_descriptions"] = []
                baseline_0_rmd["ruleset_model_descriptions"].append(
                    copy.deepcopy(rmd_b)
                )

            elif type_b == BASELINE_90:
                baseline_90_rmd = copy.deepcopy(baseline_rmd)
                baseline_90_rmd["ruleset_model_descriptions"] = []
                baseline_90_rmd["ruleset_model_descriptions"].append(
                    copy.deepcopy(rmd_b)
                )

            elif type_b == BASELINE_180:
                baseline_180_rmd = copy.deepcopy(baseline_rmd)
                baseline_180_rmd["ruleset_model_descriptions"] = []
                baseline_180_rmd["ruleset_model_descriptions"].append(
                    copy.deepcopy(rmd_b)
                )

            elif type_b == BASELINE_270:
                baseline_270_rmd = copy.deepcopy(baseline_rmd)
                baseline_270_rmd["ruleset_model_descriptions"] = []
                baseline_270_rmd["ruleset_model_descriptions"].append(
                    copy.deepcopy(rmd_b)
                )

    if "proposed" in rmd_transformations_dict:
        proposed_rmd = rmd_transformations_dict["proposed"]

    return produce_ruleset_model_description(
        USER=user_rmd,
        BASELINE_0=baseline_0_rmd,
        BASELINE_90=baseline_90_rmd,
        BASELINE_180=baseline_180_rmd,
        BASELINE_270=baseline_270_rmd,
        PROPOSED=proposed_rmd,
    )
