Created the [b36 KiCad project](./b36.kicad_pro) and [schematic](./b36.kicad_sch), including the supplied jack and inductor footprints and the four feedback selections.

**Design hold — do not build or apply 36 V as drawn.** The requested AO3401A is rated for only 30 V. The supplied jack footprint also describes a 2.5 A connector, so 3 A operation requires a current and thermal review. The 12 V setting requires an input above 12 V plus dropout; it cannot regulate from 5.5 V.

Before use, select and assign footprints for F1 and C4, verify the jack pinout, and review component ratings and feedback loading from the status LED. Close **exactly one** solder bridge before applying power.

ERC reported **0 errors and 32 symbol-library mismatch warnings**. The schematic passed structural validation.