# Functions  

## append 
Description:  Add a value to the end of a list of values.   
Inputs:  
- **value:** A value to add to a list.

Returns:  
- **new_list**: The data table value to be returned.


## data_lookup 
Description: Look up a value from a data table using a given lookup parameter.   
Inputs:  
- **appendix_g_table_number:** The number reference of the data table in ASHRAE 90.1-2019 Appendix G to retrieve data from.  
- **lookup_parameter:** The parameter name of the column used to lookup data from the table.  

Returns:  
- **table_value**: The data table value to be returned.

## match_data_element 
Description: Get the data element with the matching `name` for either a User, Proposed or Baseline RMR.   
Inputs:  
- **rmr:** The RMR data object (U_RMR, P_RMR, B_RMR) for retrieving the data element.  
- **data_group:** The name of the RMR schema Data Group for retrieving the data element.   
- **name:** The name parameter used for looking up the Data Element

Returns:  
- **data_element**: A RMR Data Element object.

## convert_event_schedule_to_hourly 
Description: Convert an event type schedule to an hourly type schedule.  
Inputs:  
- **Schedule**: The event type schedule that needs to be converted.

Returns:  
- **Schedule**: The equivalent hourly type schedule.

**[Back](_toc.md)**
