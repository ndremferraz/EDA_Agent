Created the [b29 KiCad project](./b29.kicad_pro) and its [schematic](./b29.kicad_sch). The requested module interfaces, SPI wiring, LED drivers, buzzer, and external header are connected.

**Important design limitations:**
- With 3.3 V GPIO drive, the emitter followers reach less than about 2.6 V. Green and blue LEDs may be dim or not light, depending on their forward voltage.
- Use a low-current, non-inductive 3.3 V buzzer compatible with direct GPIO drive, and verify that it operates with the series-resistor voltage drop.
- Configure the PN532 module for SPI and verify its 3.3 V supply and pinout. GPIO9 is also a boot-strapping pin.
- Footprints remain unassigned for most parts; module connector symbols represent the specified logical numbering, not a verified physical layout.

ERC reports **0 errors and 24 symbol-library mismatch warnings**.