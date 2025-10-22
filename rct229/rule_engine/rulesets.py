from importlib.metadata import entry_points


# Ruleset enumerator
class RuleSet:
    """Dynamic registry for available rulesets."""

    # Optional static declarations (for IDE awareness)
    ASHRAE9012019_RULESET: str
    ASHRAE9012022_RULESET: str

    @classmethod
    def discover(cls):
        """Discover and register all available rulesets dynamically."""
        eps = entry_points(group="rct229.rulesets")
        for ep in eps:
            attr_name = ep.name.upper().replace("-", "_") + "_RULESET"
            setattr(cls, attr_name, ep.name)
        return cls


RuleSet.discover()


class LeapYear:
    LEAP_YEAR_HOURS = 8784
    REGULAR_YEAR_HOURS = 8760
