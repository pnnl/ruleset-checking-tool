
# Envelope - Rule 5-22  

**Rule ID:** 5-22  
**Rule Description:** The baseline fenestration area for an existing building shall equal the existing fenestration area prior to the proposed work.  
**Rule Assertion:** B-RMR total (subsurface.glazed_area+subsurface.opaque_area) = expected value  
**Appendix G Section:** Section G3.1-5(c) Building Envelope Modeling Requirements for the Baseline building  
**Appendix G Section Reference:** None  

**Data Lookup:** None  
**Evaluation Context:**  Each Data Element  

**Applicability Checks:** None  

**Manual Checks:** Yes  
**Function Call:**  None  

## Rule Logic:

- Check if building is not all new: `if NOT B_RMR.building.is_all_new:`

**Rule Assertion** `CAUTION and raise_warning "BUILDING IS EXISTING. THE BASELINE VERTICAL FENESTRATION AREA FOR EXISTING BUILDINGS MUST EQUAL TO THE FENESTRATION AREA PRIOR TO THE PROPOSED SCOPE OF WORK. THE BASELINE FENESTRATION AREA MUST BE CHECKED MANUALLY."`

**[Back](../_toc.md)**
