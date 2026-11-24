Created the [b09 project](./b09.kicad_pro) and its [schematic](./b09.kicad_sch).

The schematic includes both 5.1 kΩ CC pull-downs, the requested header pin assignments, direct USB data connections, grounded shields, and no-connect markers for SBU and Micro-B ID.

ERC reports **0 errors and 5 symbol-library mismatch warnings**. The headers are assumed to use 2.54 mm pitch. The USB connector footprints remain unassigned; select footprints matching the actual receptacle and Micro-B plug before building.