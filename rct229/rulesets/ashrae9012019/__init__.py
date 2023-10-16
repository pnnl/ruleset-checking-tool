import importlib

# Add all available rule modules in __all__
# __all__ = ["section5", "section6", "section19", "section21", "section22", "section23"]
__all__ = ["section5", "section6"]
from rct229.schema.schema_enums import SchemaEnums

RMT = SchemaEnums.schema_enums[
    "RulesetModelOptions2019ASHRAE901"
]
BASELINE_0 = RMT.BASELINE_0
BASELINE_90 = RMT.BASELINE_90
BASELINE_180 = RMT.BASELINE_180
BASELINE_270 = RMT.BASELINE_270
USER = RMT.USER
PROPOSED = RMT.PROPOSED


def __getattr__(name):
    if name in __all__:
        return importlib.import_module("." + name, __name__)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    return sorted(__all__)
