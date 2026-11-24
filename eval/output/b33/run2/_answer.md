Created [b33.kicad_pro](./b33.kicad_pro) and its [schematic](./b33.kicad_sch). The schematic includes the removable memory socket, signal mapping, supply filtering and clamps, fuse, indicators, and ID divider.

**This is a preliminary design, not ready to build.** The project-local `TLV61046A_provisional` symbol was created because the part was unavailable in the searched libraries; its pinout and feedback reference must be checked against the datasheet. The design assumes a 1.23 V feedback reference and uses 5.6 V clamps on the ±5 V rails.

Also verify the charge pump’s loaded −5 V output and the DRAM’s required supply sequencing; sequencing is not implemented. ERC reported **0 errors and 32 symbol-library mismatch warnings**.