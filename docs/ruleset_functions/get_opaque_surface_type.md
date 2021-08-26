
## get_opaque_surface_type

Description: This function would determine whether it is a wall, ceiling or floor.  

Inputs:
  - **Surface**: The surface that needs to determine surface type.  

Returns:
- **opaque_surface_type**: The Opaque Surface Type [roof, heated slab-on-grade, unheated slab-on-grade, floor, above-grade wall, below-grade wall].  


Logic:  

- If surface tilt is more than or equal to 0 degree and less than 60 degrees, surface is classified as roof: ```if 0 <= surface.tilt < 60: surface_type = "ROOF"```  

- Else if surface tile is more than 120 degrees and less than or equal to 180 degrees, surface is classified as floor: ```else if 120 < surface.tilt <= 180:```  

  - Determine if surface is heated slab-on-grade: ```if ( surface.construction.has_radiant_heating ) AND ( surface.adjacent_to == "GROUND" ): surface_type = "HEATED SLAB-ON-GRADE"```  

  - Else determine if surface is unheated slab-on-grade: ```else if surface.adjacent_to == "GROUND": surface_type = "UNHEATED SLAB-ON-GRADE"```  

  - Else, surface is floor: ```else: surface_type = "FLOOR"```  

- Else, surface is classified as wall: ```else:```  

  - Determine if surface is below grade wall: ```if surface.adjacent_to == "GROUND": surface_type = "BELOW-GRADE WALL"```  

  - Else determine if surface is above grade wall: ```else: surface_type = "ABOVE-GRADE WALL"```  

**Returns** ```return surface_type```  

**Notes:**

  1. Baseline slab that is more than 24" below grade and is unregulated. Verify in RDS.

**[Back](../_toc.md)**