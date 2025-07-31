
## ASHRAE STD 229P RULESET CHECKING TOOL
### Summary Report 
##### ASHRAE 90.1-2019 Performance Rating Method (Appendix G)
##### Date: 2024-02-20 18:20:45.887364

### RMD Files
- user: C:\Users\xuwe123\Documents\GitHub\ruleset-checking-tool\examples\chicago_demo\user_model.json
- proposed: C:\Users\xuwe123\Documents\GitHub\ruleset-checking-tool\examples\chicago_demo\proposed_model.json
- baseline_0: C:\Users\xuwe123\Documents\GitHub\ruleset-checking-tool\examples\chicago_demo\baseline_model.json
- baseline_90: 
- baseline_180: 
- baseline_270: 

### Summary: All Primary Rules
|                              | All | Envelope | Lighting | Receptacles | Transformers | HVAC-HotWaterSide | HVAC - ChilledWaterSide | HVAC-AirSide | HVAC-General| HVAC-Baseline
|:----------------------------:|:---:|:--------:|:--------:|:-----------:|:------------:|:--------------:|:--------------:|:--------------:|:--------------:|:-----------:|
|Rules|163|40|9|0|0|18|41|16|36|3|
|Pass|60|8|4|0|0|13|25|3|6|1|
|Fail|15|3|3|0|0|0|5|0|3|1|
|Not Applicable|60|16|0|0|0|5|9|12|17|1|
|Undetermined (manual review)|28|13|2|0|0|0|2|1|10|0|

### Rule Evaluations
        
### Section: Envelope
            
  - **Rule Id**: 5-1
    - **Description**: There are four baseline rotations (i.e., four baseline models differing in azimuth by 90 degrees and four sets of baseline model results) if vertical fenestration area per each orientation differ by more than 5%.
    - **90.1-2019 Section**: Table G3.1#5a baseline column
    - **Overall Rule Evaluation Outcome**: FAILED
    - **Number of applicable components**: 1 
      
      | Pass %: 0| Fail %: 100| Not applicable %: 0| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 5-2
    - **Description**: The building shall be modeled so that it does not shade itself
    - **90.1-2019 Section**: Section G3.1-5(b) Building Envelope Modeling Requirements for the Baseline building
    - **Overall Rule Evaluation Outcome**: NOT_APPLICABLE
    - **Number of applicable components**: 1 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 100| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 5-3
    - **Description**: Baseline roof assemblies must conform with assemblies detailed in Appendix A
    - **90.1-2019 Section**: Section G3.1-5(b) Building Envelope Modeling Requirements for the Baseline building
    - **Overall Rule Evaluation Outcome**: UNDETERMINED
    - **Number of applicable components**: 26 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 96| Undetermined %: 3| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 5-4
    - **Description**: Baseline roof assemblies must match the appropriate assembly maximum U-factors in Tables G3.4-1 through G3.4-8.
    - **90.1-2019 Section**: Section G3.1-5(b) Building Envelope Modeling Requirements for the Baseline building
    - **Overall Rule Evaluation Outcome**: PASS
    - **Number of applicable components**: 1 
      
      | Pass %: 100| Fail %: 0| Not applicable %: 0| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 5-5
    - **Description**: Baseline below-grade walls shall conform with assemblies detailed in Appendix A Concrete block, A4)
    - **90.1-2019 Section**: Section G3.1-5(b) Building Envelope Modeling Requirements for the Baseline building
    - **Overall Rule Evaluation Outcome**: NOT_APPLICABLE
    - **Number of applicable components**: 1 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 100| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 5-6
    - **Description**: Baseline below-grade walls shall match the appropriate assembly maximum C-factors in Table G3.4-1 through G3.4-8.
    - **90.1-2019 Section**: Section G3.1-5(b) Building Envelope Modeling Requirements for the Baseline building
    - **Overall Rule Evaluation Outcome**: NOT_APPLICABLE
    - **Number of applicable components**: 1 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 100| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 5-7
    - **Description**: Baseline above-grade wall assemblies must conform with assemblies detailed in  Appendix A (Steel-framed A3.3) 
    - **90.1-2019 Section**: Section G3.1-5(b) Building Envelope Modeling Requirements for the Baseline building
    - **Overall Rule Evaluation Outcome**: UNDETERMINED
    - **Number of applicable components**: 72 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 66| Undetermined %: 33| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 5-8
    - **Description**: Baseline above-grade wall assemblies must match the appropriate assembly maximum U-factors in Tables G3.4-1 through G3.4-8.
    - **90.1-2019 Section**: Section G3.1-5(b) Building Envelope Modeling Requirements for the Baseline building
    - **Overall Rule Evaluation Outcome**: PASS
    - **Number of applicable components**: 24 
      
      | Pass %: 100| Fail %: 0| Not applicable %: 0| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 5-9
    - **Description**: Baseline floor assemblies must conform with assemblies detailed in  Appendix A (Floors—Steel-joist (A5.3))
    - **90.1-2019 Section**: Section G3.1-5(b) Building Envelope Modeling Requirements for the Baseline building
    - **Overall Rule Evaluation Outcome**: UNDETERMINED
    - **Number of applicable components**: 30 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 83| Undetermined %: 16| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 5-10
    - **Description**: Baseline floor assemblies must match the appropriate assembly maximum U-factors in Tables G3.4-1 through G3.4-9.
    - **90.1-2019 Section**: Section G3.1-5(b) Building Envelope Modeling Requirements for the Baseline building
    - **Overall Rule Evaluation Outcome**: FAILED
    - **Number of applicable components**: 5 
      
      | Pass %: 0| Fail %: 100| Not applicable %: 0| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 5-11
    - **Description**:  Baseline slab-on-grade assemblies must conform with assemblies detailed in Appendix A (Unheated Slabs A6).
    - **90.1-2019 Section**: Section G3.1-5(b) Building Envelope Modeling Requirements for the Baseline building
    - **Overall Rule Evaluation Outcome**: NOT_APPLICABLE
    - **Number of applicable components**: 1 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 100| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 5-12
    - **Description**: Baseline slab-on-grade floor assemblies must match the appropriate assembly maximum F-factors in Tables G3.4-1 through G3.4-9.
    - **90.1-2019 Section**: Section G3.1-5(b) Building Envelope Modeling Requirements for the Baseline building
    - **Overall Rule Evaluation Outcome**: NOT_APPLICABLE
    - **Number of applicable components**: 1 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 100| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 5-13
    - **Description**: Opaque surfaces that are not regulated (not part of opaque building envelope) must be modeled the same in the baseline as in the proposed design. 
    - **90.1-2019 Section**: Section G3.1-5 Building Envelope Modeling Requirements for the Baseline building
    - **Overall Rule Evaluation Outcome**: PASS
    - **Number of applicable components**: 98 
      
      | Pass %: 100| Fail %: 0| Not applicable %: 0| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 5-14
    - **Description**: For building area types included in Table G3.1.1-1, vertical fenestration areas for new buildings and additions shall equal that in Table G3.1.1-1 based on the area of gross above-grade walls that separate conditioned spaces and semi-heated spaces from the exterior.
    - **90.1-2019 Section**: Section G3.1-5(c) Building Envelope Modeling Requirements for the Baseline building
    - **Overall Rule Evaluation Outcome**: UNDETERMINED
    - **Number of applicable components**: 1 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 0| Undetermined %: 100| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 5-15
    - **Description**: For building areas not shown in Table G3.1.1-1, vertical fenestration areas for new buildings and additions shall equal that in the proposed design or 40% of gross above-grade wall area, whichever is smaller.
    - **90.1-2019 Section**: Section G3.1-5(c) Building Envelope Modeling Requirements for the Baseline building
    - **Overall Rule Evaluation Outcome**: NOT_APPLICABLE
    - **Number of applicable components**: 1 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 100| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 5-16
    - **Description**: The vertical fenestration shall be distributed on each face of the building in the same proportion as in the proposed design.
    - **90.1-2019 Section**: Section G3.1-5(c) Building Envelope Modeling Requirements for the Baseline building
    - **Overall Rule Evaluation Outcome**: PASS
    - **Number of applicable components**: 24 
      
      | Pass %: 100| Fail %: 0| Not applicable %: 0| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 5-17
    - **Description**: The baseline fenestration area for an existing building shall equal the existing fenestration area prior to the proposed work.
    - **90.1-2019 Section**: Section G3.1-5(c) Building Envelope Modeling Requirements for the Baseline building
    - **Overall Rule Evaluation Outcome**: NOT_APPLICABLE
    - **Number of applicable components**: 1 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 100| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 5-18
    - **Description**: Manually controlled dynamic glazing shall use the average of the minimum and maximum SHGC and VT.
    - **90.1-2019 Section**: Section G3.1-5(a)5 Building Envelope Modeling Requirements for the Proposed design
    - **Overall Rule Evaluation Outcome**: UNDETERMINED
    - **Number of applicable components**: 12 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 0| Undetermined %: 100| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 5-19
    - **Description**: Vertical fenestration U-factors for residential, non-residential and semi-heated spaces in the baseline model must match the appropriate requirements in Table G3.4-1 through G3.4-8 for the appropriate WWR in the baseline RMD.
    - **90.1-2019 Section**: Section G3.1-5(d) Building Envelope Modeling Requirements for the Baseline building
    - **Overall Rule Evaluation Outcome**: PASS
    - **Number of applicable components**: 13 
      
      | Pass %: 92| Fail %: 0| Not applicable %: 7| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 5-20
    - **Description**: Vertical fenestration SHGC shall match the appropriate requirements in Tables G3.4-1 through G3.4-8.
    - **90.1-2019 Section**: Section G3.1-5(d) Building Envelope Modeling Requirements for the Baseline building
    - **Overall Rule Evaluation Outcome**: PASS
    - **Number of applicable components**: 13 
      
      | Pass %: 92| Fail %: 0| Not applicable %: 7| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 5-21
    - **Description**: Subsurface that is not regulated (not part of building envelope) must be modeled with the same area, U-factor and SHGC in the baseline as in the proposed design.
    - **90.1-2019 Section**: Section G3.1-5(a) Building Envelope Modeling Requirements for the Baseline building
    - **Overall Rule Evaluation Outcome**: NOT_APPLICABLE
    - **Number of applicable components**: 1 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 100| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 5-22
    - **Description**: Baseline fenestration shall be assumed to be flush with the exterior wall, and no shading projections shall be modeled.
    - **90.1-2019 Section**: Section G3.1-5(d) Building Modeling Requirements for the Baseline building
    - **Overall Rule Evaluation Outcome**: UNDETERMINED
    - **Number of applicable components**: 13 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 7| Undetermined %: 92| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 5-23
    - **Description**: Manual fenestration shading devices, such as blinds or shades, shall be modeled or not modeled the same as in the baseline building design.
    - **90.1-2019 Section**: Section G3.1-5(a)(4) Building Modeling Requirements for the Proposed design and G3.1-5(d) Building Modeling Requirements for Baseline building
    - **Overall Rule Evaluation Outcome**: UNDETERMINED
    - **Number of applicable components**: 13 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 7| Undetermined %: 92| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 5-24
    - **Description**: If skylight area in the proposed design is 3% or less of the roof surface, the skylight area in baseline shall be equal to that in the proposed design.
    - **90.1-2019 Section**: Section G3.1-5(e) Building Envelope Modeling Requirements for the Baseline building
    - **Overall Rule Evaluation Outcome**: NOT_APPLICABLE
    - **Number of applicable components**: 1 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 100| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 5-25
    - **Description**: If the skylight area of the proposed design is greater than 3%, baseline skylight area shall be decreased in all roof components in which skylights are located to reach 3%.
    - **90.1-2019 Section**: Section G3.1-5(e) Building Envelope Modeling Requirements for the Baseline building
    - **Overall Rule Evaluation Outcome**: NOT_APPLICABLE
    - **Number of applicable components**: 1 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 100| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 5-26
    - **Description**: Skylight area must be allocated to surfaces in the same proportion in the baseline as in the proposed design.
    - **90.1-2019 Section**: Section G3.1-5(e) Building Envelope Modeling Requirements for the Baseline building
    - **Overall Rule Evaluation Outcome**: NOT_APPLICABLE
    - **Number of applicable components**: 1 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 100| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 5-27
    - **Description**: Skylight U-factors for residential, non-residential and semi-heated spaces in the baseline model must match the appropriate requirements in Table G3.4-1 through G3.4-8.
    - **90.1-2019 Section**: Section G3.1-5(e) Building Envelope Modeling Requirements for the Baseline building
    - **Overall Rule Evaluation Outcome**: NOT_APPLICABLE
    - **Number of applicable components**: 1 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 100| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 5-28
    - **Description**: Skylight SHGC properties shall match the appropriate requirements in Tables G3.4-1 through G3.4-8 using the value and the applicable skylight percentage.
    - **90.1-2019 Section**: Section G3.1-5(e) Building Envelope Modeling Requirements for the Baseline building
    - **Overall Rule Evaluation Outcome**: NOT_APPLICABLE
    - **Number of applicable components**: 1 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 100| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 5-29
    - **Description**: The baseline roof surfaces shall be modeled using a thermal emittance of 0.9
    - **90.1-2019 Section**: Section G3.1-5(f) Building Envelope Modeling Requirements for the Baseline building
    - **Overall Rule Evaluation Outcome**: UNDETERMINED
    - **Number of applicable components**: 1 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 0| Undetermined %: 100| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 5-30
    - **Description**: The proposed roof surfaces shall be modeled using the same thermal emittance as in the user model.
    - **90.1-2019 Section**: Section G3.1-1(a) Building Envelope Modeling Requirements for the Proposed design
    - **Overall Rule Evaluation Outcome**: UNDETERMINED
    - **Number of applicable components**: 1 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 0| Undetermined %: 100| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 5-31
    - **Description**:  The baseline roof surfaces shall be modeled using a solar reflectance of 0.30
    - **90.1-2019 Section**: Section G3.1-5(g) Building Envelope Modeling Requirements for the Baseline building
    - **Overall Rule Evaluation Outcome**: UNDETERMINED
    - **Number of applicable components**: 1 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 0| Undetermined %: 100| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 5-32
    - **Description**: The proposed roof surfaces shall be modeled using the same solar reflectance as in the user model if the aged test data are available, or equal to 0.7 default reflectance
    - **90.1-2019 Section**: Section G3.1-1(a) Building Envelope Modeling Requirements for the Proposed design
    - **Overall Rule Evaluation Outcome**: UNDETERMINED
    - **Number of applicable components**: 1 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 0| Undetermined %: 100| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 5-33
    - **Description**: The infiltration modeling method in the baseline includes adjustment for weather and building operation.
    - **90.1-2019 Section**: Section G3.1-5(b) Building Envelope Modeling Requirements for the Proposed design and Baseline
    - **Overall Rule Evaluation Outcome**: PASS
    - **Number of applicable components**: 1 
      
      | Pass %: 100| Fail %: 0| Not applicable %: 0| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 5-34
    - **Description**: The infiltration shall be modeled using the same methodology and adjustments for weather and building operation in both the proposed design and the baseline building design.
    - **90.1-2019 Section**: Section G3.1-5(b) Building Envelope Modeling Requirements for the Proposed design and Baseline
    - **Overall Rule Evaluation Outcome**: PASS
    - **Number of applicable components**: 1 
      
      | Pass %: 100| Fail %: 0| Not applicable %: 0| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 5-35
    - **Description**: The baseline air leakage rate of the building envelope (I_75Pa) at a fixed building pressure differential of 0.3 in. of water shall be 1 cfm/ft2. The air leakage rate of the building envelope shall be converted to appropriate units for the simulation program using one of the methods in Section G3.1.1.4.
    - **90.1-2019 Section**: Section G3.1-5(h) Building Envelope Modeling Requirements for the Baseline building
    - **Overall Rule Evaluation Outcome**: FAILED
    - **Number of applicable components**: 1 
      
      | Pass %: 0| Fail %: 100| Not applicable %: 0| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 5-36
    - **Description**: The air leakage rate in unconditioned and unenclosed spaces must be the same the baseline and proposed design.
    - **90.1-2019 Section**: Section G3.1-1 Building Envelope Modeling Requirements for the Proposed design and Baseline building
    - **Overall Rule Evaluation Outcome**: NOT_APPLICABLE
    - **Number of applicable components**: 1 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 100| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 5-37
    - **Description**: The proposed air leakage rate of the building envelope (I75Pa) at a fixed building pressure differential of 0.3 in. of water shall be 0.6 cfm/ft2 for buildings providing verification in accordance with Section 5.9.1.2. The air leakage rate of the building envelope shall be converted to appropriate units for the simulation program using one of the methods in Section G3.1.1.4. Exceptions: When whole-building air leakage testing, in accordance with Section 5.4.3.1.1, is specified during design and completed after construction, the proposed design air leakage rate of the building envelope shall be as measured.
    - **90.1-2019 Section**: Section G3.1-5(b) Building Envelope Modeling Requirements for the Proposed design
    - **Overall Rule Evaluation Outcome**: UNDETERMINED
    - **Number of applicable components**: 1 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 0| Undetermined %: 100| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 5-38
    - **Description**: It is acceptable to use either an annual average ground temperature or monthly average ground temperatures for calculation of heat loss through below-grade walls and basement floors.
    - **90.1-2019 Section**: Section G3.1-14(b) Building Envelope Modeling Requirements for the Proposed design and Baseline
    - **Overall Rule Evaluation Outcome**: NOT_APPLICABLE
    - **Number of applicable components**: 1 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 100| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 5-39
    - **Description**: U-factor of the baseline door is based on Tables G3.4-1 through G3.4-8 for the applicable door type (swinging or non-swinging) and envelope conditioning category.
    - **90.1-2019 Section**: Section G3.1-5(b) Building Envelope Modeling Requirements for the Baseline model
    - **Overall Rule Evaluation Outcome**: NOT_APPLICABLE
    - **Number of applicable components**: 1 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 100| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 5-40
    - **Description**: Opaque roof surfaces that are not regulated (not part of opaque building envelope) must be modeled with the same thermal emittance and solar reflectance in the baseline as in the proposed design. 
    - **90.1-2019 Section**: Section G3.1-5 Building Envelope Modeling Requirements for the Baseline building
    - **Overall Rule Evaluation Outcome**: UNDETERMINED
    - **Number of applicable components**: 25 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 0| Undetermined %: 100| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
### Section: Lighting
            
  - **Rule Id**: 6-1
    - **Description**: The total building interior lighting power shall not exceed the interior lighting power allowance determined using either Table G3.7 or G3.8
    - **90.1-2019 Section**: Section G1.2.1(b) Mandatory Provisions related to interior lighting power
    - **Overall Rule Evaluation Outcome**: PASS
    - **Number of applicable components**: 1 
      
      | Pass %: 100| Fail %: 0| Not applicable %: 0| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 6-2
    - **Description**: Spaces in proposed building with hardwired lighting, including Hotel/Motel Guest Rooms, Dormitory Living Quarters, Interior Lighting Power >= Table 9.6.1; For Dwelling Units, Interior Lighting Power >= 0.6W/sq.ft.
    - **90.1-2019 Section**: Table G3.1 Part 6 Lighting under Proposed Building Performance paragraph (e)
    - **Overall Rule Evaluation Outcome**: UNDETERMINED
    - **Number of applicable components**: 3 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 0| Undetermined %: 100| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 6-3
    - **Description**: Where a complete lighting system exists, the actual lighting power for each building_segment shall be used in the model. Where a lighting system has been designed and submitted with design documents, lighting power shall be determined in accordance with Sections 9.1.3 and 9.1.4. Where lighting neither exists nor is submitted with design documents, lighting shall comply with but not exceed the requirements of Section 9. Lighting power shall be determined in accordance with the Building Area Method (Section 9.5.1).
    - **90.1-2019 Section**: Section G3.1-6(a)(b)(c) Modeling Requirements for the Proposed Design
    - **Overall Rule Evaluation Outcome**: PASS
    - **Number of applicable components**: 18 
      
      | Pass %: 100| Fail %: 0| Not applicable %: 0| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 6-4
    - **Description**: Where a complete lighting system exists and where a lighting system has been designed and submitted with design documents, the baseline LPD is equal to expected value in Table G3.7. Where lighting neither exists nor is submitted with design documents, baseline LPD shall be determined in accordance with Table G3-7 for "Office-Open Plan" space type.
    - **90.1-2019 Section**: Section G3.1-6 Modeling Requirements for the Baseline
    - **Overall Rule Evaluation Outcome**: FAILED
    - **Number of applicable components**: 18 
      
      | Pass %: 0| Fail %: 100| Not applicable %: 0| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 6-5
    - **Description**: Baseline building is modeled with automatic shutoff controls in buildings >5000 sq.ft.
    - **90.1-2019 Section**: Section G3.1-6 Modeling Requirements for the Baseline building
    - **Overall Rule Evaluation Outcome**: PASS
    - **Number of applicable components**: 18 
      
      | Pass %: 83| Fail %: 0| Not applicable %: 16| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 6-6
    - **Description**: Baseline building is not modeled with daylighting control
    - **90.1-2019 Section**: Section G3.1-6 Modeling Requirements for the baseline building
    - **Overall Rule Evaluation Outcome**: PASS
    - **Number of applicable components**: 1 
      
      | Pass %: 100| Fail %: 0| Not applicable %: 0| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 6-7
    - **Description**: Proposed building is modeled with daylighting controls directly or through schedule adjustments.
    - **90.1-2019 Section**: Section G3.1-6(h) Lighting: Modeling Requirements for the Proposed design
    - **Overall Rule Evaluation Outcome**: UNDETERMINED
    - **Number of applicable components**: 18 
      
      | Pass %: 33| Fail %: 0| Not applicable %: 0| Undetermined %: 66| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 6-8
    - **Description**: Additional occupancy sensor controls in the proposed building are modeled through schedule adjustments based on factors defined in Table G3.7.
    - **90.1-2019 Section**: Section G3.1-6(i) Modeling Requirements for the Proposed design
    - **Overall Rule Evaluation Outcome**: FAILED
    - **Number of applicable components**: 1 
      
      | Pass %: 0| Fail %: 100| Not applicable %: 0| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 6-9
    - **Description**: Proposed building is modeled with other programmable lighting controls through a 10% schedule reduction in buildings less than 5,000sq.ft.
    - **90.1-2019 Section**: Section G3.1-6(i) Modeling Requirements for the Proposed design
    - **Overall Rule Evaluation Outcome**: FAILED
    - **Number of applicable components**: 1 
      
      | Pass %: 0| Fail %: 100| Not applicable %: 0| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
### Section: HVAC-Baseline
            
  - **Rule Id**: 18-1
    - **Description**: HVAC system type selection is based on ASHRAE 90.1 G3.1.1 (a-h).
    - **90.1-2019 Section**: Table G3.1.1
    - **Overall Rule Evaluation Outcome**: FAILED
    - **Number of applicable components**: 18 
      
      | Pass %: 83| Fail %: 16| Not applicable %: 0| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 18-2
    - **Description**: Does the modeled system serve the appropriate zones (one system per zone for system types 1, 2, 3, 4, 9, 10, 11, 12, and 13 and one system per floor for system types 5, 6, 7, and 8, with the exception of system types 5 or 7 serving laboratory spaces - these systems should serve ALL laboratory zones in the buidling).
    - **90.1-2019 Section**: Section 18 HVAC_SystemZoneAssignment
    - **Overall Rule Evaluation Outcome**: PASS
    - **Number of applicable components**: 3 
      
      | Pass %: 100| Fail %: 0| Not applicable %: 0| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 18-3
    - **Description**: The lab exhaust fan shall be modeled as constant horsepower (kilowatts) reflecting constant-volume stack discharge with outdoor air bypass in the baseline
    - **90.1-2019 Section**: Section G3.1-10 HVAC Systems for the baseline building
    - **Overall Rule Evaluation Outcome**: NOT_APPLICABLE
    - **Number of applicable components**: 1 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 100| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
### Section: HVAC-General
            
  - **Rule Id**: 19-1
    - **Description**: HVAC system coil capacities for the baseline building design shall be oversized by 15% for cooling and 25% for heating.
    - **90.1-2019 Section**: Section G3.1.2.2
    - **Overall Rule Evaluation Outcome**: NOT_APPLICABLE
    - **Number of applicable components**: 3 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 100| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 19-2
    - **Description**: Baseline building plant capacities shall be based on coincident loads.
    - **90.1-2019 Section**: Section G3.1.2.2
    - **Overall Rule Evaluation Outcome**: UNDETERMINED
    - **Number of applicable components**: 3 
      
      | Pass %: 66| Fail %: 0| Not applicable %: 0| Undetermined %: 33| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 19-3
    - **Description**: Weather conditions used in sizing runs to determine baseline equipment capacities shall be based either on design days developed using 99.6% heating design temperatures and 1% dry-bulb and 1% wet-bulb cooling design temperatures.
    - **90.1-2019 Section**: Section G3.1.2.2.1
    - **Overall Rule Evaluation Outcome**: UNDETERMINED
    - **Number of applicable components**: 1 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 0| Undetermined %: 100| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 19-4
    - **Description**: For baseline cooling sizing runs in residential dwelling units, the infiltration, occupants, lighting, gas and electricity using equipment hourly schedule shall be the same as the most used hourly weekday schedule from the annual simulation.
    - **90.1-2019 Section**: Section G3.1.2.2.1 Exception
    - **Overall Rule Evaluation Outcome**: NOT_APPLICABLE
    - **Number of applicable components**: 18 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 100| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 19-5
    - **Description**: Unmet load hours for the proposed design shall not exceed 300 (of the 8760 hours simulated).
    - **90.1-2019 Section**: Section G3.1.2.3
    - **Overall Rule Evaluation Outcome**: PASS
    - **Number of applicable components**: 1 
      
      | Pass %: 100| Fail %: 0| Not applicable %: 0| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 19-6
    - **Description**:  Unmet load hours for the baseline design shall not exceed 300 (of the 8760 hours simulated).
    - **90.1-2019 Section**: Section G3.1.2.3
    - **Overall Rule Evaluation Outcome**: PASS
    - **Number of applicable components**: 1 
      
      | Pass %: 100| Fail %: 0| Not applicable %: 0| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 19-7
    - **Description**: Minimum ventilation system outdoor air intake flow shall be the same for the proposed design and baseline building design except when any of the 4 exceptions defined in Section G3.1.2.5 are met.Exceptions included in this RDS: 2. When designing systems in accordance with Standard 62.1, Section 6.2, `Ventilation Rate Procedure,`reduced ventilation airflow rates may be calculated for each HVAC zone in the proposed design with a zone air distribution effectiveness (Ez) > 1.0 as defined by Standard 62.1, Table 6-2. Baseline ventilation airflow rates in those zones shall be calcu-lated using the proposed design Ventilation Rate Procedure calculation with the following change only. Zone air distribution effectiveness shall be changed to (Ez) = 1.0 in each zone having a zone air distribution effectiveness (Ez) > 1.0. Proposed design and baseline build-ing design Ventilation Rate Procedure calculations, as described in Standard 62.1, shall be submitted to the rating authority to claim credit for this exception.
    - **90.1-2019 Section**: Section G3.1.2.5 and Exception 2
    - **Overall Rule Evaluation Outcome**: PASS
    - **Number of applicable components**: 3 
      
      | Pass %: 100| Fail %: 0| Not applicable %: 0| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 19-8
    - **Description**: Demand control ventilation is modeled in the baseline design in systems with outdoor air capacity greater than 3000 cfm serving areas with an average occupant design capacity greater than 100 people per 1000 ft^2.
    - **90.1-2019 Section**: Section G3.1.2.5 Exception #1
    - **Overall Rule Evaluation Outcome**: FAILED
    - **Number of applicable components**: 3 
      
      | Pass %: 0| Fail %: 100| Not applicable %: 0| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 19-9
    - **Description**: Air economizers shall not be included in baseline HVAC Systems 1, 2, 9, and 10.
    - **90.1-2019 Section**: G3.1.2.6
    - **Overall Rule Evaluation Outcome**: NOT_APPLICABLE
    - **Number of applicable components**: 3 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 100| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 19-10
    - **Description**: Air economizers shall be included in baseline HVAC Systems 3 through 8, and 11, 12, and 13 based on climate as specified in Section G3.1.2.6 with exceptions.1. Systems that include gas-phase air cleaning to meet the requirements of Standard 62.1, Section 6.1.2. This exception shall be used only if the system in the proposed design does not match the building design.2. Where the use of outdoor air for cooling will affect supermarket open refrigerated case-work systems. This exception shall only be used if the system in the proposed design does not use an economizer. If the exception is used, an economizer shall not be included in the baseline building design.3. Systems that serve computer rooms complying with Section G3.1.2.6.1.
    - **90.1-2019 Section**: Section G3.1.2.6 including exceptions 1-3
    - **Overall Rule Evaluation Outcome**: NOT_APPLICABLE
    - **Number of applicable components**: 1 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 100| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 19-11
    - **Description**: For systems that serve computer rooms, if the baseline system is HVAC System 11, it shall include an integrated fluid economizer meeting the requirements of Section 6.5.1.2 in the baseline building design.
    - **90.1-2019 Section**: Section G3.1.2.6.1
    - **Overall Rule Evaluation Outcome**: NOT_APPLICABLE
    - **Number of applicable components**: 3 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 100| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 19-12
    - **Description**: The baseline system economizer high-limit shutoff shall be a dry-bulb fixed switch with set-point temperatures in accordance with the values in Table G3.1.2.7.
    - **90.1-2019 Section**: Section G3.1.2.7
    - **Overall Rule Evaluation Outcome**: NOT_APPLICABLE
    - **Number of applicable components**: 3 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 100| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 19-13
    - **Description**: For baseline system types 1-8 and 11-13, system design supply airflow rates shall be based on a supply-air-to-room temperature set-point difference of 20°F or the minimum outdoor airflow rate, or the airflow rate required to comply with applicable codes or accreditation standards, whichever is greater. For systems with multiple zone thermostat setpoints, use the design set point that will result in the lowest supply air cooling set point or highest supply air heating set point.
    - **90.1-2019 Section**: Section G3.1.2.8.1 and Exception 1
    - **Overall Rule Evaluation Outcome**: UNDETERMINED
    - **Number of applicable components**: 1 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 0| Undetermined %: 100| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 19-14
    - **Description**: For baseline system types 1-8 and 11-13, if return or relief fans are specified in the proposed design, the baseline building design shall also be modeled with fans serving the same functions and sized for the baseline system supply fan air quantity less the minimum outdoor air, or 90% of the supply fan air quantity, whichever is larger.
    - **90.1-2019 Section**: Section G3.1.2.8.1 Excluding Exceptions 1 and 2
    - **Overall Rule Evaluation Outcome**: PASS
    - **Number of applicable components**: 3 
      
      | Pass %: 100| Fail %: 0| Not applicable %: 0| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 19-15
    - **Description**: For baseline system types 9 & 10, the system design supply airflow rates shall be based on the temperature difference between a supply air temperature set point of 105°F and the design space-heating temperature set point, the minimum outdoor airflow rate, or the airflow rate required to comply with applicable codes or accreditation standards, whichever is greater.
    - **90.1-2019 Section**: Section G3.1.2.8.2
    - **Overall Rule Evaluation Outcome**: NOT_APPLICABLE
    - **Number of applicable components**: 1 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 100| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 19-16
    - **Description**: For zones served by baseline system types 9 & 10, if the proposed design includes a fan or fans sized and controlled to provide non-mechanical cooling, the baseline building design shall include a separate fan to provide nonmechanical cooling, sized and controlled the same as the proposed design.
    - **90.1-2019 Section**: Section G3.1.2.8.2
    - **Overall Rule Evaluation Outcome**: NOT_APPLICABLE
    - **Number of applicable components**: 1 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 100| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 19-17
    - **Description**: For baseline system 1 and 2, the total fan electrical power (Pfan) for supply, return, exhaust, and relief shall be = CFMs × 0.3, where, CFMs = the baseline system maximum design supply fan airflow rate, cfm.
    - **90.1-2019 Section**: Section G3.1.2.9
    - **Overall Rule Evaluation Outcome**: NOT_APPLICABLE
    - **Number of applicable components**: 1 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 100| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 19-18
    - **Description**: For baseline systems 3 through 8, and 11, 12, and 13, the system fan electrical power for supply, return, exhaust, and relief shall be Pfan = bhp × 746/fan motor efficiency. Where, bhp = brake horsepower of baseline fan motor from Table G3.1.2.9; fan motor efficiency = the efficiency from Table G3.9.1 for the next motor size greater than the bhp using a totally enclosed fan cooled motor at 1800 rpm..
    - **90.1-2019 Section**: Section G3.1.2.9
    - **Overall Rule Evaluation Outcome**: PASS
    - **Number of applicable components**: 3 
      
      | Pass %: 100| Fail %: 0| Not applicable %: 0| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 19-19
    - **Description**: For baseline systems 9 and 10 the system fan electrical power (Pfan) for supply, return, exhaust, and relief shall be CFMs × 0.3, where, CFMs = the baseline system maximum design supply fan airflow rate, cfm. If modeling a non-mechanical cooling fan is required by Section G3.1.2.8.2, there is a fan power allowance of Pfan = CFMnmc × 0.054, where, CFMnmc = the baseline non-mechanical cooling fan airflow, cfm for the non-mechanical cooling.
    - **90.1-2019 Section**: Section G3.1.2.9
    - **Overall Rule Evaluation Outcome**: NOT_APPLICABLE
    - **Number of applicable components**: 1 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 100| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 19-20
    - **Description**: The calculated system fan power shall be distributed to supply, return, exhaust, and relief fans in the same proportion as the proposed design.
    - **90.1-2019 Section**: Section G3.1.2.9
    - **Overall Rule Evaluation Outcome**: FAILED
    - **Number of applicable components**: 3 
      
      | Pass %: 0| Fail %: 100| Not applicable %: 0| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 19-21
    - **Description**: Baseline systems with >= 5,000 CFM supply air and >= 70 %OA shall have energy recovery modeled in the baseline design model. The following exceptions apply:1. Systems serving spaces that are not cooled and that are heated to less than 60°F.2. Systems exhausting toxic, flammable, or corrosive fumes or paint or dust. This exception shall only be used if exhaust air energy recovery is not used in the proposed design.3. Commercial kitchen hoods (grease) classified as Type 1 by NFPA 96. This exception shall only be used if exhaust air energy recovery is not used in the proposed design.4. Heating systems in Climate Zones 0 through 3.5. Cooling systems in Climate Zones 3C, 4C, 5B, 5C, 6B, 7, and 8.6. Where the largest exhaust source is less than 75% of the design outdoor airflow. This exception shall only be used if exhaust air energy recovery is not used in the proposed design.7. Systems requiring dehumidification that employ energy recovery in series with the cooling coil. This exception shall only be used if exhaust air energy recovery and series-style energy recovery coils are not used in the proposed design.
    - **90.1-2019 Section**: Section G3.1.2.10 and exceptions 1-7
    - **Overall Rule Evaluation Outcome**: UNDETERMINED
    - **Number of applicable components**: 3 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 0| Undetermined %: 100| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 19-22
    - **Description**: Baseline systems modeled with exhaust air energy recovery shall allow bypass or control heat recovery system to permit air economizer operation.
    - **90.1-2019 Section**: Section G3.1.2.2
    - **Overall Rule Evaluation Outcome**: NOT_APPLICABLE
    - **Number of applicable components**: 3 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 100| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 19-23
    - **Description**: For cooling sizing runs, schedules for internal loads, including those used for infiltration, occupants, lighting, gas and electricity using equipment, shall be equal to the highest hourly value used in the annual simulation runs and applied to the entire design day. For heating sizing runs, schedules for internal loads, including those used for occupants, lighting, gas and electricity using equipment, shall be equal to the lowest hourly value used in the annual simulation runs, and schedules for infiltration shall be equal to the highest hourly value used in the annual simulation runs and applied to the entire design day.
    - **90.1-2019 Section**: Section G3.1.2.2.1 excluding exception
    - **Overall Rule Evaluation Outcome**: FAILED
    - **Number of applicable components**: 18 
      
      | Pass %: 0| Fail %: 83| Not applicable %: 0| Undetermined %: 16| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 19-24
    - **Description**: Schedules for HVAC fans that provide outdoor air for ventilation shall run continuously whenever spaces are occupied in the proposed design.
    - **90.1-2019 Section**: Section G3.1-4 Schedules for the proposed building excluding exception #1 and Section G3.1.2.4.
    - **Overall Rule Evaluation Outcome**: UNDETERMINED
    - **Number of applicable components**: 3 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 0| Undetermined %: 100| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 19-25
    - **Description**: Schedules for HVAC fans that provide outdoor air for ventilation shall run continuously whenever spaces are occupied in the baseline design.
    - **90.1-2019 Section**: Section G3.1-4 Schedules for the proposed building excluding exception #1 and Section G3.1.2.4.
    - **Overall Rule Evaluation Outcome**: UNDETERMINED
    - **Number of applicable components**: 3 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 0| Undetermined %: 100| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 19-26
    - **Description**: HVAC fans shall remain on during unoccupied hours in spaces that have health and safety mandated minimum ventilation requirements during unoccupied hours in the proposed design.
    - **90.1-2019 Section**: Section G3.1-4 Schedules exception #2 for the proposed building and Section G3.1.2.4 Appendix G Section Reference: None
    - **Overall Rule Evaluation Outcome**: UNDETERMINED
    - **Number of applicable components**: 3 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 0| Undetermined %: 100| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 19-27
    - **Description**: HVAC fans shall remain on during unoccupied hours in spaces that have health and safety mandated minimum ventilation requirements during unoccupied hours in the baseline design.
    - **90.1-2019 Section**: Section G3.1-4 Schedules exception #2 for the proposed building and Section G3.1.2.4
    - **Overall Rule Evaluation Outcome**: NOT_APPLICABLE
    - **Number of applicable components**: 3 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 100| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 19-28
    - **Description**: chedules for HVAC fans that provide outdoor air for ventilation in the proposed design shall be cycled ON and OFF to meet heating and cooling loads during unoccupied hours excluding HVAC systems that meet Table G3.1-4 Schedules for the proposed building exceptions #2 and #3.#2 HVAC fans shall remain on during occupied and unoccupied hours in spaces that have health- and safety mandated minimum ventilation requirements during unoccupied hours.#3 HVAC fans shall remain on during occupied and unoccupied hours in systems primarily serving computer rooms.
    - **90.1-2019 Section**: Table G3.1-4 Schedules for the proposed building excluding exceptions #s 2 and 3 and Section G3.1.2.4.
    - **Overall Rule Evaluation Outcome**: UNDETERMINED
    - **Number of applicable components**: 3 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 0| Undetermined %: 100| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 19-29
    - **Description**: Schedules for HVAC fans in the baseline design model that provide outdoor air for ventilation shall be cycled ON and OFF to meet heating and cooling loads during unoccupied hours excluding HVAC systems that meet Table G3.1-4 Schedules per the proposed column exceptions #s 2 and 3.#2 HVAC fans shall remain on during occupied and unoccupied hours in spaces that have health- and safety mandated minimum ventilation requirements during unoccupied hours.#3 HVAC fans shall remain on during occupied and unoccupied hours in systems primarily serving computer rooms.
    - **90.1-2019 Section**: Table G3.1-4 Schedules proposed building column excluding exceptions #s 2 and 3 and G3.1.2.4.
    - **Overall Rule Evaluation Outcome**: PASS
    - **Number of applicable components**: 3 
      
      | Pass %: 100| Fail %: 0| Not applicable %: 0| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 19-30
    - **Description**: For Systems 6 and 8, only the terminal-unit fan and reheat coil shall be energized to meet heating set point during unoccupied hours in the baseline design.
    - **90.1-2019 Section**: Exception to Section G3.1.2.4
    - **Overall Rule Evaluation Outcome**: NOT_APPLICABLE
    - **Number of applicable components**: 3 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 100| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 19-31
    - **Description**: HVAC fans in the proposed design model shall remain on during unoccupied hours in systems primarily serving computer rooms.
    - **90.1-2019 Section**: Section G3.1-4 Schedules exception #3 for the proposed building
    - **Overall Rule Evaluation Outcome**: UNDETERMINED
    - **Number of applicable components**: 3 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 0| Undetermined %: 100| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 19-32
    - **Description**: HVAC fans in the baseline design model shall remain on during unoccupied hours in systems primarily serving computer rooms in the B_RMR.
    - **90.1-2019 Section**: Section G3.1-4 Schedules exception #3 in the proposed column
    - **Overall Rule Evaluation Outcome**: NOT_APPLICABLE
    - **Number of applicable components**: 3 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 100| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 19-33
    - **Description**: Where no heating and/or cooling system is to be installed, and a heating or cooling system is being simulated only to meet the requirements described in Section G3.1-10 HVAC Systems proposed column c and d, heating and/or cooling system fans shall simulated to be cycled ON and OFF to meet heating and cooling loads during occupied hours in the proposed design.
    - **90.1-2019 Section**: Section G3.1-10 HVAC Systems proposed column c and d
    - **Overall Rule Evaluation Outcome**: NOT_APPLICABLE
    - **Number of applicable components**: 3 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 100| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 19-34
    - **Description**: Where no heating and/or cooling system is to be installed, and a heating or cooling system is being simulated only to meet the requirements described in this table, heating and/or cooling system fans shall not be simulated as running continuously during occupied hours but shall be cycled ON and OFF to meet heating and cooling loads during all hours in the baseline design.
    - **90.1-2019 Section**: Section G3.1-4 Schedules Exception #1.
    - **Overall Rule Evaluation Outcome**: NOT_APPLICABLE
    - **Number of applicable components**: 3 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 100| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 19-35
    - **Description**: For baseline systems serving only laboratory spaces that are prohibited from recirculating return air by code or accreditation standards, the baseline system shall be modeled as 100% outdoor air. Rule only applies when baseline outdoor air CFM is modeled as greater than proposed design outdoor air CFM.
    - **90.1-2019 Section**: Section G3.1-10 HVAC Systems proposed column c and d
    - **Overall Rule Evaluation Outcome**: UNDETERMINED
    - **Number of applicable components**: 3 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 0| Undetermined %: 100| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 19-36
    - **Description**: Baseline systems required to model energy recovery per G3.1.2.10 shall be modeled with a 50% enthalpy recovery ratio.
    - **90.1-2019 Section**: Section G3.1-5(a)5 Building Envelope Modeling Requirements for the Proposed design
    - **Overall Rule Evaluation Outcome**: NOT_APPLICABLE
    - **Number of applicable components**: 3 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 100| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
### Section: HVAC-HotWaterSide
            
  - **Rule Id**: 21-1
    - **Description**: For systems using purchased hot water or steam, the heating source shall be modeled as purchased hot water or steam in both the proposed design and baseline building design. If any system in the proposed design uses purchased hot water or steam, all baseline systems with hot water coils shall use the same type of purchased hot water or steam.
    - **90.1-2019 Section**: Section G3.1.1.3 Baseline HVAC System Requirements for Systems Utilizing Purchased Chilled Water and/or Purchased Heat
    - **Overall Rule Evaluation Outcome**: NOT_APPLICABLE
    - **Number of applicable components**: 1 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 100| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 21-2
    - **Description**: For purchased HW/steam in the proposed model, the baseline shall have the same number of pumps as proposed.
    - **90.1-2019 Section**: Section G3.1.1.3 Baseline HVAC System Requirements for Systems Utilizing Purchased Chilled Water and/or Purchased Heat
    - **Overall Rule Evaluation Outcome**: NOT_APPLICABLE
    - **Number of applicable components**: 1 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 100| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 21-3
    - **Description**: Heating hot water plant capacity shall be based on coincident loads.
    - **90.1-2019 Section**: Section G3.1.2.2 Building System-Specific Modeling Requirements for the Baseline model
    - **Overall Rule Evaluation Outcome**: PASS
    - **Number of applicable components**: 1 
      
      | Pass %: 100| Fail %: 0| Not applicable %: 0| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 21-4
    - **Description**: When baseline building does not use purchased heat, baseline systems 1,5,7,11,12 shall be modeled with natural draft boilers.
    - **90.1-2019 Section**: Section G3.1.3.2 Building System-Specific Modeling Requirements for the Baseline model
    - **Overall Rule Evaluation Outcome**: PASS
    - **Number of applicable components**: 2 
      
      | Pass %: 100| Fail %: 0| Not applicable %: 0| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 21-5
    - **Description**: The baseline building design boiler plant shall be modeled as having a single boiler if the baseline building design plant serves a conditioned floor area of 15,000sq.ft. or less, and as having two equally sized boilers for plants serving more than 15,000sq.ft.
    - **90.1-2019 Section**: Section G3.1.3.2 Building System-Specific Modeling Requirements for the Baseline model
    - **Overall Rule Evaluation Outcome**: PASS
    - **Number of applicable components**: 1 
      
      | Pass %: 100| Fail %: 0| Not applicable %: 0| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 21-6
    - **Description**: When baseline building includes two boilers each shall stage as required by load.
    - **90.1-2019 Section**: Section G3.1.3.2 Building System-Specific Modeling Requirements for the Baseline model
    - **Overall Rule Evaluation Outcome**: NOT_APPLICABLE
    - **Number of applicable components**: 1 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 100| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 21-7
    - **Description**: When baseline building requires boilers, systems 1,5,7,11 and 12 - Model HWST = 180F and return design temp = 130F.
    - **90.1-2019 Section**: Section G3.1.3.3 Building System-Specific Modeling Requirements for the Baseline model
    - **Overall Rule Evaluation Outcome**: PASS
    - **Number of applicable components**: 1 
      
      | Pass %: 100| Fail %: 0| Not applicable %: 0| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 21-8
    - **Description**: When the baseline building requires boilers, (for baseline system type = 1,5,7,11 and 12), HWST for the baseline building shall be reset using an outdoor air dry-bulb reset schedule. 180F at 20F OAT, 150Fat 50F OAT, ramped linerarly between 150F and 180F.
    - **90.1-2019 Section**: Section G3.1.3.3 Building System-Specific Modeling Requirements for the Baseline model
    - **Overall Rule Evaluation Outcome**: PASS
    - **Number of applicable components**: 1 
      
      | Pass %: 100| Fail %: 0| Not applicable %: 0| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 21-9
    - **Description**: When baseline building includes boilers, Hot Water Pump Power = 19W/gpm.
    - **90.1-2019 Section**: Section G3.1.3.5 Building System-Specific Modeling Requirements for the Baseline model
    - **Overall Rule Evaluation Outcome**: PASS
    - **Number of applicable components**: 1 
      
      | Pass %: 100| Fail %: 0| Not applicable %: 0| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 21-10
    - **Description**: When the building is modeled with HHW plant (served by either boiler(s) or purchased hot water/steam), the hot water pump shall be modeled as riding the pump curve if the hot water system serves less than 120,000 ft^2 otherwise it shall be modeled with a VFD.
    - **90.1-2019 Section**: Section G3.1.3.5 Building System-Specific Modeling Requirements for the Baseline model
    - **Overall Rule Evaluation Outcome**: PASS
    - **Number of applicable components**: 1 
      
      | Pass %: 100| Fail %: 0| Not applicable %: 0| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 21-11
    - **Description**: The baseline building design uses boilers or purchased hot water, the hot water pumping system shall be modeled as primary-only.
    - **90.1-2019 Section**: Section G3.1.3.5 Building System-Specific Modeling Requirements for the Baseline model
    - **Overall Rule Evaluation Outcome**: PASS
    - **Number of applicable components**: 1 
      
      | Pass %: 100| Fail %: 0| Not applicable %: 0| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 21-12
    - **Description**: The baseline building design uses boilers or purchased hot water, the hot water pumping system shall be modeled with continuous variable flow.
    - **90.1-2019 Section**: Section G3.1.3.5 Building System-Specific Modeling Requirements for the Baseline model
    - **Overall Rule Evaluation Outcome**: PASS
    - **Number of applicable components**: 1 
      
      | Pass %: 100| Fail %: 0| Not applicable %: 0| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 21-13
    - **Description**: The baseline building design uses boilers or purchased hot water, the hot water pumping system shall be modeled with a minimum turndown ratio of 0.25.
    - **90.1-2019 Section**: Section G3.1.3.5 Building System-Specific Modeling Requirements for the Baseline model
    - **Overall Rule Evaluation Outcome**: PASS
    - **Number of applicable components**: 1 
      
      | Pass %: 100| Fail %: 0| Not applicable %: 0| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 21-14
    - **Description**: When the baseline building is modeled with a hot water plant, served by purchased HW system, hot water supply temperature reset is not modeled.
    - **90.1-2019 Section**: Section G3.1.1.3 Baseline HVAC System Requirements for Systems Utilizing Purchased Chilled Water and/or Purchased Heat
    - **Overall Rule Evaluation Outcome**: NOT_APPLICABLE
    - **Number of applicable components**: 1 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 100| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 21-15
    - **Description**: When the baseline building is modeled with a hot water plant, served by purchased HW system, the hot water pump power shall be 14 W/gpm.
    - **90.1-2019 Section**: Section G3.1.1.3 Baseline HVAC System Requirements for Systems Utilizing Purchased Chilled Water and/or Purchased Heat
    - **Overall Rule Evaluation Outcome**: NOT_APPLICABLE
    - **Number of applicable components**: 1 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 100| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 21-16
    - **Description**: Baseline shall have only one heating hot water plant.
    - **90.1-2019 Section**: Section G3.1.3.2 Building System-Specific Modeling Requirements for the Baseline model
    - **Overall Rule Evaluation Outcome**: PASS
    - **Number of applicable components**: 1 
      
      | Pass %: 100| Fail %: 0| Not applicable %: 0| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 21-17
    - **Description**: All boilers in the baseline building design shall be modeled at the minimum efficiency levels, both part load and full load, in accordance with Tables G3.5.6.
    - **90.1-2019 Section**: Section G3.1.2.1 General Baseline HVAC System Requirements - Equipment Efficiencies
    - **Overall Rule Evaluation Outcome**: PASS
    - **Number of applicable components**: 2 
      
      | Pass %: 100| Fail %: 0| Not applicable %: 0| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 21-18
    - **Description**: For baseline building, fossil fuel systems shall be modeled using natural gas as their fuel source. Exception: For fossil fuel systems where natural gas is not available for the proposed building site as determined by the rating authority, the baseline HVAC systems shall be modeled using propane as their fuel.
    - **90.1-2019 Section**: Section G3.1.2.1 General Baseline HVAC System Requirements - Equipment Efficiencies
    - **Overall Rule Evaluation Outcome**: PASS
    - **Number of applicable components**: 2 
      
      | Pass %: 100| Fail %: 0| Not applicable %: 0| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
### Section: HVAC-ChilledWaterSide
            
  - **Rule Id**: 22-1
    - **Description**: Baseline chilled water design supply temperature shall be modeled at 44F.
    - **90.1-2019 Section**: Section G3.1.3.8 Chilled-water design supply temperature (System 7, 8, 11, 12 and 13)
    - **Overall Rule Evaluation Outcome**: PASS
    - **Number of applicable components**: 1 
      
      | Pass %: 100| Fail %: 0| Not applicable %: 0| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 22-2
    - **Description**: Baseline chilled water design return temperature shall be modeled at 56F.
    - **90.1-2019 Section**: Section G3.1.3.8 Chilled-water design supply temperature (System 7, 8, 11, 12 and 13)
    - **Overall Rule Evaluation Outcome**: PASS
    - **Number of applicable components**: 1 
      
      | Pass %: 100| Fail %: 0| Not applicable %: 0| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 22-3
    - **Description**: For Baseline chilled water loop that is not purchased cooling, chilled-water supply temperature shall be reset based on outdoor dry-bulb temperature if loop does not serve any Baseline System Type-11.
    - **90.1-2019 Section**: Section G3.1.3.9 Chilled-water supply temperature reset (System 7, 8, 11, 12 and 13)
    - **Overall Rule Evaluation Outcome**: PASS
    - **Number of applicable components**: 1 
      
      | Pass %: 100| Fail %: 0| Not applicable %: 0| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 22-4
    - **Description**: For Baseline chilled water loop that is not purchased chilled water and does not serve any computer room HVAC systems, chilled-water supply temperature shall be reset using the following schedule: 44F at outdoor dry-bulb temperature of 80F and above, 54F at 60F and below, and ramped linearly between 44F and 54F at temperature between 80F and 60F.
    - **90.1-2019 Section**: Section G3.1.3.9 Chilled-water supply temperature reset (System 7, 8, 11, 12 and 13)
    - **Overall Rule Evaluation Outcome**: PASS
    - **Number of applicable components**: 1 
      
      | Pass %: 100| Fail %: 0| Not applicable %: 0| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 22-5
    - **Description**: For Baseline chilled water loop that is not purchased chilled water and serves computer room HVAC systems (System Type-11), chilled-water supply temperature shall be reset higher based on the HVAC system requiring the most cooling.
    - **90.1-2019 Section**: Section G3.1.3.9 Chilled-water supply temperature reset (System 7, 8, 11, 12 and 13)
    - **Overall Rule Evaluation Outcome**: NOT_APPLICABLE
    - **Number of applicable components**: 1 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 100| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 22-6
    - **Description**: For Baseline chilled water loop that is not purchased chilled water and serves computer room HVAC systems (System Type-11), The maximum reset chilled-water supply temperature shall be 54F.
    - **90.1-2019 Section**: Section G3.1.3.9 Chilled-water supply temperature reset (System 7, 8, 11, 12 and 13)
    - **Overall Rule Evaluation Outcome**: NOT_APPLICABLE
    - **Number of applicable components**: 1 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 100| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 22-7
    - **Description**: Baseline chilled water system that does not use purchased chilled water shall be modeled as primary/secondary systems.
    - **90.1-2019 Section**: Section G3.1.3.10 Chilled-Water Pumps (Systems 7, 8, 11, 12, and 13)
    - **Overall Rule Evaluation Outcome**: PASS
    - **Number of applicable components**: 1 
      
      | Pass %: 100| Fail %: 0| Not applicable %: 0| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 22-8
    - **Description**: For Baseline chilled water system with cooling capacity of 300 tons or more, the secondary pump shall be modeled with variable-speed drives.
    - **90.1-2019 Section**: Section G3.1.3.10 Chilled-water pumps (System 7, 8, 11, 12 and 13)
    - **Overall Rule Evaluation Outcome**: PASS
    - **Number of applicable components**: 1 
      
      | Pass %: 100| Fail %: 0| Not applicable %: 0| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 22-9
    - **Description**: For Baseline chilled water system with cooling capacity of 300 tons or more, the secondary loop shall be modeled with a minimum flow of 25% of the design flow rate.
    - **90.1-2019 Section**: Section G3.1.3.10 Chilled-water pumps (System 7, 8, 11, 12 and 13)
    - **Overall Rule Evaluation Outcome**: PASS
    - **Number of applicable components**: 1 
      
      | Pass %: 100| Fail %: 0| Not applicable %: 0| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 22-10
    - **Description**: For Baseline chilled water system with cooling capacity less than 300ton, the secondary pump shall be modeled as riding the pump curve. For Baseline chilled water system with cooling capacity of 300 tons or more, the secondary pump shall be modeled with variable-speed drives.
    - **90.1-2019 Section**: Section G3.1.3.10 Chilled-water pumps (System 7, 8, 11, 12 and 13)
    - **Overall Rule Evaluation Outcome**: PASS
    - **Number of applicable components**: 1 
      
      | Pass %: 100| Fail %: 0| Not applicable %: 0| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 22-11
    - **Description**: For Baseline chilled-water system that does not use purchased chilled water, variable-flow secondary pump shall be modeled as 13W/gpm at design conditions.
    - **90.1-2019 Section**: Section G3.1.3.10 Chilled-water pumps (System 7, 8, 11, 12 and 13)
    - **Overall Rule Evaluation Outcome**: FAILED
    - **Number of applicable components**: 1 
      
      | Pass %: 0| Fail %: 100| Not applicable %: 0| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 22-12
    - **Description**: The heat rejection system shall be a single loop, modeled with a single cooling tower.
    - **90.1-2019 Section**: Section 22 CHW&CW Loop
    - **Overall Rule Evaluation Outcome**: PASS
    - **Number of applicable components**: 1 
      
      | Pass %: 100| Fail %: 0| Not applicable %: 0| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 22-13
    - **Description**: The baseline heat rejection loop shall be an axial-fan open circuit cooling tower.
    - **90.1-2019 Section**: Section 22 CHW&CW Loop
    - **Overall Rule Evaluation Outcome**: PASS
    - **Number of applicable components**: 1 
      
      | Pass %: 100| Fail %: 0| Not applicable %: 0| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 22-14
    - **Description**: The baseline heat-rejection device shall have a design temperature rise of 10°F.
    - **90.1-2019 Section**: Section G3.1.3.11 Heat Rejection (System 7, 8, 11, 12 and 13)
    - **Overall Rule Evaluation Outcome**: PASS
    - **Number of applicable components**: 1 
      
      | Pass %: 100| Fail %: 0| Not applicable %: 0| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 22-15
    - **Description**: Heat Rejection Device Approach calculated correctly (T/F), Approach = 25.72-(0.24*WB)
    - **90.1-2019 Section**: Section 22 CHW&CW Loop
    - **Overall Rule Evaluation Outcome**: FAILED
    - **Number of applicable components**: 1 
      
      | Pass %: 0| Fail %: 100| Not applicable %: 0| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 22-16
    - **Description**: The baseline condenser-water design supply temperature shall be calculated using the cooling tower approach to the 0.4% evaporation design wet-bulb temperature, valid for wet-bulbs from 55°F to 90°F.
    - **90.1-2019 Section**: Section G3.1.3.11 Heat Rejection (System 7, 8, 11, 12 and 13)
    - **Overall Rule Evaluation Outcome**: PASS
    - **Number of applicable components**: 1 
      
      | Pass %: 100| Fail %: 0| Not applicable %: 0| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 22-17
    - **Description**: The baseline heat rejection device shall have an efficiency of 38.2 gpm/hp.
    - **90.1-2019 Section**: Section 22 CHW&CW Loop
    - **Overall Rule Evaluation Outcome**: UNDETERMINED
    - **Number of applicable components**: 1 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 0| Undetermined %: 100| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 22-18
    - **Description**: The baseline heat rejection device shall be modeled with variable speed fan control.
    - **90.1-2019 Section**: Section 22 CHW&CW Loop
    - **Overall Rule Evaluation Outcome**: PASS
    - **Number of applicable components**: 1 
      
      | Pass %: 100| Fail %: 0| Not applicable %: 0| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 22-19
    - **Description**: The tower shall be controlled to maintain a leaving water temperature, where weather permits.
    - **90.1-2019 Section**: Section G3.1.3.11 Heat Rejection (System 7, 8, 11, 12 and 13)
    - **Overall Rule Evaluation Outcome**: PASS
    - **Number of applicable components**: 1 
      
      | Pass %: 100| Fail %: 0| Not applicable %: 0| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 22-20
    - **Description**: The baseline minimum condenser water reset temperature is per Table G3.1.3.11.
    - **90.1-2019 Section**: Section G3.1.3.11 Heat Rejection (System 7, 8, 11, 12 and 13)
    - **Overall Rule Evaluation Outcome**: FAILED
    - **Number of applicable components**: 1 
      
      | Pass %: 0| Fail %: 100| Not applicable %: 0| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 22-21
    - **Description**: The baseline building design’s chiller plant shall be modeled with chillers having the type as indicated in Table G3.1.3.7 as a function of building peak cooling load.
    - **90.1-2019 Section**: Section G3.1.3.1 Type and Number of Chillers (System 7, 8, 11, 12 and 13)
    - **Overall Rule Evaluation Outcome**: PASS
    - **Number of applicable components**: 2 
      
      | Pass %: 100| Fail %: 0| Not applicable %: 0| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 22-22
    - **Description**: The baseline chiller efficiencies shall be modeled at the minimum efficiency levels for full load, in accordance with Tables G3.5.3.
    - **90.1-2019 Section**: Section G3.1.2.1 Equipment Efficiencies
    - **Overall Rule Evaluation Outcome**: PASS
    - **Number of applicable components**: 2 
      
      | Pass %: 100| Fail %: 0| Not applicable %: 0| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 22-23
    - **Description**: Each baseline chiller shall be modeled with separate chilled water pump interlocked to operate with the associated chiller.
    - **90.1-2019 Section**: Section G3.1.3.11 Heat Rejection (Systems 7, 8, 11, 12, and 13)
    - **Overall Rule Evaluation Outcome**: PASS
    - **Number of applicable components**: 1 
      
      | Pass %: 100| Fail %: 0| Not applicable %: 0| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 22-24
    - **Description**: For baseline chilled-water systems served by chiller(s), the primary pump shall be modeled as constant volume.
    - **90.1-2019 Section**: Section G3.1.3.10 Chilled-water pumps (Systems 7, 8, 11, 12, and 13)
    - **Overall Rule Evaluation Outcome**: PASS
    - **Number of applicable components**: 2 
      
      | Pass %: 100| Fail %: 0| Not applicable %: 0| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 22-25
    - **Description**: For chilled-water systems served by chiller(s) and does not serve baseline System-11, the baseline building constant-volume primary pump power shall be modeled as 9 W/gpm.
    - **90.1-2019 Section**: Section G3.1.3.10 Chilled-water pumps (Systems 7, 8, 11, 12, and 13)
    - **Overall Rule Evaluation Outcome**: FAILED
    - **Number of applicable components**: 1 
      
      | Pass %: 0| Fail %: 100| Not applicable %: 0| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 22-26
    - **Description**: For chilled-water systems served by chiller(s) and serves baseline System-11, the baseline building constant-volume primary pump power shall be modeled as 12 W/gpm.
    - **90.1-2019 Section**: Section G3.1.3.10 Chilled-water pumps (Systems 7, 8, 11, 12, and 13)
    - **Overall Rule Evaluation Outcome**: NOT_APPLICABLE
    - **Number of applicable components**: 1 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 100| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 22-27
    - **Description**: Each baseline chiller shall be modeled with separate condenser-water pump interlocked to operate with the associated chiller.
    - **90.1-2019 Section**: Section G3.1.3.11 Heat Rejection (Systems 7, 8, 11, 12, and 13)
    - **Overall Rule Evaluation Outcome**: PASS
    - **Number of applicable components**: 2 
      
      | Pass %: 100| Fail %: 0| Not applicable %: 0| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 22-28
    - **Description**: The baseline building design condenser-water pump shall be modeled as constant volume.
    - **90.1-2019 Section**: Section 22 CHW&CW Loop
    - **Overall Rule Evaluation Outcome**: PASS
    - **Number of applicable components**: 1 
      
      | Pass %: 100| Fail %: 0| Not applicable %: 0| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 22-29
    - **Description**: For chilled-water systems served by chiller(s) and does not serve baseline System-11, condenser-water pump power shall be 19 W/gpm.
    - **90.1-2019 Section**: Section G3.1.3.11 Heat Rejection (Systems 7, 8, 11, 12, and 13)
    - **Overall Rule Evaluation Outcome**: PASS
    - **Number of applicable components**: 1 
      
      | Pass %: 100| Fail %: 0| Not applicable %: 0| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 22-30
    - **Description**: For chilled-water systems served by chiller(s) and serves baseline System-11, condenser-water pump power shall be 22 W/gpm.
    - **90.1-2019 Section**: Section G3.1.3.11 Heat Rejection (Systems 7, 8, 11, 12, and 13)
    - **Overall Rule Evaluation Outcome**: NOT_APPLICABLE
    - **Number of applicable components**: 1 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 100| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 22-31
    - **Description**: The baseline building design's chiller plant shall be modeled with chillers having the number as indicated in Table G3.1.3.7 as a function of building peak cooling load.
    - **90.1-2019 Section**: Section G3.1.3.1 Type and Number of Chillers (System 7, 8, 11, 12 and 13)
    - **Overall Rule Evaluation Outcome**: PASS
    - **Number of applicable components**: 1 
      
      | Pass %: 100| Fail %: 0| Not applicable %: 0| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 22-32
    - **Description**: The baseline chiller efficiencies shall be modeled at the minimum efficiency levels for part load, in accordance with Tables G3.5.3.
    - **90.1-2019 Section**: Section G3.1.2.1 Equipment Efficiencies
    - **Overall Rule Evaluation Outcome**: FAILED
    - **Number of applicable components**: 2 
      
      | Pass %: 0| Fail %: 100| Not applicable %: 0| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 22-33
    - **Description**: Baseline chilled water system that does not use purchased chilled water must have no more than one CHW plant.
    - **90.1-2019 Section**: Section G3.1.3.2 Building System-Specific Modeling Requirements for the Baseline model
    - **Overall Rule Evaluation Outcome**: PASS
    - **Number of applicable components**: 1 
      
      | Pass %: 100| Fail %: 0| Not applicable %: 0| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 22-34
    - **Description**: For baseline cooling chilled water plant that is served by chiller(s), the capacity shall be based on coincident loads.
    - **90.1-2019 Section**: Section G3.1.2.2 Building System-Specific Modeling Requirements for the Baseline model
    - **Overall Rule Evaluation Outcome**: PASS
    - **Number of applicable components**: 1 
      
      | Pass %: 100| Fail %: 0| Not applicable %: 0| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 22-35
    - **Description**: Baseline systems served by purchased chilled water shall not be modeled with chilled water reset
    - **90.1-2019 Section**: Section G3.1.3.10 Chilled-Water Pumps (Systems 7, 8, 11, 12, and 13)
    - **Overall Rule Evaluation Outcome**: NOT_APPLICABLE
    - **Number of applicable components**: 1 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 100| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 22-36
    - **Description**: Baseline chilled water system that does not use purchased chilled water shall be modeled with constant flow primary loop and variable flow secondary loop.
    - **90.1-2019 Section**: Section G3.1.3.10 Chilled-Water Pumps (Systems 7, 8, 11, 12, and 13)
    - **Overall Rule Evaluation Outcome**: PASS
    - **Number of applicable components**: 1 
      
      | Pass %: 100| Fail %: 0| Not applicable %: 0| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 22-37
    - **Description**: Baseline systems served by purchased chilled water loop shall be modeled with a distribution pump with a variable speed drive
    - **90.1-2019 Section**: Section G3.1.3.10 Chilled-Water Pumps (Systems 7, 8, 11, 12, and 13)
    - **Overall Rule Evaluation Outcome**: NOT_APPLICABLE
    - **Number of applicable components**: 1 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 100| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 22-38
    - **Description**: Baseline systems served by purchased chilled water loop shall have a minimum flow setpoint of 25%
    - **90.1-2019 Section**: Section G3.1.3.10 Chilled-Water Pumps (Systems 7, 8, 11, 12, and 13)
    - **Overall Rule Evaluation Outcome**: NOT_APPLICABLE
    - **Number of applicable components**: 1 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 100| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 22-39
    - **Description**: Baseline systems served by purchased chilled water loop shall be modeled with a distribution pump whose pump power is 16W/gpm
    - **90.1-2019 Section**: Section G3.1.3.10 Chilled-Water Pumps (Systems 7, 8, 11, 12, and 13)
    - **Overall Rule Evaluation Outcome**: NOT_APPLICABLE
    - **Number of applicable components**: 1 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 100| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 22-40
    - **Description**: For systems using purchased chilled water, the cooling source shall be modeled as purchased chilled water in both the proposed design and baseline building design. If any system in the proposed design uses purchased chilled water, all baseline systems with chilled water coils shall use purchased chilled water. On-site chillers and direct expansion equipment shall not be modeled in the baseline building design.
    - **90.1-2019 Section**: Section G3.1.1.1 & G3.1.1.3.1 Building System-Specific Modeling Requirements for the Baseline model
    - **Overall Rule Evaluation Outcome**: NOT_APPLICABLE
    - **Number of applicable components**: 1 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 100| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 22-41
    - **Description**: Purchased CHW systems must be modeled with only one external fluid loop in the baseline design.
    - **90.1-2019 Section**: Section 22 CHW&CW Loop
    - **Overall Rule Evaluation Outcome**: UNDETERMINED
    - **Number of applicable components**: 1 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 0| Undetermined %: 100| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
### Section: HVAC-AirSide
            
  - **Rule Id**: 23-1
    - **Description**: System 2 and 4 - Electric air-source heat pumps shall be modeled with electric auxiliary heat and an outdoor air thermostat. The systems shall be controlled to energize auxiliary heat only when the outdoor air temperature is less than 40°F. The air-source heat pump shall be modeled to continue to operate while auxiliary heat is energized.
    - **90.1-2019 Section**: G3.1.3.1 Heat Pumps (Systems 2 and 4)
    - **Overall Rule Evaluation Outcome**: NOT_APPLICABLE
    - **Number of applicable components**: 1 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 100| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 23-2
    - **Description**: For baseline systems 5-8 and 11, the SAT is reset higher by 5F under minimum cooling load conditions.
    - **90.1-2019 Section**: Section G3.1.3.12 Supply Air Temperature Reset (Systems 5 through 8 and 11)
    - **Overall Rule Evaluation Outcome**: PASS
    - **Number of applicable components**: 3 
      
      | Pass %: 100| Fail %: 0| Not applicable %: 0| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 23-3
    - **Description**: System 5, 6, 7 and 8 minimum volume setpoint shall be 30% of zone peak airflow, minimum outdoor airflow, or rate required to comply with minium accreditation standards whichever is larger.
    - **90.1-2019 Section**: Section G3.1.3.13 VAV Minimum Flow Set Points (Systems 5 and 7) and Section G3.1.3.14 Fan Power and Control (Systems 6 and 8)
    - **Overall Rule Evaluation Outcome**: PASS
    - **Number of applicable components**: 15 
      
      | Pass %: 100| Fail %: 0| Not applicable %: 0| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 23-4
    - **Description**: Baseline systems 5 & 7 serving lab spaces per G3.1.1c shall reduce lab exhaust and makeup air during unoccupied periods to 50% of zone peak airflow, the minimum outdoor airflow, or rate required to comply with minimum accreditation standards whichever is larger.
    - **90.1-2019 Section**: Exception to G3.1.3.13 VAV Minimum Flow Set Points (Systems 5 and 7)
    - **Overall Rule Evaluation Outcome**: NOT_APPLICABLE
    - **Number of applicable components**: 1 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 100| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 23-5
    - **Description**: For baseline systems 6 and 8, Fans in parallel VAV fan-powered boxes shall run as the first stage of heating before the reheat coil is energized.
    - **90.1-2019 Section**: G3.1.3.14 Fan Power and Control (Systems 6 and 8)
    - **Overall Rule Evaluation Outcome**: NOT_APPLICABLE
    - **Number of applicable components**: 15 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 100| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 23-6
    - **Description**: For baseline systems 6 and 8, Fans in parallel VAV fan-powered boxes shall be sized for 50% of the peak design primary air (from the VAV air-handling unit) flow rate and shall be modeled with 0.35 W/cfm fan power.
    - **90.1-2019 Section**: Section G3.1.3.14 Fan Power and Control (Systems 6 and 8)
    - **Overall Rule Evaluation Outcome**: NOT_APPLICABLE
    - **Number of applicable components**: 1 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 100| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 23-7
    - **Description**: Systems 6&8: Supply air temperature setpoint shall be constant at the design condition.
    - **90.1-2019 Section**: Section G3.1.3.14 Fan Power and Control (Systems 6 and 8)
    - **Overall Rule Evaluation Outcome**: NOT_APPLICABLE
    - **Number of applicable components**: 1 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 100| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 23-8
    - **Description**: System 5-8 and 11 - part load VAV fan power shall be modeled using either method 1 or 2 in Table G3.1.3.15. This rule will only validate data points from Method-1 Part-load Fan Power Data. However, both methods are equivalent. When modeling inputs are based on Method 2, values should be converted to Method 1 when writing to RMD.
    - **90.1-2019 Section**: Section G3.1.3.15 VAV Fan Part-Load Performance (Systems 5 through 8 and 11)
    - **Overall Rule Evaluation Outcome**: UNDETERMINED
    - **Number of applicable components**: 3 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 0| Undetermined %: 100| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 23-9
    - **Description**: System 11 Minimum volume setpoint shall be the largest of 50% of the maximum design airflow rate, the minimum ventilation airflow rate or the airflow required to comply with codes or accredidation standards.
    - **90.1-2019 Section**: Exception to G3.1.3.13
    - **Overall Rule Evaluation Outcome**: NOT_APPLICABLE
    - **Number of applicable components**: 1 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 100| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 23-10
    - **Description**: System 11 Fan volume shall be reset from 100% airflow at 100% cooling load to minimum airflow at 50% cooling load. 
    - **90.1-2019 Section**: G3.1.3.17 System 11 Supply Air Temperature and Fan Control
    - **Overall Rule Evaluation Outcome**: NOT_APPLICABLE
    - **Number of applicable components**: 1 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 100| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 23-11
    - **Description**: System 11 Supply air temperature shall be reset from minimum supply air temp at 50% cooling load to room temp at 0% cooling load.  OR the SAT is reset higher by 5F under minimum cooling load conditions.
    - **90.1-2019 Section**: G3.1.3.17 System 11 Supply Air Temperature and Fan Control & G3.1.3.12 OR Section G3.1.3.12 Supply Air Temperature Reset.
    - **Overall Rule Evaluation Outcome**: NOT_APPLICABLE
    - **Number of applicable components**: 1 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 100| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 23-12
    - **Description**: System 11 in heating mode supply air temperature shall be modulated to maintain space temp and airflow shall be fixed at minimum airflow.
    - **90.1-2019 Section**: G3.1.3.17 System 11 Supply Air Temperature and Fan Control
    - **Overall Rule Evaluation Outcome**: NOT_APPLICABLE
    - **Number of applicable components**: 1 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 100| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 23-13
    - **Description**: If proposed design includes humidistatic controls then the baseline shall use mechanical cooling for dehumidification and shall reheat to avoid overcooling.
    - **90.1-2019 Section**: G3.1.3.18 Dehumidification (Systems 3 through 8 and 11, 12, and 13)
    - **Overall Rule Evaluation Outcome**: NOT_APPLICABLE
    - **Number of applicable components**: 3 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 100| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 23-14
    - **Description**: If the baseline system does not comply with exceptions in Section 6.5.2.3 then only 25% of the system reheat energy shall be included in the baseline building performance.
    - **90.1-2019 Section**: G3.1.3.18 Dehumidification (Systems 3 through 8 and 11, 12, and 13)
    - **Overall Rule Evaluation Outcome**: NOT_APPLICABLE
    - **Number of applicable components**: 3 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 100| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 23-15
    - **Description**: Dehumidification reheat shall be the same as the system heating type.
    - **90.1-2019 Section**: G3.1.3.18 Dehumidification (Systems 3 through 8 and 11, 12, and 13)
    - **Overall Rule Evaluation Outcome**: NOT_APPLICABLE
    - **Number of applicable components**: 3 
      
      | Pass %: 0| Fail %: 0| Not applicable %: 100| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        
  - **Rule Id**: 23-16
    - **Description**: Systems 5 - 8, the baseline system shall be modeled with preheat coils controlled to a fixed set point 20F less than the design room heating temperature setpoint.
    - **90.1-2019 Section**: Section G3.1.3.19 Preheat Coils (Systems 5 through 8)
    - **Overall Rule Evaluation Outcome**: PASS
    - **Number of applicable components**: 3 
      
      | Pass %: 100| Fail %: 0| Not applicable %: 0| Undetermined %: 0| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        