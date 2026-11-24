Created [b08.kicad_sch](./b08.kicad_sch) with the FFC, microSD socket, and two identically wired expansion headers. Headphone common is separate from GND; card detection is unused.

**The schematic is not yet build-ready:** J5 is a functionally wired TRRS placeholder without a selected jack or footprint. Select a jack and verify its terminal mapping before use. The custom FFC symbol also assumes the mounting-pad number is `MP`; check it against the supplied footprint.

ERC reported **0 errors and 5 symbol-library mismatch warnings**. The design assumes 2.54 mm headers and host-provided power and bus pull-ups.