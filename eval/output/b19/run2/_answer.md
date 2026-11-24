Created the [b19 KiCad schematic](./b19.kicad_sch) using the supplied probe, battery-holder and radio footprints.

**Verification:** ERC reports 0 errors and 20 symbol-library mismatch warnings. The schematic connectivity and connector pin orders were checked.

**Before building:**
- Check the pinouts of the project-local ATSHA204A, radio-module and battery-holder symbols, especially the radio module’s pad mapping.
- Connect all battery-holder pad 3 contacts together for the series midpoint.
- Use battery-compatible programming and FTDI voltages; do not exceed the radio’s 3.6 V supply limit. Configure the MCU for the 8 MHz resonator and observe its voltage-versus-frequency limits.