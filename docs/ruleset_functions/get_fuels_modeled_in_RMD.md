# get_fuels_modeled_in_RMD

**Schema Version:** 0.0.23
**Description:** Get a list of the fuels used in the RMR.  Includes fuels used by HVAC systems including terminal units, chillers, boilers, ExternalFluidSources, and SWHs.

**Inputs:**
- **U, P, or B-RMR**: To determine a list of the fuels used in the RMR.  Includes fuels used by HVAC systems including terminal units, chillers, boilers, ExternalFluidSources, and SWHs in the RMR.

**Returns:**
- **fuels_list_x**: A list that saves all the fuels modeled in the RMR.

**Function Call:**  None

## Logic:  
- Create object from the RMR that has been input in the function: `X_RMR = RMR`
Set boolean variables to FALSE. Default is fuel is not used for space or SWH heating in the RMR. These boolean variable will be set to true as this function goes through the heating sources in the RMR and determines if each specific fuel has been modeled.
- Set boolean variable to FALSE: `fuels_propane_x = FALSE`
- Set boolean variable to FALSE: `fuels_natural_gas_x = FALSE`
- Set boolean variable to FALSE: `fuels_electricity_x = FALSE`
- Set boolean variable to FALSE: `fuels_oil_x = FALSE`
- Set boolean variable to FALSE: `fuels_other_x = FALSE`

- Loop through boilers to determine the fuels used by the boilers in the RMR. Boolean variables are set to TRUE accordingly, for each boiler_x in the X_RMR: `for boiler_x in X_RMR...Boiler:`  
    - Reset energy source variable: `energy_source_type_x = ""`
    - Get the energy_source_type: `energy_source_type_x = boiler_x.energy_source_type` 
    - Check if the energy source is propane, if so then set boolean variable to true: `if energy_source_type_p in ["PROPANE"]:fuels_propane_x = TRUE`
    - Check else if the energy source is natural gas, if so then set boolean variable to true: `elif energy_source_type_x in ["NATURAL_GAS"]:fuels_natural_gas_x = TRUE`
    - Check else if the energy source is electricity, if so then set boolean variable to true: `elif energy_source_type_x in ["ELECTRICITY"]:fuels_electricity_x = TRUE`
    - Check else if the energy source is fuel oil, if so then set boolean variable to true: `elif energy_source_type_x in ["FUEL_OIL"]:fuels_oil_x = TRUE`
    - Else, set other boolean variable to true: `Else:fuels_other_x = TRUE`   
- Loop through chillers to determine the fuels used by the chillers in the RMR. Boolean variables are set to TRUE accordingly, for each chiller_x in the X_RMR: `for chiller_x in X_RMR...Chiller:`  
    - Reset energy source variable: `energy_source_type_x = ""`
    - Get the energy_source_type: `energy_source_type_x = chiller_x.energy_source_type` 
    - Check if the energy source is propane, if so then set boolean variable to true: `if energy_source_type_x in ["PROPANE"]:fuels_propane_x = TRUE`
    - Check else if the energy source is natural gas, if so then set boolean variable to true: `elif energy_source_type_x in ["NATURAL_GAS"]:fuels_natural_gas_x = TRUE`
    - Check else if the energy source is electricity, if so then set boolean variable to true: `elif energy_source_type_x in ["ELECTRICITY"]:fuels_electricity_x = TRUE`
    - Check else if the energy source is fuel oil, if so then set boolean variable to true: `elif energy_source_type_x in ["FUEL_OIL"]:fuels_oil_x = TRUE`
    - Else, set other boolean variable to true: `Else:fuels_other_x = TRUE`   
- Loop through all ExternalFluidSources to determine the fuels used by the ExternalFluidSources in the RMR. Boolean variables are set to TRUE accordingly, for each ExternalFluidSources_x in the X_RMR: `for ExternalFluidSources_x in X_RMR...ExternalFluidSource:`  
    - Reset energy source variable: `energy_source_type_x = ""`
    - Get the energy_source_type: `energy_source_type_x = ExternalFluidSources_x.energy_source_type` 
    - Check if the energy source is propane, if so then set boolean variable to true: `if energy_source_type_x in ["PROPANE"]:fuels_propane_x = TRUE`
    - Check else if the energy source is natural gas, if so then set boolean variable to true: `elif energy_source_type_x in ["NATURAL_GAS"]:fuels_natural_gas_x = TRUE`
    - Check else if the energy source is electricity, if so then set boolean variable to true: `elif energy_source_type_x in ["ELECTRICITY"]:fuels_electricity_x = TRUE`
    - Check else if the energy source is fuel oil, if so then set boolean variable to true: `elif energy_source_type_x in ["FUEL_OIL"]:fuels_oil_x = TRUE`
    - Else, set other boolean variable to true: `Else:fuels_other_x = TRUE`  
- Loop through all HVAC systems in the X_RMR and check which fuels are used for heating. Boolean variables are set to TRUE accordingly, for each hvac_x in the X_RMR: `for hvac_x in X_RMR...HeatingVentilatingAirConditioningSystem:`  
    - Loop through the heating systems associated with the hvac system, for each heating system in hvac_x: `For heating_systems_x in hvac_x.heating_system:`
        - Reset energy source variable: `energy_source_type_x = ""`
        - Get the energy_source_type: `energy_source_type_x = heating_systems_x.energy_source_type`
        - Check if the energy source is propane, if so then set boolean variable to true: `if energy_source_type_x in ["PROPANE"]:fuels_propane_x = TRUE`
        - Check else if the energy source is natural gas, if so then set boolean variable to true: `elif energy_source_type_x in ["NATURAL_GAS"]:fuels_natural_gas_x = TRUE`
        - Check else if the energy source is electricity, if so then set boolean variable to true: `elif energy_source_type_x in ["ELECTRICITY"]:fuels_electricity_x = TRUE`
        - Check else if the energy source is fuel oil, if so then set boolean variable to true: `elif energy_source_type_x in ["FUEL_OIL"]:fuels_oil_x = TRUE`
        - Else, set other boolean variable to true: `Else:fuels_other_x = TRUE`  
    - Loop through the preheat systems associated with the hvac system, for each preheat system in hvac_x: `For preheat_systems_x in hvac_x.preheat_systems:`
        - Reset energy source variable: `energy_source_type_x = ""`
        - Get the energy_source_type: `energy_source_type_x = preheat_systems_x.energy_source_type`
        - Check if the energy source is propane, if so then set boolean variable to true: `if energy_source_type_x in ["PROPANE"]:fuels_propane_x = TRUE`
        - Check else if the energy source is natural gas, if so then set boolean variable to true: `elif energy_source_type_x in ["NATURAL_GAS"]:fuels_natural_gas_x = TRUE`
        - Check else if the energy source is electricity, if so then set boolean variable to true: `elif energy_source_type_x in ["ELECTRICITY"]:fuels_electricity_x = TRUE`
        - Check else if the energy source is fuel oil, if so then set boolean variable to true: `elif energy_source_type_x in ["FUEL_OIL"]:fuels_oil_x = TRUE`
        - Else, set other boolean variable to true: `Else:fuels_other_x = TRUE`  
- Loop through all terminal units and check the heat source associated with each. Boolean variables are set to TRUE accordingly, for each terminal_x in the X_RMR: `for terminal_x in X_RMR...Terminal:`
    - Reset energy source variable: `energy_source_type_x = ""`
    - Get terminal heat source: `energy_source_type_x = terminal_x.heat_source`
    - Check if the energy source is electric, if so then set boolean variable to true: `if energy_source_type_x in ["ELECTRIC"]:fuels_electricity_x = TRUE`
    - Check else if the energy source is other, if so then set boolean variable to true (else, do nothing): `elif energy_source_type_x in ["OTHER"]:fuels_other_x = TRUE`  
- Loop through all ServiceWaterHeatingEquipment to determine the fuels used by the ServiceWaterHeatingEquipment in the RMR. Boolean variables are set to TRUE accordingly, for each ServiceWaterHeatingEquipment_x in the X_RMR: `for ServiceWaterHeatingEquipment_x in X_RMR...ServiceWaterHeatingEquipment:`  
    - Reset energy source variable: `energy_source_type_x = ""`
    - Get the energy_source_type: `energy_source_type_x = ServiceWaterHeatingEquipment_x.heater_fuel_type` 
    - Check if the energy source is propane, if so then set boolean variable to true: `if energy_source_type_x in ["PROPANE"]:fuels_propane_x = TRUE`
    - Check else if the energy source is natural gas, if so then set boolean variable to true: `elif energy_source_type_x in ["NATURAL_GAS"]:fuels_natural_gas_x = TRUE`
    - Check else if the energy source is electricity, if so then set boolean variable to true: `elif energy_source_type_x in ["ELECTRICITY"]:fuels_electricity_x = TRUE`
    - Check else if the energy source is fuel oil, if so then set boolean variable to true: `elif energy_source_type_x in ["FUEL_OIL"]:fuels_oil_x = TRUE`
    - Else, set other boolean variable to true: `Else:fuels_other_x = TRUE`  
- Loop through all MiscellaneousEquipment objects to determine the fuels used by the MiscellaneousEquipment in the RMR. Boolean variables are set to TRUE accordingly, for each MiscellaneousEquipment_x in the X_RMR: `for MiscellaneousEquipment_x in X_RMR...MiscellaneousEquipment:`  
    - Reset energy source variable: `energy_source_type_x = ""`
    - Get the energy_source_type: `energy_source_type_x = MiscellaneousEquipment_x.energy_type` 
    - Check if the energy source is propane, if so then set boolean variable to true: `if energy_source_type_x in ["PROPANE"]:fuels_propane_x = TRUE`
    - Check else if the energy source is natural gas, if so then set boolean variable to true: `elif energy_source_type_x in ["NATURAL_GAS"]:fuels_natural_gas_x = TRUE`
    - Check else if the energy source is electricity, if so then set boolean variable to true: `elif energy_source_type_x in ["ELECTRICITY"]:fuels_electricity_x = TRUE`
    - Check else if the energy source is fuel oil, if so then set boolean variable to true: `elif energy_source_type_x in ["FUEL_OIL"]:fuels_oil_x = TRUE`
    - Else, set other boolean variable to true: `Else:fuels_other_x = TRUE`  

This section creates a list of the applicable fuel types the RMR based on the outcome of the boolean variables above.
- if fuels_propane_x equals true then list item 1 equals "PROPANE" otherwise "": `if fuels_propane_x == TRUE: list_item_1 = "PROPANE"`
- else: `list_item_1 = ""`
- if fuels_natural_gas_x equals true then list item 2 equals "NATURAL_GAS" otherwise "": `if fuels_natural_gas_x == TRUE: list_item_2 = "NATURAL_GAS"`
- else: `list_item_2 = ""`
- if fuels_electricity_x equals true then list item 3 equals "ELECTRICITY" otherwise "": `if fuels_electricity_x == TRUE: list_item_3 = "ELECTRICITY"`
- else: `list_item_3 = ""`
- if fuels_oil_x equals true then list item 4 equals "FUEL_OIL" otherwise "": `if fuels_oil_x == TRUE: list_item_4 = "FUEL_OIL"`
- else: `list_item_4 = ""`
- if fuels_other_x equals true then list item 5 equals "OTHER" otherwise "": `if fuels_other_x == TRUE: list_item_5 = "OTHER"`
- else: `list_item_5 = ""`

- Return list of fuels: `fuels_list_x = [list_item_1,list_item_2,list_item_3,list_item_4,list_item_5]`  
**Returns** `return fuels_list_x`

**[Back](../_toc.md)**
