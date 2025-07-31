import importlib
import inspect

import rct229.reports as reports

__all__ = [
    "ashrae9012019",
    "general",
]

from rct229.report_engine.rct_report import RCTReport
from rct229.schema.schema_store import SchemaStore


def __getreports__():
    modules = []
    report_list = inspect.getmembers(reports, inspect.ismodule)
    for report in report_list:
        if report[0] == "general" or report[0] == SchemaStore.SELECTED_RULESET:
            report_modules = inspect.getmembers(report[1], inspect.ismodule)
            for mod in report_modules:
                modules.append(mod)

    # --- End adding base class names
    available_reports = []
    for module in modules:
        available_reports += [
            f
            for f in inspect.getmembers(
                module[1],
                lambda obj: inspect.isclass(obj) and issubclass(obj, RCTReport),
            )
            if (not f[0] == "RCTReport")
        ]
    return available_reports


def __getattr__(name):
    if name in __all__:
        return importlib.import_module("." + name, __name__)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    return sorted(__all__)
