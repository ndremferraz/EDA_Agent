Created the [b13 project](./b13.kicad_pro) and its [schematic](./b13.kicad_sch). The design uses the standard CH330N symbol, with the requested header order, active-low TX/RX LEDs, bypass capacitors, grounded USB shield, and unused ID and RTS pins.

**Verification:** ERC reports no errors and nine symbol-library mismatch warnings; refreshing the affected symbols did not clear the warnings.

**Assumptions and caution:** VBUS is 5 V, and RXD/TXD are named from the bridge’s perspective. With a 2 V LED, each 220 Ω indicator can draw roughly 14 mA when its UART line is low. Verify that both the CH330N and the external RXD driver can sink that current.