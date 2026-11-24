Created [b37.kicad_pro](./b37.kicad_pro) and its [schematic](./b37.kicad_sch), using the supplied dumta symbols and reversible footprints.

The netlist confirms the requested 18-key matrix, diode orientation, display connections, battery switch and reset button. ERC reports **0 errors and 41 symbol-library mismatch warnings**; refreshing the library snapshots did not clear those warnings.

Assumptions: a protected 1-cell LiPo and firmware-configured matrix pull-ups. Close the controller and display solder jumpers for the chosen side. With the battery switch off, the battery is also disconnected from the module’s charger.