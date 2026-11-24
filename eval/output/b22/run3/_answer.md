Created the [b22 KiCad project](./b22.kicad_pro) and [schematic](./b22.kicad_sch), using the supplied sensor, regulator and FFC libraries.

Assumptions and assembly notes:
- VIN is assumed to be a regulated 3.3 V logic supply. Match host signal levels to the selected VDDIO, and bridge only one side of JP1.
- R4 and C3 are marked **DNP** for the TLV74318. Verify their pin-4 network before fitting an alternate regulator.

ERC reports **0 errors and 25 warnings**; all warnings are embedded-symbol/library mismatch warnings.