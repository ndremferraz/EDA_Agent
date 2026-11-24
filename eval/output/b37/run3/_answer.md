Created the [b37 KiCad project](./b37.kicad_pro) and its [schematic](./b37.kicad_sch), using the supplied dumta symbols and reversible footprints.

The netlist matches the requested matrix, diode polarity, display, battery-switch and reset connections. ERC reports **0 errors and 41 symbol-library mismatch warnings**; refreshing the standard-library symbols did not clear the warnings.

Assumptions: a single-cell LiPo is used, and firmware scans with rows driven low and column pull-ups enabled. Bridge the reversible module and display jumpers for the chosen assembly side. The battery must be switched on to charge through the module.