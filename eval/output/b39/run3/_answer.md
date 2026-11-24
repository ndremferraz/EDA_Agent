Created the [b39 KiCad project](./b39.kicad_pro) and its [schematic](./b39.kicad_sch). The requested keyboard, LED chain, peripherals, power circuit and recovery chord are represented and connected.

**The schematic is a draft, not build-ready.** The available tools did not provide a way to resize or split the sheet, so much of the circuitry lies outside the A4 frame. ERC reports **0 errors and 192 warnings**, principally symbol-library mismatches.

Before building, verify the selected MicroMod module’s 3.3 V power direction against the AZ1117 supply, and check the TPS2553 current-limit setting and power budget. The design assumes a 1.5 A-hold input fuse, a 33 kΩ LED-limit resistor, and an ideal current-sense scale of 1 V/A.

I created a project-local W25Q64JVSSIQ symbol and electrical-type-corrected copies of the supplied MicroMod and 74HC589 symbols. Their pinouts and the selected footprints should be checked against the actual parts.