import pint
import os

# Initialize pint ureg
def get_pint_unit_registry():

    ureg = pint.UnitRegistry()

    # Import unit definitions from text file
    path_to_units = os.path.join(
        os.path.dirname(__file__), "resources", "unit_registry.txt"
    )
    ureg.load_definitions(path_to_units)

    return ureg

