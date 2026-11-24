Created the [b28 KiCad project](./b28.kicad_pro) and its [schematic](./b28.kicad_sch). The requested USB-C, protection, power, clock, bypassing, raw USB-data connector and castellated interfaces are present and connected.

**Checks:** ERC reports 0 errors and 25 warnings: 24 symbol-library mismatch warnings and one for the grounded bidirectional HWB pin.

**Assumptions and cautions:** The crystal is assumed to have a 12 pF load rating; verify its load capacitors against the selected part and PCB. The Schottky and fuse drops can bring VCC below the guaranteed 16 MHz operating range at low USB voltage or high load. A schematic note also overlaps the title-block area.