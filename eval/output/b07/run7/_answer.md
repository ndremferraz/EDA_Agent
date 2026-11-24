Created the [b07 KiCad project](./b07.kicad_pro) and [schematic](./b07.kicad_sch) using the supplied translator symbol and footprint.

Both headers, all four signal pairs, direction controls, active-low enable, and the two 100 nF supply decoupling capacitors are connected as requested. ERC reports **0 violations**.

Assumptions: the host supplies both rails with a common ground and drives all control inputs. The supplied footprint references a 3D model that was not present in the project library.