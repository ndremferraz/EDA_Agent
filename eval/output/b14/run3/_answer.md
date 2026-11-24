Created the [b14 KiCad project](b14.kicad_pro) and [schematic](b14.kicad_sch). The requested module connectors, GPIO assignments, programming button, and joined reset/enable signals are wired.

**Verification:** ERC reported 0 errors and 18 warnings: 17 library-symbol mismatch warnings and one for grounding the bidirectional GPIO15 pin.

**Assembly assumptions:**
- Verify the regulator module pinout: pin 1 GND, pin 2 3.3 V output, pin 3 5 V input.
- Use 3.3 V-compatible peripheral modules and FTDI UART logic. Power from J1 **or** FTDI, not both.
- Hold PROGRAM during power-up to flash; release it and power-cycle to run.