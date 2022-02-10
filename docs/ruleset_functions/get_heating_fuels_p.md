## get_heating_fuels_p

**Description:** Get a list of the heating fuels used in the P-RMR.  

**Inputs:**
- **P-RMR**: To determine the heating fuels used in the P-RMR.

**Returns:**
- **heating_fuels_list_p**: A list that saves all the heating fuels used in the P_RMR.
 
**Function Call:** None


**Logic:**
# Set boolean variables to FALSE. Default is fuel is not used for space heating in the P_RMR. These boolean variable will be set to true as this function goes through the heating sources in the P_RMR and determines if each specific fuel has been modeled.
- Set boolean variable to FALSE: `fuels_propane_p = FALSE`
- Set boolean variable to FALSE: `fuels_natural_gas_p = FALSE`
- Set boolean variable to FALSE: `fuels_electricity_p = FALSE`
- Set boolean variable to FALSE: `fuels_oil_p = FALSE`
- Set boolean variable to FALSE: `fuels_other_p = FALSE`

# Loop through boilers to determine the fuels used by the boilers in the P_RMR. Boolean variables are set to TRUE accordingly.
- For each rulesetModelInstance_p in the P_RMR: `for rulesetModelInstance_p in P_RMR:`
    - For each boiler_p in rulesetModelInstance_p.boilers: `for boiler_p in rulesetModelInstance_p.boilers:`
    - Reset energy source variable: `energy_source_type_p = ""`
    - Get the energy_source_type: `energy_source_type_p = boiler_p.energy_source_type` 
    - Check if the energy source is propane, if so then set boolean variable to true: `if energy_source_type_p in ["PROPANE"]:fuels_propane_p = TRUE`
    - Check else if the energy source is natural gas, if so then set boolean variable to true: `elif energy_source_type_p in ["NATURAL_GAS"]:fuels_natural_gas_p = TRUE`
    - Check else if the energy source is electricity, if so then set boolean variable to true: `elif energy_source_type_p in ["ELECTRICITY"]:fuels_electricity_p = TRUE`
    - Check else if the energy source is fuel oil, if so then set boolean variable to true: `elif energy_source_type_p in ["FUEL_OIL"]:fuels_oil_p = TRUE`
    - Else, set other boolean variable to true: `Else:fuels_other_p = TRUE`
# Loop through all HVAC systems in the P_RMR and check which fuels are used for heating. Boolean variables are set to TRUE accordingly.
- For each building_segment_p in the P_RMR: `for building_segment_p in P_RMR..BuildingSegment:`
    - For each hvac_p in each building_segment_p: `for hvac_p in building_segment_p.heating_ventilation_air_conditioning_systems:`
        # Loop through the heating systems associated with the hvac system.
        - For each heating system in hvac_p: `heating_systems_p in hvac_p.heating_systems:`
        - Reset energy source variable: `energy_source_type_p = ""`
        - Get the energy_source_type: `energy_source_type_p = heating_systems_p.energy_source_type`
        - Check if the energy source is propane, if so then set boolean variable to true: `if energy_source_type_p in ["PROPANE"]:fuels_propane_p = TRUE`
        - Check else if the energy source is natural gas, if so then set boolean variable to true: `elif energy_source_type_p in ["NATURAL_GAS"]:fuels_natural_gas_p = TRUE`
        - Check else if the energy source is electricity, if so then set boolean variable to true: `elif energy_source_type_p in ["ELECTRICITY"]:fuels_electricity_p = TRUE`
        - Check else if the energy source is fuel oil, if so then set boolean variable to true: `elif energy_source_type_p in ["FUEL_OIL"]:fuels_oil_p = TRUE`
        - Else, set other boolean variable to true: `Else:fuels_other_p = TRUE`
        # Loop through the preheat systems associated with the hvac system.
        - For each preheat system in hvac_p: `preheat_systems_p in hvac_p.preheat_systems:`
        - Reset energy source variable: `energy_source_type_p = ""`
        - Get the energy_source_type: `energy_source_type_p = preheat_systems_p.energy_source_type`
        - Check if the energy source is propane, if so then set boolean variable to true: `if energy_source_type_p in ["PROPANE"]:fuels_propane_p = TRUE`
        - Check else if the energy source is natural gas, if so then set boolean variable to true: `elif energy_source_type_p in ["NATURAL_GAS"]:fuels_natural_gas_p = TRUE`
        - Check else if the energy source is electricity, if so then set boolean variable to true: `elif energy_source_type_p in ["ELECTRICITY"]:fuels_electricity_p = TRUE`
        - Check else if the energy source is fuel oil, if so then set boolean variable to true: `elif energy_source_type_p in ["FUEL_OIL"]:fuels_oil_p = TRUE`
        - Else, set other boolean variable to true: `Else:fuels_other_p = TRUE`
    # Loop through all terminal units and check the heat source associated with each. Boolean variables are set to TRUE accordingly.
    - For each zone_p in each building_segment_p: `for zone_p in building_segment_p.zones:`
        - For each terminal_p in zone_p: `for terminal_p in zone_p.terminals:`
            - Reset energy source variable: `energy_source_type_p = ""`
            - Get terminal heat source: `energy_source_type_p = terminal_p.heat_source`
            - Check if the energy source is electric, if so then set boolean variable to true: `if energy_source_type_p in ["ELECTRIC"]:fuels_electricity_p = TRUE`
            - Check else if the energy source is other, if so then set boolean variable to true (else, do nothing): `elif energy_source_type_p in ["OTHER"]:fuels_other_p = TRUE`
# This section creates a list of the applicable fuel types that provide heating in the proposed design model based on the outcome of the boolean variables above.
- if fuels_propane_p equals true then list item 1 equals "PROPANE" otherwise "": `if fuels_propane_p == TRUE: list_item_1 = "PROPANE"`
    - else: `list_item_1 = ""`
- if fuels_natural_gas_p equals true then list item 2 equals "NATURAL_GAS" otherwise "": `if fuels_natural_gas_p == TRUE: list_item_2 = "NATURAL_GAS"`
    - else: `list_item_2 = ""`
- if fuels_electricity_p equals true then list item 3 equals "ELECTRICITY" otherwise "": `if fuels_electricity_p == TRUE: list_item_3 = "ELECTRICITY"`
    - else: `list_item_3 = ""`
- if fuels_oil_p equals true then list item 4 equals "FUEL_OIL" otherwise "": `if fuels_oil_p == TRUE: list_item_4 = "FUEL_OIL"`
    - else: `list_item_4 = ""`
- if fuels_other_p equals true then list item 5 equals "OTHER" otherwise "": `if fuels_other_p == TRUE: list_item_5 = "OTHER"`
    - else: `list_item_5 = ""`

- Return list of fuels: `heating_fuels_list_p = [list_item_1,list_item_2,list_item_3,list_item_4,list_item_5]`
**Returns** `return heating_fuels_list_p`

**[Back](../_toc.md)**