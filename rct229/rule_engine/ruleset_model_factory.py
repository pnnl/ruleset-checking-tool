from rct229.rule_engine.rulesets import RuleSet
from rct229.schema.schema_enums import SchemaEnums
from rct229.schema.schema_store import SchemaStore
from rct229.utils.assertions import assert_

ruleset_model_dict = {
    RuleSet.ASHRAE9012019_RULESET: [
        "RulesetModelOptions2019ASHRAE901",
        "CommonRulesetModelOptions",
    ]
}


def get_ruleset_model_types(self):
    return list(self.__dict__)


def __getitem__(self, item):
    assert_(
        item in self.__dict__,
        f"model type {item} is not in the available model types: {list(self.__dict__)}",
    )
    return self.__dict__.get(item)


def __setitem__(self, key, item):
    assert_(
        key in self.__dict__,
        f"model type {key} is not in the available model types: {list(self.__dict__)}",
    )
    self.__dict__[key] = item


def __setattr__(self, key, val):
    self.__dict__[key] = val


RuleSetModels = type(
    "RuleSetModels",
    (),
    {
        # functions
        "__getitem__": __getitem__,
        "__setitem__": __setitem__,
        "__setattr__": __setattr__,
        "get_ruleset_model_types": get_ruleset_model_types,
    },
)


def get_rmd_instance():
    """
    Function to create a RMD instance from RuleSetModel object
    Returns RuleSetModels
    -------

    """
    rmd = RuleSetModels()
    ruleset_model_types_enums = [
        SchemaEnums.schema_enums[rmt]
        for rmt in ruleset_model_dict[SchemaStore.SELECTED_RULESET]
    ]

    ruleset_model_types_enum_list = list(
        set(
            [
                model_type_enum
                for ruleset_model_types_enum in ruleset_model_types_enums
                for model_type_enum in ruleset_model_types_enum.get_list()
            ]
        )
    )

    for ruleset_model in ruleset_model_types_enum_list:
        rmd.__setattr__(ruleset_model, None)
    return rmd


def produce_ruleset_model_description(**kwargs):
    """
    Factory function to manufacture a RuleSetModels instances based
    on user specifications

    Parameters
    ----------
    kwargs: provide key-value inputs - for example USER=False, BASELINE_0=TRUE

    Returns
    -------

    """
    ruleset_models = get_rmd_instance()
    for key in kwargs:
        ruleset_models.__setitem__(key, kwargs[key])
    return ruleset_models
