from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_instance
from rct229.rule_engine.rulesets import RuleSet
from rct229.schema.schema_store import SchemaStore


def get_ruletest_rmd_models(test_dict: dict):
    rmd = None
    if SchemaStore.SELECTED_RULESET == RuleSet.ASHRAE9012019_RULESET:
        rmd = get_9012019_rmd_models(test_dict)

    return rmd


def get_9012019_rmd_models(test_dict: dict):

    # Each of these will remain None unless it is specified in
    # rmr_transformations.
    user_rmr = None
    baseline_rmr = None
    proposed_rmr = None

    # Read in transformations dictionary. This will perturb a template or fully define an RMR (if no template defined)
    rmr_transformations_dict = test_dict["rmr_transformations"]

    # If user/baseline/proposed RMR transformations exist, either update their existing template or set them directly
    # from RMR transformations
    if "user" in rmr_transformations_dict:
        user_rmr = rmr_transformations_dict["user"]

    if "baseline" in rmr_transformations_dict:
        baseline_rmr = rmr_transformations_dict["baseline"]

    if "proposed" in rmr_transformations_dict:
        proposed_rmr = rmr_transformations_dict["proposed"]

    return produce_ruleset_model_instance(
        USER=user_rmr, BASELINE_0=baseline_rmr, PROPOSED=proposed_rmr
    )