Created the [b17 KiCad project](./b17.kicad_pro) and its [schematic](./b17.kicad_sch). It includes the requested four-BSS138 topology, headers, pull-ups, gate-bias network and two fiducials, plus supply decoupling.

**Important limitation:** The specified VCC/2 gate bias does not guarantee BSS138 switching at 1.65 V, and unequal supplies can cause backfeed. The schematic assumes common ground and open-drain signals; it should not be treated as validated across the full requested voltage range.

ERC reported **0 errors and 13 symbol-library mismatch warnings**.