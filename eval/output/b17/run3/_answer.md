Created the [b17 KiCad project](./b17.kicad_pro) and its [schematic](./b17.kicad_sch). It includes the requested four BSS138s, headers, pull-ups, gate divider, bypass capacitor, and two fiducials.

**Important limitation:** The specified half-VCC gate bias does not guarantee translation across the full 1.65–5.5 V range. At VCC = 1.65 V, the gate bias is only 0.825 V, which may not adequately turn on a BSS138. A redesign is needed for guaranteed operation. The schematic assumes open-drain signals and a common ground.

ERC reported **0 errors and 11 symbol-library mismatch warnings**.