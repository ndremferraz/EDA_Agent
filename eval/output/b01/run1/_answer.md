Created the [b01 KiCad project](./b01.kicad_pro) and [schematic](./b01.kicad_sch). The schematic uses the supplied Cherry MX RGB symbol and Kailh-socket footprint, a six-pin 2.54 mm header, and a 100 nF supply bypass capacitor.

Header pins 1–6 are **GND, DIN, DOUT, VCC, SW1, SW2**. The host must provide a compatible LED supply and data signal, plus switch bias and debouncing.

ERC reported **0 errors and 2 warnings**: the cached connector and capacitor symbols differ from their library copies.