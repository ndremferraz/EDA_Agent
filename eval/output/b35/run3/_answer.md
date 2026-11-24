Created the [b35 KiCad project](./b35.kicad_pro) and [schematic](./b35.kicad_sch). The requested rows, test pads, power path, charger, switched output, sensing, LEDs, crystal, SWD header and open variant jumper are connected.

**Assumptions and checks:**
- RPROG is 10 kΩ, targeting approximately 100 mA. This assumes a protected single-cell LiPo rated for that charge current.
- The supplied TP4057 symbol was corrected to a five-pin pinout, and a project-local USB-C symbol was created. Check both pinouts against the selected parts before building.
- ERC reports **0 errors and 43 symbol-library mismatch warnings**. Standard footprint libraries were unavailable to the tool, so those footprint assignments also need verification.
- P0.09/P0.10 require NFC-as-GPIO configuration; SWD ground is available on the row header.