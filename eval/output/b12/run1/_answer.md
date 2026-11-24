Created the [b12 KiCad project]( /home/andreferraz/EDA_Agent/eval/output/b12/run1/b12.kicad_pro ) and its [schematic]( /home/andreferraz/EDA_Agent/eval/output/b12/run1/b12.kicad_sch ).

The schematic includes the requested MOSFET, Schottky diode, 10 kΩ pull-down and five solder connections. The grounds are common; the charger and battery protection remain external.

**Assumptions:** The charger input is nominally 5 V, and the battery connection is the external protected OUT+. The load voltage is unregulated and drops across the diode when input power is present. The input supply must support both charging and load current.

ERC reported **0 errors and 6 symbol-library mismatch warnings** for the test-point and resistor symbols. No PCB layout or manufacturing files were created.