Created the [b05 KiCad project](./b05.kicad_pro) and [schematic](./b05.kicad_sch). All 28 BM28 pads are connected independently to the requested header pins, using the supplied BM28 footprint.

Assumption: the 2.54 mm headers use vertical through-hole pin-header footprints.

ERC reports **0 errors and 3 warnings** that the connector symbols differ from their library copies. The netlist confirms the requested mapping.