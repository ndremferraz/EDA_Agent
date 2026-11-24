Created the [b22 KiCad project](./b22.kicad_pro) and its [schematic](./b22.kicad_sch), using the supplied sensor, regulator and FFC dependencies.

**Checks:** ERC reports 0 errors and 24 symbol-library mismatch warnings. The requested connections were checked against the netlist.

**Assembly assumptions:** Bridge JP1 to only one supply, and use host logic compatible with the selected VDDIO. R4 and C3 are labeled DNP for the TLV74318; their alternate-regulator topology must be verified before fitting them. Their DNP status is recorded as text and metadata, not as KiCad’s native DNP flag.