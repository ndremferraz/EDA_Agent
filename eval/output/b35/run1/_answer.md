Created the [b35 KiCad project](./b35.kicad_pro) and [schematic](./b35.kicad_sch). The requested headers, test pads, power path, charger, regulator, LEDs, crystal and open variant jumper are connected.

**Verification:** ERC reports 0 errors and 38 warnings, including symbol-library mismatch warnings that remain to be reviewed.

**Assumptions and checks:**
- A protected single-cell LiPo of at least 200 mAh; 10 kΩ programs approximately 100 mA charging.
- The external 3.3 V switch is active-low and defaults **on**. Its MOSFET body diode permits reverse current.
- The supplied TP4057 symbol was replaced in the project-local library because its PROG pin was malformed. **Check the revised pinout against the selected part’s datasheet before building.**
- Crystal load capacitors assume a 12.5 pF crystal and require layout-dependent verification.