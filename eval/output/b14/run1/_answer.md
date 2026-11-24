Created the [b14 KiCad project](./b14.kicad_pro) and [schematic](./b14.kicad_sch). The requested module connectors, GPIO assignments, programming button, and local interface footprints are included.

**Before assembly:**
- J2 assumes the regulator module pinout is **1 = 5 V in, 2 = GND, 3 = 3.3 V out**. Verify it against the actual module, including its required output capacitor.
- J1 and the FTDI 5 V pin are directly connected; use only one 5 V source at a time. FTDI and peripheral signals must be 3.3 V compatible.

ERC reported **0 errors and 20 warnings**: 19 library-symbol mismatch warnings and one warning for GPIO15 tied to ground.