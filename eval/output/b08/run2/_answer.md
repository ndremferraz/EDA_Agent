Created the [b08 schematic](./b08.kicad_sch) with the requested signal connections, separate headphone common, two identical headers, and a 100 nF SD supply capacitor.

**It is not yet ready to build:** the microSD socket and TRRS jack need selected parts and footprints, with their physical pin mappings verified. The supplied FFC footprint is assigned, but the custom FFC symbol’s mounting-pin number (`MP`) must also be checked against it.

Assumptions: 2.54 mm headers and host-provided SD/I²C pull-ups. Card detection is unused.

ERC reports **0 errors and 6 library-symbol mismatch warnings**. Standard library lookup was unavailable, which also prevented verification of the remaining footprints.