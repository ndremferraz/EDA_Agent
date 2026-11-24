Created the [b01 KiCad project](./b01.kicad_pro) and [schematic](./b01.kicad_sch). The schematic uses the supplied Cherry MX RGB symbol and Kailh-socket footprint, a 6-pin 2.54 mm header, and a 100 nF LED supply decoupling capacitor.

**Header pins 1–6:** GND, LED DIN, LED DOUT, VLED, SW_A, SW_B.

The design assumes the host supplies VLED, compatible LED data, and switch pull-up circuitry. Verify the LED’s supply range and pinout before assembly.

ERC reports **0 errors and 2 warnings**: the capacitor and connector symbols differ from their standard-library copies.