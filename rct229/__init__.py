__version__ = "0.4.1"


def _initialize_rulesets():
    from rct229.rulesets import discover_ruleset_plugins, register_rulesets

    discover_ruleset_plugins()
    register_rulesets()


_initialize_rulesets()
