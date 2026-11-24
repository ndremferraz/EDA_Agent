Created the [b26 KiCad project](./b26.kicad_pro) and [schematic](./b26.kicad_sch).

The schematic includes both parallel UEXT connectors, the CH390D, crystal and bypassing, reset and LED resistors, shield coupling, two mounting holes, and four fiducials. ERC reports **0 errors and 23 symbol-library mismatch warnings**.

**Not yet ready to build:** the custom jack symbol uses placeholder LED and shield pin numbers and has no assigned footprint. The custom CH390D symbol and its assumed QFN footprint also need datasheet verification, along with the jack COM bias, LED polarity, and regulator bypassing. The mini connector is assumed to be a 1.0 mm JST-SH; the crystal load capacitors assume a 12 pF load crystal.