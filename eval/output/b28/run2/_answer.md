Created the [b28 KiCad project](./b28.kicad_pro) and its [schematic](./b28.kicad_sch). The requested castellated pin orders, USB protection and power path are connected; no 3.3 V regulator is fitted.

ERC reports **0 errors and 25 warnings**: 24 symbol-library mismatch warnings and one for grounding the bidirectional HWB pin. Schematic validation passed.

Assumptions: the crystal uses a 16 pF load specification, and the 22 pF capacitors assume approximately 5 pF stray capacitance. Verify that VCC remains within the MCU’s 16 MHz operating range after the fuse and Schottky voltage drops, particularly at minimum USB voltage and maximum load.