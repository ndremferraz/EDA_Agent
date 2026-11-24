Created the [b19 KiCad schematic](./b19.kicad_sch) with the requested MCU, radio, authentication device, probe front end and programming headers.

**Verification:** ERC reports 0 errors and 21 library-symbol mismatch warnings. The requested nets and header orders were checked.

**Assumptions and checks before build:**
- The radio footprint’s pad order was assumed; verify it against the selected module.
- The ATSHA204A-SS symbol was created locally; verify its pinout against the selected device’s datasheet.
- Use battery-voltage-compatible ISP and FTDI interfaces. The battery must remain within the ATmega’s permitted voltage range at 8 MHz.
- The one-contact probe relies on an environmental capacitive return and needs in-situ calibration.