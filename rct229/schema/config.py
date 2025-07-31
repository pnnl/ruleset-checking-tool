# from icecream import install as install_icecream

from rct229.schema.config_functions import *

# Constants
schema_dict = get_schema_definitions_dictionary()
schema_version = get_schema_version()
unit_convention_dict = get_unit_conventions_dictionary()
ureg = get_pint_unit_registry()


# Add icecream to the builtins modules so it can be called
# fom anywhere for debugging purposes
# install_icecream()
