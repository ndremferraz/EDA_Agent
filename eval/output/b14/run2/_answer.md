Created the [b14 KiCad project](file:///home/andreferraz/EDA_Agent/eval/output/b14/run2/b14.kicad_pro) and its [schematic](file:///home/andreferraz/EDA_Agent/eval/output/b14/run2/b14.kicad_sch). The requested module interfaces and GPIO assignments are wired, using the supplied footprint library.

**ERC:** 0 errors and 17 warnings: 16 symbol-library mismatch warnings and one for GPIO15 being tied directly to ground, as requested.

Before assembly, verify the AP1117 module pinout assumed in the schematic: **1 GND, 2 output, 3 input**. Use 3.3 V-compatible module and FTDI logic, and power from only one 5 V source at a time; the two 5 V connections are not isolated. GPIO2 must remain high during boot.