Created [b07.kicad_pro](./b07.kicad_pro) and its [schematic](./b07.kicad_sch), using the supplied translator symbol and footprint.

The schematic has the requested header pinouts, independent supply inputs, four signal pairs, host-controlled DIR and nOE inputs, and one 100 nF decoupling capacitor per supply. It assumes 1.2–3.6 V supplies and a common ground; the host must drive all control inputs.

ERC reported **0 errors and 7 warnings**. The warnings concern cached standard symbols differing from their library copies. The supplied footprint also references a 3D model that is not present in the project.