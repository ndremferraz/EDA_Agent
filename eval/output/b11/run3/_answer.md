Created the [b11 KiCad project](./b11.kicad_pro) and [schematic](./b11.kicad_sch). The schematic uses the supplied sensor symbol and footprints, the requested six-pin host mapping, and a 51 Ω LED feed resistor. No MCU or regulator was added.

ERC reports **0 errors and 6 symbol-library mismatch warnings**. The schematic netlist confirms the requested connections.

**Before building:** VDDA was assumed to be an internally supplied bypass node, with 2.2 µF to ground. The sensor datasheet was not available to verify that assumption or the capacitor value. Also verify the LED polarity and the supplied footprint’s unnumbered copper shapes against the LED datasheet.