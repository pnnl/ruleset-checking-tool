from rct229.rule_engine.rulesets import RuleSet


class SchemaStore:
    SCHEMA_KEY = "ASHRAE229.schema.json"
    SCHEMA_9012019_ENUM_KEY = "Enumerations2019ASHRAE901.schema.json"
    SCHEMA_9012022_ENUM_KEY = "Enumerations2019ASHRAE901.schema.json"
    SCHEMA_RESNET_ENUM_KEY = "EnumerationsRESNET.schema.json"
    SCHEMA_T24_ENUM_KEY = "Enumerations2019T24.schema.json"
    SCHEMA_9012019_OUTPUT_KEY = "Output2019ASHRAE901.schema.json"
    SCHEMA_9012022_OUTPUT_KEY = "Output2019ASHRAE901.schema.json"
    SELECTED_RULESET = ""

    @staticmethod
    def get_active_enum_schema():

        match SchemaStore.SELECTED_RULESET:

            case RuleSet.ASHRAE9012019_RULESET:
                return SchemaStore.SCHEMA_9012019_ENUM_KEY
            case RuleSet.ASHRAE9012022_RULESET:
                return SchemaStore.SCHEMA_9012022_ENUM_KEY

    @staticmethod
    def get_active_output_schema():

        match SchemaStore.SELECTED_RULESET:
            case RuleSet.ASHRAE9012019_RULESET:
                return SchemaStore.SCHEMA_9012019_OUTPUT_KEY
            case RuleSet.ASHRAE9012022_RULESET:
                return SchemaStore.SCHEMA_9012022_OUTPUT_KEY

    @staticmethod
    def get_enum_schema_by_ruleset(ruleset: str):
        from rct229.rulesets import register_rulesets, discover_ruleset_plugins

        if not any(a.endswith("_RULESET") for a in vars(RuleSet)):
            discover_ruleset_plugins()
            register_rulesets()

        match ruleset:
            case RuleSet.ASHRAE9012019_RULESET:
                return "Enumerations2019ASHRAE901.schema.json"
            case RuleSet.ASHRAE9012022_RULESET:
                return "Enumerations2019ASHRAE901.schema.json"
            case _:
                raise ValueError(f"Unknown ruleset: {ruleset}")

    @staticmethod
    def get_output_schema_by_ruleset(ruleset: str):
        from rct229.rulesets import register_rulesets, discover_ruleset_plugins

        if not any(attr.endswith("_RULESET") for attr in vars(RuleSet)):
            discover_ruleset_plugins()
            register_rulesets()

        match ruleset:
            case RuleSet.ASHRAE9012019_RULESET:
                return SchemaStore.SCHEMA_9012019_OUTPUT_KEY
            case RuleSet.ASHRAE9012022_RULESET:
                return SchemaStore.SCHEMA_9012022_OUTPUT_KEY

    @staticmethod
    def set_ruleset(ruleset: str):
        # prevent overriding the ruleset if multiprocessing.
        if SchemaStore.SELECTED_RULESET in (
            RuleSet.ASHRAE9012019_RULESET,
            RuleSet.ASHRAE9012022_RULESET,
        ):
            SchemaStore.SELECTED_RULESET = ruleset
        elif not SchemaStore.SELECTED_RULESET:
            SchemaStore.SELECTED_RULESET = ruleset
