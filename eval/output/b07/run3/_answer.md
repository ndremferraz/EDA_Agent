Created the [b07 KiCad project](./b07.kicad_pro) and [schematic](./b07.kicad_sch).

The schematic uses the supplied translator symbol and footprint, both specified 1×8 header pinouts, independent supply inputs, and a 100 nF capacitor on each supply. DIR1–DIR4 and nOE are exposed without straps; the host must drive them.

**ERC:** 0 errors, 7 warnings that standard-library symbols differ from their cached copies. The supplied footprint also references a 3D model that is not present in the project.