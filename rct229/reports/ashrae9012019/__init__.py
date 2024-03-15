import importlib

__all__ = ["ashrae901_2019_summary_report", "ashrae901_2019_detail_report"]


def __getattr__(name):
    if name in __all__:
        return importlib.import_module("." + name, __name__)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    return sorted(__all__)
