Created the [b14 KiCad project](file:///home/andreferraz/EDA_Agent/eval/output/b14/run4/b14.kicad_pro) and its [schematic](file:///home/andreferraz/EDA_Agent/eval/output/b14/run4/b14.kicad_sch), using the supplied module footprints.

The requested GPIO assignments, module connectors, programming button, joined reset/enable, and grounded GPIO15 are wired. ERC reports **0 errors and 20 warnings**: 19 library-copy mismatches and one warning for GPIO15 connected to ground.

Before assembly, verify the assumed regulator-module pinout: **1 = 5 V input, 2 = GND, 3 = 3.3 V output**, and confirm its stability capacitors. The ESP-12 uses the standard ESP-07 symbol with a matching 16-pin pinout; verify the module variant. Use a 3.3 V-logic FTDI adapter and only one 5 V source at a time.