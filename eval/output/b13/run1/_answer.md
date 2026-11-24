Created the [b13 KiCad project](./b13.kicad_pro) and its [schematic](./b13.kicad_sch).

The design uses a CH330N, a GND–RXD–TXD–VBUS header, grounded USB shield, bypass capacitors, and buffered active-low TX/RX LEDs with 220 Ω resistors. USB ID and RTS are marked unused.

**Assumption:** The UART uses 5 V logic; it is not intended for direct connection to a 3.3 V-only device.

ERC reported **0 errors and 13 symbol-library mismatch warnings**. Footprints are assigned, but the footprint lookup tool could not verify them; check them against the selected physical parts before fabrication.