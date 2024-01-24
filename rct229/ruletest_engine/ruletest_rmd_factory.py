import copy

from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_instance
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
    # rmr_transformations.
    user_rmr = None
    baseline_0_rmr = None
    baseline_90_rmr = None
    baseline_180_rmr = None
    baseline_270_rmr = None
    proposed_rmr = None

    # Read in transformations dictionary. This will perturb a template or fully define an RMR (if no template defined)
    rmr_transformations_dict = test_dict["rmr_transformations"]

    # If user/baseline/proposed RMR transformations exist, either update their existing template or set them directly
    # from RMR transformations
    if "user" in rmr_transformations_dict:
        user_rmr = rmr_transformations_dict["user"]

    if "baseline" in rmr_transformations_dict:
        baseline_rmr = rmr_transformations_dict["baseline"]

        for rmd_b in baseline_rmr["ruleset_model_descriptions"]:
            type_b = getattr_(rmd_b, "RMD", "type")
            if type_b == BASELINE_0:
                baseline_0_rmr = copy.deepcopy(baseline_rmr)
                baseline_0_rmr["ruleset_model_descriptions"] = []
                baseline_0_rmr["ruleset_model_descriptions"].append(
                    copy.deepcopy(rmd_b)
                )

            elif type_b == BASELINE_90:
                baseline_90_rmr = copy.deepcopy(baseline_rmr)
                baseline_90_rmr["ruleset_model_descriptions"] = []
                baseline_90_rmr["ruleset_model_descriptions"].append(
                    copy.deepcopy(rmd_b)
                )

            elif type_b == BASELINE_180:
                baseline_180_rmr = copy.deepcopy(baseline_rmr)
                baseline_180_rmr["ruleset_model_descriptions"] = []
                baseline_180_rmr["ruleset_model_descriptions"].append(
                    copy.deepcopy(rmd_b)
                )

            elif type_b == BASELINE_270:
                baseline_270_rmr = copy.deepcopy(baseline_rmr)
                baseline_270_rmr["ruleset_model_descriptions"] = []
                baseline_270_rmr["ruleset_model_descriptions"].append(
                    copy.deepcopy(rmd_b)
                )

    if "proposed" in rmr_transformations_dict:
        proposed_rmr = rmr_transformations_dict["proposed"]

    return produce_ruleset_model_instance(
        USER=user_rmr,
        BASELINE_0=baseline_0_rmr,
        BASELINE_90=baseline_90_rmr,
        BASELINE_180=baseline_180_rmr,
        BASELINE_270=baseline_270_rmr,
        PROPOSED=proposed_rmr,
    )
