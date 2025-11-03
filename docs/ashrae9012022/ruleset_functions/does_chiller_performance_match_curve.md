# does_chiller_performance_match_curve

**Description:** Evaluates whether the chiller performance curves align with the sets of performance curves specified in Appendix J of ASHRAE 90.1-2022 Appendix G.

**Inputs:**  
- **Chiller data group**: The chiller object containing all relevant data for the chiller to be validated against the performance curves in Appendix J of ASHRAE 90.1-2022.  This includes the rated capacity, full load efficiency (COP), compressor type, and the lists of capacity and power operating points.
- **curve_set**: The curve set that the chiller is expected to align with.  This should be a letter code of A, B, etc. to lookup in either Table J-4 or J-6.

**Returns:**  
- **is_chiller_performance_app_j**: boolean value indicating whether the chiller performance validation passed or failed.

**Function Call:**  None

## Logic: 
- use the curve set to determine which table to use for the lookup of coefficients. A through U is Table J-4, V through AB is Table J-6. Raise error for developers if anything else is passed as an argument: `if curve_set in ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U"]: table_lookup = "J-4" elif curve_set in ["V","X","Y","Z","AA","AB"]: table_lookup="J-6" else: raise ValueError("Invalid curve set provided. Must be A-U for Table J-4 or V-AB for Table J-6.")`
- calculate the chiller rated power by dividing the chiller rated capacity by the chiller full load efficiency (cop): `rated_power = chiller["rated_capacity"] / chiller["full_load_efficiency"]`
- create a list of the expected capacity operating points: `expected_validation_plr = [0.25, 0.5, 0.75, 1]`
- create a list of the expected chiller water temperatures for the validation calculations: `expected_chwt_temps = [39, 45, 50, 55]`
- create a list of the expected entering condenser temperatures for the condenser water temperature: `expected_ecwt_temps = [60, 104, 85, 72.5, 97.5]`

- get the coefficients for the EIR-f-T curve (IP units) using a table lookup from either table J-4 or J-6.  This assumes that the lookup function will return a list with the coefficients in order (C1,C2,...): `if table_lookup == "J-4": eir_f_t_coefficients = table_J_4_lookup(curve_set,"EIR-f-T") else: eir_f_t_coefficients = table_J_6_lookup(curve_set,"EIR-f-T")`
- get the coefficients for the CAP-f-T curve (IP units) using a table lookup from either table J-4 or J-6.  This assumes that the lookup function will return a list with the coefficients in order (C1,C2,...): `if table_lookup == "J-4": cap_f_t_coefficients = table_J_4_lookup(curve_set,"Cap-f-T") else: cap_f_t_coefficients = table_J_6_lookup(curve_set,"Cap-f-T")`
- get the coefficients for the PLR curve (IP units) using a table lookup from either table J-4 or J-6.  This assumes that the lookup function will return a list with the coefficients in order (C1,C2,...): `if table_lookup == "J-4": eir_f_t_coefficients = table_J_4_lookup(curve_set,"EIR-f-PLR") else: plr_coefficients = table_J_6_lookup(curve_set,"EIR-f-PLR")`

- initialize a dict to store the chilled water supply temperatures, condenser temperatures in a string as keys, and capacity operating point results as the values: `capacity_operating_pts_dict = {}`
- iterate through the capacity operating points: `for capacity_operating_point in chiller["capacity_operating_points"]:`
    - create the key string: `dict_key = f"{capacity_operating_point.chilled_water_supply_temperature}, {capacity_operating_point.condenser_temperature}"`
    - add the item to the dict: `capacity_operating_pts_dict[dict_key] = capacity_operating_point.capacity`

- initialize a dict to store the chilled water supply temperatures, condenser temperatures in a string as keys, and lists of power operating points as the values: `power_operating_pts_dict = {}`
- look at each value in chiller power operating points: `for power_operating_point in chiller["power_operating_points"]:`
    - create the key string: `dict_key = f"{power_operating_point.chilled_water_supply_temperature}, {power_operating_point.condenser_temperature}"`
    - set the default to a blank list: `power_operating_pts_dict.setdefault([dict_key], [])`
    - append the power operating point to the list at this given: `power_operating_pts_dict[dict_key].append(power_operating_point)`

- create a dictionary of the expected capacities for use in the power validation check: `given_capacities = {}`
- the following lines or logic do the capacity validation check:
- create a list of non-matching capacity operating points: `non_matching_capacity_operating_points = []`
- create a list of missing capacity operating points: `missing_capacity_operating_points = []`
- loop through the expected_chwt_temps: `for chwt in expected_chwt_temps:`
    - loop through each expected_ecwt_temps: `for ecwt in expected_ecwt_temps:`
        - create the key: `dict_key = f"{chwt}, {ecwt}"`
        - look for the capacity operating point in capacity_operating_pts_dict: `if dict_key in capacity_operating_pts_dict:`
            - calculate the expected capacity by multiplying the result of the formula by the rated_capacity: `expected_capacity = (cap_f_t_coefficients[0] + cap_f_t_coefficients[1] * chwt + cap_f_t_coefficients[2] * chwt^2 + cap_f_t_coefficients[3] * ecwt + cap_f_t_coefficients[4] * ecwt^2 + cap_f_t_coefficients[5] * chwt * ecwt) * rated_capacity`
            - get the given capacity: `given_capacity = capacity_operating_pts_dict[dict_key]`
            - add the given capacity to the given_capacities dictionary: `given_capacities[dict_key] = given_capacity`
            - Compare the expected capacity to the given capacity.  This should not be an exact match, but with a margin of error (see notes at the bottom for suggested margins of errors).  We don't need to do anything if the capacities match, but if they don't match we need to add the conditions to the non_matching_capacity_operating_points list: `if expected_capacity != given_capacity: non_matching_capacity_operating_points.append({"CHWT": chwt, "ECWT": ecwt})`
        - otherwise this value doesn't exist, append these conditions to the missing_capacity_operating_points list: `else: missing_capacity_operating_points.append({"CHWT": chwt, "ECWT": ecwt})`

- the following lines or logic do the power validation check:
- create a list of non-matching power operating points: `non_matching_power_operating_points = []`
- create a list of missing power operating points: `missing_power_operating_points = []`
- loop through the expected_chwt_temps: `for chwt in expected_chwt_temps:`
    - loop through each expected_ect_temps: `for ecwt in expected_ecwt_temps:`
        - create the key: `dict_key = f"{chwt}, {ecwt}"`
        - look for the power operating points in power operating points dict: `if dict_key in power_operating_pts_dict:`
            - we are expecting to see multiple operating points aligning with the expected validation PLR.  Create a list of part load ratios that are given.  Later we'll compare this with the expected list to make sure that all points are given: `given_plrs = []`
            - look at each power operating point in the list: `for power_operating_point in power_operating_pts_dict[dict_key]:`
                - get the load: `load = power_operating_point.load`
                - get the given power: `given_power = power_operating_point.power`
                - calculate the PLR by dividing the load by the given capacity at these operating conditions: `plr = load / given_capacities[dict_key]`
                - check whether the plr is one of the plrs that we need to check - note to dev team, please accept a match that is with 0.01 of the expected: `if plr in expected_validation_plr:`
                    - add the plr to the list of plrs provided: `given_plrs.append(plr)`
                    - calculate eir_plr using the coefficients given: `eir_plr = plr_coefficients[0] + plr_coefficients[1] * plr + plr_coefficients[2] * plr^2`
                    - calculate the eir_ft using the coefficients given: `eir_ft = eir_f_t_coefficients[0] + eir_f_t_coefficients[1] * chwt + eir_f_t_coefficients[2] * chwt^2 + eir_f_t_coefficients[3] * ecwt + eir_f_t_coefficients[4] * ecwt^2 + eir_f_t_coefficients[5] * chwt * ecwt`
                    - calculate the expected power using the formula:
                        - Chiller operating power = Rated Capacity × CAP-f-T × EIR-f-T × EIR-f-PLR × Chiller Input Power at Rated Conditions/Chiller Capacity at Rated Conditions
                    - in this case, the given capacity under these operating conditions is the rated capacity * cap_ft, so the modified formula is as follows: `expected_power = given_capacity[dict_key] * eir_ft * eir_plr * rated_power/rated_capacity`
                    - check whether the expected power and the given power are equal.  This should not be an exact match, but with a margin of error (see notes at the bottom for suggested margins of errors).  If the expected power and given power do not match, add the conditions to the non_matching_power_operating_points list: `if expected_power != given_power: non_matching_power_operating_points.append({"CHWT": chwt, "ECWT": ecwt, "PLR": plr})`
                - otherwise, this particular plr is not given, append these conditions to the missing_power_operating_points list: `missing_power_operating_points.append({"CHWT": chwt, "ECWT": ecwt, "PLR": plr})`
        - otherwise, this point isn't given, append these conditions to the missing_power_operating_points list: `missing_power_operating_points.append({"CHWT": chwt, "ECWT": ecwt, "PLR": "ALL"})`

- Chiller performance aligns with App J if all lists of missing or non-matching operating points have a length of zero: `does_chiller_performance_match_curve = len(non_matching_capacity_operating_points) == len(missing_capacity_operating_points) == len(non_matching_power_operating_points) == len(missing_power_operating_points) == 0`


**Returns** `does_chiller_performance_match_curve`  

**Questions:**  None