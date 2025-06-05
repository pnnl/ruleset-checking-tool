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
Description: Get the data element with the matching `name` for either a User, Proposed or Baseline RMD.   
Inputs:  
- **rmd:** The RMD data object (U_RMD, P_RMD, B_RMD) for retrieving the data element.  
- **data_group:** The name of the RMD schema Data Group for retrieving the data element.   
- **name:** The name parameter used for looking up the Data Element

Returns:  
- **data_element**: A RMD Data Element object.

## match_data_element_exist
Description: Returns a true or false to indicate whether there is a data element with the matching `name` in either a User, Proposed or Baseline RMD. True means that it exists and false means that it does not exist.
Inputs:  
- **rmd:** The RMD data object (U_RMD, P_RMD, B_RMD) for determining if there is a matching data element.  
- **data_group:** The name of the RMD schema Data Group for looking up the data element.   
- **name:** The name parameter used for looking up the Data Element.

Returns:  
- **data_element_exist**: True or False.

**[Back](_toc.md)**