# Transformer - Table 8.4.4  
**Table ID:** 8-4-4  
**Table Description:** Minimum Nominal Efficiency Levels for Low-Voltage Dry-Type Distribution Transformer  
**Appendix G Section:** Transformer  
**Appendix G Section Reference:** Table 8.4.4  
**Notes:**
- Distribution transformer efficiency is regulated by [CFR10.431.196](https://www.ecfr.gov/cgi-bin/retrieveECFR?n=pt10.3.431#sp10.3.431.k), which Table 8.4.4 references.
- Transformer kVA ratings listed in Table 8.4.4 correspond to standard NEMA kVA ratings, but modeled transformers that fall in between NEMA kVA ratings must be evaluated according to the actual kVA rating.
- CFR10.431.196 requires linear interpolation of efficiency values for transformers that fall in between kVA ratings in Table 8.4.4.
- The standard does not regulate the efficiency of transformers with capacity below the minimum listed kVA and above the maximum listed kVA value.

---

## JSON Data
**Data File Location:** rct229/data/ashrae_90_1_prm_transformers.json  
**Notes:**
- The JSON file has the form
```
{
  "transformers": [
    {
      "capacity": A number in units of kVA,
      "efficiency": A decimal number,
      "phase": One of the strings "Single-Phase" or "Three-Phase"
    },
    ...
  ]
}
```

**[Back](../_toc.md)**
