# get_building_total_lab_exhaust_from_zone_exhaust_fans  
**Schema Version:** 0.0.28  

**Description:** determines the total exhaust air flowrate for zone exhaust fans in zones that have laboratory spaces  
  
**Inputs:**  
- **RMI**

**Returns:**  
- **total_exhaust**: a numerical value indicating the total building exhaust airflow for zone exhaust fans in zones that have laboratory spaces

**Function Call:**  
- **get_building_lab_zones**

## Logic:  

- set the result variable to zero: `total_exhaust = 0`
- get a list of the zone.ids for all zones in the RMI serving zones that have laboratory spaces: `laboratory_zone_list = get_building_lab_zones(RMI)`
- Now find the laboratory exhaust for each zone in the laboratory_zones list. `Loop through each zone: for z_id in laboratory_zones_list:`
   - get the zone: `z = get_object_by_id(P_RMI, z_id)`
   - Add zonal exhaust fan airflow to zone_total_exhaust: `if z.zone_exhaust_fans ?:`
       - look at each exhaust fan: `for exhaust_fan in z.zone_exhaust_fans:`
         - add the airflow to the total exhaust: `total_exhaust += exhaust_fan.design_airflow`
        

**Returns** `total_exhaust`


**Notes/Questions:**  


**[Back](../_toc.md)**
