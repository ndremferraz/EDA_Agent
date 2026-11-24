Created the schematic at [b36.kicad_sch](./b36.kicad_sch), using the supplied barrel-jack and inductor footprints.

**It is not ready to build for the full requested range.** The AO3401A is rated for 30 V drain-to-source, so it cannot provide reverse-polarity protection at 36 V. F1 is specified as a 60 V, 3 A-hold polyfuse, but a fitting part has not been selected. The supplied jack footprint describes a 2.5 A connector, which can limit input current. Component ratings, transient margin and thermal performance need review.

The feedback legs use 1.13 kΩ, 5.90 kΩ, 3.24 kΩ and 21 kΩ for 12 V, 3.3 V, 5 V and 1.8 V respectively, with a 10 kΩ upper resistor. **Close exactly one bridge before powering.** As a buck converter, it also requires input voltage above the selected output plus dropout.

ERC reported **0 errors and 32 symbol-library mismatch warnings**.