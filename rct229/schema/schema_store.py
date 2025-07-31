from rct229.rule_engine.rulesets import RuleSet


class SchemaStore:
    SCHEMA_KEY = "ASHRAE229.schema.json"
    SCHEMA_9012019_ENUM_KEY = "Enumerations2019ASHRAE901.schema.json"
    SCHEMA_RESNET_ENUM_KEY = "EnumerationsRESNET.schema.json"
    SCHEMA_T24_ENUM_KEY = "Enumerations2019T24.schema.json"
    SCHEMA_9012019_OUTPUT_KEY = "Output2019ASHRAE901.schema.json"
    SELECTED_RULESET = ""

    @staticmethod
    def get_enum_schema_by_ruleset():
        if SchemaStore.SELECTED_RULESET == RuleSet.ASHRAE9012019_RULESET:
            return SchemaStore.SCHEMA_9012019_ENUM_KEY

    @staticmethod
    def get_output_schema_by_ruleset():
        if SchemaStore.SELECTED_RULESET == RuleSet.ASHRAE9012019_RULESET:
            return SchemaStore.SCHEMA_9012019_OUTPUT_KEY

    @staticmethod
    def set_ruleset(ruleset: RuleSet):
        # prevent overriding the ruleset if multi-processing.
        if not SchemaStore.SELECTED_RULESET:
            SchemaStore.SELECTED_RULESET = ruleset
