
## get_surface_conditioning_category
**Schema Version:** 0.1.3  
Description: This function relies on get_surface_conditioning_category_for_single_RMD to return a dictionary that provides the more stringent conditioning category between two RMDs.  This funciton is updated for ASHRAE 90.1-2022 to ensure that the surface conditioning categories comply with the following:  
  "Space conditioning categories used to determine applicability of the envelope requirements in Tables G3.4-1 through G3.4-8 shall be the same as in the proposed design.  
  
  Exception: Envelope components of the HVAC zones that are semiheated in the proposed design must meet conditioned envelope requirements in Tables G3.4-1 through G3.4-8 if, based on the sizing runs, these zones are served by a baseline system with sensible cooling output capacity >= 5 Btu/h·ft2 of floor area, or with heating output capacity greater than or equal to the criteria in Table G3.4-9, or that are indirectly conditioned spaces."  

Inputs:

  - **RMD1**: The RMD - usually the Baseline RMD - primarily used to determine surface conditioning category.
  - **RMD2**: The other RMD - usually the P_RMD - used to determine the surface conditioning category.  If RMD2 is not provided, the program should supply P_RMD by default.  If RMD1 and RMD2 is equal, this function will return exactly the same result as get_surface_conditioning_category_for_single_RMD.

Functions:  
  - **get_surface_conditioning_category_for_single_RMD**

Returns:

  - **surface_conditioning_category**: The Surface Conditioning Category [exterior residential, exterior non-residential, exterior mixed, semi-exterior, unregulated].  

Logic:  

- Get the surface conditioning category dictionary for RMD1 (usually the baseline, so we'll name the dictionary b_...): `b_surface_conditioning_category = get_surface_conditioning_category_for_single_RMD(RMD1)`

- Get the surface conditioning category dictionary for RMD2 (usually the proposed, so we'll name the dictionary p_...): `p_surface_conditioning_category = get_surface_conditioning_category_for_single_RMD(RMD2)`
  
- Create a new surface conditioning category dictionary that will be a combination of the two: `surface_conditioning_category = {}`

- Look at each surface id in RMD1: `for surface_id in b_surface_conditioning_category:`

  - Check to see if the two conditioning cateogries match: `if b_surface_conditioning_category[surface_id] == p_surface_conditioning_category[surface_id]:`
 
    - then this category is the category to be used.  Add this category to surface_conditioning_category: `surface_conditioning_category[surface_id] = b_surface_conditioning_category[surface_id]`
   
    - Otherwise, if the proposed is semi-exterior, and the baseline is one of [exterior residential, exterior non-residential, exterior mixed], then the conditioning category needs to be the more stringent: `if b_surface_conditioning_category[surface_id] in ["exterior residential", "exterior non-residential", "exterior mixed"] and p_surface_conditioning_category[surface_id] == "semi-exterior": surface_conditioning_category[surface_id] = b_surface_conditioning_category[surface_id]`
   
    - All other cases, set the conditioning category equal to that in the proposed: `surface_conditioning_category[surface_id] = p_surface_conditioning_category[surface_id]`

**Returns** `return surface_conditioning_category_dict`  

**Notes**
1.  What if the proposed is "unregulated" and the baseline is a different category?

**[Back](../_toc.md)**
